"""Small, standard-library transport and durable run journal."""
import hashlib
import json
import os
from pathlib import Path
import time
import urllib.error
import urllib.parse
import urllib.request


class Stop(RuntimeError):
    pass


def digest(value):
    data = value if isinstance(value, bytes) else json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8", "strict")
    return hashlib.sha256(data).hexdigest()


def read_json(path):
    return json.loads(Path(path).read_bytes().decode("utf-8", "strict"))


def save_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".tmp")
    fd = os.open(str(temp), os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as out:
        json.dump(value, out, ensure_ascii=False, indent=2)
        out.write("\n")
        out.flush()
        os.fsync(out.fileno())
    os.replace(temp, path)


SECRET_KEYS = {"api_key", "apikey", "client_id", "clientid", "secret_id", "secret_key", "token", "cos_credential", "authorization", "headers"}


def redacted(value):
    if isinstance(value, dict):
        return {k: "[redacted]" if k.lower() in SECRET_KEYS else redacted(v) for k, v in value.items()}
    if isinstance(value, list):
        return [redacted(v) for v in value]
    return value


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise Stop("Refusing redirect; credentials remain at the official ima API.")


READ_METHODS = {"get_knowledge_base", "get_knowledge_list", "get_media_info", "search_knowledge_base", "check_repeated_names", "get_doc_content"}
WRITE_METHODS = {"create_knowledge_base", "create_folder", "import_urls", "import_doc", "add_knowledge", "set_knowledge_top", "create_media", "update_knowledge_base_basic_info"}


class ImaClient:
    def __init__(self):
        config = Path.home() / ".config" / "ima"
        def credential(names, filename):
            for name in names:
                if os.environ.get(name):
                    return os.environ[name].strip()
            p = config / filename
            return p.read_text().strip() if p.is_file() else ""
        self.client_id = credential(["IMA_OPENAPI_CLIENTID", "IMA_CLIENT_ID"], "client_id")
        self.api_key = credential(["IMA_OPENAPI_APIKEY", "IMA_API_KEY"], "api_key")
        if not self.client_id or not self.api_key:
            raise Stop("ima connection missing. Configure your credentials privately at https://ima.qq.com/agent-interface; never paste them into chat.")
        self.opener = urllib.request.build_opener(NoRedirect())

    def call(self, method, body):
        if method not in READ_METHODS | WRITE_METHODS:
            raise Stop("Unsupported method. Permission setters are intentionally excluded until their semantics and readback are verified.")
        namespace = "note" if method in {"import_doc", "get_doc_content"} else "wiki"
        request = urllib.request.Request("https://ima.qq.com/openapi/" + namespace + "/v1/" + method,
            data=json.dumps(body, ensure_ascii=False).encode("utf-8", "strict"),
            headers={"Content-Type": "application/json", "ima-openapi-clientid": self.client_id, "ima-openapi-apikey": self.api_key})
        try:
            with self.opener.open(request, timeout=40) as response:
                payload = response.read()
        except urllib.error.HTTPError as exc:
            raise Stop("ima HTTP error " + str(exc.code) + "; inspect the current connected API contract before retrying.") from None
        except (OSError, TimeoutError):
            raise Stop("ima connection interrupted. A write may have reached the server; reconcile it before retrying.") from None
        try:
            result = json.loads(payload.decode("utf-8", "strict"))
        except (ValueError, UnicodeError):
            raise Stop("ima returned invalid JSON; do not infer success.") from None
        if result.get("code") != 0:
            raise Stop("ima rejected the request: " + str(result.get("msg", "unknown business error")))
        return result

    def pages(self, method, body, key):
        items, cursor, seen = [], "", set()
        while True:
            if cursor in seen:
                raise Stop("Repeated ima cursor; completeness is not established.")
            seen.add(cursor)
            result = self.call(method, dict(body, cursor=cursor, limit=50 if method == "get_knowledge_list" else 20))
            data = result.get("data", {})
            if key not in data or not isinstance(data[key], list) or "is_end" not in data:
                raise Stop("Unexpected ima pagination schema.")
            items.extend(data[key])
            if data["is_end"] is True:
                return items
            cursor = data.get("next_cursor")
            if not isinstance(cursor, str) or not cursor:
                raise Stop("Missing continuation cursor; the list is incomplete.")


class Journal:
    def __init__(self, path, client):
        self.path, self.client = Path(path), client
        self.state = read_json(path)

    def save(self):
        save_json(self.path, self.state)

    def write(self, key, method, body):
        fingerprint = digest({"method": method, "body": body})
        previous = self.state.setdefault("operations", {}).get(key)
        if previous:
            if previous["fingerprint"] != fingerprint:
                raise Stop("Operation inputs changed: " + key + ". Review the difference; do not overwrite silently.")
            if previous["status"] == "api_ack":
                return previous["response"]
            raise Stop("Operation needs reconciliation: " + key + ". Do not resubmit an uncertain or rejected write blindly.")
        record = {"method": method, "fingerprint": fingerprint, "request": redacted(body), "status": "in_flight", "started_at": time.time()}
        self.state["operations"][key] = record
        self.save()
        try:
            response = self.client.call(method, body)
        except Exception:
            record["status"] = "needs_reconciliation"
            self.save()
            raise
        record.update(status="api_ack", response=redacted(response))
        self.save()
        return response

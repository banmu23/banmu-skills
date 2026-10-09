"""Read only the supplied Feishu wiki subtree. No Feishu mutations."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import urllib.parse
from runtime import Stop, digest, save_json


def wiki_origin(url):
    parsed = urllib.parse.urlsplit(url)
    host = (parsed.hostname or "").lower()
    allowed = host == "feishu.cn" or host.endswith(".feishu.cn") or host == "larksuite.com" or host.endswith(".larksuite.com")
    if parsed.scheme != "https" or not allowed or parsed.username or parsed.password or not parsed.path.startswith("/wiki/"):
        raise Stop("Provide the complete HTTPS Feishu/Lark wiki homepage link.")
    return parsed.scheme + "://" + parsed.netloc


class Lark:
    def __init__(self):
        candidates = [os.environ.get("LARK_CLI", ""), shutil.which("lark-cli") or "", str(Path.home() / "Library/pnpm/bin/lark-cli")]
        self.executable = next((p for p in candidates if p and Path(p).is_file()), "")
        if not self.executable:
            raise Stop("Feishu CLI is not available. Use the connected Feishu reader, or guide the owner through official CLI setup.")

    def __call__(self, args):
        result = subprocess.run([self.executable] + args + ["--as", "user", "--format", "json"], capture_output=True, timeout=60)
        if result.returncode:
            # Do not echo arbitrary stderr that might contain credentials.
            try:
                error = json.loads(result.stderr.decode("utf-8"))["error"]
                raise Stop("Feishu: " + str(error.get("type", "error")) + "; " + str(error.get("message", "read failed")))
            except (ValueError, KeyError, UnicodeError):
                raise Stop("Feishu read failed. Inspect authentication, CLI availability and the specified resource permission.") from None
        try:
            envelope = json.loads(result.stdout.decode("utf-8", "strict"))
        except (ValueError, UnicodeError):
            raise Stop("Feishu did not return valid UTF-8 JSON.") from None
        if envelope.get("ok") is not True:
            raise Stop("Feishu success envelope missing; do not infer success from HTTP status.")
        return envelope["data"]


def scan(url, caller):
    origin = wiki_origin(url)
    root = caller(["wiki", "+node-get", "--node-token", url])
    if "node" in root:
        root = root["node"]
    if not root.get("space_id") or not root.get("node_token"):
        raise Stop("Feishu root identifiers missing.")
    reads, visited = [], {root["node_token"]}
    def children(parent):
        nodes, cursor, cursors = [], "", set()
        while True:
            if cursor in cursors:
                raise Stop("Repeated Feishu cursor; source completeness is unknown.")
            cursors.add(cursor)
            args = ["wiki", "+node-list", "--space-id", root["space_id"], "--parent-node-token", parent, "--page-size", "50"]
            if cursor:
                args += ["--page-token", cursor]
            data = caller(args)
            reads.append({"parent": parent, "cursor": cursor, "has_more": data.get("has_more")})
            if not isinstance(data.get("nodes"), list) or "has_more" not in data:
                raise Stop("Unexpected Feishu list schema.")
            nodes.extend(data["nodes"])
            if data["has_more"] is False:
                return nodes
            cursor = data.get("page_token")
            if not cursor:
                raise Stop("Feishu continuation cursor missing.")

    def walk(node, path):
        token = node["node_token"]
        if token in visited:
            raise Stop("Repeated source node or cycle: inspect the supplied subtree.")
        visited.add(token)
        item = {"id": token, "title": node.get("title", ""), "url": node.get("url") or origin + "/wiki/" + token,
                "obj_type": node.get("obj_type", ""), "node_type": node.get("node_type", ""), "path": path + [node.get("title", "")]}
        result = [item]
        if node.get("has_child"):
            for child in children(token):
                result.extend(walk(child, item["path"]))
        return result

    modules = []
    for node in children(root["node_token"]):
        if node["node_token"] in visited:
            raise Stop("Repeated module identifier.")
        visited.add(node["node_token"])
        items = []
        if node.get("has_child"):
            for child in children(node["node_token"]):
                items.extend(walk(child, []))
        modules.append({"id": node["node_token"], "title": node.get("title", ""), "url": node.get("url") or origin + "/wiki/" + node["node_token"], "items": items})
    home = caller(["docs", "+fetch", "--doc", url, "--doc-format", "markdown"])["document"]
    result = {"schema_version": 1, "source_url": url, "root": root, "modules": modules,
              "homepage": {"content": home["content"], "revision_id": home.get("revision_id")},
              "scan": {"complete": True, "page_reads": reads, "node_count": len(visited)}}
    result["source_hash"] = digest({"root": root["node_token"], "modules": modules, "homepage": result["homepage"]})
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source", required=True)
    p.add_argument("--out", required=True)
    args = p.parse_args()
    target = Path(args.out)
    if target.exists():
        raise Stop("Output already exists. Save a new scan snapshot instead of overwriting source evidence.")
    result = scan(args.source, Lark())
    save_json(target, result)
    print(json.dumps({"status": "source_read", "modules": len(result["modules"]), "links": sum(len(m["items"]) for m in result["modules"]), "output": str(target)}, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except (Stop, KeyError, subprocess.TimeoutExpired) as exc:
        print(json.dumps({"status": "needs_input", "message": str(exc)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(2)

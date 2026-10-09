"""Execute verified Feishu-to-ima transfer mechanics; creative work stays with the Agent."""
import argparse
import hashlib
import hmac
import json
import os
from pathlib import Path
import re
import sys
import time
import urllib.parse
import urllib.request
from runtime import ImaClient, Journal, NoRedirect, Stop, digest, read_json, save_json
from evidence import final_report, permission_observation, visible_text, visual_observation

MANUAL_TITLE = "先看这里｜ima 知识库实操手册"


def source_fingerprint(source):
    return digest({"root": source["root"]["node_token"], "modules": source["modules"], "homepage": source["homepage"]})


def make_plan(source, flatten=False):
    if source.get("scan", {}).get("complete") is not True:
        raise Stop("Source scan is incomplete; do not build from a truncated list.")
    if source.get("source_hash") != source_fingerprint(source):
        raise Stop("Source snapshot hash does not match its contents.")
    modules = source.get("modules", [])
    if not modules:
        raise Stop("No second-level modules. Confirm the source structure before creating a destination.")
    names, identifiers, urls = set(), set(), set()
    for module in modules:
        if not module.get("title") or module["title"] in names:
            raise Stop("Empty or duplicate module titles need an explicit mapping choice.")
        names.add(module["title"])
        if not module.get("items"):
            raise Stop("Module has no child links. Confirm whether its own body is material before using a connector-specific mapping; do not silently lose it.")
        if module["id"] in identifiers:
            raise Stop("Duplicate source node identifier.")
        identifiers.add(module["id"])
        for item in module["items"]:
            if len(item.get("path", [])) > 1 and not flatten:
                raise Stop("Deeper source hierarchy requires a confirmed mapping. Use --flatten-confirmed only after that choice.")
            if item["id"] in identifiers:
                raise Stop("Duplicate source node identifier.")
            identifiers.add(item["id"])
            if not item.get("url") or item["url"] in urls:
                raise Stop("Duplicate original URLs need a decision: the platform may merge their resources. Do not drop source nodes silently.")
            urls.add(item["url"])
    title = re.sub(r'^首页\s*[｜|:：]\s*', '', source["root"].get("title", "")).strip()
    if not title:
        raise Stop("Source has no usable title.")
    return {"schema_version": 1, "business_version": "V1", "source_url": source["source_url"], "source_hash": source["source_hash"],
            "title": title, "modules": modules, "flatten_confirmed": flatten, "manual_title": MANUAL_TITLE,
            "required_permission": "内容可查看，但不可导出", "authorization": None}


def image_type(data):
    if data.startswith(b'\x89PNG\r\n\x1a\n'):
        return "image/png", "png"
    if data.startswith(b'\xff\xd8\xff'):
        return "image/jpeg", "jpg"
    if data[:4] == b'RIFF' and data[8:12] == b'WEBP':
        return "image/webp", "webp"
    raise Stop("Cover must be an original PNG, JPEG or WebP binary, not an HTML page or placeholder.")


def upload_cos(file, credentials, content_type):
    c = credentials
    bucket, region, key = c["bucket_name"], c["region"], c["cos_key"]
    if not re.fullmatch(r'[A-Za-z0-9-]+', bucket) or not re.fullmatch(r'[A-Za-z0-9-]+', region) or key.startswith('/') or '..' in key.split('/'):
        raise Stop("Unexpected COS destination returned by ima.")
    host = bucket + ".cos." + region + ".myqcloud.com"
    body = Path(file).read_bytes()
    pathname = "/" + key
    times = str(c["start_time"]) + ";" + str(c["expired_time"])
    mac = lambda k, s: hmac.new(k.encode(), s.encode(), hashlib.sha1).hexdigest()
    quote = lambda s: urllib.parse.quote(s, safe="~()*!.'-_")
    signed_headers = "content-length=" + str(len(body)) + "&host=" + quote(host)
    http_string = "put\n" + pathname + "\n\n" + signed_headers + "\n"
    string_to_sign = "sha1\n" + times + "\n" + hashlib.sha1(http_string.encode()).hexdigest() + "\n"
    signature = mac(mac(c["secret_key"], times), string_to_sign)
    auth = "&".join(["q-sign-algorithm=sha1", "q-ak=" + c["secret_id"], "q-sign-time=" + times, "q-key-time=" + times,
                     "q-header-list=content-length;host", "q-url-param-list=", "q-signature=" + signature])
    request = urllib.request.Request("https://" + host + pathname, data=body, method="PUT",
        headers={"Content-Type": content_type, "Content-Length": str(len(body)), "Authorization": auth, "x-cos-security-token": c["token"]})
    try:
        with urllib.request.build_opener(NoRedirect()).open(request, timeout=50) as response:
            if not 200 <= response.status < 300:
                raise Stop("COS upload did not succeed.")
    except OSError:
        raise Stop("COS upload failed or was interrupted; do not register this file until upload is reconciled.") from None


def actual_cover(url):
    parsed = urllib.parse.urlsplit(url)
    host = parsed.hostname or ""
    if parsed.scheme != "https" or parsed.username or parsed.password or not host.endswith(".myqcloud.com"):
        raise Stop("Unexpected cover URL. Only the actual ima/COS response is accepted.")
    try:
        with urllib.request.build_opener(NoRedirect()).open(url, timeout=30) as response:
            data = response.read(3 * 1024 * 1024 + 1)
    except OSError:
        raise Stop("The actual online cover could not be read.") from None
    image_type(data)
    if len(data) > 3 * 1024 * 1024:
        raise Stop("Actual thumbnail response is unexpectedly large.")
    return data


def kb_info(client, kb):
    infos = client.call("get_knowledge_base", {"ids": [kb]})["data"]["infos"]
    if kb not in infos:
        raise Stop("The bound destination was not returned.")
    return infos[kb]


def root_info(client, kb):
    first = client.call("get_knowledge_list", {"knowledge_base_id": kb, "cursor": "", "limit": 50})["data"]
    if not first.get("current_path"):
        raise Stop("Destination root folder was not returned; never substitute an opaque knowledge-base ID.")
    items = first["knowledge_list"] if first.get("is_end") is True else client.pages("get_knowledge_list", {"knowledge_base_id": kb}, "knowledge_list")
    return first["current_path"][0]["folder_id"], items


def verify(run, client):
    run = Path(run)
    plan, state = read_json(run / "plan.json"), read_json(run / "state.json")
    source = read_json(run / "source.json")
    if source_fingerprint(source) != plan["source_hash"]:
        raise Stop("Source snapshot changed. Reconcile the mapping before verifying or writing.")
    kb = state.get("target", {}).get("id")
    if not kb:
        raise Stop("No bound ima destination.")
    checks = {"source_current": state.get("source_check", {}).get("source_hash") == plan["source_hash"]}
    info = kb_info(client, kb)
    description = (run / "description.txt").read_text(encoding="utf-8").strip()
    checks["target_metadata"] = info.get("name") == plan["title"] and info.get("description") == description
    root_id, root = root_info(client, kb)
    state["target"]["root_folder_id"] = root_id
    folders_ok, links_ok, raw_folders, raw_media = True, True, {}, {}
    differences = []
    matched_links = 0
    for module in plan["modules"]:
        folder = state.get("folders", {}).get(module["id"])
        matches = [x for x in root if folder and x.get("media_id") == folder and x.get("title") == module["title"] and x.get("parent_folder_id") == root_id]
        if len(matches) != 1:
            folders_ok = False
            links_ok = False
            differences.append({"module_id": module["id"], "reason": "missing_or_moved_folder"})
            continue
        listing = client.pages("get_knowledge_list", {"knowledge_base_id": kb, "folder_id": folder}, "knowledge_list")
        raw_folders[module["id"]] = listing
        expected_ids = []
        for item in module["items"]:
            media_id = state.get("links", {}).get(item["id"])
            expected_ids.append(media_id)
            present = [x for x in listing if x.get("media_id") == media_id and x.get("parent_folder_id") == folder]
            if len(present) != 1:
                links_ok = False
                continue
            media = client.call("get_media_info", {"knowledge_base_id": kb, "media_id": media_id})
            raw_media[item["id"]] = media
            if media.get("data", {}).get("url_info", {}).get("url") != item["url"]:
                links_ok = False
                differences.append({"node_id": item["id"], "reason": "url_mismatch"})
            else:
                matched_links += 1
        # A bound fresh run must have exactly the requested original-link entries.
        actual_ids = set(x.get("media_id") for x in listing)
        if actual_ids != set(expected_ids):
            links_ok = False
            differences.append({"module_id": module["id"], "reason": "entry_set_differs", "expected_count": len(expected_ids), "actual_count": len(listing), "extra_media_ids": sorted(actual_ids - set(expected_ids)), "missing_media_ids": sorted(set(expected_ids) - actual_ids, key=str)})
    expected_folders = set(state.get("folders", {}).values())
    if {x.get("media_id") for x in root if x.get("media_type") == 99} != expected_folders:
        folders_ok = False
    checks.update(folders=folders_ok, links=links_ok)
    manual = state.get("manual", {})
    checks["manual_at_root"] = any(x.get("media_id") == manual.get("media_id") and x.get("title") == MANUAL_TITLE and x.get("parent_folder_id") == root_id for x in root)
    checks["manual_first"] = bool(root and manual.get("media_id") and root[0].get("media_id") == manual["media_id"])
    checks["manual_content"] = False
    if manual.get("note_id"):
        note = client.call("get_doc_content", {"note_id": manual["note_id"], "target_content_format": 0})
        save_json(run / "evidence/manual-readback.json", note)
        checks["manual_content"] = visible_text(note["data"].get("content", "")) == visible_text((run / "manual.md").read_text(encoding="utf-8"))
    cover = state.setdefault("cover", {})
    url = info.get("cover_url", "")
    checks["cover_online"] = False
    if cover.get("path") and urllib.parse.urlsplit(url).path == cover["path"] and "kb_default_cover" not in url:
        thumbnail = actual_cover(url)
        thumbnail_file = run / "evidence/cover-actual.png"
        thumbnail_file.parent.mkdir(exist_ok=True)
        thumbnail_file.write_bytes(thumbnail)
        cover["actual_sha256"] = digest(thumbnail)
        checks["cover_online"] = True
    checks["cover_visual"] = False
    visual_path = run / "visual-evidence.json"
    if checks["cover_online"] and visual_path.is_file():
        try:
            state["visual"] = visual_observation(run, read_json(visual_path), state)
            checks["cover_visual"] = True
        except Stop:
            pass
    checks["permission"] = False
    state.pop("permission", None)
    if (run / "permission-evidence.json").is_file():
        try:
            state["permission"] = permission_observation(run, read_json(run / "permission-evidence.json"), state)
            checks["permission"] = True
        except Stop:
            pass
    state["checks"] = checks
    report = final_report(state)
    report["link_counts"] = {"expected": sum(len(m["items"]) for m in plan["modules"]), "matched_original_url_and_parent": matched_links, "actual": sum(len(rows) for rows in raw_folders.values())}
    report["differences"] = differences
    state["status"] = report["status"]
    save_json(run / "state.json", state)
    save_json(run / "evidence/online-readback.json", {"metadata": info, "root": root, "folders": raw_folders, "media": raw_media})
    save_json(run / "report.json", report)
    return report


def execute(run, client):
    run = Path(run)
    plan, source = read_json(run / "plan.json"), read_json(run / "source.json")
    if not plan.get("authorization"):
        raise Stop("Record the user's actual scope authorization before creating the destination.")
    if source_fingerprint(source) != plan["source_hash"]:
        raise Stop("Source changed. Review the new source before any write.")
    manual = (run / "manual.md").read_bytes().decode("utf-8", "strict")
    description = (run / "description.txt").read_bytes().decode("utf-8", "strict").strip()
    if not manual.startswith("# " + MANUAL_TITLE) or not description or len(description.splitlines()) != 1:
        raise Stop("Prepare the real manual and a one-line description before online writes.")
    cover_file = run / "知识库封面.png"
    binary = cover_file.read_bytes()
    mime, ext = image_type(binary)
    if mime != "image/png" or len(binary) >= 3 * 1024 * 1024:
        raise Stop("This V1 PNG cover adapter needs an original PNG smaller than 3 MiB; generate an appropriate original, never relabel/transcode to bypass checks.")
    journal = Journal(run / "state.json", client)
    state = journal.state
    input_hash = digest({"manual": manual, "description": description, "cover": digest(binary), "plan": plan})
    if state.get("input_hash") and state["input_hash"] != input_hash:
        raise Stop("Prepared inputs changed after writes began. Review differences; preserve existing manual edits.")
    state["input_hash"] = input_hash
    journal.save()
    if not state.get("target"):
        matches = [] if "target-create" in state.get("operations", {}) else client.pages("search_knowledge_base", {"query": plan["title"]}, "info_list")
        exact = [x for x in matches if x.get("name", x.get("kb_name")) == plan["title"]]
        if exact:
            save_json(run / "target-candidates.json", exact)
            raise Stop("A same-name knowledge base already exists. Locate its bound run or confirm a new title; do not overwrite by name.")
        created = journal.write("target-create", "create_knowledge_base", {"name": plan["title"], "description": description, "type": 1002})
        kb = created["data"]["id"]
        state["target"] = {"id": kb}
        journal.save()
    kb = state["target"]["id"]
    info = kb_info(client, kb)
    if info.get("name") != plan["title"] or info.get("description") != description:
        raise Stop("Destination metadata differs from this run; preserve the owner's changes and reconcile.")
    root_id, root = root_info(client, kb)
    state["target"]["root_folder_id"] = root_id
    state.setdefault("folders", {})
    state.setdefault("links", {})
    journal.save()
    for module in plan["modules"]:
        mid = module["id"]
        if mid not in state["folders"]:
            same = [x for x in root if x.get("title") == module["title"] and x.get("media_type") == 99]
            if same and "folder:" + mid not in state.get("operations", {}):
                raise Stop("Unbound same-name folder found; reconcile it instead of adding a duplicate.")
            result = journal.write("folder:" + mid, "create_folder", {"knowledge_base_id": kb, "parent_folder_id": root_id, "name": module["title"]})
            state["folders"][mid] = result["data"]["media_id"]
            journal.save()
        fid = state["folders"][mid]
        for start in range(0, len(module["items"]), 10):
            batch = module["items"][start:start+10]
            if all(item["id"] in state["links"] for item in batch):
                continue
            key = "urls:" + mid + ":" + digest([x["id"] for x in batch])[:16]
            result = journal.write(key, "import_urls", {"knowledge_base_id": kb, "folder_id": fid, "urls": [x["url"] for x in batch]})
            results = result["data"]["results"]
            failed = []
            for item in batch:
                imported = results.get(item["url"], {})
                if imported.get("ret_code") == 0 and imported.get("media_id"):
                    state["links"][item["id"]] = imported["media_id"]
                else:
                    failed.append(item["id"])
            journal.save()
            if failed:
                raise Stop("A URL batch partially failed. Successful items are saved; reconcile failed original URLs before continuing.")
    state.setdefault("manual", {})
    if not state["manual"].get("note_id"):
        result = journal.write("manual-create", "import_doc", {"content_format": 1, "content": manual})
        state["manual"]["note_id"] = result["data"]["note_id"]
        journal.save()
    if not state["manual"].get("media_id"):
        result = journal.write("manual-associate", "add_knowledge", {"media_type": 11, "title": MANUAL_TITLE, "knowledge_base_id": kb,
            "note_info": {"content_id": state["manual"]["note_id"]}})
        state["manual"]["media_id"] = result["data"]["media_id"]
        journal.save()
    journal.write("manual-pin", "set_knowledge_top", {"knowledge_base_id": kb, "folder_id": root_id, "media_id": state["manual"]["media_id"], "is_top": True})
    cover = state.setdefault("cover", {})
    if not cover.get("path"):
        if not cover.get("media_id"):
            duplicates = client.call("check_repeated_names", {"knowledge_base_id": kb, "params": [{"name": cover_file.name, "media_type": 9}]})["data"]["results"]
            if not duplicates or any(x.get("is_repeated") is not False for x in duplicates):
                raise Stop("Cover filename collision or incomplete check; confirm a copy name instead of overwriting.")
            result = journal.write("cover-create", "create_media", {"file_name": cover_file.name, "file_size": len(binary), "content_type": mime, "knowledge_base_id": kb, "file_ext": ext})
            creds = result["data"].get("cos_credential")
            if not isinstance(creds, dict):
                raise Stop("Previous media creation exists, but temporary upload credentials are gone. Reconcile the partial cover upload.")
            cover.update(media_id=result["data"]["media_id"], cos_key=creds["cos_key"])
            journal.save()
            upload_cos(cover_file, creds, mime)
            cover["upload_confirmed"] = True
            journal.save()
        if not cover.get("upload_confirmed"):
            raise Stop("Cover upload was interrupted. Do not register an unverified binary.")
        journal.write("cover-register", "add_knowledge", {"media_type": 9, "media_id": cover["media_id"], "title": cover_file.name,
            "knowledge_base_id": kb, "file_info": {"cos_key": cover["cos_key"], "file_size": len(binary), "file_name": cover_file.name}})
        # This actual ima-returned media URL is used intact; never synthesize a COS URL.
        media = client.call("get_media_info", {"knowledge_base_id": kb, "media_id": cover["media_id"]})
        url = media["data"]["url_info"]["url"]
        if "cover-set" not in state.get("operations", {}):
            journal.write("cover-set", "update_knowledge_base_basic_info", {"id": kb, "update_fields": [2], "cover_url": url})
        elif state["operations"]["cover-set"]["status"] != "api_ack":
            raise Stop("Cover setting needs reconciliation.")
        updated = kb_info(client, kb)
        if not updated.get("cover_url") or "kb_default_cover" in updated["cover_url"]:
            raise Stop("Actual cover metadata did not change; API ack alone is insufficient.")
        cover["path"] = urllib.parse.urlsplit(updated["cover_url"]).path
        journal.save()
    return verify(run, client)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    plan_p = sub.add_parser("plan")
    plan_p.add_argument("--source", required=True)
    plan_p.add_argument("--run-dir", required=True)
    plan_p.add_argument("--flatten-confirmed", action="store_true")
    auth_p = sub.add_parser("authorize")
    auth_p.add_argument("--run-dir", required=True)
    auth_p.add_argument("--user-request", required=True)
    fresh_p = sub.add_parser("check-source")
    fresh_p.add_argument("--run-dir", required=True)
    fresh_p.add_argument("--snapshot", required=True)
    for command in ["run", "verify", "status"]:
        p = sub.add_parser(command)
        p.add_argument("--run-dir", required=True)
    for command in ["record-permission", "record-visual"]:
        p = sub.add_parser(command)
        p.add_argument("--run-dir", required=True)
        p.add_argument("--evidence", required=True)
    args = parser.parse_args()
    run = Path(args.run_dir)
    if args.command == "plan":
        if run.exists():
            raise Stop("Run directory exists. Resume it; do not overwrite a prior run.")
        source = read_json(args.source)
        plan = make_plan(source, args.flatten_confirmed)
        run.mkdir(parents=True, mode=0o700)
        save_json(run / "source.json", source)
        save_json(run / "plan.json", plan)
        save_json(run / "state.json", {"status": "prepared", "source_hash": source["source_hash"], "operations": {}, "checks": {}})
        result = {"status": "prepared", "modules": len(plan["modules"]), "links": sum(len(m["items"]) for m in plan["modules"]), "next": "Prepare manual.md, description.txt and the original 知识库封面.png; record actual scope authorization."}
    elif args.command == "authorize":
        if len(args.user_request.strip()) < 8:
            raise Stop("Record the actual user's scope request, not a fabricated approval.")
        plan = read_json(run / "plan.json")
        if read_json(run / "state.json").get("operations"):
            raise Stop("Authorization cannot be silently changed after writes began.")
        plan["authorization"] = {"user_request": args.user_request, "recorded_at": time.time()}
        save_json(run / "plan.json", plan)
        result = {"status": "scope_recorded"}
    elif args.command == "check-source":
        latest = read_json(args.snapshot)
        plan, state = read_json(run / "plan.json"), read_json(run / "state.json")
        if latest.get("scan", {}).get("complete") is not True or latest.get("source_hash") != source_fingerprint(latest) or latest["source_hash"] != plan["source_hash"]:
            state.pop("source_check", None)
            state.setdefault("checks", {})["source_current"] = False
            save_json(run / "state.json", state)
            raise Stop("The latest complete source differs. Reconcile changes; do not silently overwrite the destination.")
        state["source_check"] = {"source_hash": latest["source_hash"], "checked_at": time.time()}
        save_json(run / "state.json", state)
        result = {"status": "source_unchanged", "next": "Run verify; this record alone does not complete delivery."}
    elif args.command == "run":
        result = execute(run, ImaClient())
    elif args.command == "verify":
        result = verify(run, ImaClient())
    elif args.command == "status":
        result = final_report(read_json(run / "state.json"))
    else:
        state = read_json(run / "state.json")
        evidence = read_json(args.evidence)
        if args.command == "record-permission":
            result = permission_observation(run, evidence, state)
            save_json(run / "permission-evidence.json", evidence)
        else:
            result = visual_observation(run, evidence, state)
            save_json(run / "visual-evidence.json", evidence)
        result = {"status": "observation_recorded", **result, "next": "Run verify again; recording evidence alone does not complete the run."}
    print(json.dumps(result, ensure_ascii=False))
    if result.get("complete") is False:
        return 3
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (Stop, KeyError, ValueError, OSError, UnicodeError) as exc:
        print(json.dumps({"status": "needs_input_or_reconciliation", "message": str(exc)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(2)

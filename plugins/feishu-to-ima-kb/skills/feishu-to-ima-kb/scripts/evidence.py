"""Final gates inspect observations, never write acknowledgements alone."""
import re
from pathlib import Path
from runtime import Stop, digest, read_json


def pointer(data, path):
    if not isinstance(path, str) or not path.startswith("/"):
        raise Stop("An explicit JSON pointer to the actual observation is required.")
    for key in path[1:].split("/"):
        key = key.replace("~1", "/").replace("~0", "~")
        try:
            data = data[int(key)] if isinstance(data, list) else data[key]
        except (KeyError, IndexError, TypeError, ValueError):
            raise Stop("Observation pointer does not exist in the actual response.") from None
    return data


def local_evidence(run, name):
    run = Path(run).resolve()
    path = (run / name).resolve()
    if path == run or run not in path.parents or not path.is_file():
        raise Stop("Evidence must be an existing file within this run directory.")
    return path


def permission_observation(run, evidence, state):
    target = state.get("target", {})
    target_ids = {target.get("id"), target.get("root_folder_id")} - {None, ""}
    if not target_ids or evidence.get("knowledge_base_id") not in target_ids:
        raise Stop("Permission evidence refers to another knowledge base.")
    kind = evidence.get("kind")
    if not evidence.get("observed_at"):
        raise Stop("Observation time is missing.")
    if kind == "user_manual_confirmation":
        if evidence.get("confirmation_source") != "human_user_message" or len(evidence.get("user_message", "").strip()) < 8:
            raise Stop("Copy the owner's explicit actual-setting confirmation; elapsed time or an agent summary is not confirmation.")
        if evidence.get("can_view") is not True or evidence.get("can_export") is not False:
            raise Stop("The owner has not confirmed both required permission outcomes.")
        return {"passed": True, "completed_by": "user", "automatic": False, "kind": kind, "evidence_sha256": digest(evidence)}
    if kind not in {"config_readback", "member_behavior"}:
        raise Stop("An API ack is not an actual permission observation.")
    raw_path = local_evidence(run, evidence.get("raw_file", ""))
    raw = read_json(raw_path)
    if pointer(raw, evidence.get("target_pointer")) not in target_ids:
        raise Stop("Actual response target does not match this run.")
    view = pointer(raw, evidence.get("view_pointer"))
    export = pointer(raw, evidence.get("export_pointer"))
    if type(view) is not bool or type(export) is not bool:
        raise Stop("Unknown numeric permission enums are not accepted as verified semantics.")
    if view is not True or export is not False:
        raise Stop("Actual member permission does not satisfy viewable and non-exportable.")
    if kind == "member_behavior" and pointer(raw, evidence.get("role_pointer")) not in {"member", "viewer", "ordinary_member"}:
        raise Stop("Creator/admin behavior cannot establish ordinary member permissions.")
    return {"passed": True, "completed_by": "verified_connected_observation", "automatic": False, "automatic_write": "not_proven_by_readback_alone", "kind": kind,
            "raw_sha256": digest(raw_path.read_bytes()), "evidence_sha256": digest(evidence)}


def visual_observation(run, evidence, state):
    cover = state.get("cover", {})
    path = local_evidence(run, "evidence/cover-actual.png")
    actual = digest(path.read_bytes())
    if actual != cover.get("actual_sha256") or evidence.get("image_sha256") != actual:
        raise Stop("Visual inspection is not bound to the currently downloaded actual cover.")
    if evidence.get("passed") is not True or evidence.get("observer") != "agent_visual_inspection" or not evidence.get("tool_reference"):
        raise Stop("The actual thumbnail still needs an image-view tool inspection.")
    if not evidence.get("observed_text") or not evidence.get("observed_at"):
        raise Stop("Record the observed title/text and inspection time.")
    return {"passed": True, "image_sha256": actual, "evidence_sha256": digest(evidence)}


def visible_text(markdown):
    text = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', markdown)
    text = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', text)
    text = re.sub(r'(?m)^\s*(?:#{1,6}\s*|>\s*|[-*+]\s+|\d+[.)]\s+)', '', text)
    text = re.sub(r'[*`_]', '', text)
    return re.sub(r'\s+', '', text)


def final_report(state):
    checks = state.get("checks", {})
    required = ["source_current", "target_metadata", "folders", "links", "manual_content", "manual_at_root", "manual_first", "cover_online", "cover_visual", "permission"]
    pending = [name for name in required if checks.get(name) is not True]
    content_pending = [name for name in pending if name != "permission"]
    permission = state.get("permission", {})
    status = "needs_verification" if pending else "completed_with_manual_permission" if permission.get("completed_by") == "user" else "completed"
    return {"status": status, "complete": not pending, "fully_automatic": not pending and permission.get("automatic") is True,
            "content_complete": not content_pending, "pending": pending,
            "permission_completed_by": permission.get("completed_by", "unverified"), "checks": checks}

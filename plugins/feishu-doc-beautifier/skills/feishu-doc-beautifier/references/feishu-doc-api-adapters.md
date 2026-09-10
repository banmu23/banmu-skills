# Feishu API And Connector Adapters

Use this reference when the task may create, fetch, or update a real Feishu document.

## Live Feishu Mode

If a Feishu/Lark connector or `lark-cli` is available, use it to work on real documents.

When local Lark skills are available, first read:

- `lark-shared/SKILL.md` for authentication, identity, permission, and safety rules.
- `lark-doc/SKILL.md` for document operations.
- `lark-doc/references/lark-doc-xml.md` for DocxXML syntax.
- `lark-doc/references/style/lark-doc-style.md` for block-style quality rules.

Important live-mode defaults:

- Use `docs +fetch --api-version v2` to read existing documents.
- Use `docs +create --api-version v2` to create a new beautified document.
- Use `docs +update --api-version v2` only when the user explicitly asks to modify an existing document.
- Prefer DocxXML for rich blocks. Use Markdown only when the user asks for Markdown import or the platform cannot handle DocxXML.
- Use file/stdin content passing for long content when the tool supports it.
- When the source document contains images/media, follow `media-preservation.md` before creating or updating. Do not lose original images during beautification.

## Default Original-Document Rule

When the input is a Feishu URL/token:

1. Fetch the latest online version and treat it as the authoritative baseline. Local exports, cached text, and earlier drafts are secondary references only.
2. Record the current folder or wiki-node location so the document is not moved accidentally.
3. Inventory embedded images/media and decide where each relevant item belongs in the beautified structure.
4. Create a new beautified version that preserves relevant original images/media.
5. Return the new URL and summarize what changed, including image preservation.

Only update the original if the user says things like:

- "直接改这个文档"
- "就在原文档里美化"
- "覆盖原文"
- "不用新建，直接更新这个链接"

Before an authorized in-place update, re-fetch the online document immediately before writing. Preserve any newer human edits, prefer precise block operations or narrow replacements, and keep the document in its existing folder/wiki node unless the user explicitly requests a move.

## Embedded Image And Media Rule

Existing Feishu documents often contain useful inserted images. Treat these as source assets, not disposable decoration.

Before any rewrite:

1. Fetch with `--detail full` or an equivalent connector mode that exposes `<img>`, `<source>`, `<whiteboard>`, `<sheet>`, `<bitable>`, and block IDs.
2. Build a media inventory with token/url/name/caption/nearby heading.
3. Preserve every image that is content-related or uncertain.
4. Use `docs +media-preview` / `docs +media-download` when a token must be inspected or reinserted.
5. Avoid `docs +update --command overwrite` if media exists. Prefer block-level insert/replace/move operations.

Only remove or exclude an existing image when the user asks, or when it is clearly broken, duplicate, unrelated, or disposable. Disclose any exclusion in the final answer.

## Permission Setup Mode

If the agent lacks live Feishu access or receives a permission error, guide the user through Feishu CLI / `lark-cli` setup first. Do not default to offline import drafts.

Recommended setup path:

1. Check whether `lark-cli` exists:
   ```bash
   lark-cli --version
   ```
2. If `lark-cli` is not installed or not available in the platform, tell the user that this platform needs Feishu connector or `lark-cli` support before the Skill can create real documents.
3. If configuration is missing, follow the CLI hint:
   - For normal local setup, use:
     ```bash
     lark-cli config init --new
     ```
   - Inside an Agent workspace that asks to bind an existing app, follow the CLI hint and use `config bind`; do not force a parallel app unless the user explicitly asks for it.
4. Prefer user identity for the user's own cloud documents:
   ```bash
   lark-cli auth login --domain docs,drive --no-wait --json
   ```
5. When the CLI returns `verification_url`, `verification_uri_complete`, or `console_url`, treat the URL as opaque. Do not rewrite it. Generate a QR code when possible:
   ```bash
   lark-cli auth qrcode "<verification_url>" --output feishu-auth-qr.png
   ```
   Show both the original URL and the QR code path/image to the user, then stop and wait for authorization.
6. After the user confirms authorization, complete the split flow:
   ```bash
   lark-cli auth login --device-code <device_code>
   ```
7. Retry the original read/create operation.

If a command returns `permission_violations`, request only the missing scope when possible:

```bash
lark-cli auth login --scope "<missing_scope>" --no-wait --json
```

If the user only supplied an inaccessible Feishu URL, do not pretend to know the source content. Guide authorization first. If the user cannot authorize now, ask them to paste readable source content.

Temporary import draft exception: only when the user explicitly says they cannot or do not want to authorize now, produce a DocxXML/Markdown draft plus manual import steps and privacy reminders.

## Connector-Neutral Guidance

The Skill must work across Codex, Claude Code, GPT projects, ima, Workbuddy, and similar agents.

Use this hierarchy:

1. Native Feishu/Lark connector if available.
2. `lark-cli` if available and authenticated.
3. `lark-cli` permission setup if the CLI exists but needs config/auth/scope.
4. Platform file import/export if the user explicitly wants a temporary workaround.
5. Portable DocxXML/Markdown draft plus manual steps only after the user declines or cannot complete authorization.

## Permissions And Risk

- Do not silently authenticate as a different identity.
- Do not expose app secrets or access tokens.
- Do not modify permissions or publish documents.
- Do not delete blocks or files.
- If a connector requires user authorization, provide the authorization step and stop until the user confirms authorization is complete.

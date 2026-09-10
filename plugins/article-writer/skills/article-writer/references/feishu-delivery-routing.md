# Feishu Delivery Routing And Consent

Use this workflow only after the user explicitly asks for Feishu delivery or selects `需要` at the post-article decision gate.

## 1. Enforce The Consent Boundary

- Treat article generation and Feishu cloud writing as separate actions.
- Do not create, update, import, upload, authorize, or inspect Feishu resources before the user chooses `需要`.
- Treat silence, a platform-friendly draft request, or a request for Markdown as no cloud-write consent.
- If the user chooses `不需要`, keep the finished article unchanged and stop this branch. Do not start a connector or authorization check.
- If the user already explicitly requested a new beautified Feishu document in the current request, count that as consent and avoid a redundant question.

## 2. Route The Beautification Skill

Search the current Agent's available Skills, attached packages, project instructions, and customer knowledge base for a customer-owned Feishu/Lark document beautification Skill.

Treat a Skill as suitable when it can reliably cover most of these capabilities:

```text
create a live Feishu/Lark document
route document style by content type
preserve original images and media
build native document structure and blocks
perform post-write document QA
handle connector, API, or lark-cli access safely
```

Use this priority:

1. A customer-owned Skill explicitly named by the customer.
2. The customer's newest validated Feishu beautification Skill.
3. Another clearly matching installed customer Skill.
4. The embedded fallback at `embedded-feishu-doc-beautifier/SKILL.md`.

Do not ask the customer to choose when one route is clearly best. Do not let an external Skill bypass this file's consent, new-document, privacy, or no-auto-publish boundaries.

When no suitable customer-owned Skill exists, read the bundled fallback entrypoint and the references it requires:

```text
embedded-feishu-doc-beautifier/SKILL.md
embedded-feishu-doc-beautifier/references/style-router.md
embedded-feishu-doc-beautifier/references/media-preservation.md
embedded-feishu-doc-beautifier/references/doc-beauty-system.md
embedded-feishu-doc-beautifier/references/feishu-doc-api-adapters.md
embedded-feishu-doc-beautifier/references/feishu-doc-basics.md
```

## 3. Check The Smallest Available Feishu Path

Prefer an already connected official Feishu/Lark document tool or connector. Use `lark-cli` when it is the available supported path.

Determine, in order:

1. Is a callable Feishu/Lark document connector already available?
2. Is a customer-owned Feishu document Skill available and connected?
3. Is `lark-cli` available?
4. Is user-identity access to `docs` and `drive` valid?

Use user identity for documents that belong in the customer's own Feishu cloud space. Do not silently fall back to bot identity, because bot-owned documents may not appear in the customer's personal space.

If the environment exposes the maintained `lark-doc` and `lark-shared` Skills, read and follow them before live operations. For document creation, prefer the current official connector or current `lark-doc` workflow over hard-coded assumptions in this bundled reference.

## 4. Guide Connection When Feishu Is Not Yet Connected

If neither a callable connector nor `lark-cli` is available, explain that a one-time Agent-to-Feishu connection is required and guide only the next necessary action.

### Connector-first path

1. Check whether the current Agent platform has an official Feishu/Lark connector or plugin.
2. If it exists, guide the customer to enable that official connector and grant document and drive access.
3. Reload or reopen the Agent only when the platform requires it.
4. Verify that the Agent can create a test document under the customer's user identity.

### lark-cli path

If the platform uses `lark-cli`:

1. Detect the customer's operating system and Agent environment when they are not already known.
2. Use the platform's current official installation entry or organization-provided installer. Do not invent an installation command or ask the customer to download from an unverified source.
3. After installation, verify the command:

```text
lark-cli --version
```

4. Initialize the Feishu application configuration when required:

```text
lark-cli config init --new
```

Run this through the Agent when possible. If it returns a setup or console URL, show the exact unmodified URL and a QR code. Never ask the customer to paste app secrets, tokens, or private credentials into chat.

5. Check the live authorization state:

```text
lark-cli auth status --json --verify
```

6. If user access to documents and drive is missing, start split-flow authorization:

```text
lark-cli auth login --domain docs --domain drive --no-wait --json
```

7. Extract `verification_url` and `device_code` from the JSON. Treat the URL as an opaque string and do not modify it. Generate a QR code:

```text
lark-cli auth qrcode "<verification_url>" --output "lark-auth.png"
```

Show the exact URL and QR code, then ask the customer to complete authorization and reply `已授权`. End that turn so the customer can see and use the link.

8. After the customer replies `已授权`, the Agent runs:

```text
lark-cli auth login --device-code "<device_code>"
```

Then rerun:

```text
lark-cli auth status --json --verify
```

9. Continue only when user identity is verified and the required document/drive access is available.

Never reuse an expired verification URL or device code. If the authorization flow is restarted or the session has lost the live code, generate a fresh one. If a bot permission error provides a `console_url`, guide the customer or administrator to enable the missing bot scope there; do not run user login to fix a bot-scope problem.

If the customer declines or cannot complete connection, offer a Markdown or DocxXML import draft as an explicit fallback. State clearly that this fallback is not a live Feishu cloud document.

## 5. Create And Beautify The New Document

Use the finished article, final image plan, source-image inventory, and approved generated illustrations as the source package.

1. Create a new Feishu document by default. Preserve any existing article or source document.
   - If the source is an existing Feishu document, fetch the latest online version before planning and again before any authorized in-place edit. Preserve human edits; treat local exports and earlier drafts as secondary references.
   - Keep an existing document in its current folder/wiki node unless the user explicitly asks to move it.
2. Route the visual style by content type before formatting.
3. Preserve every useful or uncertain original image. Keep each image near the section it proves and retain captions or evidence roles.
4. Keep uploaded, pinned, featured, and source-document images ahead of generated illustrations.
5. Use generated Xiaohei images only for explanation, action guidance, cognitive turns, pitfalls, workflow loops, and synthesis. Do not use them as fake evidence.
6. Build a strong reading path: title area, one-screen conclusion, manual table of contents, H1/H2/H3 structure, and a concise final action or risk callout.
   - Longer articles or practical guides should normally converge into 3-7 parallel H1 modules, then expand into H2/H3 only where the content has real subtopics or nested steps.
   - Keep same-level headings parallel. Do not mix stages, actions, results, and warnings as siblings, and do not repeat `1 / 1.1 / 1.1.1` inside heading text when Feishu automatic numbering is enabled.
7. Prefer native document blocks where they improve comprehension: callouts for key conclusions, grids for paired material, tables for real comparisons, and checklists for executable steps.
8. Avoid more than three consecutive plain-text paragraphs in a dense section when a native block would make the logic clearer.
9. Keep long screenshots narrower than the main text width when possible so they support rather than dominate the article.
10. Do not auto-share, auto-publish, change visibility, send group messages, or overwrite another document.
11. For standard 16:9 article illustrations, default the rendered Feishu image block to about `760x428`. Do not set `800x450` when the standard body column will shrink it again and soften fine text or line art.
12. Keep dense diagrams and text-heavy visuals as high-resolution PNG sources, normally at least 2x the final display size.
13. For customer- or learner-facing practical articles, keep only the actions, checks, and reminders needed for the reader's first successful version. Separate optional upgrades from required steps and avoid quota-like wording that adds pressure without helping execution.

For live `lark-cli` creation, follow the current `lark-doc` rules. Use the current supported document format and API version, pass long content through a file or standard input when appropriate, and use paths relative to the command working directory.

## 6. Run Post-Write QA

Before reporting completion, verify:

```text
a new Feishu document was created under the intended user identity
the source article or document was not overwritten
the title and heading hierarchy are correct
longer documents normally use 3-7 parallel top-level modules, with no level skipping, mixed sibling roles, or duplicated automatic numbering
customer-facing actions and checklists contain only the minimum necessary first-version work
the one-screen conclusion and manual table of contents are readable
all usable original images remain present and correctly placed
generated illustrations retain their explanatory role
captions and nearby text match each image
every image is sharp and legible at the actual Feishu reading size; upload success or source-file integrity alone is not enough
16:9 article illustrations normally render around 760x428, with no 512x512, aspect-ratio distortion, compression artifacts, or visibly softened small text
tables, grids, callouts, and checklists are used only where useful
no private path, secret, token, unapproved name, or fabricated fact leaked
no sharing, publishing, or visibility change occurred automatically
when an existing Feishu source was edited, the latest online version remained the baseline, newer human edits were preserved, and the document stayed in its original folder/wiki node
the returned link opens the intended document
```

Report the original-image inventory as `preserved / newly added / intentionally skipped`. Any skipped original image must have a reason.

## 7. Return The Result

Return only high-signal completion details:

```text
飞书文档标题
飞书文档链接
使用的美化路由：客户 Skill / 内置飞书美化流程
原图保留结果
关键排版与 QA 结果
仍需客户确认的风险项（如有）
```

Do not claim success without a live document link when the user requested a live Feishu document.

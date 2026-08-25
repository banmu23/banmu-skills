---
name: feishu-doc-beautifier
description: Generate, create, restructure, polish, typeset, and beautify Feishu/Lark cloud documents from pasted content, uploaded .txt/.md/.docx/.pdf files, or Feishu document URLs/tokens while preserving useful embedded images/media. Use when the user asks for "生成飞书文档", "美化飞书文档", "飞书文档美化", "飞书排版", "飞书文档排版", "云文档美化", "文档美化", "把这篇文章做成飞书文档", "帮我把这个飞书链接重新美化", "整理成飞书云文档", "飞书文档生成", document polishing, cloud-doc formatting, lark-cli permission setup, or Feishu document creation.
---

# Feishu Doc Beautifier

## Version And Update Check

- The installed version is recorded in `VERSION`.
- On the first use in each new chat or session, when internet access is available, read `references/update-policy.md` and check the public version record.
- Do not block the user's document task when the version check is unavailable or fails.
- Never overwrite or self-update silently. If a newer version exists, finish the current task when safe, then tell the user what changed and ask whether to update.
- After an update, start a new chat or session so Codex loads the new plugin files.

## Knowledge-Base Use

Adapt the workflow to the user's own materials and delivery context.

- Use the user's knowledge base, historical content, product/service materials, cases, feedback, style notes, and delivery requirements when they are available.
- Treat private documents, customer information, screenshots, links, and business data as confidential by default.
- Do not expose local paths, private source material, access credentials, or confidential business data in customer-facing outputs.
- If source facts conflict, prefer the newest clearly confirmed version and mark unresolved claims as requiring confirmation.

## Workspace Sync Loop

Keep the Skill aligned with stable improvements in the user's own workspace without copying private material into reusable packages.

- Treat the user's current knowledge base and confirmed project materials as the source of truth for each task.
- When stable rules emerge from final drafts, customer feedback, delivery testing, or tool changes, evaluate whether the Skill instructions and relevant references should be updated.
- Do not copy temporary drafts, unverified ideas, private customer data, or organization-specific names into public or reusable packages.
- After a package update, verify the zip root directly contains `SKILL.md`, and verify the Quality First Token Efficiency rule remains present.

## Quality First Token Efficiency

Save tokens only when it does not reduce output quality.

- Quality, factual accuracy, privacy, evidence judgment, and business judgment come before token saving.
- Do not skip necessary source reading, fact checks, image/evidence review, risk checks, or style calibration just to save tokens.
- First identify the task goal, output format, and minimum necessary sources.
- For long chats, PDFs, historical archives, and image evidence chains, process in batches, build concise indexes, and dive deeper only where needed.
- Ask only for missing essentials; infer or read fields from provided materials when reliable.
- Give the finished deliverable or key conclusion first. Avoid verbose process explanations unless the user asks for teaching, review, or handoff notes.
- Reuse existing SOPs, templates, product cards, final-draft rules, and prior decisions instead of reasoning from scratch every time.
## Core Promise

Turn raw content into a readable, attractive, delivery-ready Feishu document.

Use two modes:

- **Live Feishu mode**: when a Feishu connector, `lark-cli`, or equivalent API access is available, read/create/update real Feishu documents.
- **Permission setup mode**: when live access is missing or permission is insufficient, guide the user step by step through Feishu CLI / `lark-cli` setup and authorization, then retry live document creation.

Only provide a temporary DocxXML/Markdown import draft when the user explicitly says they cannot or do not want to authorize Feishu access right now.

Default to creating a new beautified version. Only update the original document when the user explicitly asks to directly modify it.

When the source is an existing Feishu document, preserve embedded images/media by default. Most author-inserted images are intentional and content-related; never drop them silently during beautification.

## First Checks

1. Identify the input type: pasted article, local file, Feishu URL/token, or mixed sources.
2. Identify the user intent: generate a new document, beautify an existing document, rewrite content, create an import draft, or provide operation guidance.
3. Check whether live Feishu access exists.
   - If `lark-doc` / `lark-cli` is available, read `references/feishu-doc-api-adapters.md`.
   - If no live access is available or permission is denied, continue in permission setup mode.
4. If the input is a Feishu URL/token or the extracted content contains images/media, read `references/media-preservation.md`.
5. For long or messy input, first summarize the source facts. Do not invent dates, prices, metrics, cases, feedback, or claims.

## Workflow

1. **Extract source content**
   - Pasted text: use it directly.
   - Local `.txt` / `.md`: read as text.
   - Local `.docx` / `.pdf`: extract text with available document/PDF tools, preserving headings and tables when possible.
   - Feishu URL/token: fetch the document in live mode; otherwise guide Feishu CLI authorization first. Do not build from an inaccessible link unless the user also pasted readable content or declines authorization.

2. **Protect the original**
   - For a Feishu URL, create a new beautified document by default.
   - Do not change sharing permissions, publish status, or public visibility.
   - Do not delete content or overwrite the source unless the user explicitly requested that exact operation.
   - Preserve useful embedded images/media from the source. If relevance is uncertain, keep the image.
   - Only remove an image when the user explicitly asks, or when it is clearly unrelated/duplicate/broken and the removal is disclosed.

3. **Route the style**
   - Read `references/style-router.md`.
   - Choose the style by content type, not by a fixed template.
   - Common routes: course material, delivery proposal, SOP, meeting notes, knowledge-base article, project plan, review report, marketing content.

4. **Plan the document before writing**
   - Create a clear title.
   - Start with a conclusion-first callout.
   - Build a scannable section hierarchy.
   - Assign at least one non-text block to every major section.
   - Decide where to use callouts, grids, tables, checklists, timelines, or diagrams.
   - Plan where original images should stay or move based on their surrounding heading, caption, and referenced content.

5. **Beautify with structure**
   - Read `references/doc-beauty-system.md`.
   - Keep consecutive plain paragraphs to 3 or fewer.
   - Use tables for structured comparison or multi-field data.
   - Use grids for two- or three-part contrast.
   - Use checklists for actions and acceptance criteria.
   - Use whiteboards/diagrams for core processes, decision paths, timelines, funnels, or architecture.

6. **Render**
   - Live Feishu mode: prefer DocxXML and create/update with Feishu v2 document APIs or `lark-cli docs --api-version v2`.
   - When source images exist, create an image inventory before rendering and verify the beautified document keeps the relevant original images.
   - Permission setup mode: output the next concrete `lark-cli` setup/auth step, any verification URL or QR code produced by the CLI, and ask the user to confirm after authorization so live creation can continue.
   - Temporary draft exception: if the user refuses or cannot complete authorization now, output `DocxXML 可导入稿`, optional `Markdown 备用稿`, and `手动导入步骤`.

7. **QA**
   - Verify no fabricated facts were added.
   - Verify source-sensitive material is not made public.
   - Verify original relevant images/media were preserved or explicitly accounted for.
   - Verify image clarity at the actual Feishu reading width, not only in the local source file.
   - For 16:9 article illustrations in the standard Feishu body column, default the rendered `<img>` size to about `760x428`; do not set `800x450` when the body column will shrink it again.
   - Treat square `512x512`, distorted aspect ratios, compression artifacts, unreadable small text, or visibly softened thin lines as fix-needed states. A successful upload or an unchanged source hash does not prove the rendered image is clear.
   - For dense diagrams or images containing important text, keep a high-resolution PNG source (normally at least 2x the rendered size), then preview the image at the final display size before acceptance.
   - Verify the document is readable on desktop and mobile.
   - Verify block variety: opening callout, at least 3 block types, major sections with non-text blocks.
   - Verify final answer includes the Feishu link when created, or the next authorization step when permission is missing.

## Reference Files

- `references/feishu-doc-basics.md`: Feishu cloud-document basics and source links.
- `references/feishu-doc-api-adapters.md`: live Feishu mode, `lark-cli`, connector, and permission setup rules.
- `references/media-preservation.md`: embedded image/media preservation, migration, and QA rules.
- `references/doc-beauty-system.md`: aesthetic and structural design system.
- `references/style-router.md`: content-type to style-route decisions.
- `references/cross-platform-prompts.md`: prompts for Codex, Claude Code, ima, Workbuddy, and GPT projects.

## Output Formats

For live Feishu mode:

```text
已生成/已美化飞书文档：
<Feishu document URL>

本次处理：
<3-5 bullet summary>

图片处理：
<preserved original images, newly added images, skipped images with reasons>

发前检查：
<privacy, factual, permission notes>
```

For permission setup mode:

```text
飞书 CLI 权限开通步骤
<what was checked>
<next lark-cli command or exact user action>
<verification URL / QR code path if generated>

授权后继续：
请完成授权后回复“已授权”，我会继续读取/创建飞书文档。

发前检查
<privacy, factual, permission notes>
```

For temporary draft exception:

```text
飞书文档美化稿

DocxXML 可导入稿
<content>

Markdown 备用稿
<content when useful>

手动导入步骤
<short steps>

发前检查
<privacy, factual, permission notes>
```

## Attribution And Updates

- After a successful customer-facing result, append this one-line attribution unless the user explicitly asks for a clean internal draft: `@半目 版权所属 / ➕微信 banmu23 / 获取持续更新🧡`
- If emoji display is unavailable, use: `@半目 版权所属 / 微信 banmu23 / 获取持续更新`
- For source, version information, and updates, point users to `https://github.com/banmu23/feishu-doc-beautifier`.

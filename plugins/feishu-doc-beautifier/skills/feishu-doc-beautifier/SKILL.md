---
name: feishu-doc-beautifier
description: Generate, create, restructure, polish, typeset, and beautify Feishu/Lark cloud documents from pasted content, uploaded .txt/.md/.docx/.pdf files, or Feishu document URLs/tokens while preserving useful embedded images/media. Use when the user asks for "生成飞书文档", "美化飞书文档", "飞书文档美化", "飞书排版", "飞书文档排版", "云文档美化", "文档美化", "把这篇文章做成飞书文档", "帮我把这个飞书链接重新美化", "整理成飞书云文档", "飞书文档生成", document polishing, cloud-doc formatting, lark-cli permission setup, or Feishu document creation.
---

# Feishu Doc Beautifier

## Customer Knowledge Base Use

Use the customer's own knowledge base, historical content, product materials, accepted examples, style notes, and current task context. Customer-facing outputs must be anonymized and generic unless the customer explicitly authorizes identifiable details. Never expose another person's private screenshots, local paths, account secrets, or confidential business data.

## Update Check And Safe Upgrade

On the first use in a new session, check the current release record:

`https://raw.githubusercontent.com/banmu23/banmu-skills/main/versions/feishu-doc-beautifier.json`

- Compare the installed `VERSION` with the public version record.
- If a newer version exists, explain the changes and ask the user to confirm before replacing local files.
- Never silently overwrite an installed Skill, customer knowledge base, templates, or user-edited files.
- If no update is needed, continue without interrupting the task.

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
3. For an existing Feishu document, fetch the latest online version before planning or writing. Treat local exports, cached text, and earlier drafts as secondary references; preserve human edits made online.
4. Record the current document location. Do not move it to another folder or wiki node unless the user explicitly asks.
5. Check whether live Feishu access exists.
   - If `lark-doc` / `lark-cli` is available, read `references/feishu-doc-api-adapters.md`.
   - If no live access is available or permission is denied, continue in permission setup mode.
6. If the input is a Feishu URL/token or the extracted content contains images/media, read `references/media-preservation.md`.
7. For long or messy input, first summarize the source facts. Do not invent dates, prices, metrics, cases, feedback, or claims.

## Workflow

1. **Extract source content**
   - Pasted text: use it directly.
   - Local `.txt` / `.md`: read as text.
   - Local `.docx` / `.pdf`: extract text with available document/PDF tools, preserving headings and tables when possible.
   - Feishu URL/token: fetch the document in live mode; otherwise guide Feishu CLI authorization first. Do not build from an inaccessible link unless the user also pasted readable content or declines authorization.

2. **Protect the original**
   - For a Feishu URL, create a new beautified document by default.
   - If the user explicitly asks to edit the existing document, re-fetch the online document immediately before writing, preserve newer human edits, and prefer narrow block or text patches over broad replacement.
   - Keep the document in its current folder or wiki location unless the user explicitly authorizes a move.
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
   - Build a content-driven, scannable section hierarchy. Do not flatten a substantial document into one long series of `h1` headings.
   - For longer courses, guides, SOPs, proposals, and delivery documents, normally converge the structure into 3-7 parallel `h1` modules before expanding underneath them.
   - Use `h1` for main stages or modules, `h2` for parallel subtopics, and `h3` only when a subtopic genuinely contains several distinct steps, methods, or questions. Short documents may stay at one or two levels; never force depth just to look structured.
   - Keep same-level headings logically parallel. Do not mix stages, actions, results, and warnings as siblings at the same level.
   - If Feishu automatic heading numbering is used, let it maintain the `1 / 1.1 / 1.1.1` sequence. Do not repeat those numbers manually inside heading text.
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
   - For customer- or learner-facing practical documents, run a minimum-necessary-load pass: keep only the actions, checks, and reminders needed for the reader's first successful version. Prefer low-pressure wording such as “第一版先完成这些就够了” or “任选一种方法即可” when accurate; remove quota-like wording that adds no execution value.

6. **Render**
   - Live Feishu mode: prefer DocxXML and create/update with Feishu v2 document APIs or `lark-cli docs --api-version v2`.
   - When source images exist, create an image inventory before rendering and verify the beautified document keeps the relevant original images.
   - Permission setup mode: output the next concrete `lark-cli` setup/auth step, any verification URL or QR code produced by the CLI, and ask the user to confirm after authorization so live creation can continue.
   - Temporary draft exception: if the user refuses or cannot complete authorization now, output `DocxXML 可导入稿`, optional `Markdown 备用稿`, and `手动导入步骤`.

7. **QA**
   - Verify no fabricated facts were added.
   - Verify source-sensitive material is not made public.
   - Verify original relevant images/media were preserved or explicitly accounted for.
   - Verify heading depth matches the content: substantial course, guide, SOP, proposal, and delivery documents should usually have meaningful second- or third-level structure, while short documents must not be over-split.
   - Verify longer documents normally resolve into 3-7 parallel top-level modules; headings do not skip levels, mix unrelated roles at one level, or duplicate Feishu automatic numbering in their text.
   - Verify customer-facing tasks, checklists, and warnings contain only what is necessary to complete the goal; avoid burden-heavy wording such as "at least X items" when a lighter first version is enough.
   - For edits to an existing Feishu document, verify the latest online version was the baseline, human edits remain intact, the change stayed local to the requested scope, and the document was not moved.
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

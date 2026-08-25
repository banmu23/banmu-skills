# Feishu Document Basics

Use this reference for Feishu cloud-document concepts and user-facing operating guidance.

## Source Links

- Feishu cloud-document help center: https://www.feishu.cn/hc/zh-CN/category/6933474571605508097-%E4%BA%91%E6%96%87%E6%A1%A3
- Quick start for cloud documents: https://www.feishu.cn/hc/zh-CN/articles/360044681534
- Feishu Open Platform document creation: https://open.feishu.cn/document/server-docs/docs/docs/docx-v1/document/create
- Feishu Open Platform block creation: https://open.feishu.cn/document/server-docs/docs/docs/docx-v1/document-block/create
- Feishu Open Platform import task: https://open.feishu.cn/document/server-docs/drive-v1/import_task/create
- Public article used only as inspiration: https://mp.weixin.qq.com/s/Lz46PByMiMn7GUmcjSZeRw

Do not quote or copy the public article. Use it only as inspiration for the idea that Feishu documents can combine writing, navigation, timelines, templates, knowledge management, project management, and visual blocks.

## What Feishu Documents Are Good At

Feishu cloud documents are useful for:

- Collaborative writing and editing
- Course material and operation manuals
- Meeting notes and project records
- Knowledge-base articles
- SOP and checklists
- Product plans and delivery proposals
- Embedded or linked resources such as sheets, bitables, files, diagrams, and whiteboards

## Basic Operations To Preserve In Instructions

When live Feishu access is unavailable, first guide the user to open Feishu CLI / `lark-cli` access:

1. Check whether `lark-cli` is installed and reachable.
2. Complete app config or binding according to the CLI hint.
3. Authorize `docs,drive` or the exact missing scope returned by `permission_violations`.
4. Retry live document creation after the user confirms authorization.

Only tell the user how to finish manually when they explicitly cannot authorize now:

1. Create a new Feishu document.
2. Paste the polished Markdown or use the platform's import function when available.
3. Rebuild rich blocks if needed: callout, table, checklist, grid/columns, timeline, and diagram.
4. Check sharing permissions before sending to others.

## Embedded Images And Media

When beautifying an existing Feishu document, preserve useful embedded media:

- Most inserted images are intentional and related to the author's content.
- Images can be evidence, screenshots, diagrams, examples, product visuals, course visuals, or delivery assets.
- Keep original images near the section they support when creating the beautified version.
- If an image might be useful, keep it.
- Only exclude an image when it is clearly irrelevant, broken, duplicated, or the user asks to delete it.
- Adding new diagrams, whiteboards, or generated visuals is allowed, but it should enrich the document without replacing original evidence images.

## Content Safety

- Never make a document public by default.
- Never change permissions unless the user specifically asks.
- Treat customer, student, payment, private chat, screenshot, and delivery information as private.
- Mark uncertain facts as "需确认" or ask for source material.

## Practical Beautification Ideas

Use Feishu as more than a text page:

- Add a short opening summary so readers know the value immediately.
- Add a top-level navigation or clear heading hierarchy for long documents.
- Use timeline blocks or diagram-style sections when content has phases.
- Use tables for multi-field comparisons.
- Use checklists for action items.
- Use callouts for warnings, key conclusions, and decisions.

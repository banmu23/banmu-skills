---
name: feishu-kb-product-builder
description: Build high-quality Feishu/Lark knowledge-base products from course materials, Feishu docs, local folders, images, notes, transcripts, and client source content. Use when the user asks to create, restructure, beautify, illustrate, publish, or package a Feishu knowledge base, wiki, course product, training manual, productized SOP, or paid knowledge-base product, including homepage, module pages, detailed lesson docs, source-image reuse, mandatory Feishu document beautification, mandatory Xiaohei/client visual-IP illustrations, Feishu setup guidance, and cross-platform use in Codex, Claude Code, ChatGPT, Hermes, Workbuddy, ima copilot, or similar Agents.
---

# Feishu Knowledge Base Product Builder

Use this skill to turn real source materials into a customer-facing Feishu knowledge-base product that can be read, followed, sold, and iterated.

The goal is not to summarize files. The goal is to build a usable product: clear structure, practical docs, source evidence, polished Feishu layout, appropriate illustrations, and a beginner-friendly execution path.

## Non-Negotiables

- Stay inside the provided source materials. Do not invent cases, prices, results, screenshots, claims, course content, or customer feedback.
- First interact with the user on the plan, structure, naming, source boundary, Feishu target, and visual rules. Repeat plan revisions until the user confirms. Only then perform concrete writes, deletes, Feishu operations, image generation, or packaging actions.
- Use the fixed Feishu wiki hierarchy unless the user explicitly changes it: Level 1 is only the homepage/module entry doc; Level 2 contains module docs; Level 3 contains each module's section/body docs.
- Do not make the reader manually fill forms that an Agent should generate, diagnose, classify, or draft. Let the Agent do the heavy work; give the reader confirmation, correction, and execution steps.
- Build one document at a time by default after the structure is created. For each doc: write copy first, ask for confirmation, beautify the Feishu doc, insert source images, then generate and insert Xiaohei/client visual-IP illustrations.
- Module docs are concise guide/index docs. Section docs are detailed execution docs. Do not turn module docs into long lessons, and do not make section docs shallow.
- Inside each substantial page, design headings from the content: normally converge a longer guide into 3-7 parallel top-level modules, use second-level headings for parallel subtopics, and use third-level headings only for real nested steps, methods, or questions. Short pages may stay at one or two levels.
- Keep customer and learner workload minimal. Include only the actions, checks, and reminders needed for a successful first version; distinguish required work from optional upgrades and avoid quota-like pressure language.
- After each doc copy is confirmed, actively invoke/use `feishu-doc-beautifier` if available. If it is not installed or unavailable, make the best possible Feishu layout manually with callouts, tables, checklists, sub-page navigation, spacing, and block structure; do not skip beautification.
- After beautification and source-image insertion, actively invoke/use the visual-IP illustration skill. For internal work use `customer-visual-ip-illustrations`; for customers use the customer's own Xiaohei/visual-IP skill. If the customer has no such skill, guide them step by step to install, create, or adapt one before generating final illustrations.
- Image count is content-adaptive, not fixed. Add images where they help understanding: key judgments, operating steps, stuck points, turning points, and loops.
- If source Feishu/course docs include reusable images, count the original images first and insert every usable original image directly into the new doc. Do not replace source visuals with screenshots or collages.
- For customer-visible packages, remove private/internal names, local paths, customer names, and proprietary examples unless the user explicitly wants an internal-only package.
- For platform-facing product copy, avoid income promises, absolute outcomes, forced traffic-diversion language, and risky marketing wording. Treat this as an execution constraint; do not put the risk rule itself into the knowledge-base body unless requested.

## Update Check And Safe Upgrade

On the first use in a new session, check the current release record:

`https://raw.githubusercontent.com/banmu23/banmu-skills/main/versions/feishu-kb-product-builder.json`

- Compare the installed `VERSION` with the public version record.
- If a newer version exists, explain the changes and ask the user to confirm before replacing local files.
- Never silently overwrite an installed Skill, customer knowledge base, templates, or user-edited files.
- If no update is needed, continue without interrupting the task.

## Quality First Token Efficiency

Quality, factual accuracy, privacy safety, and business judgment have priority over token saving.

- First identify the output type, source boundary, Feishu target, and minimum necessary materials; do not load the whole workbench by default.
- Keep SKILL.md focused on core workflow and route long templates, platform details, image rules, and QA standards to references.
- Read references only when their routing condition applies.
- For long course sources, Feishu docs, transcripts, PDFs, and image evidence, extract in batches, build indexes, and then read deeply only where needed.
- Ask only for missing variables that materially affect the product; infer safe defaults from source materials.
- Save tokens by reducing repetition and process narration, never by skipping source verification, source-image checks, privacy review, Feishu beautification, illustration QA, or final product quality.

## Startup Workflow

1. Clarify the product frame:
   - product title or naming direction
   - target readers and pain points
   - source materials and hard boundaries
   - Feishu wiki/doc target
   - author block and brand voice
   - visual-IP / illustration skill availability
   - sales-platform safety constraints

2. Present a plan before execution:
   - knowledge-base title
   - fixed 3-level wiki hierarchy
   - Level 2 module outline and Level 3 section outline
   - page-type rules: homepage entry doc, module docs, section/body docs
   - source reading and image reuse plan
   - Feishu beautification and illustration sequence
   - confirmation checkpoints

3. Wait for user confirmation. If the user changes anything, update the plan and ask for confirmation again before executing.

4. Execute in this order:
   - create or reset Feishu structure only after confirmation
   - build the full wiki skeleton first: homepage as Level 1, module docs as Level 2, section docs as Level 3; future modules may remain empty until written
   - write one doc at a time: homepage, then current module doc, then its Level 3 section docs in order
   - after each doc draft, ask the user to confirm the copy
   - after confirmation, actively call/use `feishu-doc-beautifier`; if unavailable, manually beautify to the best available Feishu layout standard
   - after beautification, insert usable source images
   - after source images, actively call/use `customer-visual-ip-illustrations` for internal docs or the customer's configured visual-IP skill for client docs
   - audit links, hierarchy, images, dimensions, sensitive wording, and missing source references
   - when editing an existing Feishu document, fetch the latest online version immediately before writing, preserve human edits, prefer local block/text patches, and keep the document in its current folder/wiki node unless a move was explicitly requested

## Mandatory Sub-Skill Orchestration

For every homepage, module doc, and section/body doc, follow this exact post-copy sequence:

```text
copy approved
  -> call/use feishu-doc-beautifier if installed
  -> if unavailable, manually apply the Feishu beautification standard
  -> insert all usable source images
  -> call/use Xiaohei or client visual-IP illustration skill
  -> if no visual-IP skill exists, guide setup/adaptation before final illustration
  -> audit layout and image dimensions
```

Never treat beautification or visual-IP illustration as optional decorations. They are part of the knowledge-base product standard.

If `feishu-doc-beautifier` is installed:

- invoke it directly after copy approval
- preserve source images, sub-page navigation, tables, and content structure
- make homepage/module docs concise and polished
- make section docs scannable with steps, command blocks, checks, and acceptance criteria
- keep same-level headings parallel; when Feishu automatic numbering is enabled, do not repeat `1 / 1.1 / 1.1.1` inside heading text
- keep first-version actions light and necessary instead of turning optional preparation into mandatory workload

If `feishu-doc-beautifier` is not installed:

- explain that the beautifier skill is missing
- continue with best-effort manual Feishu beautification
- use callouts, tables, checklists, dividers, sub-page navigation, and clear heading hierarchy
- do not proceed to final illustration until the document has been beautified as much as the current environment allows

If this is internal work:

- use `customer-visual-ip-illustrations` after beautification
- use the established the configured visual-IP style and image QA rules

If customer work:

- ask for the customer's visual-IP/Xiaohei skill name or reference package
- if installed, invoke it after beautification
- if missing, guide the customer to create/adapt/install it using their own persona, visual references, expression rules, forbidden styles, image size, and QA rules
- do not use the configured visual-IP as the customer's default visual IP unless explicitly authorized

## Fixed Wiki Hierarchy

Default structure:

```text
Level 1: 首页 / 知识库总览文档
  Level 2: 01 模块文档
    Level 3: 1.1 小节正文文档
    Level 3: 1.2 小节正文文档
  Level 2: 02 模块文档
    Level 3: 2.1 小节正文文档
```

Do not create extra shortcut indexes, backstage pages, update logs, homework pages, or sibling root modules unless the user explicitly asks. If Feishu uses the wiki root doc as the homepage, treat that doc as Level 1 and put all module docs underneath it.

## Page Types

- Homepage entry doc: concise global overview, customer pain points, who it is for, what it helps the reader do, what it does not do, the full module navigation, and how to use the knowledge base. It should be the only Level 1 doc.
- Module doc: concise guide/index doc for one Level 2 module. It summarizes the module's key judgment, outcomes, sub-doc route, and expected deliverables. It must include Feishu sub-page navigation. It is not a full lesson.
- Section/body doc: detailed Level 3 execution doc. It must be practical enough that a beginner can follow it step by step, using Agent prompts, source images, checks, and acceptance standards.

Detailed writing, structure, image, Feishu, and QA standards live in `references/制作标准.md`.

## Reference Routing

Read only the files needed for the current task:

- `references/制作标准.md`: use for any actual knowledge-base structure, writing, beautification, image, QA, or delivery work.
- `references/飞书打通引导.md`: use when Feishu/Lark access, CLI, wiki, docx, media upload, permissions, or manual fallback is needed.
- `references/视觉IP配图引导.md`: use when generating or inserting Xiaohei-style or client visual-IP illustrations.
- `references/美化与配图强制流程.md`: use before finishing any document; it defines mandatory beautifier and visual-IP orchestration.
- `references/客户素材清单.md`: use when the source materials or product boundary are unclear.
- `references/跨平台调用指南.md`: use when the user wants this skill to run in Claude Code, ChatGPT, Hermes, Workbuddy, ima copilot, or another Agent.

## Default Variables

Ask only for missing variables that materially affect output. Use reasonable defaults where safe.

```text
{product_title}
{target_reader}
{source_materials}
{target_feishu_wiki_or_doc}
{author_block}
{brand_voice}
{visual_ip_name}
{visual_ip_skill_or_reference}
{platform_safety_rules}
{privacy_boundary}
```

For internal use, pass the exact author block in `{author_block}`. For customer-visible packages, keep it configurable:

```text
✔️原创作者：{author_name}丨{contact_or_brand}
```

For customer-visible packages, make author identity configurable and do not expose the service provider's private product names, customer names, local paths, or private cases.

## Output Discipline

When working with a live Feishu knowledge base, report progress in plain language:

- what was created or updated
- which document is waiting for copy confirmation
- whether beautification and illustration have been completed
- what still needs user review

Do not expose internal block IDs, placeholder tokens, API quirks, tool failures, or local file paths in customer-facing docs.

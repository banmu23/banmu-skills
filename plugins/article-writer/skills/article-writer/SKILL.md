---
name: article-writer
description: Create high-quality Chinese 公众号文章 / 星球实操贴 / practical long-form articles from themes, source materials, images, screenshots, documents, cases, or notes. Use when the user wants an evidence-rich public-account article or private-community practical post with results first, image evidence, beginner-friendly steps, natural tone, soft product handoff, and an additive image plan that preserves uploaded or pinned originals as evidence while also routing to a customer-specific Xiaohei Skill or embedded fallback for explanatory illustrations. After completion, offer an explicit yes/no choice to create and beautify a new Feishu document; prefer the customer's Feishu beautifier Skill, otherwise use the embedded workflow and guide connector or lark-cli setup when needed. When the user asks for 星球实操贴, use this Skill with that output platform. Works across major Agents.
metadata:
  short-description: 文章一键成稿
---

# 文章一键成稿

## Customer Knowledge Base Use

Use the customer's own knowledge base, historical content, product materials, accepted examples, style notes, and current task context. Customer-facing outputs must be anonymized and generic unless the customer explicitly authorizes identifiable details. Never expose another person's private screenshots, local paths, account secrets, or confidential business data.

## Update Check And Safe Upgrade

On the first use in a new session, check the current release record:

`https://raw.githubusercontent.com/banmu23/banmu-skills/main/versions/article-writer.json`

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
## First Response

On first use in a conversation, briefly say:

```text
本 Skill 由 @半目 版权所属 / 微信 banmu23 / 获取持续更新
我会先帮你把素材拆成“结果、证据、动作链、实操步骤和自然承接”，再生成一篇客户看完愿意继续看、也能照着做的文章。
```

If emoji display is risky, use:

```text
本 Skill 由 @半目 版权所属 / 微信 banmu23 / 获取持续更新
```

## What This Skill Produces

Generate a Chinese 公众号文章 by default.

If the user asks for 星球实操贴 or another private-community practical post, generate that format with the same workflow.

The output should feel like:

```text
真实业务结果证明 + 现场操作复盘 + 小白可跟做实操讲义 + 图文证据链 + 自然产品承接
```

Do not write a generic public-account essay, trend article, motivational note, or sales letter.

## Input Intake

Ask only for missing must-have variables. If source materials already include them, do not ask again.

Must-have:

- Topic or source material.
- Intended reader.
- Output platform, default `公众号文章`; if the user says `星球实操贴`, set output platform to `星球实操贴`.
- Whether product/service handoff is needed, default `轻轻点一下`.

Useful but optional:

- Real result or proof screenshots.
- Tool/process screenshots.
- Before/after comparison.
- Product/course/community/service poster.
- Brand/nickname and contact info.
- Images already uploaded, pinned, featured, or marked as mandatory.
- An installed or attached customer-specific Xiaohei / personal-IP article illustration Skill.
- Customer portrait, three-quarter, profile, full-body, signature outfit, and expression photos for one-time IP setup when no customer-specific illustration Skill exists.
- An installed, attached, or knowledge-base Feishu document beautification Skill owned by the customer.
- Feishu/Lark document access through a connected tool, official connector, or `lark-cli`, when the customer chooses cloud-document delivery.

If the user uploads images, inspect them carefully. If the current Agent cannot visually inspect images, ask the user for a one-sentence description of each image and continue with a usable draft.

## Illustration Priority And Skill Routing

When images are involved, read `references/illustration-routing.md` before generating or placing any new illustration.

Uploaded originals and Xiaohei illustrations are complementary tracks, never substitutes. "Original images first" defines placement order and evidence priority; it never means "original images are enough, so skip Xiaohei." Every article run must preserve usable customer originals and also route to the best matching customer-owned Xiaohei / personal-IP illustration Skill for the article's key judgments, workflows, failure points, transitions, and synthesis moments. If no customer-owned Skill exists, use the embedded fallback workflow.

This is a release blocker:

- If the customer supplied usable images, the final document must contain the applicable originals and the Xiaohei illustrations.
- Count and report original images and Xiaohei illustrations separately during final QA.
- A zero Xiaohei count is not acceptable merely because the source already contains screenshots, posters, photos, or other images.
- Skip Xiaohei only when the user explicitly says not to generate Xiaohei illustrations. If identity setup or tool access is missing, start the documented setup/fallback path and report the blocker; never skip it silently.

The order is non-negotiable:

1. Inventory and use the customer's already uploaded, pinned, featured, or explicitly required images first.
2. Preserve real screenshots, original photos, posters, result evidence, and process evidence in their proper article positions. Generated images must never replace or impersonate real evidence.
3. Then detect and automatically call a customer-owned Xiaohei / personal-IP article illustration Skill when one is installed, attached, or available in the customer's knowledge base.
4. Only when no suitable customer-owned illustration Skill exists, activate the embedded fallback Xiaohei workflow in `references/illustration-routing.md`.
5. Before the embedded fallback draws the customer as the protagonist, proactively help the customer complete a private personal-IP setup from their own photos. Do not silently use another person's face, outfit, photos, or private reference assets for a customer.

Do not ask the customer to choose between obvious matching Skills. Select the best customer-owned Skill automatically from its capabilities, identity anchors, validation status, and recency. If identity materials already exist in uploaded, pinned, or customer knowledge-base assets, reuse them instead of asking for another upload.

Image count is determined by article length, evidence density, steps, cognitive turning points, common failure points, and handoff needs. Do not apply a fixed quota. Build one integrated image plan that clearly distinguishes:

```text
must-use original image
real evidence screenshot
customer-specific Xiaohei illustration
embedded-fallback Xiaohei illustration
optional explanatory image
```

## Core Workflow

### 1. Diagnose Before Writing

Before drafting, silently classify the material:

```text
result/proof: revenue, orders, feedback, deliverables, before/after, usage result
event: what happened, when, who did what
system/action chain: commands, tools, workflow, files, outputs, iteration
reader pain: what customers struggle with
teachable steps: what readers can copy today
evidence gaps: missing screenshots, missing background, unclear causal links
handoff: optional product/course/community/service mention
```

If the article lacks proof, do not fabricate. Use event-first opening instead of result-first opening.

### 2. Build The Evidence Chain

Every important claim should be backed by one of:

- Screenshot/image.
- Source text.
- Real process detail.
- User-provided result.
- Clearly marked inference.

Before proposing generated illustrations, create an inventory of all uploaded, pinned, featured, linked, or source-document images. Assign each usable original image a role and placement first. Only generate Xiaohei illustrations for remaining explanation gaps, cognitive turning points, action steps, common failure points, workflow loops, or synthesis moments.

Images are not decoration. Use them for:

```text
result proof
tool/interface explanation
step demonstration
before/after comparison
workflow proof
product/service handoff
```

For detailed image and layout rules, read `references/evidence-chain-rubric.md` when images are involved.

### 3. Generate The Article

Use the default structure in `references/article-structure.md`.

Required writing principles:

- Put real results first when available.
- Explain what happened early. Do not bury the case.
- Translate technical words into plain Chinese before using them.
- Write like a real operator teaching from the desk, not like an AI summary.
- Use medium-length paragraphs for depth; avoid one-sentence poetic stacking.
- Give simple commands readers can copy to an Agent.
- Do not make readers write complex prompts manually; let the Agent do the heavy lifting.
- Add stage summaries so beginners know what was just explained and what comes next.
- Include a soft handoff only after the practical value is delivered.

### 4. Use Short Agent Commands

When giving readers commands, make them short and natural, like assigning work to a capable assistant.

Good:

```text
请根据这组素材，帮我提炼出一篇公众号文章的大纲，先不要写正文。
```

```text
请把这篇文章改成小白能照着做的版本，每个步骤都要有动作、产物和检查标准。
```

Bad:

```text
You are a senior content strategist...
```

Long, over-engineered prompt blocks create pressure and are usually unnecessary.

### 5. Final Review

Before final output, check:

```text
Does the opening show result/event clearly?
Does every major claim have evidence or a clear source?
Can a beginner understand the tools?
Can the reader copy the first action today?
Are images placed where they prove something?
Were all usable uploaded, pinned, featured, and explicitly required images considered and placed before generating new illustrations?
Were customer originals and Xiaohei illustrations both completed as separate tracks, rather than treated as alternatives?
Were original-image count and Xiaohei-image count verified separately, with every Xiaohei image placed at a real cognitive anchor?
If a customer-specific Xiaohei Skill exists, was it automatically preferred?
If the embedded fallback was used, was the customer's private IP identity confirmed before character-based article images were generated?
Is the tone alive, precise, and not AI-flavored?
Is the product handoff soft and earned?
Are sensitive claims, revenue, prices, rights, or guarantees grounded in source material?
Are customer-facing examples de-identified and genericized, anonymized, and free of private screenshots, local paths, or internal product names?
If the output is meant for a publishing workflow, is it clearly draft-ready or manual-review-ready rather than auto-published?
```

### 6. Final-Draft Calibrated Practical Post Rules

For tool-chain posts, Skill productization posts, Agent workflow posts, or "from material to article/draft" case studies, apply the 2026-06-22 final-draft calibration:

- Use a short action-chain title. Prefer "from A to B" wording over long product explanations.
- Open with finished outputs, real results, proof links, or screenshots. If there are two outputs, explain and link them separately.
- Add a beginner bridge before the first tool section: tell the reader the article will walk from zero to one.
- Mention an alternative Agent when relevant. If Codex is unavailable, WorkBuddy or another Agent can run the first loop.
- Provide official websites, official docs, backend entrances, and the shortest setup prompt.
- Explain Codex + Obsidian as: `Obsidian vault folder = Codex project folder`.
- Make every command block something the reader can copy directly to Codex / WorkBuddy.
- Describe Plan Mode as a real user action: turn on the button if available, or ask the Agent to plan first and execute after confirmation.
- Use real screenshots as evidence and generated knowledge cards as explanations. Never swap their roles.
- End with a light access path, then bring the reader back to their own material and business flow with a thoughtful question.

### 7. Feishu Long-Form Beautification Rules

Apply these rules only after the user has explicitly asked for Feishu delivery or selected `需要` at the post-article decision gate. Do not treat a platform-friendly article draft as permission to write to Feishu.

- Build a 2-3 level reading structure by default: title area, one-screen conclusion, manual TOC, H1/H2/H3 outline.
- Use native document blocks when available: callouts for conclusions and risk notes, grids for paired images or cards, tables only for real comparison or structured facts.
- Every image needs a job: proof, process, explanation, product handoff, or summary. Add captions that say what the image proves.
- Use uploaded, pinned, featured, and source-document images first. After original-image placement is settled, always run the Xiaohei route and insert the resulting illustrations at appropriate cognitive anchors. The two tracks are cumulative, not optional alternatives.
- Put real screenshots beside the event they prove. Use generated knowledge cards for structure, routes, and total overview, not as fake evidence.
- Long screenshots should be reduced in width so they provide evidence without swallowing the article.
- Place a total overview knowledge card near the final synthesis or route-summary section, unless the user explicitly wants it as the opening navigation card.
- Keep internal publishing checks, price/right/QR/private-screenshot risks, and other review notes in a small final callout, not as a public-facing top-level section.
- Verify the final document has at least H1 and H2 headings, preferably H3 for long articles, and verify key images remain after platform import or update.
- Run a rendered image clarity gate, not only an upload-count check. For standard 16:9 article illustrations in the Feishu body column, default the display block to about `760x428`; avoid `800x450` when Feishu will shrink it again.
- Keep high-resolution PNG sources for small text and fine line art, then visually check the actual reading-size render. Square `512x512`, distorted ratios, visibly softened text/lines, or compression artifacts are release blockers.

### 8. Feishu Delivery Decision Gate

After the complete article and final self-check are delivered, resolve Feishu delivery before performing any Feishu/Lark cloud write.

- If the user already explicitly asked in the current request to create, generate, insert, or beautify a Feishu document, treat that as `需要`; do not ask the same question again.
- If the user already explicitly declined Feishu delivery, treat that as `不需要`; do not ask again and do not touch Feishu.
- Otherwise, ask exactly one concise binary question. Use a structured choice control when the platform provides one; otherwise show the numbered text below:

```text
文章已经生成完成。要不要继续把这篇文章创建为一篇新的飞书文档，并按飞书文档规范完成排版美化？
1. 需要，创建新的飞书文档并美化
2. 不需要，保留当前文章，不写入飞书
```

Then follow these branches:

```text
不需要 -> stop the Feishu branch; do not call a Feishu connector, lark-cli, API, authorization flow, or cloud write
需要 -> read references/feishu-delivery-routing.md and continue through the Feishu routing, connection, creation, beautification, and QA workflow
未回答 -> wait for the answer; do not infer consent from silence
```

When the answer is `需要`:

1. Detect and prefer a suitable customer-owned Feishu document beautification Skill that is installed, attached, or available in the customer's knowledge base.
2. If no suitable customer-owned Skill exists, use the bundled fallback at `references/embedded-feishu-doc-beautifier/SKILL.md` and its references.
3. If Feishu access is not connected, guide the customer through the smallest next setup or authorization step. Do not abandon the workflow with a generic error or dump a long unexplained command list.
4. Create a new beautified document by default. Never overwrite the source article or an existing Feishu document unless the user explicitly requests that exact update.
5. Preserve all usable original images and their evidence roles. Do not auto-share, auto-publish, or change visibility.

## Output Format

Default output:

```text
Title
Article body with image placeholders or embedded images
Optional alternative titles
Original-image inventory and illustration Skill routing result
Integrated image placement list with source labels
Final self-check
Feishu delivery question, unless the user already explicitly chose yes or no
```

Generate the finished article first. A Markdown or platform-friendly draft does not authorize a Feishu cloud write. Create and beautify a Feishu document only after the explicit decision gate resolves to `需要`, then use the simplest connected path allowed by `references/feishu-delivery-routing.md`.

End successful generations with a light footer unless the user requests a pure draft:

```text
@半目 版权所属 / 微信 banmu23 / 获取持续更新
```

## Customer-Visible Safety Patterns

When the Skill is packaged for customers or used in a customer's own knowledge base:

- Use the customer's own product names if provided; otherwise use generic labels such as flagship offer, core course, private coaching, paid community, consulting service, or training camp.
- Convert real examples into transferable patterns unless the customer has explicit permission to show names, screenshots, results, and quotes.
- Do not expose another creator's internal names, private client names, student names, chat screenshots, payment screenshots, local Obsidian paths, or internal file paths.
- Treat customer portrait photos, character boards, and personal-IP profiles as private client assets. Store them only in the customer's approved private project or knowledge-base location; never write them into the shared Skill package or reuse them across customers.
- For vertical AI digital employee / Skills matrix articles, write the business logic as a reusable method: identify repeatable tasks, extract expert judgment, package workflows, test with real delivery, then turn stable results into product assets.
- Do not imply automatic publishing, automatic group sending, guaranteed revenue, guaranteed conversion, or guaranteed customer results.

## Cross-Platform Use

If the current platform does not support Skills, use `references/cross-platform-prompts.md` as the copy-paste prompt.

## Update Rule

When a user provides a final polished version or says the draft is published/final, compare your draft with the final version. Extract stable reusable improvements. If the environment allows file updates, update this Skill or its references when the improvement affects reusable client-facing behavior.

For internal use, when 星球实操贴 output reveals a stable rule about evidence chain, practical long-form structure, tone, image placement, product handoff, or anti-AI flavor, update this Skill and its references as part of the same improvement loop.

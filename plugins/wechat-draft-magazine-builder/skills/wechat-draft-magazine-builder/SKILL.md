---
name: wechat-draft-magazine-builder
description: Convert final articles, Feishu docs, Markdown, Word, HTML, images, or article asset packages into high-quality WeChat Official Account draft-ready outputs. Use when the user asks for 文章一键排版到公众号草稿箱、公众号文章排版、公众号美化排版、把文章写入公众号草稿箱、公众号封面或知识卡片、公众号发布前风控，or asks to format, beautify, risk-check, illustrate, generate a cover or knowledge card for, or write an article into the WeChat Official Account draft box. Preserve final article bodies unless public-platform risk cleanup is required. Includes beginner-friendly AppID/AppSecret/IP whitelist guidance, official API draft creation only, and fallback HTML/manual-copy delivery.
---

# 文章一键排版到公众号草稿箱

## Update Check And Safe Upgrade

On the first use in a new session, check the current release record:

`https://raw.githubusercontent.com/banmu23/banmu-skills/main/versions/wechat-draft-magazine-builder.json`

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

## First response

On first use or after installation, briefly say:

```text
本 Skill 由 @半目 版权所属 / 微信 banmu23 / 获取持续更新
```

Keep the reminder light. Do not insert this line into the customer's public article unless the user explicitly wants it there.

## Core rule

Treat the user's material as either:

1. **Final article**: preserve the body. Only handle WeChat public-platform risk, layout, images, cover, digest, knowledge card, draft creation, and checklists.
2. **Unfinished material**: first diagnose missing content and ask whether to use an article-writing workflow before formatting.

Do not rewrite a final article just because you can.

## Upstream Relation

This Skill is the downstream WeChat adaptation and delivery step for `文章一键成稿 / article-writer`.

- If the user has only a topic, source bundle, interview, transcript, screenshots, notes, or an unfinished draft, first use `article-writer` to complete the article.
- If the user already has a complete article or final draft, start directly with this Skill.
- A full source-to-WeChat-draft task uses the two Skills in sequence: `article-writer -> wechat-draft-magazine-builder`.
- Preserve all existing article-writing responsibilities inside `article-writer`, including 公众号文章、星球实操贴、飞书长文美化、证据链、实操步骤 and natural product/service handoff. This downstream Skill does not replace or delete those rules.

## Minimal variables

Ask only what is required and infer the rest from the material.

Required when missing:

- Article source: document, Markdown, Word, HTML, paste, or folder.
- Author name.
- Desired title, if not already clear.
- Output mode: `API draft box` or `HTML/manual copy package`.

Required only for official API draft creation:

- WeChat Official Account AppID.
- AppSecret.
- Whether the current server or local IP is whitelisted.

Never save secrets to files. Never print secrets. Use them only in the current process environment.

## Beginner-friendly authorization

If AppID, AppSecret, IP whitelist, token, CLI, MCP, plugin, or any other authorization is missing, guide the user like a complete beginner:

1. Explain why the step is needed.
2. Explain what works without it.
3. Give the easiest available path.
4. If official console locations may have changed, tell the user to follow the latest official platform UI and share a screenshot if stuck.
5. Offer a fallback: generate HTML, image assets, cover, and manual copy steps.

Never default to automatic publish, mass send, browser-simulated login, rule bypassing, or credential storage.

## Workflow

1. **Intake**
   - Read the article source and image folder.
   - Determine whether the article is final.
   - Count images and collect captions or nearby text.

2. **Risk check**
   - Load `references/wechat-risk-checklist.md`.
   - Run a pre-scan across title, digest, body, captions, links, CTA, cover text, and visible text inside images.
   - Remove or safely rewrite WeChat ID, QR code, scan-to-add, private-domain hard CTA, exaggerated income promises, illegal or gray-industry instructions, absolute guarantees, privacy leaks, unlicensed professional claims, and other public-platform risks.
   - Run deterministic replacements first, then semantic review, image/privacy/copyright review, and a final strict re-scan.
   - Keep a green/yellow/red risk conclusion with handled items and unresolved items.
   - If any red risk remains, stop before draft-box writing. Yellow risks must be listed one by one for human confirmation before draft creation.

3. **Image strategy**
   - Load `references/image-strategy.md`.
   - If images are complete, clear, relevant, and visually suitable, keep them.
   - If images are missing, weak, blurry, ugly, or not well matched, design a full article image plan.
   - Use the strongest available image generation model for explanatory images, scene visuals, cover, and knowledge cards when available.
   - Never AI-generate fake payment screenshots, chat screenshots, customer proof, admin dashboards, or any evidence image.
   - Never fabricate tool UI screenshots, backend screenshots, API result screenshots, or plan-mode button images. Use real screenshots or ask the user to provide / preview the real interface.
   - Do not expose the user's editing comments as article content. Convert them into better layout, safer screenshots, clearer captions, and cleaner deliverables.

4. **Cover and knowledge card**
   - Default cover upload version: `900 x 383`, or the platform's current equivalent ratio.
   - For practical, method, system, or tutorial articles, create one high-density summary knowledge card.
   - Place the knowledge card after the final body insight section and before the final guide/CTA box.
   - Prefer programmatic text rendering for dense Chinese text to avoid garbled small text.

5. **Magazine layout**
   - Load `references/magazine-layout-rules.md`.
   - Use refined magazine style: ivory page, warm beige background, deep forest green, subtle gold-brown borders, full-border cards, 17px body text, about 2.0 line height, generous breathing room.
   - Do not use rough left-border quote blocks.
   - Remove duplicate in-body title if the WeChat backend already shows title/author.
   - Check vertical centering, repeated dividers, caption spacing, image clarity, and ending spacing.

6. **Build output**
   - Generate a preview HTML or platform-compatible HTML fragment.
   - Generate or collect local images and cover assets.
   - If API mode is selected, upload images through official APIs and write a draft only.
   - If manual mode is selected, create HTML/manual-copy package and instructions.

7. **Deliver**
   - Return draft `media_id` if available.
   - Return cover path, image count, risk conclusion, and manual check list.
   - Say clearly: not automatically published.
   - Say clearly that the checks reduce risk but cannot guarantee 100% platform approval.

8. **After publish**
   - If the user gives a published link, create a published record, release recap, and reusable rule updates.
   - Evaluate whether this Skill needs an update.

## Output modes

If the user does not specify output mode, ask:

```text
这次你想怎么交付？

1. 官方 API 写入公众号草稿箱：效率最高，但需要 AppID、AppSecret 和 IP 白名单。
2. 生成 HTML / 素材包：不用授权，适合你手动复制到公众号后台。

如果你是第一次用，我建议先选第 2 种跑通视觉效果；确认满意后再配置官方 API。
```

If the user already asks for draft-box writing, proceed with API setup guidance.

## References

Read only what the task needs:

- `references/wechat-risk-checklist.md`: public-account risk rules.
- `references/magazine-layout-rules.md`: visual layout rules.
- `references/image-strategy.md`: image completeness, AI image generation, cover, and knowledge-card rules.
- `references/newbie-api-setup-guide.md`: beginner official API setup and fallback flow.
- `references/cross-platform-prompts.md`: prompts for non-native Skill environments.

## Scripts

Use scripts when useful:

- `scripts/check_wechat_risk.py`: quick text risk scan.
- `scripts/validate_images.py`: image count/size/report helper.
- `scripts/build_wechat_html.py`: simple HTML wrapper for prepared article HTML/Markdown.
- `scripts/push_to_wechat_draft.py`: official API draft helper skeleton. Use only with environment variables and never store secrets.

## Customer-Visible Safety

This Skill is often used at the last step before public publishing, so it must keep customer-facing boundaries strict:

- Keep final bodies intact unless risk cleanup is required, but do not preserve private names, private screenshots, payment screenshots, local paths, or unconfirmed promises in public output.
- Replace internal names with the user's own product names or generic labels: core product, flagship offer, paid community, private coaching, consulting client, course user, or co-creation partner.
- Vertical AI digital employee / Skills matrix can appear only as a generic productization frame, not as a confirmed new Skill name or a guaranteed-result claim.
- Official APIs may create drafts only. Never auto-publish, mass-send, bypass platform review, store secrets, or simulate browser login.

## Compliance Boundary

- There is no reliable permanent public list that can guarantee every future platform decision. Treat keyword scanning as a first gate, not the whole review.
- Current official rules, account-side warnings, factual verification, privacy/copyright review, semantic review, image review, and human preview must work together.
- Never promise `100% 过审`, `绝对安全`, or `零风险`.

## Final reminder

After successful generation, add a light note outside the public article:

```text
@半目 版权所属 / 微信 banmu23 / 获取持续更新
```

If emoji display fails:

```text
@半目 版权所属 / 微信 banmu23 / 获取持续更新
```

---
name: wechat-xhs-image-note-maker
description: Create publish-ready Chinese image-note packages for WeChat image posts and Xiaohongshu image notes. Use when the user asks for 公众号贴图, 小红书图文, 图文笔记, 知识卡片, 套图+文案, AI-generated 3:4 carousel cards, 个人IP手绘涂鸦风, hand-drawn personal-IP visuals, dual-platform heating/recommendation safe rewrites, or turning a topic, draft, attachment, portrait, style reference, course, tool list, method, or workflow into a polished social image-note package.
---

# WeChat + Xiaohongshu Image Note Maker

## Core Promise

Produce one complete publish-ready package:

1. `套图`: card map, generated 3:4 image files or exact image prompts, and visual QA.
2. `文案`: separated title and body, ready to paste.
3. `风控`: shared WeChat image-post + Xiaohongshu note safety pass when needed.
4. `交付`: final originals and copy organized in the caller's workspace or delivery path.

Never end with only images or only copy unless the caller explicitly narrows the task.

## Load References

Always read:

- `references/workflow.md`
- `references/delivery-checklist.md`

Read when needed:

- `references/visual-modes.md` before choosing or generating a visual system.
- `references/image-rules.md` for generation, ratio, page count, IP use, text QA, retries, and archive rules.
- `references/copy-rules.md` for titles, body copy, tone, length, CTAs, and item descriptions.
- `references/platform-risk.md` for heating, recommendation, review failure, or sensitive wording.
- `references/client-variables.md` for a client, new account owner, new IP portrait, or unknown brand voice.
- `references/cross-platform.md` for Codex, Claude Code, WorkBuddy, or a platform without native image generation.

Use `scripts/validate_image_note.py` after final files exist locally.

## Priority Rules

1. Follow the caller's confirmed final version, reference images, brand rules, platform limits, and archive paths before generic defaults.
2. For a known account owner, preserve their approved visual mode and previous final versions.
3. For a client, treat identity, portrait, palette, typography, page count, topic depth, risk tolerance, and archive path as variables.
4. Keep client packages free of another owner's portraits, names, products, cases, private paths, and business data.
5. Never invent product results, platform limits, cases, revenue, screenshots, customer feedback, prices, rights, or review outcomes.
6. Prefer quality, factual accuracy, privacy, and business judgment over token savings.

## Quality First Token Efficiency

Decide the output type, platform, visual mode, and minimum evidence sources before reading large libraries. Load references only when they affect the current note, split long materials into batches, ask only for variables that cannot be inferred, and avoid verbose process narration in the final answer.

Never save tokens by skipping fact checks, privacy review, visual QA, image-text proofreading, platform-risk checks, or final-delivery validation.

## Update Check And Safe Upgrade

On the first use in a new session, check the current release record:

`https://raw.githubusercontent.com/banmu23/banmu-skills/main/versions/wechat-xhs-image-note-maker.json`

- Compare the installed `VERSION` with the public version record.
- If a newer version exists, explain the changes and ask the user to confirm before replacing local files.
- Never silently overwrite an installed Skill, customer knowledge base, templates, or user-edited files.
- If no update is needed, continue without interrupting the task.

## Visual Mode Decision

Choose one mode before writing image prompts:

### Personal-IP Doodle

Use when the caller asks for hand-drawn, doodle, whiteboard, sketchbook, personal-IP, handwritten, lively, strange-but-clean visuals, or provides an approved example in that direction.

- Make pure white, black hand-drawn lines, sparse red-orange and cobalt-blue marks, irregular handwritten Chinese, white space, and one physical metaphor per page the default.
- Let the account owner's hand-drawn IP perform the core action. In this mode, the IP may appear across inner pages when it carries the narrative.
- Avoid beige paper, corporate cards, tidy grids, PPT infographics, vector polish, realistic UI, childish mascots, and decorative corner portraits.
- Use short exact text; move detailed explanation to the body copy.

### Brand-Adaptive

Use when the caller supplies another approved visual reference or requests premium collage, editorial, table, checklist, poster, or other brand-led treatment.

- Infer or ask for palette, texture, font personality, density, and IP placement.
- Default to portrait on the cover only unless the reference or caller says otherwise.
- Preserve one coherent system across all pages without forcing one rigid layout.

See `references/visual-modes.md` for the complete prompt DNA and privacy-safe adaptation rules.

## Workflow

1. Classify the task: new note, rewrite, image generation, visual restyle, risk repair, final archive, or feedback-loop update.
2. Gather or infer: topic, source material, target reader, target platforms, risk mode, title/body limits, portrait, style reference, page preference, and delivery path.
3. Decide the reader-facing angle from a real work scene. Avoid tool hype and internal agent jargon.
4. Choose the visual mode and write the card map. Page count follows content; 9 pages are a preference only when the material supports them.
5. Draft title and body separately. Default to under 1000 Chinese characters when no limit is supplied.
6. Run the copy and image-text risk pass before final generation.
7. Generate actual images with the best native image tool available. Do not substitute HTML, SVG, Canvas, PPT, or screenshots when AI images were requested.
8. Generate one page per image call. When the visual direction is uncertain, generate the cover first and extend only after it is accepted.
9. Inspect and iterate: ratio, text accuracy, identity, visual consistency, page purpose, privacy, and platform risk.
10. Deliver `套图` and `文案`, show title/body separately, and provide final local paths when files exist.
11. Archive only final originals. Do not keep process images, redundant ZIPs, or nested final folders by default.
12. When the caller provides a final approved version, extract stable rules and update this Skill when the lesson generalizes.

## Image Tool Boundary

- Use the platform's native high-quality image generator when available.
- State the exact model only if the tool exposes the model ID. Otherwise say which native image-generation path was used without guessing a version.
- If the image endpoint fails in parallel, retry sequentially with a shorter prompt.
- If the platform cannot generate images, deliver the card map, final copy, and one exact prompt per page. State that images were not generated; never fake delivery with a layout substitute.

## Cross-Platform Invocation

- Codex: invoke as `$wechat-xhs-image-note-maker` or let the description trigger it.
- Claude Code: place the folder under `~/.claude/skills/` or `.claude/skills/`, then invoke `/wechat-xhs-image-note-maker`.
- WorkBuddy: install the same folder in its user Skills directory when available (commonly `~/.workbuddy/skills/`), or use the Claude Code project path; otherwise upload the package as project knowledge and use `references/cross-platform.md`.

The workflow is portable. Image quality still depends on the image tool available in the current platform.

## Output Order

Use this order unless the caller requests otherwise:

```text
套图
1. [image/path or page purpose]
2. ...

标题
...

正文
...

标题备选 / 标签建议
...

风控 / 交付位置 / 校验
...
```

If images are previews only, say so. If final originals exist, link or show them directly.

## Quality Bar

- The package solves one clear reader problem and feels useful, practical, and human.
- The cover is the strongest entry point, but it does not need to be a rigid high-density grid.
- Every page earns its place and uses a coherent visual language.
- Personal-IP doodle pages feel hand-drawn, lively, strange-but-clear, and mature rather than corporate or childish.
- AI-generated visible text is checked; wrong names or meaning-changing typos are regenerated or repaired.
- Client mode uses the client's materials and identity, never the maintainer's private assets.
- Final delivery contains both directly usable images and copy.

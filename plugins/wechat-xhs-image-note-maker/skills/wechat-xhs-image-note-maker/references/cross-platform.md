# Cross-Platform Use

This Skill follows the portable `SKILL.md + references + scripts` layout. The workflow is shared across platforms; image generation depends on the tools available in the current runtime.

## Codex

- Personal install: place the unzipped folder in the Codex skills directory.
- One-click package: upload the ZIP when the interface supports Skill import.
- Invoke with `$wechat-xhs-image-note-maker` or a natural request matching the description.
- Use the native image generation tool when available.

## Claude Code

Place the unzipped folder in one of these locations:

```text
~/.claude/skills/wechat-xhs-image-note-maker/
.claude/skills/wechat-xhs-image-note-maker/
```

Invoke with:

```text
/wechat-xhs-image-note-maker
```

Claude Code reads `SKILL.md` and supporting files directly. If the current Claude environment has no image-generation tool, it must still produce the card map, final copy, and one exact prompt per page, while clearly stating that final images were not generated.

## WorkBuddy

If the current WorkBuddy edition explicitly exposes a user Skills directory, place the unzipped folder in:

```text
~/.workbuddy/skills/wechat-xhs-image-note-maker/
```

When WorkBuddy instead exposes a Claude Code project runtime, place the same folder under the project's `.claude/skills/` path and invoke it by name.

When the interface supports only file or knowledge uploads:

1. Upload the ZIP or the unzipped Skill folder.
2. Upload the customer's portrait, visual references, product facts, and final-post samples separately.
3. Use the invocation prompt below.
4. Ask WorkBuddy to use its strongest available image tool. If none exists, request prompts rather than fake final images.

## Universal Invocation Prompt

```text
Use wechat-xhs-image-note-maker.

Create one publish-ready WeChat image-post + Xiaohongshu image-note package from my topic and files.

Visual mode: personal-IP hand-drawn doodle / brand-adaptive
Page count: content-driven / 5 / 9 / another number
Target reader: ...
Topic: ...
Materials: ...
Portrait and visual references: ...
Risk mode: normal / heating-recommendation safe

Deliver:
1. Card map and one purpose per page
2. Final images if a native image tool is available; otherwise exact prompts per page
3. Title
4. Body
5. Alternative titles and tags
6. Risk check and final file status

Keep title and body separate. Do not invent cases, results, prices, platform rules, or customer feedback.
```

## Portability Limits

- Do not claim the same underlying image model across platforms.
- Do not claim that every platform supports one-click ZIP installation.
- Do not substitute HTML, SVG, PPT, or screenshot composition for requested AI images.
- Do not ship one account owner's private portrait or business data inside a reusable customer package.
- WorkBuddy editions may expose different import surfaces; use the user Skills directory only when the current edition exposes it, then fall back to `.claude/skills/` or project knowledge upload.

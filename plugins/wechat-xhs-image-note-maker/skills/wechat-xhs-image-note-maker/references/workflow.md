# Workflow

Use this workflow to turn a topic, draft, attachment set, or reference post into a publish-ready image note.

## 1. Intake

Collect or infer:

- Topic, source copy, and target reader.
- Target platforms: WeChat image post, Xiaohongshu image note, or both.
- Delivery mode: normal publishing, heating/recommendation safe version, review-failure repair, or published archive.
- Available materials: screenshots, tables, reference posts, IP portrait, style image, product screenshots, previous final drafts.
- Visual mode: `Personal-IP Doodle` or `Brand-Adaptive`.
- Account preferences: palette, tone, page count, title/body limits, archive path.

If key inputs are missing but the task is still executable, continue with clear assumptions. Ask only when the missing input would materially change the result.

## 2. Decide the Core Problem

One image note should focus on one core reader problem or a tight set of related problems. Show the practical use before explaining the concept. Avoid turning the note into a high-barrier theory lesson.

## 3. Preserve What Already Works

If the user provides a successful reference or a published version with good data, preserve its useful structure and repair only the weak part. Do not erase a proven high-density list merely to make it look more conventional.

## 4. Choose the Visual Mode

Read `visual-modes.md`.

- Use `Personal-IP Doodle` when the user asks for hand-drawn, doodle, marker, white-background, playful, IP-led, or signature personal-brand visuals.
- Use `Brand-Adaptive` when the user supplies another clear brand system or requests a different aesthetic.
- If the user has a confirmed visual preference, it wins over the fallback.

In doodle mode, use the portrait as an identity anchor, then translate it into a repeatable drawn character. The character may appear on inner pages when it actively demonstrates the page idea; it should not be pasted into every page without purpose.

## 5. Build the Card Map

Page count is content-driven:

- 1-3 pages: one small tip, quote, before/after, or single workflow.
- 4-6 pages: normal tutorial, comparison, or compact checklist.
- 7-9 pages: dense collection, multi-item list, step-by-step guide, or full social set.
- More than 9 pages: only when the platform and user explicitly support it.

For each page define:

```text
page role
one core message
one visual metaphor or action
visible Chinese text
IP action if useful
```

Do not let several metaphors compete on one page.

## 6. Write the Copy Before Final Images

Draft the title and body first so each image prompt knows what it must communicate. For every listed item explain what it helps a beginner do, who should try it, and one practical boundary if needed.

## 7. Risk Pass

Run the same risk pass on body copy and visible card text:

- exaggerated or guaranteed claims
- “must install” or “magic tool” language
- automation-sounding language
- AI trace-hiding language
- interaction bait
- private-traffic or QR-code prompts
- unsupported results or case claims

For heating/recommendation, use `platform-risk.md`.

## 8. Image Generation

Use an available AI image-generation tool for the final card images and default to 3:4.

Generate one page per image call. When the visual direction is uncertain, generate the cover first, inspect it, then extend the accepted system to the inner pages. If parallel generation fails or becomes inconsistent, retry sequentially with shorter page-specific prompts.

Do not use HTML, screenshots, or local layout as the default substitute. If no image model is available, deliver the complete card map, prompts, and copy, and state that final bitmap generation remains pending.

Only name a specific image model when the environment exposes its exact identifier. Otherwise say “the current built-in image-generation capability.”

## 9. Visual QA and Iteration

Check:

- every page is 3:4
- visible Chinese is readable and correct
- key item names are present
- no hallucinated slogan or fake claim remains
- the cover has enough information density
- inner pages match the content instead of repeating one rigid layout
- doodle mode keeps a pure-white field, black hand-drawn linework, sparse accent colors, and generous whitespace
- the IP character is recognizable and only appears where it serves the narrative
- no process images remain in the final archive

If a page contains bad text or the wrong visual logic, regenerate it. Do not explain away a visible error.

## 10. Final Delivery

Deliver:

- final image set previews or file paths
- title
- body
- risk/validation note
- final archive location when files were saved

Keep title and body separate.

## 11. Feedback Loop

When the user gives a final title, final body, or approved images:

1. Treat them as higher priority than the draft.
2. Extract why the edits improved the note.
3. Update copy, image, risk, or delivery rules when the lesson generalizes.
4. Keep one-off preferences local; do not turn every edit into a permanent law.

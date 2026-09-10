# Document Beauty System

Use this reference to turn raw content into an attractive Feishu document. Beauty here means clarity, hierarchy, rhythm, and useful structure.

## Principles

1. Put the result first.
2. Make the reading path obvious.
3. Use structure instead of long plain text.
4. Keep the same type of information in the same visual form.
5. Let each section have one job.
6. Add diagrams when relationships, flow, time, or decisions matter.
7. Avoid decorative complexity that does not help the reader.
8. Preserve useful source images; beauty must not erase evidence, examples, screenshots, diagrams, or author-intended visuals.

## Required Structure

Every polished document should normally include:

- A clear title
- A conclusion-first opening callout
- A short "how to read this document" or key-summary section when the document is long
- 3-7 main sections
- A content-driven heading hierarchy: use level 1 for main stages, level 2 for parallel subtopics, and level 3 only for genuinely distinct steps, methods, or questions within a subtopic
- Same-level headings that are logically parallel; do not place a stage, action, result, and warning side by side as if they play the same role
- No long document flattened into only level-1 headings; no forced second or third level when the content is too short or simple
- For longer courses, guides, SOPs, proposals, and delivery documents, usually 3-7 level-1 modules before content-driven level-2 or level-3 expansion
- When Feishu automatic heading numbering is enabled, use it for the `1 / 1.1 / 1.1.1` sequence and do not duplicate those numbers in heading text
- At least one non-text block in every major section
- A final action list, decision list, or next-step summary when applicable

## Block Selection

Use:

- `callout`: core conclusion, warning, decision, recommendation
- `grid`: two-column comparison, before/after, problem/solution
- `table`: structured multi-field data, roles, modules, deliverables, metrics
- `checkbox`: action items, acceptance criteria, launch checklist
- `whiteboard`: process, timeline, architecture, funnel, decision tree, mind map
- `img`: preserved source evidence, screenshots, diagrams, examples, product/course visuals, or newly added visual aids
- `blockquote`: source quote or voice-of-customer excerpt, only when the source is real
- `pre`: code, command, exact prompt, configuration
- `hr`: section rhythm and separation

## Color Semantics

Keep color meanings stable:

- Blue: explanation or information
- Green: recommendation, success, finished item
- Yellow: attention, pending confirmation
- Red: risk, error, hard warning
- Gray: neutral structure, table headers, metadata

Do not turn the whole document into one color family. Use color sparingly for meaning.

## Richness Checklist

Before final output, check:

- Opening callout exists.
- Continuous plain paragraphs are 3 or fewer.
- At least 3 block types are used.
- Every major section has a non-text block.
- Important process or comparison content is diagrammed or tabulated.
- Relevant original images/media are preserved and placed near the content they support.
- Heading levels reflect real parent-child relationships; substantial documents are not a flat list of level-1 headings, and short documents are not over-structured.
- Customer-facing tasks and checks keep only the minimum necessary actions and avoid burden-heavy wording when a lighter first version is sufficient.
- Practical customer or learner documents clearly separate required first-version actions from optional upgrades; use low-pressure alternatives such as “第一版先完成这些就够了” or “任选一种方法即可” when they are true.
- The final document can be scanned in 30 seconds.

## Image Clarity Gate

Feishu image quality must be judged at the final reading size, not only from the local source file.

- For standard 16:9 article illustrations, use a high-resolution PNG source and default the rendered Feishu block to about `760x428`.
- Avoid setting `800x450` in a standard body column when Feishu will shrink it to roughly 760 pixels; the extra resampling can soften thin handwriting, fine line art, and small labels.
- Keep the source image at least 2x the rendered dimensions when the visual contains small text or dense diagrams. A source around `1600x900` or larger is preferred for a `760x428` display block.
- Preserve aspect ratio. Reject square `512x512`, stretched, cropped, compressed, or visibly blurry results unless the source intentionally uses that format.
- After insertion, fetch the document with full detail, audit every `<img>` width and height, and visually preview any image with fine text or line work at its actual display size.
- A byte-identical uploaded file can still look blurry when the document block is rendered at the wrong width. Stored-file integrity and rendered clarity are separate checks.

## DocxXML Starter Skeleton

Use this only as a starting point. Adapt the sections to the source content.

```xml
<title>文档标题</title>

<callout emoji="📌" background-color="light-blue" border-color="blue">
  <p><b>核心结论：</b>用一句话说明这份文档解决什么问题、适合谁看、读完能做什么。</p>
</callout>

<h1>一、快速概览</h1>
<grid>
  <column width-ratio="0.5">
    <p><b>适合阅读的人</b></p>
    <ul><li>角色或场景</li></ul>
  </column>
  <column width-ratio="0.5">
    <p><b>读完可以得到</b></p>
    <ul><li>结果或行动</li></ul>
  </column>
</grid>

<hr/>

<h1>二、主体内容</h1>
<p>每个章节先给要旨，再展开必要信息。</p>

<h1>三、下一步</h1>
<checkbox done="false">第一项行动</checkbox>
```

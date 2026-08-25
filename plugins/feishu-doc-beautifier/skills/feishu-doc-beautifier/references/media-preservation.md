# Media Preservation Rules

Use this reference whenever the source is an existing Feishu/Lark document or extracted content contains images, files, whiteboards, or other media blocks.

## Default Bias

Assume author-inserted images are intentional and useful. In most documents, embedded images are evidence, diagrams, screenshots, examples, product visuals, or context anchors. Do not treat them as decorative clutter.

If relevance is uncertain, keep the image.

## Required Inventory

Before rewriting or creating the beautified document from a Feishu URL/token:

1. Fetch the source document with enough detail to see media and block IDs:
   ```bash
   lark-cli docs +fetch --api-version v2 --doc "<doc>" --detail full
   ```
2. Build a media inventory for every relevant block:
   - block id
   - media type: image, file/source, whiteboard, sheet, bitable, synced reference
   - token / url / name / caption / dimensions when present
   - nearest heading
   - preceding and following text
   - likely content role
3. Use `docs +media-preview` or `docs +media-download` when a token exists but the image content is not clear enough to classify.

## Relevance Rules

Preserve an image when any of these are true:

- It is near the paragraph, step, table, case, example, or section it illustrates.
- The surrounding text mentions "如下图", "截图", "案例", "证据", "示意图", "流程", "界面", "海报", "成果", "反馈", "二维码", "对比", or similar visual cues.
- It is a screenshot, diagram, UI capture, product image, course image, proof image, chart, handout, whiteboard, or customer-facing visual.
- It has a caption or meaningful filename.
- It is the only visual in a section.
- You are not sure whether it is useful.

Only consider removing or excluding an image when it is clearly one of these:

- exact duplicate already preserved elsewhere
- broken placeholder with no visible content
- unrelated ad/banner/logo accidentally pasted into the document
- empty spacer, tracking pixel, or low-value artifact
- explicitly marked by the user as不要保留、删除、废弃、垃圾图

Even for suspected junk images, do not silently delete. Mention the reason, and keep it unless the user asked for automatic cleanup or the evidence is obvious.

## Preservation Strategy

For a new beautified document:

1. Keep original media in the same semantic section, even if the surrounding text is rewritten.
2. If the original section is moved, move its media with that section.
3. If the document is heavily restructured, place the image immediately after the paragraph, checklist, table, or callout it supports.
4. Preserve captions or add a neutral caption only when it is directly supported by source context.
5. Keep original image dimensions or aspect ratio unless the layout clearly needs a smaller display width.

Implementation options:

- If the fetched XML contains usable `<img .../>` tags and the target API accepts them, carry the image tag forward with its token/url/size metadata.
- If token reuse fails or the target document cannot reference the original media token, download/preview the media and reinsert it into the new document.
- If a public or signed `url` is available, inserting `<img href="..."/>` after the target block is acceptable when supported by the platform.
- If only local upload works, use `docs +media-download` followed by `docs +media-insert` or a block-level insert after the matching section.

Do not dump all preserved images at the end unless the platform cannot place them precisely. If forced to use an end-of-document insertion fallback, add a short "原文图片保留区" and explain that placement may need a final manual adjustment.

## Update Existing Document

When the user explicitly asks to directly modify the original document:

- Prefer precise block operations: `block_insert_after`, `block_replace`, `block_move_after`, and narrow `str_replace`.
- Avoid `overwrite` whenever the source contains images/media. `overwrite` can lose images, comments, and resource blocks.
- Never `block_delete` an image/media block unless the user asked for deletion or the block is clearly disposable and you disclose it.
- Preserve resource tags exactly when replacing nearby text: `<img>`, `<source>`, `<whiteboard>`, `<sheet>`, `<bitable>`, `<synced_reference>`, and rich `<cite>` tags.

If a full rebuild is the only practical path, create a new beautified document first, migrate the media inventory, verify preservation, and only then ask the user whether to replace or archive the original.

## Generated Images

The Skill may still add new visuals when they improve the document:

- diagrams or whiteboards for processes, timelines, decision trees, funnels, or architecture
- generated cover/section images when the user asks or the content clearly benefits
- screenshots or product images supplied by the user

Always distinguish original preserved images from newly generated or newly inserted images in the final summary.

## Rendered Clarity Rules

Preserving the original file is necessary but not sufficient. The Feishu image block can still look soft after browser-side resizing.

- For a standard Feishu body column, render 16:9 article illustrations at about `760x428` by default.
- Do not use `800x450` when the page will shrink it to the narrower body column. Fine handwriting, one-pixel line art, and small labels are especially vulnerable to this resampling.
- Prefer PNG sources at least 2x the rendered dimensions for text-heavy or line-heavy visuals.
- After insertion, fetch full XML and inspect every `<img>` width, height, scale, name, and token.
- If clarity is uncertain, preview the stored token and compare it with the source, then inspect the actual reading-size render. Matching dimensions or hashes confirms storage integrity, not display sharpness.
- Fix or replace images that are square `512x512`, distorted, visibly compressed, blurry, or unreadable at normal desktop and mobile reading sizes.

## QA Checklist

Before final response:

- Count source media blocks and preserved/migrated media blocks.
- Confirm every relevant original image has a destination.
- Confirm no original image was removed silently.
- Confirm newly added images do not replace or obscure original evidence images.
- Confirm each image is sharp and legible at its actual Feishu display size; the default 16:9 article block should normally be about `760x428`.
- Confirm the final response reports:
  - original images preserved
  - new images added
  - images not preserved, with reasons
  - any manual placement limitations

# Image Rules

## Generation Method

Use the best available AI image-generation capability for actual card images. In Codex-like environments, use the built-in image tool when available. Do not default to HTML, CSS, screenshots, or slide exports unless the user explicitly asks for that approach.

Generate one page per call. If several calls fail or drift, switch to sequential generation and reduce each prompt to the page goal, visible text, character action, and fixed style DNA.

Do not guess the exact model name. State it only when the environment exposes the identifier.

## Ratio and Size

Default ratio: 3:4. Verify actual dimensions after generation; width divided by height should be about `0.75`.

## Page Count

Match the material:

- simple idea: fewer pages
- normal tutorial: 4-6 pages
- dense checklist or full social set: 7-9 pages

Do not lock every task to nine pages.

## Cover

The cover is the collection trigger. It should contain a clear title, a useful subtitle or count, and enough real information to establish value. Avoid a beautiful but empty cover.

In `Personal-IP Doodle` mode, the cover should feel like a lively hand-drawn workshop board, not a corporate poster. Use the client’s portrait as the identity anchor, not as a pasted photographic cutout unless the user requests a photo-collage look.

## Personal-IP Doodle Mode

Read `visual-modes.md`. The non-negotiable visual DNA is:

```text
pure white background
black marker-like hand-drawn linework
sparse orange-red and cobalt-blue accents
irregular handwritten Chinese typography
generous whitespace
one physical metaphor or action per page
small arrows, circles, underlines, motion lines, and handwritten notes
```

The result should feel handmade, slightly strange, energetic, and clear. It should not look like a polished corporate infographic, a children’s coloring book, a dense comic page, or a generic Canva template.

## IP Character

- Cover: use the IP character when a portrait is provided and recognition matters.
- Inner pages in doodle mode: allow the character to demonstrate the idea through actions such as building, sorting, interviewing, packaging, operating a pipeline, watering a community, or assisting a sale.
- Inner pages in brand-adaptive mode: default to cover-only unless the user asks for recurring character storytelling.
- Keep facial anchors, hairstyle, glasses, clothing cues, and overall temperament consistent.
- Do not expose another client’s portrait, name, product, case, or local path.

## Inner Pages

Choose the composition from the content:

- process: path, conveyor, staircase, or timeline
- comparison: split board or two-sided sketch
- system: workshop table, machine, control panel, or modular blocks
- warning: obstacle, leak, knot, broken bridge, or sticky-note cluster
- result: assembled product, harvest, delivered box, or clean closing board

Use one dominant composition per page. The IP character, labels, and props must all support the same core message.

## Visible Text

Keep image text short. Prefer:

```text
one headline
one short explanation
two to four labels
one small handwritten note
```

Long copy belongs in the note body, not inside the image. Inspect every page for malformed Chinese, wrong names, unreadable text, and unsupported claims.

## Final Archive

- Save final originals only.
- Put them directly in the topic folder unless another archive rule is supplied.
- Do not keep process images in the final folder.
- Do not add a nested `final` folder by default.
- Do not create a ZIP unless requested.
- If pages were revised, rebuild the final set from the latest approved versions.

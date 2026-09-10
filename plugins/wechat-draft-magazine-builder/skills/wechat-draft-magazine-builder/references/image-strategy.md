# Image Strategy

## Decide first

Before creating any image, judge the user's current images:

```text
complete?
clear?
relevant?
beautiful enough?
consistent style?
safe for public publishing?
```

If all are yes, keep the original images and only improve order, captions, and layout.

If any are no, create an image plan.

## Image types

Separate images into:

```text
evidence images: real screenshots, proof, records
explanatory images: diagrams, process cards, conceptual visuals
cover image: click-through visual
section images: visual rhythm between long sections
knowledge card: dense summary and collection asset
```

## AI generation rules

Use the strongest image generation model available in the current Agent environment for:

```text
cover
explanatory images
section visuals
knowledge card visual concept
IP-style character illustration
```

Never use AI generation to fake:

```text
payment screenshots
chat records
customer feedback
admin dashboards
platform backend data
legal or official documents
tool UI screenshots
API result screenshots
plan-mode button screenshots
customer authorization proof
revenue proof
WeChat or Feishu draft-box screenshots pretending to be real output
```

If the article needs a real interface image, use a real screenshot from the user's interface or ask the user to bring the interface forward / provide a screenshot. Do not generate a fake UI image and present it as real evidence.

If only private evidence exists, keep it internal, blur it, or summarize it in text. Do not place private customer screenshots or payment screenshots into the public draft unless the user confirms public authorization.

Regenerate generated images when they show:

```text
crowded modules
overlapping text
cropped labels
unbalanced vertical spacing
low-end template feeling
distorted portrait
missing chin or face crop
strange hands
```

## Full article illustration plan

When images are incomplete or weak, propose:

```text
1 cover image
1 opening proof or result image if real evidence exists
2-5 explanatory/process images for key sections
1 high-density knowledge card near the end
```

Do not over-illustrate. Each image must reduce reading friction or strengthen proof.

## Knowledge card

Use knowledge cards for:

```text
practical long articles
system case studies
methodology breakdowns
tool tutorials
SOP explanations
```

Default placement:

```text
after the final body insight section
before the final guide/CTA box
```

Default caption for customer package:

```text
本篇文章精华总结图｜想收藏高清详版原图，后台找作者获取
```

If the user's brand name is known, replace `作者` with the brand name.

## Dense Chinese text

For high-density cards with Chinese text:

```text
Use AI for visual concept and illustration.
Use programmatic rendering for final Chinese text when possible.
```

This avoids garbled small text, typo-like artifacts, and blurry labels.

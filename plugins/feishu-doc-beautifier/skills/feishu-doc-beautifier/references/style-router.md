# Style Router

Choose the document style from the content type and reader goal. Do not force every document into one template.

## Routing Table

| Content type | Reader goal | Style | Recommended blocks |
|-|-|-|-|
| Course material | Learn and follow steps | Teaching notes | callout, numbered sections, checklist, table, diagram |
| Training review draft | Review and approve scope | Review document | scope table, agenda hierarchy, decision callout, revision comparison |
| Training preparation guide | Complete only necessary setup | Low-burden setup guide | minimal checklist, real screenshots, optional-path callout, acceptance check |
| Delivery proposal | Decide whether to approve or buy | Executive proposal | opening conclusion, problem/solution grid, scope table, next-step checklist |
| SOP | Execute without confusion | Operational manual | checklist, step table, decision tree, risk callout |
| Meeting notes | Review decisions and actions | Decision record | summary callout, table for decisions, checkbox action list, timeline |
| Knowledge-base article | Understand and reuse | Reference page | overview callout, concept table, examples, FAQ |
| Project plan | Coordinate work | Project roadmap | timeline, owner table, milestone checklist, risk callout |
| Review report | See what happened and what to improve | Retrospective | before/after grid, evidence table, action list, trend diagram |
| Marketing content | Present value clearly | Showcase document | stronger title, benefit grid, proof section, CTA checklist |

## Style Rules By Route

### Teaching Notes

- Start with what the learner can do after reading.
- Use steps and examples.
- Add a final practice checklist.

### Training Review Document

- Keep the confirmed title, order, duration, scope, and commitments unchanged unless the user asks to revise them.
- Show the detailed agenda, teaching focus, boundaries, and decisions the reviewer actually needs; keep full prompts, internal troubleshooting, and test progress in preparation materials.
- When comparing revisions, distinguish the first-version baseline, explicit customer feedback, later stakeholder suggestions, and new trainer design. Do not present the agent's own ideas as customer requirements.

### Low-Burden Training Preparation Guide

- Include only the software, authorization, materials, and checks truly required for this event's first successful run.
- Reuse the guidance style of a prior event without copying its time, location, price, assignments, or tool list.
- Prefer current real screenshots near the matching step. If the screenshot shows an older interface, state which old-interface controls the reader should ignore.
- If format conversion or transfer reduces clarity, use the original source image and validate the rendered Feishu page rather than trusting upload success.

### Executive Proposal

- Start with recommendation and business value.
- Separate "why", "what", "how", and "next step".
- Put scope, deliverables, assumptions, and risks in tables.

### Operational Manual

- Make every step actionable.
- Put exceptions and risks in callouts.
- Use a decision tree when there are branches.

### Decision Record

- Prioritize decisions, owners, deadlines, and unresolved questions.
- Avoid rewriting the entire meeting transcript.
- End with action items.

### Reference Page

- Use definitions, examples, and quick lookup tables.
- Keep paragraphs short.
- Add links or source notes if available.

### Project Roadmap

- Show phase order and dependencies.
- Use timeline or milestone tables.
- Mark risks and pending confirmations.

### Retrospective

- Separate facts, interpretation, and next action.
- Do not overstate results.
- Use evidence and source notes.

### Showcase Document

- Keep it polished but factual.
- Use proof only when source material supports it.
- Avoid exaggerated claims.

## If The Input Is Mixed

When the source combines multiple types, choose the dominant user goal:

- "给客户看" -> Executive proposal or showcase document
- "交付给学员" -> Teaching notes or operational manual
- "内部执行" -> SOP or project roadmap
- "复盘" -> Retrospective
- "沉淀知识库" -> Reference page

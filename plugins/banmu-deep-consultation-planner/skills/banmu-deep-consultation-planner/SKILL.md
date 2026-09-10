---
name: banmu-deep-consultation-planner
description: Generate complete, precise, and execution-ready deep consultation plans from a customer's own knowledge base and real source materials. Use when the user provides intake forms, questionnaires, screenshots, chat records, account links, product/service materials, or asks for 深度咨询方案, 客户咨询方案, 咨询前方案, 咨询交付方案, or a client-ready implementation plan.
---

# 深度咨询方案一键生成

Create a deep consultation plan that helps the customer execute, not just understand. Default to a client-ready document unless the user explicitly asks for internal prep notes.

Treat a complex deep-consultation plan as a customer execution system, not a long-form summary. Match the depth of the latest accepted accepted delivery: diagnose from evidence, correct the priority after real customer confirmation, specify staged deliverables and gates, provide copyable execution assets, and close every important question with an action or explicit open item.

## Operating Mode

- **Client-ready mode (default):** Write directly to the customer as "你". Do not mention internal delivery mechanics such as 腾讯会议, 会议演示, 现场演示, 会前内部提醒, 会后复盘, internal file paths, parsing issues, or tool failures. Translate every tool choice into customer business value.
- **Internal prep mode:** Only use this when the user explicitly asks for备课, 内部方案, 会议脚本, 演示流程, or承接判断. Internal mode may include demo sequence, call agenda, and upgrade strategy.
- **Customer-knowledge-base mode:** When the user says this is for a customer's own knowledge base or external generic use, use the same workflow but remove creator-specific names, customer names, private case names, local paths, and product promises unless they are part of the customer's own materials.

## Required Source Routing

Start from the customer's current materials. Extract facts before reading background context.

For any consultation task, read the smallest necessary set: customer-provided primary materials, the customer's current product/service definitions, accepted delivery examples, relevant SOPs, and the latest dated evidence.

If a customer has their own knowledge base, read their knowledge base and product materials first; use 方法库材料 only for method, quality standards, and consultation logic.

Always apply latest-version priority: when multiple materials discuss the same customer, product, delivery method, price, right, or expression rule, prefer the file with the latest explicit date or filename date. Older materials are background, not the current rule.

For the same consultation session, use courseware for the planned path, the raw transcript for what was actually discussed and corrected, and AI meeting notes only for navigation. Do not let an AI summary override transcript facts.

When a customer already has one or more earlier plans, read them as working drafts. Preserve valid analysis and assets, but let the latest raw transcript, final customer confirmation, and latest dated materials correct the old priority. Do not keep an earlier P0 merely because it looked commercially logical before the customer confirmed a different first loop.

## Depth And Granularity Standard

For a complex customer, design enough detail that the customer can begin without another interpretation layer. Do not pad the document to hit a section count, but normally cover these layers when the source supports them:

1. Evidence-based current-state and strongest assets.
2. One opening core judgment and the real bottleneck.
3. A staged P0-P4 or equivalent roadmap with one focus per stage.
4. `do now / pause / later` decisions.
5. Visible deliverables, entry conditions, exit gates, and acceptance criteria for each important stage.
6. Product, content, acquisition, conversion, delivery, knowledge-base, team, and monetization implications that are actually relevant.
7. One first business loop written as an end-to-end SOP: inputs -> Plan -> confirmation -> execution -> small-scale test -> final feedback -> rule/Skill update.
8. Tool, device, network, time, team, and maintenance constraints translated into route decisions.
9. A customer-question coverage matrix for multi-question cases.
10. A 7-day launch plan and, for substantial cases, a 30-day staged roadmap.
11. Three to five or more copyable prompts/templates when they materially reduce execution friction.
12. Industry-specific privacy, compliance, human-review, claims, permission, and version-control boundaries.
13. A short final `start with these actions` section.
14. For complex plans, a compact `72-hour start card` containing one action, one real input, one tool, one visible deliverable, one acceptance line, one support/escalation route, and an explicit pause list.

Use tables for real comparisons, stages, product ladders, mappings, gates, or checklists. Use paragraphs for diagnosis and reasoning. Avoid turning the document into an outline with shallow bullets.

## Workflow

1. **Extract customer facts.** Identify identity, business, products, audience, current channels, AI baseline, constraints, assets, goals, urgent blockers, willingness, available time, device/network conditions, and the customer's own stated next action. Do not invent missing facts; mark them as `需补充`.
2. **Build an evidence and conflict sheet.** Separate confirmed facts, customer hypotheses, consultant judgments, outdated statements, price/right items requiring confirmation, and unresolved questions. Apply latest-version priority before writing conclusions. Assume AI summaries may misname tools or products, merge prices/periods, or turn conditional discussion into a final decision; verify any important item against the raw transcript or latest customer confirmation.
3. **Diagnose the real bottleneck.** State what the customer is actually stuck on in the business chain: content, offer, acquisition, conversion, delivery, knowledge base, workflow, team replication, compliance, or tool access. When the customer provides multiple questions, map each high-priority question to a solution section, deliverable, phase, and risk boundary before drafting.
4. **Correct the priority using actual readiness.** Choose the first loop from the intersection of business value, existing assets, urgency, customer willingness, available time, and tool readiness. Prefer the loop the customer can genuinely start now over a theoretically valuable but unsupported system. If the customer already has high-performing content, sales, renewals, referrals, or a mature process, prioritize reproducing that proven win before inventing a new line. Record what the old plan got right and what the latest evidence changes; do not expose that comparison in the client-facing document.
5. **Choose the AI path by stage.** Do not blindly recommend the most advanced stack. Put most of the client-facing teaching and execution detail on the level the customer can reproduce now.
   - **Level A:** AI baseline is low, network/tool barrier is unresolved, or the task is simple knowledge Q&A/content assistance. Start with ima copilot, Feishu, or another low-friction knowledge-base tool and one real task.
   - **Level B:** A repeatable task exists and the customer needs multi-step file work, automation, or team trial. Use Workbuddy + a plain local folder. Do not require Obsidian unless it creates clear value for this customer.
   - **Level C:** A capable founder needs a durable local operating system, complex file handling, or Skill productization and is willing to maintain it. Use Codex + Obsidian for deep work while employees or customers may stay on Level A/B.
   - Keep founder and team knowledge aligned through the same desensitized, permissioned knowledge base, accepted examples, and QA rules.
   - Needs productized workflow: propose SOP -> Skill -> Agent workflow only after a manual loop has been proven.
6. **Define stage gates.** For each major stage, state the single focus, visible deliverable, entry condition, completion/acceptance line, and observable condition for moving forward. Include the gates for Level A -> B, manual workflow -> Skill, and Level B -> C when relevant. Do not write vague future upgrades. A beginner's stage is not complete because they understood the route, installed an app, built folders, or opened a page; completion requires a repeatable real-task result.
7. **Validate the direction and public positioning before scaling.** Use proven benchmarks to test whether the audience, problem, content entry, offer, and result already have market evidence. No benchmark does not automatically mean no opportunity, but it raises the evidence burden. Treat an unsupported direction as a hypothesis and run a small content, consultation, preorder, or sample-delivery test before making it P0. Lead the public positioning with the audience, problem, and business result; keep AI, Agent, and Skill backstage as the production method unless the target customer is explicitly buying AI learning or peer enablement. Judge product freshness by target-customer use and results, not by whether the AI practitioner market considers the format new.
8. **Design the shortest executable loop.** Write one real workflow end to end: source inputs -> Plan mode -> customer/founder confirmation -> first complete output -> small-scale test -> accepted final -> difference review -> knowledge/SOP/Skill update. The plan must tell the customer what to do first, what to pause, and what to upgrade later. When the customer already owns recordings, workshops, consultation records, courseware, templates, or accepted examples, test an existing-asset-first MVP before proposing from-scratch production. When a new course or service lacks stable delivery evidence, run it as a narrow service prototype for real users, iterate several times, and only then package a curriculum or broad rights. Every major recommendation should expose a proof chain: real input -> core operation -> process screenshot/sample -> visible result -> acceptance line -> human-review boundary.
9. **Decide whether a Skill is justified.** Only propose a Skill when the task is frequent, stable, has clear inputs/outputs, at least one accepted final, forbidden patterns, a QA line, and real reuse value. Keep exploratory or low-frequency personal work as project rules, knowledge, or SOP. Split Skills only at quality, recovery, or human-confirmation boundaries. Keep the client-facing operation to one entry and usually no more than two or three visible steps; internal orchestration may be more modular.
10. **Define human and AI ownership.** For IP, content, courses, consulting, and professional services, state what the customer must author or judge, what AI may assist, and what requires final human review. Core experience, real stories, key cases, professional judgment, facts, client promises, and publication responsibility cannot be silently delegated to AI.
11. **Standardize team delivery when relevant.** Use one narrow, high-frequency pilot: let the Agent complete a full first draft, revise it to an accepted final, capture reasons and QA rules, extract a small focused Skill, let the team run it with the same knowledge base, compare outputs, and feed final differences back into the Skill. A Skill install alone is not team replication.
12. **Create practical assets.** Include the smallest useful knowledge-base/workbench structure, product or workflow tables when relevant, prompt blocks, a 7-day launch list, a 30-day roadmap for substantial cases, first deliverables, and acceptance criteria. For team cases, include input checklist, accepted samples, forbidden patterns, QA checklist, and escalation rules.
13. **Choose build, buy, partner, or wait.** Do not recommend a custom app, website, or enterprise workbench before repeated demand, an accepted manual/service MVP, sustained use, clear data boundaries, maintenance ownership, and willingness to pay or measurable business value exist. For data-bearing tools, also require known source locations, separation of real and demo data, successful export and restore tests, versioning, upgrade compatibility, customer data isolation, privacy, and maintenance ownership. Until then, keep it a Demo or customized service MVP. Prefer trying, distributing, partnering on, or co-creating an existing product when those conditions are missing.
14. **Connect to business outcomes.** Tie every suggestion to acquisition, conversion, delivery efficiency, monetization loop, business amplification, or team replication. Explain why the recommendation is sequenced now rather than later.
15. **Close high-stakes risks.** For finance, tax, medical, legal, policy, contracts, education, recordings, or sensitive data, explicitly define what AI may draft, what requires professional human review, what needs permission or masking, what cannot enter public models, and what needs current official or professional verification. For email, quotes, contracts, policy interpretations, and customer promises, default the first phase to AI draft -> human check -> human send/confirm. Recordings reused for products or public content require consent plus removal or replacement of identifiable names, faces, voices, enterprise data, and professional data. If source consultations raised but did not solve a risk, mark it as an open closure item.
16. **Check rights, privacy, claims, and platform boundaries.** Do not expose private client data, income, screenshots, payment details, confidential chats, or unverified outcomes. Prices, rights, dates, quotas, promises, device compatibility, platform operations, and external links need latest confirmation where applicable. Never propagate historical third-party account, network-access, recharge, registration, payment, shared-session, or unofficial service links. Before using external Skills, code, templates, images, courses, or datasets in a product, verify source, license, attribution, modification, commercial-use, redistribution, privacy, and platform terms. Do not remove watermarks, repackage without permission, scrape private data, or automate interactions that evade platform controls.
17. **Handle sync, troubleshooting, and naming accurately.** File synchronization does not automatically synchronize chat context, Agent runtime state, installed Skills, local permissions, login state, or platform workflows. For cross-device plans, define one source of truth, versioning, backup, and conflict handling. For a tool-blocked customer, diagnose in order: environment/network -> official source and version -> account/login -> least privilege -> model/quota -> file read/write -> one real-task acceptance test. Do not default to full access or request passwords/session keys. If a tool/product/model name cannot be matched confidently to its current official name or capability, mark it `需核验`; live-verify decision-critical capability, version, price, or rule.
18. **Separate unrelated business lines.** If two lines have meaningfully different audiences, promises, knowledge, account identities, or compliance boundaries, separate them first. Merge only after a shared customer journey is proven.
19. **Close the action and support loop.** For a complex plan, finish with a 72-hour start card. In internal mode, also capture the customer's confirmed first action, time window, acceptance line, support route and required screenshots/information, and the next review or upgrade condition. Client-ready mode shows action and support, not the internal conversion design.
20. **Draft and audit the client document.** Remove internal history, meeting mechanics, source filenames, local paths, old-vs-new comparison, upsell strategy, and tool failures. The customer should see the final judgment, not the backstage reasoning.



## Update Check And Safe Upgrade

On the first use in a new session, check the current release record:

`https://raw.githubusercontent.com/banmu23/banmu-skills/main/versions/banmu-deep-consultation-planner.json`

- Compare the installed `VERSION` with the public version record.
- If a newer version exists, explain the changes and ask the user to confirm before replacing local files.
- Never silently overwrite an installed Skill, customer knowledge base, templates, or user-edited files.
- If no update is needed, continue without interrupting the task.

## Quality First Token Efficiency

Optimize token use without lowering consultation quality:

- Read customer materials first, then the smallest relevant workbench set.
- Use indexes, outlines, latest finals, and targeted searches before opening full historical collections.
- Summarize long transcripts in evidence batches, but inspect the original passages that determine priorities, prices, rights, risks, or customer confirmation.
- Reuse maintained SOPs, templates, prior accepted plans, and source maps instead of rebuilding from zero.
- Ask only for missing information that cannot be safely inferred or found.
- Keep the client output focused on decisions and execution; omit internal reasoning history.

Never save tokens by skipping source verification, latest-version checks, customer-question coverage, risk review, visual/document QA, or final delivery validation.

## Output Requirements

Default output must be a complete client-ready plan with:

- Customer current-state diagnosis
- Core path judgment
- AI tool route by stage
- Staged roadmap with visible deliverables and completion gates
- Immediate / pause / later priorities
- Knowledge base structure
- One end-to-end first business loop SOP
- Proof chain for major recommendations: real input, sample/screenshot, visible result, acceptance line, and human boundary
- Skill eligibility and granularity judgment when Skill/Agent productization is relevant
- Human-authored, AI-assisted, and final-review boundaries when content, IP, course, consulting, or professional work is involved
- Practical prompts the customer can copy
- Content/product/delivery/monetization loop suggestions
- Team replication workflow and QA assets when employees or assistants are involved
- 7-day action plan
- 30-day staged roadmap for complex cases
- Risk and compliance boundaries
- Next-stage upgrade path
- Final immediate action list
- A 72-hour start card for complex or beginner cases
- Missing information list only if needed

Read `references/client-ready-template.md` before drafting a client-facing plan. Read `references/source-and-quality-rules.md` when sources are complex, materials conflict, or the plan may touch prices, rights, compliance, or high-ticket product routing.

## Quality Bar

The plan is not done until it passes these checks:

- It is specific to the customer's actual materials, not generic AI advice.
- A beginner can follow it step by step.
- It gives priorities and tradeoffs, not a pile of options.
- Its P0 reflects the latest confirmed customer readiness, not merely the earliest draft or the consultant's preferred system.
- Each major stage has a visible deliverable, acceptance line, and upgrade gate.
- It recommends tools according to the customer's constraints and current stage.
- It spends most execution detail on the tool level the customer can reproduce now and does not force Obsidian into Level B.
- It tests unsupported positioning or product ideas before treating them as the main line.
- It checks whether existing recordings, workshops, consultations, courseware, templates, or accepted examples can produce a faster MVP than starting from zero.
- Every major recommendation has a visible proof and acceptance chain, not only theory or prompts.
- A proposed Skill passes the frequency, stability, accepted-example, QA, and reuse test; Skill splits follow quality boundaries and keep customer operation simple.
- Human judgment, AI assistance, and final human review are explicit where authenticity or professional responsibility matters.
- Custom app/workbench recommendations pass demand, use, data, payment/value, and maintenance gates.
- Every high-priority customer question is closed by a solution, deliverable, or explicit open item.
- It includes copyable prompts or execution blocks when useful.
- A complex or beginner plan ends with one 72-hour start card and an explicit pause list.
- It does not treat understanding, installation, folders, or a page opening as a business result.
- Existing proven wins are evaluated before new tools or new business lines.
- Public positioning leads with customer problem and result unless AI itself is the product.
- A new course/service without evidence is prototyped through real delivery before broad packaging.
- A data-bearing AI product passes persistence, export/restore, version, upgrade, isolation, privacy, and maintenance checks.
- Tool troubleshooting closes with a repeatable real task and least-privilege access.
- Separate business lines are not forcibly merged when audiences, promises, knowledge, or compliance differ.
- The first real workflow runs from inputs through test, final feedback, and rule/Skill iteration.
- Complex cases include both an immediate launch window and a 30-day progression.
- Team cases align Skill, knowledge base, accepted samples, QA, and feedback updates.
- Regulated or sensitive cases include human-review and data boundaries, not only tool advice.
- It avoids internal delivery language in client-ready mode.
- It does not fabricate facts, results, cases, income, product rights, or compliance claims.
- It does not treat an AI summary as proof of a tool name, price, period, device decision, or customer commitment.
- It distinguishes source-file sync from Agent/chat/Skill/runtime sync.
- External resources pass license, attribution, commercial-use, redistribution, privacy, and platform-term checks.
- It naturally supports deeper follow-up services only when that matches the customer's situation.

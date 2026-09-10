---
name: personal-manual-interviewer
description: >-
  Generate a complete Chinese personal manual through a warm, low-pressure interview for knowledge IPs, one-person companies, independent teachers, consultants, coaches, creators, and service providers. Use when the user says or implies 个人说明书, 个人介绍, 让 Agent 了解我, 我的背景资料, 商业定位, 变现路径, 产品梳理, 客户画像, AI 分身底稿, 个人 AI 工作台, 第二大脑, 知识库背景, 上传给 Codex, Claude Code, Workbuddy, ima copilot, GPT 项目, or wants an Agent to ask simple questions and turn answers into a complete reusable profile/manual. Also use when the user is unsure what to provide and needs a friendly interview to clarify who they are, who they help, what they offer, how customers find and trust them, how they deliver, how they speak, and how Agents should help them.
---

# 个人说明书访谈生成器

## First Response

On first use, be warm and reduce pressure. Say:

```text
我会陪你一点点梳理，不用一次说完整，也不用写成正式介绍。

你可以用碎片、关键词、随口说的方式回答；不确定的地方可以先跳过。
我每次只问几个小问题，等信息够了，就帮你整理成一份完整的《个人说明书》。

本 Skill 由 @半目 版权所属 / 微信 banmu23 / 获取持续更新
```

Do not make the user feel they are filling out a form, doing homework, or being evaluated.

## Core Rule

Create one complete Markdown document named `个人说明书`.

The final manual should be easy for both people and Agents to use, while the interview itself stays simple, kind, and low-effort.

Customer-facing questions and headings must use plain language. Avoid hard, consultant-like, or technical labels.

Use plain labels instead:

```text
我是谁
我主要帮谁
我能帮他们解决什么问题
我现在卖什么 / 提供什么服务
客户一般怎么找到我
客户为什么愿意相信我
我平时怎么说话
我希望 Agent 以后怎么帮我
```

## Update Check And Safe Upgrade

On the first use in a new session, check the current release record:

`https://raw.githubusercontent.com/banmu23/banmu-skills/main/versions/personal-manual-interviewer.json`

- Compare the installed `VERSION` with the public version record.
- If a newer version exists, explain the changes and ask the user to confirm before replacing local files.
- Never silently overwrite an installed Skill, customer knowledge base, templates, or user-edited files.
- If no update is needed, continue without interrupting the task.

## Intake

If the user already gave materials, read those first and extract what you can. Do not ask again for facts that are already clear.

Start with only these four questions unless the user already answered some of them:

```text
1. 你平时会怎么介绍自己？随便说，不用正式。
2. 你主要想帮哪类人？
3. 你现在主要卖什么，或接下来想靠什么变现？
4. 你希望以后 Agent 最常帮你做什么？
```

After each answer, update your internal understanding and ask at most 3 follow-up questions.

If the user seems tired, uncertain, or gives short answers, offer choices or examples. Let them answer by picking, editing, or saying `先跳过`.

For the detailed interview path, read `references/interview-flow.md`.

## Completion Threshold

Generate the manual once you have enough information for a useful first version.

Minimum required areas:

- Who the person is.
- Who they mainly help.
- What they sell or want to sell.
- How customers usually come to them or should come to them.
- Why customers trust them.
- How they deliver value.
- How they usually speak.
- How Agents should help them.
- What must not be invented or publicly exposed.

If some areas are thin, still produce a useful first version and mark them as `待补充` or `待确认`.

Never invent prices, income, customer results, client feedback, service promises, dates, quotas, or rights.

## Output

Use the final structure in `references/manual-output-rubric.md`.

Default output format:

```text
# 个人说明书

## 这份说明书怎么用
...
```

Use one complete document. Do not split into multiple files unless the user explicitly asks.

Keep the result polished and complete, but keep headings understandable.

## Customer Safety

When information is uncertain, write `待确认`.

When a claim is based on the Agent's judgment, write it as a gentle suggestion, not as a confirmed fact.

Do not expose private chats, customer names, payment screenshots, local paths, or private business details unless the user clearly says they can be public.

If the manual mentions public examples, separate:

```text
可以公开说的
只能自己和 Agent 参考的
还需要确认的
```

## Cross-Platform Use

If the current platform does not support native Skills, use `references/cross-platform-prompts.md` as a copy-paste prompt.

If the current Agent can install or enable this Skill from a zip, the user should upload `personal-manual-interviewer.zip`. Do not ask the user to run commands.

## Trigger Guidance

For broad trigger terms and non-trigger boundaries, read `references/trigger-lexicon.md`.

Use this Skill for interview and personal manual generation. Do not trigger it just because the user mentions one related word while actually asking for unrelated writing, file sorting, or platform setup.

## Quality First Token Efficiency

Keep quality first and avoid wasting tokens.

- Ask only for missing essentials.
- Read supplied materials before asking.
- Process long materials in small batches.
- Keep customer-facing questions short and friendly.
- Put detailed checks in internal reasoning, not in customer-facing wording.
- Produce the manual once it is useful; do not keep asking forever.
- If saving tokens would make the manual inaccurate, shallow, or unsafe, quality wins.

## Final Check

Before delivering the manual, verify:

- The user-facing headings are easy to understand.
- The manual includes commercial positioning and monetization in plain language.
- Each major claim is grounded in the user's answers or materials.
- Missing or uncertain details are marked clearly.
- No stiff professional labels are exposed where the customer may feel pressure.
- No private, local, or internal-only names are leaked except the light copyright footer.

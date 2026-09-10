# Cross-Platform Prompts

Use these prompts when the platform does not support native Skill installation.

## Universal Prompt

```text
请你用“个人说明书访谈生成器”的方式帮我。

目标：通过轻松、贴心、低压力的多轮问答，帮我整理出一份完整的《个人说明书》，以后给 Codex、Claude Code、Workbuddy、ima copilot、GPT 项目或其他 Agent 使用。

要求：
1. 不要一次给我很长问卷。
2. 每轮最多问 3-5 个小问题。
3. 问题要短、好回答、像聊天一样。
4. 我可以用碎片、关键词回答，不确定可以先跳过。
5. 不要把听起来很硬、很像报告的话直接丢给我。
6. 最后只生成一份完整 Markdown《个人说明书》，不要拆成多个文件。
7. 说明书里必须用我能看懂的标题，比如：我是谁、我主要帮谁、我现在卖什么 / 提供什么服务、客户为什么愿意相信我、我平时怎么说话、我希望 Agent 以后怎么帮我。
8. 商业定位和变现路径要写清楚，但用人话表达。
9. 不要编造价格、收入、客户结果、案例反馈、权益承诺、日期和名额；不确定就标注待确认。

请先问我第一轮 4 个问题：
1. 你平时会怎么介绍自己？随便说，不用正式。
2. 你主要想帮哪类人？
3. 你现在主要卖什么，或接下来想靠什么变现？
4. 你希望以后 Agent 最常帮你做什么？
```

## Codex

```text
Use $personal-manual-interviewer to interview me warmly and generate a complete Chinese personal manual. Keep each round short and friendly. Do not use professional labels in customer-facing questions.
```

If the Skill zip is available, upload:

```text
personal-manual-interviewer.zip
```

## Claude Code

```text
请使用个人说明书访谈生成器的流程，先用 4 个简单问题访谈我，再根据我的回答继续少量追问，最后整理成一份完整 Markdown《个人说明书》。问题要像聊天，不要像问卷。
```

## Workbuddy

```text
请帮我做一份个人说明书。先别让我填表，你用轻松访谈的方式问我几个小问题，我可以碎片回答。等信息够了，请生成一份完整 Markdown，方便以后 Agent 了解我、我的客户、我的产品服务、我的变现路径和我希望 AI 怎么帮我。
```

## ima copilot

```text
请按“个人说明书访谈生成器”的方式帮我建立个人背景资料。你先问我 4 个轻松问题，再逐步补充缺口。最终生成一份完整《个人说明书》，用于我的知识库和后续 Agent 协作。
```

## GPT Project

```text
You are helping me build a Chinese personal manual for future AI collaboration. Interview me warmly, ask only a few simple questions per turn, avoid jargon, and produce one complete Markdown document titled 个人说明书.
```

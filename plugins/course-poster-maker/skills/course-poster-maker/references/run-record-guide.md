# 运行记录填写

复制 run-template.json 到本次任务目录。相对路径以记录所在目录为基准；实际资料和证据均保留在客户自己的任务目录，不放进安装包。

- `has_outline` 必须为布尔值。课程清单是否充当大纲页已有明确选择时记录依据。
- `facts_confirmed` 只在原始事实足以制作、关键价格/权益/日期等已明确时为 true；不要求为本次没使用的商业信息额外询问。
- `source_files` 为 `{ "path": "资料.md", "sha256": "真实文件哈希" }` 列表。
- `items` 每项为 `{ "id": "I01", "kind": "outline|offer|price|audience|teacher|schedule|signup|value|title|navigation|other", "text": "完整原文", "page": 1, "only_once": true, "source": "资料.md的段落或页码" }`。拆分到足以检查遗漏的粒度，大纲的每个具体小点单独列项。
- `tool.evidence` 指向本次能力说明文件，记录可用入口、可见型号或 unknown、参数/文档依据、核验日期和未知边界。不能把官方 API 型号写成原生已选型号。
- 每个节点 `status` 使用 `pending/running/passed/failed/waiting/not_applicable`；passed 需 `evidence` 指向非空真实文件。只有无大纲的 P10 可 not_applicable，并写 reason。工具调用信息保留工具名、调用编号或时间及返回路径；记录是辅助，不可伪造调用回执。
- `pages` 每项：`page`、`file`、`sha256`、`actual_size:[宽,高]`、`prompt_file`、`call_evidence`、`review_file`、`visual_review:"passed|failed"`、`observed_items:["I01"]`。observed_items 是实际查看后确认出现的清单，每项通常只记录一次。
- `review_file` 写清：实际打开了哪些原图、整图与局部/手机尺度检查、逐项文字检查、问题与返工、并排一致性；不能仅写“通过”。
- `canvas` 记录请求比例、理由及双图是否同尺寸；实际比例由原图读取。请求未达到时在 open_issues 说明，未解决不交付为已通过。
- `open_issues` 不为空时 final 检查失败；`next_action` 记录真实接续节点。

脚本验证前序节点、记录结构、哈希、实际图片像素、分图与条目覆盖。它不能判断观察记录是否诚实，也不能凭记录证明文字正确或审美达标；Agent 仍须真实执行和验收。

# V2运行记录契约

复制[模板](run-template.json)到客户任务目录。相对路径以记录所在目录为基准；素材、调用和记录保存在本次任务里，不放进安装包。旧V1记录保留，另建schema_version:2记录，不批量改历史记录。

## P01–P06：制作前

- `poster_mode`：`single`一张整合图，或`split`主海报＋大纲海报。**单张可以有大纲**；不从has_outline推定张数。选项和依据写入P03证据。
- `has_outline`：是否有可用真实大纲依据，布尔值。可以有大纲但不展示。`outline_display_mode`是`full`完整、`overview`方向概览、`none`不展示；full/overview都须有真实依据，split只允许full。
- `facts_confirmed`：本次实际使用的价格、权益、讲师、课题等事实已经确认；没有使用的资料不要求额外补全。
- `edit_mode`：是否为修改。为true时填`baseline:{file,sha256}`，指向本轮修改前清晰版本；与允许变化项／区域一起保存，不自行放宽。
- `requested_roles`：客户明确要求使用但可能尚未上传的角色列表，默认`[]`，值仅允许`reference/portrait/evidence/logo`。需求与实际素材分开登记；素材缺失仍保留请求，不能把分支改为不适用。最终交付前，每个请求角色都必须有对应的实际asset及有效文件/哈希。
- `source_files`：`[{"path":"资料.md","sha256":"64位小写真实哈希"}]`。`asset_roles`：`[{"role":"reference|portrait|evidence|logo","path":"图片.png","sha256":"真实哈希"}]`，同图承担多种角色时可分别列出。无图片输入为`[]`，不能只登记文件却不真正看图。
- `items`：`{id,kind,text,page,only_once,source}`。id必须唯一字符串；`text`完整，`source`能追溯到正文/页码。`kind: outline`仅用于full中的具体大纲小点，overview使用`direction`；其余可用title/navigation/value/offer/price/audience/teacher/schedule/signup/other。`only_once`为布尔值。single全部page:1；split的outline在page:2，其他非title/navigation内容在page:1。必要的重复标题用不同ID明确映射，而不是把同一only_once条目重复两次。
- `design_plan:{file,confirmed}`：文件写参考采用／舍弃、网格、同层字号段距、信息组、转场、人物/证据安排、版面文案映射和修改允许范围。confirmed:true可来自本轮确认或已沿用的既有授权，必须在文件中说明；不能自行把尚未确认的重大变化记为已确认。
- `render_route:{kind,authorized,evidence}`：kind为`native`原生、`native_composite`原生素材与真实原件机械组合、`html`、`hybrid`。默认native；非native需authorized:true并有`evidence`文件记录具体授权依据与范围。不要用笼统“最优解”替代确需确认的付费API或资料外传授权。
- `tool:{native,entry,model_name,verified_at,evidence}`：能力记录。包含原生内容时native:true；型号不暴露写unknown。tool.evidence记实际入口、字段、日期和未知项，不能把API可用写成当前平台已实测。
- `canvas:{requested_ratio,rationale,same_size}`：尺寸和手机阅读理由，same_size为布尔值；双图若已明确异高，可false并在rationale说明。实际输出尺寸另由pages记录，不冒称原生4K或精确尺寸支持。

## 条件分支：有输入就有检查

`conditional_reviews`固定含reference/portrait/evidence/revision四项，格式`{status,evidence:[],reason}`：

|分支|触发|检查重点|
|---|---|---|
|reference|已上传reference或requested_roles已请求|已真实看参考图，拆解结构、配色、字体、材质、光影、留白；采用与调整有依据，不复制参考事实或第三方照片|
|portrait|已上传portrait或requested_roles已请求|用途授权、原照身份、面容眼神与肢体、清晰度、与背景融合；简介只用确认事实|
|evidence|已上传evidence或requested_roles已请求|原图优先、真实内容完整、头像昵称群名含括号昵称脱敏、实际观看尺寸可读性、无AI重画|
|revision|edit_mode:true|对照baseline与允许变动，已认可区域冻结；像素核验和可读性验收分开|

已触发分支：final必须`status:"passed"`，evidence至少一个非空文件；已请求角色也必须有实际素材。plan时，**已上传的reference**仍须passed（设计前已拆解）；仅在已请求但尚缺素材时，其分支可pending/running/waiting_for_key_material，不能记passed或not_applicable。人物/证据/修改分支已有素材时，plan也可pending/running/waiting_for_key_material或passed，有passed就需证据。只有既未请求也未使用的分支才可`not_applicable`并说明reason；缺材料不等于不适用。Logo没有单独的conditional_reviews键，但请求了Logo同样必须在final提供实际素材。记录只能证明存在书面证据，不能证明实际看过图。

## P07–P12：制作后

- 每个`nodes.P01`至`P12`填status和evidence。状态是pending/running/passed/failed/waiting_for_key_material/not_applicable。passed需真实文件证据，只有single的P10可不适用并附理由；其他核心节点不可跳过。
- `pages`每项：`page,file,sha256,actual_size:[宽,高],production_mode,prompt_file,call_evidence,review_file,visual_review,observed_items`。
- `production_mode`：`generated`真实生成；`native_reuse`复用原生字稿/图层；`html_render`可编辑源渲染。native/native_composite允许前两项；html只能html_render；hybrid可三者。native_reuse及hybrid均需`source_native_evidence`文件追溯原生来源。生成调用或复用溯源都保留真实记录，不虚报新增调用次数。
- `prompt_file`：精确提示词；复用时可用原始提示词记录，若源稿没有可回溯提示词则保存明确注明缺口的复用说明，不伪造历史。`call_evidence`必须明确本轮实际调用、机械组合或复用来源。
- html/hybrid的每张图必须填`editable_source`指向非空可编辑源文件。
- `review_file`写实际打开的原图、原尺寸／局部／手机尺度检查、逐项文字、人物／证据／Logo检查、失败修复与并排一致性；`visual_review:"passed"`由实际检查后填写。`observed_items`是实际看见的文案ID；只出现一次的条目不能重复登记。
- `open_issues`是未解决问题；不为空时final检查失败。客户已接受的具体源限制单独记`accepted_limits`及客户确认依据，不继续当阻断，也不隐瞒其物理限制。`acceptance`区分技术通过、客户已认可范围与整套最终认可；脚本不推定客户认可。`next_action`写真实接续位置。

## Agent执行检查

```bash
python3 scripts/check_run.py /path/to/run.json --stage plan
python3 scripts/check_run.py /path/to/run.json --stage final
```

检查器仅验证记录结构、文件/哈希、尺寸头、条件分支、节点、张数、文案分配与only_once。它不解码验收整图，不证明真实调用、文字正确、隐私完整或审美达标。OCR或脚本通过均不能代替真实目视。

修改核验可在已有Pillow环境使用只读辅助工具（不负责修图或生图）：

```bash
python3 scripts/compare_regions.py before.png after.png --allowed 100,80,320,40 --output new-comparison.json
```

区域为`x,y,width,height`，可重复`--allowed`；只允许记录中的指定区域变动。尺寸不同先记录已授权几何变化，再选相应核验，不能伪造0变化。工具不覆盖图片或已有报告，8位常规图按解码RGBA比较；未改像素一致仍不能证明截图细字可读。没有Pillow时用平台已有等价核验或人工逐区对照，不强迫客户安装，也不能宣称0像素变化。

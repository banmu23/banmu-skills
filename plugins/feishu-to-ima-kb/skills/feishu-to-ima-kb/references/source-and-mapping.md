# 来源与映射

只读用户指定首页节点的子树。默认结构：来源首页→二级模块→三级资料；目标：根目录手册＋一级文件夹→二级原链接。模块顺序与标题来自原目录，资料真实 URL 是内容，不生成替代文章。

## 连接检查

优先当前已有的飞书连接器/CLI；已有 ima 连接直接用。lark-cli 适配器可由 `LARK_CLI` 指定路径，或从 PATH、用户目录已知安装位置定位。不要为 PATH 问题先重装。CLI 必须显式 `--as user --format json`，解析 `ok:true`，不能套 ima 的 `code=0`。

```bash
lark-cli wiki +node-get --node-token '<首页 URL>' --as user --format json
lark-cli wiki +node-list --space-id '<真实 space_id>' --parent-node-token '<真实 node_token>' --page-size 50 --as user --format json
lark-cli docs +fetch --doc '<首页 URL>' --doc-format markdown --as user --format json
```

列表 `has_more:true` 时携带真实 `page_token` 继续，直到明确结束；循环游标、缺失游标或未知响应结构均停止。只递归指定节点，不列出整个账号的飞书知识库。权限失败不换身份绕过；由资源所有者授权后重试必要只读动作。

## 来源快照契约

`scripts/scan_feishu.py` 输出：`source_url` 原首页链接、`root` 原节点、`modules[{id,title,url,items[{id,title,url,obj_type,node_type,path}]}]`、`homepage{content,revision_id}`、`scan{complete,page_reads,node_count}`、`source_hash`。哈希由根节点标识、完整 modules 和 homepage 的规范 JSON 计算。只有读取到分页末尾才写 complete=true。

节点响应自带 URL 时原样保存；若接口只给 node_token，则构造该来源域名的 `/wiki/<token>` 标准节点地址并记录这个来源，不声称保留了不存在的复制参数。用户提供的实际资料 URL 优先，不能把查询参数擅自删掉。

## 特殊情况

| 情况 | 动作与通过条件 |
|---|---|
| 正常二级模块＋三级资料 | 自动按固定对应关系执行，无须逐项确认 |
| 更深层级 | 给“保留更多层级”或“按所属模块展开”选择。内置两层执行器仅支持已确认展开，保留来源路径；另一方案需当前连接器适配并重新核验 |
| 二级节点无子页但有正文 | 停止确认它是模块说明还是也应作为原链接；不得生成一个空目录就算迁移了正文 |
| 三级正文中另有链接集合 | 按客户指定语义读取该正文中的实际链接；默认扫描器仅映射 wiki 节点地址，不能声称已经抽取正文链接。使用连接器建立有来源版本和逐条原值证据的映射后再执行/验收 |
| 重复或空模块标题 | 明确目标命名/复用方案，保留来源到目标的映射；内置执行器会停止，不静默改名 |
| 同一 URL 出现在多个节点 | 平台可能合并资源；先确定多位置策略并实际验证。不能自动去重后报告全量成功 |
| 受限、失效或快捷方式 | 核对来源权限、快捷方式实际目标，保留原 URL。导入失败逐条报告，不绕过授权、不替换成公开副本 |
| 迁移期间源发生变化 | 新快照与已绑定哈希比较，不同则回 C 节点重新计算差异；不得复用旧完成证据 |

初版脚本对重复 URL、更深层级、空/同名标题执行拦截。特殊结构需要 Agent 的业务选择及连接器适配，不把默认脚本说成覆盖所有飞书内容形态。必要模块说明与正文按真实需要读取，尤其用于判断二级正文是否承载资料。

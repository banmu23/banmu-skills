# ima 连接与已验证调用机制

当前适配器仅访问 `https://ima.qq.com/openapi/{wiki|note}/v1/<method>`。密钥从环境变量 `IMA_OPENAPI_CLIENTID`/`IMA_OPENAPI_APIKEY`（兼容 IMA_CLIENT_ID/IMA_API_KEY）或用户私有 `~/.config/ima/client_id`、`api_key` 读取；严禁在对话、报错、客户包中暴露。登录或密钥本人动作由客户完成，Agent 不擅自申请新权限。

临时 COS 上传凭证只用于 ima 返回的 `.myqcloud.com` 上传目标，不能发送到其他域名；不把短期凭证写入持久日志。请求禁止带密钥重定向。错误提示需脱敏。接口改变先核实当前连接契约，停止相应步骤，不猜字段重试。

## 标准两层执行顺序

| 动作 | 关键请求和实际验收 |
|---|---|
| 查找同名目标 | `search_knowledge_base` 读完 cursor/is_end；同名不等于本任务目标，有冲突先定位已绑定记录或确认新名称 |
| 新共享库 | `create_knowledge_base {name,description,type:1002}`；返回 `data.id` 是 opaque KB 标识，随后 get_knowledge_base 回读 |
| 根目录 | `get_knowledge_list {knowledge_base_id,cursor:"",limit:50}` 的 current_path 返回真实 root folder_id；不要用 opaque KB ID 代替 folder_id |
| 文件夹 | `create_folder {knowledge_base_id,parent_folder_id:<root>,name:<原模块标题>}`；返回 data.media_id；回读标题与 parent_folder_id |
| 原链接 | `import_urls {knowledge_base_id,folder_id,urls:[原URL...]}` 每批最多 10；逐条检查 data.results[URL].ret_code 和 media_id，再 `get_media_info` 对比 url_info.url 与原字符串及目录列表归属 |
| 手册笔记 | note/import_doc `{content_format:1,content:<Markdown>}` 返回 note_id；wiki/add_knowledge `{media_type:11,title,knowledge_base_id,note_info:{content_id:note_id}}` 关联根目录。get_doc_content 读取实际内容比对可见正文 |
| 手册置顶 | `set_knowledge_top {knowledge_base_id,folder_id:<root>,media_id,is_top:true}`；根目录回读手册在根且为第一入口 |
| 封面上传 | 文件实际检查→check_repeated_names→create_media→用短期 COS 凭证 PUT 原始二进制→上传成功后 add_knowledge 注册文件；title 与 file_name 完全一致，不能只 create_media 就视为知识内容 |
| 设置封面 | 注册后 get_media_info 获取实际 media URL，完整传给 `update_knowledge_base_basic_info {id,update_fields:[2],cover_url}`；再读知识库 cover_url 与真实缩略图目视检查。这里 [2] 是本适配器已验证的封面更新用法，不能迁移到权限接口 |

封面文件注册后保留在库内供可靠复用；不擅自删除附件。签名 URL 属临时访问证据，客户包不带运行日志。复核时应通过 get_media_info 或库 metadata 取新 URL，不自行拼接 COS 地址。列表必须读到 is_end，遇到无游标/重复游标停止。

## 权限能力单独核实

V1 不提供默认权限写入方法。曾出现接口成功却实际未生效的情况，不能猜 update_fields、把前端枚举当 OpenAPI 契约或复制未经验证的字段。只有当前连接已证明字段语义、目标身份和实际配置/成员观察路径，Agent 才能走 H03 自动设置分支。

自动分支必须同时有实际保存配置或普通成员效果证据，绑定目标标识；只返回 code=0 的回执不能验收。创建者、管理员自己的导出能力不能代表普通成员。没有可靠连接能力就走 H07/H08，客户设置并明确反馈，标注客户手动完成。现有已由客户设好的权限不能为了测试重置。

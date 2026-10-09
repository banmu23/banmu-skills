# 证据、断点与完成条件

运行目录保存 `source.json`、`plan.json`、`state.json`、`manual.md`、`description.txt`、原始封面及 `evidence/`，属于客户私密数据，不进入客户 Skill 分发包或公开仓库。输入和线上目标绑定后保持一致；人工修改优先保留。状态应有当前节点、已确认选择、真实目标、失败原因、下一步以及证据路径。

## 写入日志与接续

`Journal.write` 先持久记录 in_flight 再发请求；明确业务成功保存 api_ack。同一操作、同一输入重跑直接复用回执，再用实际线上读取验收，不重复创建。网络中断、未知结果、业务错误保存 needs_reconciliation，不自动重发。

同一原模块采用稳定的原始批次，不因为前一批部分成功就把剩余链接重新分组重复导入。成功条目保留；失败条目在同一回执重跑仍会停止，等待具体修复。重复调用 run 不会把部分失败当成功。

遇到未知写入时，Agent 先用当前连接读取实际目标、文件夹、URL、笔记或封面。将请求、实际标识、原始回读和比对结果存入独立 reconciliation 文件，逐项确认：实际已成功则绑定已存在资源；确实未发生则确认可重试范围。由 Agent 精确修复当前任务的状态/调用适配，保留旧日志与证明，不能只把失败状态改成 api_ack，也不能删除整个 state 重建。证据无法排除重复时保持暂停。

封面临时凭证不持久化；若中断导致上传结果未知或凭证丢失，先读取实际上传/注册状态并使用当前已验证连接能力恢复，不自动重新 create_media 堆积附件。这个边界会停在缺口，不声称所有网络故障都能无人工判断恢复。

## 权限证据

以下 JSON 中尖括号均需替换真实值，示例本身不能用作通过证据。

```json
{"kind":"config_readback","knowledge_base_id":"<本任务目标ID>","observed_at":"<实际时间>","raw_file":"evidence/permission-actual.json","target_pointer":"/knowledge_base_id","view_pointer":"/members/can_view","export_pointer":"/members/can_export"}
```

原始文件必须是当前连接实际返回的已保存配置，两个指针明确指向 true 和 false。不能由 Agent 将未知数字枚举翻译后伪造 raw。若原接口是枚举，先独立核实含义并升级经过验证的适配器和流程，再验收；V1 保守验证器会拒绝数字。

`kind:member_behavior` 还必须提供 role_pointer 指向 member/viewer/ordinary_member，以及真实查看和导出观察；owner/admin 不通过。保留观察来源，不能使用创建者账号做普通成员测试。

当客户亲自设置且明确回复后，可记录：

```json
{"kind":"user_manual_confirmation","knowledge_base_id":"<真实目标ID>","observed_at":"<实际回复时间>","confirmation_source":"human_user_message","user_message":"<客户对实际设置结果的原话>","can_view":true,"can_export":false}
```

客户原话须明确实际已经设置；“好的”“稍后做”、沉默、Agent 自己的总结或历史上另一座库的确认均无效。`record-permission --evidence <文件> --run-dir <运行目录>` 仅保存证据，之后仍需 verify。

## 视觉证据

Agent 必须用图像查看工具实际打开当前下载的 cover-actual.png：

```json
{"observer":"agent_visual_inspection","passed":true,"image_sha256":"<当前实际缩略图SHA256>","tool_reference":"<实际图像查看调用引用>","observed_at":"<检查时间>","observed_text":"<看到的真实标题、裁切与清晰度检查结论>"}
```

`record-visual` 保存后仍需 verify。封面字节变化使旧目视证据失效；脚本只能比哈希，不能代替目视。

## 最终关卡和状态

最终重新扫描同一来源，保存新文件，执行 check-source 比对；再执行 verify，核对 source_current、target_metadata、folders、links、manual_content、manual_at_root、manual_first、cover_online、cover_visual、permission 共 10 项。任何一项缺失或未知均不可完成。

- `needs_verification`：有必需项待验收，报告具体缺项。
- `completed_with_manual_permission`：其余项通过，客户明确手动设置权限；必须标注客户手动完成。
- `completed`：全部通过，包括经过验证的连接权限观察；是否全自动还须证明实际自动设置过程，不能只看库已存在。V1 的配置/成员回读只证明实际效果，保守保持 fully_automatic=false；以后只有补齐经过验证的自动权限写入适配与证据，才允许升级这个声明。

`status` 只是查看上次状态，不能取代最终最新源扫描和在线 verify。最终源变化使 source_current 失败；接口回执不能使任一实际关卡通过。

交付入口使用库实际返回/已验证的可打开地址；当前共享库可用真实 root_folder_id 构成 `https://ima.qq.com/wikis/?knowledgeBaseId=<root_folder_id>&knowledgeBaseType=1002`，须核对目标。它是拥有者访问入口，不自动承诺为公开加入链接；客户邀请入口需当前分享接口真实返回。

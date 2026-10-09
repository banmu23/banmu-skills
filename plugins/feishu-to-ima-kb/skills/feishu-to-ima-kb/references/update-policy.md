# 版本检查与更新

唯一公开发行源：https://github.com/banmu23/banmu-skills 。本 Skill 的版本清单位于 `https://raw.githubusercontent.com/banmu23/banmu-skills/main/versions/feishu-to-ima-kb.json`，当前业务版本 V1，兼容版本 1.0.0（本地 VERSION）。

每个新会话首次使用本 Skill 时，若具备网络读取能力，读取公开版本清单，比较 name、version/displayVersion。读取失败不阻塞客户当前转换任务，说明本次沿用已安装版本，不重复长时间重试。不能把检查更新当成客户已授权升级。

发现新版本时，展示实际变化，询问是否升级。客户确认后才下载对应英文 ZIP，核对清单中的 SHA256、ZIP 根目录 SKILL.md、路径无越界以及英文身份一致，保留当前安装快照再替换；不覆盖客户运行记录、知识库、密钥或其他 Skill。不同 Agent 的安装接口按实际能力执行，没有实际启动测试就不能说该平台安装成功。

工作台稳定变化或客户真实反馈影响本能力时，记录维护候选，并同步检查流程图、节点契约、源、引用、脚本、说明、模板与安装包。公开产物不得带客户私密材料；开发者的自动 GitHub 同步规则不构成客户运行时向外发布资料的授权。

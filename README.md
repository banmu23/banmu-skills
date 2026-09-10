# 半目 Skill 市场

这里集中发布半目自研与封装的 Agent Skills，供 Codex、WorkBuddy 及其他支持 Skill 的 Agent 使用。

## 一键安装

优先下载对应英文 ZIP，并直接上传到 Agent。每个 ZIP 根目录都直接包含 `SKILL.md`。

## Skills

| Skill | 英文名 | 版本 | GitHub 页面 | 一键安装包 |
|---|---|---:|---|---|
| 飞书文档美化 | `feishu-doc-beautifier` | 1.2.0 | [介绍页](https://github.com/banmu23/banmu-skills/tree/main/plugins/feishu-doc-beautifier) | [下载 ZIP](https://raw.githubusercontent.com/banmu23/banmu-skills/main/packages/feishu-doc-beautifier/1.2.0/feishu-doc-beautifier.zip) |
| 个人说明书访谈生成器 | `personal-manual-interviewer` | 1.0.0 | [介绍页](https://github.com/banmu23/banmu-skills/tree/main/plugins/personal-manual-interviewer) | [下载 ZIP](https://raw.githubusercontent.com/banmu23/banmu-skills/main/packages/personal-manual-interviewer/1.0.0/personal-manual-interviewer.zip) |
| 飞书知识库产品一键生成 | `feishu-kb-product-builder` | 1.1.0 | [介绍页](https://github.com/banmu23/banmu-skills/tree/main/plugins/feishu-kb-product-builder) | [下载 ZIP](https://raw.githubusercontent.com/banmu23/banmu-skills/main/packages/feishu-kb-product-builder/1.1.0/feishu-kb-product-builder.zip) |
| 公众号贴图与小红书图文一键成稿 | `wechat-xhs-image-note-maker` | 1.0.0 | [介绍页](https://github.com/banmu23/banmu-skills/tree/main/plugins/wechat-xhs-image-note-maker) | [下载 ZIP](https://raw.githubusercontent.com/banmu23/banmu-skills/main/packages/wechat-xhs-image-note-maker/1.0.0/wechat-xhs-image-note-maker.zip) |
| 文章一键成稿 | `article-writer` | 2.1.0 | [介绍页](https://github.com/banmu23/banmu-skills/tree/main/plugins/article-writer) | [下载 ZIP](https://raw.githubusercontent.com/banmu23/banmu-skills/main/packages/article-writer/2.1.0/article-writer.zip) |
| 公众号文章一键排版到草稿箱 | `wechat-draft-magazine-builder` | 2.0.0 | [介绍页](https://github.com/banmu23/banmu-skills/tree/main/plugins/wechat-draft-magazine-builder) | [下载 ZIP](https://raw.githubusercontent.com/banmu23/banmu-skills/main/packages/wechat-draft-magazine-builder/2.0.0/wechat-draft-magazine-builder.zip) |
| 口播逐字稿一键生成 | `talking-head-scriptwriter` | 1.0.0 | [介绍页](https://github.com/banmu23/banmu-skills/tree/main/plugins/talking-head-scriptwriter) | [下载 ZIP](https://raw.githubusercontent.com/banmu23/banmu-skills/main/packages/talking-head-scriptwriter/1.0.0/talking-head-scriptwriter.zip) |
| 高质量朋友圈一键生成 | `wechat-moments-copywriter` | 2.0.0 | [介绍页](https://github.com/banmu23/banmu-skills/tree/main/plugins/wechat-moments-copywriter) | [下载 ZIP](https://raw.githubusercontent.com/banmu23/banmu-skills/main/packages/wechat-moments-copywriter/2.0.0/wechat-moments-copywriter.zip) |
| 深度咨询方案一键生成 | `banmu-deep-consultation-planner` | 1.0.0 | [介绍页](https://github.com/banmu23/banmu-skills/tree/main/plugins/banmu-deep-consultation-planner) | [下载 ZIP](https://raw.githubusercontent.com/banmu23/banmu-skills/main/packages/banmu-deep-consultation-planner/1.0.0/banmu-deep-consultation-planner.zip) |

## Codex 市场安装

在支持 Plugins 的 Codex 中添加本仓库作为 marketplace，再从 `/plugins` 选择需要的插件。安装完成后新开一个任务，让 Skill 被重新发现。

## 更新机制

GitHub 是公开发行源，本地工作台是维护源。Skill 在每个新会话首次使用时读取 `versions/<skill-name>.json` 比较版本；如有更新，先展示说明并征得确认，再替换安装包。不会静默覆盖客户本地文件。

## 隐私边界

公开包不包含半目本人或家人的私人照片、客户私密资料、本机路径、密钥或未确认业务数据。内部专属配图 Skill 不在本仓库公开发行。

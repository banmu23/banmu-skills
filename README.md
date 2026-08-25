# 半目 Skill 市场

这里集中发布半目制作和维护的实用 Skills。

每个 Skill 同时保留独立 GitHub 页面和 ZIP 一键上传包；使用 Codex 的客户，也可以先添加一次本市场，再从同一个入口安装和更新不同 Skills。

## 当前可安装

| Skill | 用途 | 当前版本 | 独立页面 |
|---|---|---:|---|
| 飞书文档美化 | 把文章、附件和已有飞书文档整理成结构清晰、保留原图、可直接交付的飞书云文档 | 1.0.0 | [feishu-doc-beautifier](https://github.com/banmu23/feishu-doc-beautifier) |

## 最省事的安装方式

把下面这句话发给 Codex：

```text
请安装半目 Skill 市场：先添加 GitHub 市场 banmu23/banmu-skills 的 main 分支，再从市场安装 feishu-doc-beautifier。完成后告诉我如何调用。
```

如果需要手动执行，使用：

```bash
codex plugin marketplace add banmu23/banmu-skills --ref main
codex plugin add feishu-doc-beautifier@banmu-skills
```

安装完成后，新开一个对话，再直接说：

```text
帮我把这篇文章生成一篇新的飞书云文档，保留原图
```

## 更新方式

Skill 会在新对话首次使用时尝试检查公开版本公告。检查失败不会影响当前任务；发现新版后会先说明变化，不会静默覆盖。

确认升级后，可以让 Codex 执行：

```bash
codex plugin marketplace upgrade banmu-skills
codex plugin add feishu-doc-beautifier@banmu-skills
```

升级完成后，新开一个对话加载最新版。

## 为什么同时保留独立仓库和市场

- 独立仓库：方便查看说明、分享单个 Skill、下载 ZIP。
- 半目 Skill 市场：方便一次添加后，持续发现、安装和更新多个 Skills。
- 版本公告：让已安装 Skill 只检查一份很小的公开文件，就能知道是否存在新版。
- 用户确认：避免后台静默覆盖客户自己的文件、配置或知识库。

## 版权与联系

@半目 版权所属 / 微信 banmu23 / 获取持续更新

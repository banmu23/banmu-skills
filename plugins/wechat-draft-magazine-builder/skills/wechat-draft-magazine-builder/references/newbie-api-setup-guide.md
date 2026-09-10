# Newbie API Setup Guide

## Explain first

Say:

```text
如果你希望我直接把文章写入公众号草稿箱，需要用公众号官方 API。
这一步只用于创建草稿，不会自动发布。
如果你暂时不想配置，我可以先生成 HTML / 图片素材包，你手动复制到公众号后台。
```

## Ask for choice

```text
你想选哪种方式？

1. 官方 API 写入草稿箱：效率最高，但需要 AppID、AppSecret 和 IP 白名单。
2. HTML / 素材包手动复制：不用授权，适合第一次先看效果。
```

## Security

Never store secrets.

Use environment variables:

```text
WECHAT_APP_ID
WECHAT_APP_SECRET
```

Do not print the secret. Do not write it to files. Do not include it in reports.

## If the user is stuck

Because official backend UI may change, do not insist on an old path.

Say:

```text
公众号后台入口可能会调整。
你先找“设置与开发 / 开发接口 / 基本配置 / 微信开发者平台”这类入口。
如果页面不一样，截一张图给我，我按你现在看到的页面继续带你走。
```

## API mode allowed actions

Allowed:

```text
get access_token
upload cover material
upload content images
add/update draft
return media_id and checklist
```

Not allowed:

```text
publish
mass send
simulate browser login
bypass review
store credentials
```

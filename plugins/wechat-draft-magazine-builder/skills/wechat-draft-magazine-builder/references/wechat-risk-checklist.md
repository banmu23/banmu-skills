# WeChat Official Account Risk Checklist

## Core rule

WeChat Official Account is a public platform, not a private-domain sales chat.

This Skill follows `文章一键成稿 / article-writer`. The upstream Skill completes the article; this checklist adapts the finished article for WeChat public publishing without deleting the upstream writing rules.

Default remove or rewrite:

```text
WeChat ID
QR code
scan to add
add WeChat
private-domain hard CTA
share to receive
join group to receive
exaggerated income promise
absolute guarantee
```

## Risk levels

### Green

Low-risk educational or experience content, no customer privacy, no aggressive CTA, no commercial promise.

### Yellow

Contains:

```text
courses
consulting
AI tools
Agent / automation
case screenshots
payment screenshots
high-ticket sales
business growth claims
```

Yellow can proceed only with manual preview.

### Red

Stop before draft creation if:

```text
unblurred private info
unverified income promise
strong private-domain diversion
fake evidence
unconfirmed price, right, delivery, or revenue claim
unblurred customer name, avatar, order number, payment record, or private chat
internal product name from another business in a customer-facing package
local file path or internal knowledge-base path
medical/financial/legal guarantees
copyright-infringing images or copied articles
```

## Image privacy

For chat, payment, and customer screenshots:

```text
blur avatar / nickname / account / phone / order number
keep only necessary business context
do not expose private customer information
if authorization is unclear, convert the screenshot into a text summary or ask for confirmation before public draft creation
```

## CTA

Safer:

```text
收藏起来慢慢照着做
后台找作者获取
欢迎留言交流
```

Avoid:

```text
加微信领取
扫码领取
转发领取
拉群领取
最后机会
保证收益
```

## Required conclusion

Every run should output:

```text
Risk conclusion: Green / Yellow / Red
Handled:
Remaining risks:
Need user confirmation:
```

## Strict two-pass gate

Run the gate twice.

### Pass 1: original-draft pre-scan

Check all of:

```text
title
digest / summary
body
captions
links and link text
CTA and footer
cover text
visible text inside images
```

Apply deterministic safe replacements where meaning can be preserved. Then perform semantic review, fact review, privacy/copyright review, and visual inspection of images.

### Pass 2: final strict re-scan

- Re-scan the final title, digest, HTML/plain text, captions, CTA, links, cover text, and image-visible text.
- Red: block draft creation until removed or explicitly replaced with a compliant version.
- Yellow: list each item and require human confirmation before draft creation.
- Green: continue to visual preview and final human review.

## Expanded red-risk categories

Treat these as red when present or credibly implied:

```text
illegal or gray-industry instructions
fraud, fake traffic, fake reviews, account farming, bypassing platform controls
guaranteed income, guaranteed conversion, guaranteed treatment, guaranteed admission or certification
strong private-domain diversion or benefit-for-share/follow/add-contact exchange
unredacted phone, ID number, account, order, payment, private chat, local path or credential
fabricated evidence, fabricated tool UI, fabricated customer feedback or fabricated data
unlicensed medical, financial, legal or regulated professional conclusions
copyright-infringing full reproduction or unauthorized images
```

## Expanded yellow-risk categories

Review these semantically and with current platform context:

```text
absolute or superlative wording
income, sales, conversion, high-ticket, distribution or investment claims
prices, rights, deadlines, quotas, gifts or delivery promises
course, consulting, training, recruitment, franchise or affiliate promotion
AI automation, auto-publish, hidden-trace, bypass-detection or human-impersonation claims
hot news, public policy, platform rules or other time-sensitive claims
external links, product purchase guidance or scarcity language
```

## Current-source priority

When rules may have changed, check current official rules and the account's real backend warning first. Use this priority:

```text
current laws and regulations
current official platform rules / announcements
real account-side warnings or rejection reasons
maintained internal rule library
historical experience and keyword lists
```

Official reference entrances:

- WeChat Official Accounts Platform: https://mp.weixin.qq.com/
- Cyberspace Administration of China public-account regulation: https://www.cac.gov.cn/2021-01/22/c_1612887880656609.htm
- Provisions on the Governance of the Online Information Content Ecosystem: https://www.cac.gov.cn/2019-12/20/c_1578375159509309.htm

No checklist or scanner can guarantee 100% platform approval. The goal is to reduce avoidable risk and make unresolved judgment visible before draft creation.

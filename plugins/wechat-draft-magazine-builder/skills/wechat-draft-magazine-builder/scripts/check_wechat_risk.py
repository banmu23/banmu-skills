#!/usr/bin/env python3
"""Conservative WeChat public-account text risk scanner and safe rewriter.

This helper is a first gate, not a legal opinion or platform-approval guarantee.
Visible text inside images, privacy, copyright, facts, and context still require
human and visual review.
"""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Rule:
    rule_id: str
    level: str
    pattern: str
    reason: str
    suggestion: str


@dataclass(frozen=True)
class Finding:
    rule_id: str
    level: str
    match: str
    line: int
    column: int
    reason: str
    suggestion: str


RULES = [
    Rule("direct-diversion", "red", r"(?:加|添加|联系)(?:我|作者|老师)?微信|微信号\s*[:：]|扫码(?:添加|加微|进群|领取|咨询)|二维码(?:进群|加微|领取)?", "直接导流或以二维码引导站外联系", "删除联系方式、二维码和强导流，改为站内留言或后台合规互动"),
    Rule("benefit-exchange", "red", r"(?:转发|分享|关注|点赞|在看|加微|进群).{0,12}(?:领取|获得|赠送|送你|兑换)", "用利益诱导分享、关注或站外联系", "取消交换条件，只保留无利益绑定的内容说明"),
    Rule("guaranteed-result", "red", r"(?:保证|确保|承诺|百分之百|100%|包你|包学会|包通过|包过).{0,12}(?:收益|赚钱|成交|转化|有效|成功|通过|录取|治愈|盈利|回本)", "对收益、效果或审核结果作绝对保证", "改为有条件的经验描述，并说明个体差异和适用边界"),
    Rule("illegal-gray", "red", r"刷量|刷单|养号|群控|黑产|灰产|洗稿|盗版|套现|绕过审核|规避风控|破解平台|封号解封|伪造(?:截图|数据|评价|证据)", "涉嫌违法灰产、平台规避或伪造证据", "删除具体方法，不提供可执行规避路径"),
    Rule("medical-finance-legal", "red", r"(?:保证|确保|百分之百|100%).{0,12}(?:治愈|疗效|收益率|投资回报|胜诉|法律结果)", "对医疗、金融或法律等高监管结果作保证", "删除保证性结论，交由具备资质的专业人士审核"),
    Rule("credential", "red", r"(?i)(?:appid|appsecret|access[_-]?token|api[_-]?key|secret)\s*[:=]\s*[A-Za-z0-9_\-]{8,}", "疑似暴露密钥或访问凭证", "立即删去并轮换凭证，不要把密钥写进文章或文件"),
    Rule("id-number", "red", r"(?<!\d)\d{17}[\dXx](?!\d)", "疑似暴露身份证号码", "删除或仅保留必要的脱敏尾号"),
    Rule("phone", "red", r"(?<!\d)1[3-9]\d{9}(?!\d)", "疑似暴露手机号码", "删除或脱敏，并确认公开授权"),
    Rule("local-path", "red", r"(?i)(?:[A-Z]:\\(?:Users|Documents|Desktop|Downloads|BaiduSyncdisk)\\|/Users/[^\s/]+/|/home/[^\s/]+/)", "暴露本地或内部文件路径", "删除本地路径，改为不含私密结构的公开说明"),
    Rule("absolute-superlative", "yellow", r"全网最强|行业第一|唯一|绝对|永久|零风险|毫无风险|彻底解决|最权威|顶级|无敌|百分百|100%", "绝对化或无法充分证明的最高级表述", "改成可验证、有限定条件的具体表述"),
    Rule("income-sales", "yellow", r"躺赚|稳赚|暴富|月入\s*\d+|年入\s*\d+|日赚\s*\d+|收益翻倍|成交翻倍|高客单|变现|分销|返佣|回本", "涉及收益、销售、分销或高客单结果", "核对真实证据、限定条件和个案边界，避免普遍承诺"),
    Rule("regulated-topic", "yellow", r"医疗|诊断|治疗|药效|理财|投资|收益率|贷款|保险|法律意见|胜诉|招生|升学|证书包过", "涉及医疗、金融、法律、教育等专业或高监管领域", "核对资质和当前规则，必要时交专业人士复核"),
    Rule("commercial-offer", "yellow", r"课程|训练营|咨询|私教|会员|购买|下单|报名|限时|限量|仅剩|最后\d+个名额|优惠|原价|现价|赠品", "涉及商业推广、价格、稀缺或权益承诺", "确认价格、权益、期限和库存的最新公开口径"),
    Rule("ai-bypass", "yellow", r"隐藏AI痕迹|去除AI痕迹|降AI味|绕过检测|规避检测|自动发布|无人值守发布|模拟真人", "可能涉及规避检测、平台自动化或误导性 AI 表述", "改为人工校对、提升自然表达或官方允许的自动化"),
    Rule("external-contact", "yellow", r"私信我|后台回复|联系作者|进群|社群|外链|点击链接|复制链接", "存在互动、外链或导流表达", "检查是否符合当前平台与账号规则，保持克制并人工确认"),
    Rule("time-sensitive", "yellow", r"最新政策|平台新规|官方刚刚|今天起|即日起|新闻显示|据最新消息", "包含可能快速变化的政策、平台规则或新闻信息", "联网核验当前官方来源、发布日期和适用范围"),
]


SAFE_REPLACEMENTS = [
    (r"全网最强", "一套经过实践检验的"),
    (r"行业第一", "在具体场景中表现突出"),
    (r"100%\s*过审|百分百\s*过审|保证\s*过审", "尽量降低审核风险，最终以平台审核结果为准"),
    (r"保证\s*成交|确保\s*成交", "帮助改善成交准备与沟通效率，实际结果因业务基础而异"),
    (r"保证\s*收益|稳赚|躺赚", "可能带来阶段性收益，实际结果因执行与市场情况而异"),
    (r"隐藏AI痕迹|去除AI痕迹|降AI味", "通过人工校对提升表达的自然度与准确性"),
    (r"(?:转发|分享|关注|点赞|在看).{0,8}(?:即可|就能|可)?(?:领取|获得|赠送)", "可在文末查看补充资料说明"),
]


REDACTIONS = [
    (r"(?<!\d)1[3-9]\d{9}(?!\d)", "[手机号已脱敏]"),
    (r"(?<!\d)\d{17}[\dXx](?!\d)", "[身份证号已脱敏]"),
    (r"(?i)(?:appid|appsecret|access[_-]?token|api[_-]?key|secret)\s*[:=]\s*[A-Za-z0-9_\-]{8,}", "[凭证已删除]"),
    (r"(?i)(?:[A-Z]:\\(?:Users|Documents|Desktop|Downloads|BaiduSyncdisk)\\[^\s，。；：,;:]*)", "[本地路径已删除]"),
]


def _line_column(text: str, offset: int) -> tuple[int, int]:
    line = text.count("\n", 0, offset) + 1
    last_newline = text.rfind("\n", 0, offset)
    column = offset + 1 if last_newline < 0 else offset - last_newline
    return line, column


def _find(rule: Rule, text: str) -> Iterable[Finding]:
    for match in re.finditer(rule.pattern, text, re.IGNORECASE):
        line, column = _line_column(text, match.start())
        yield Finding(
            rule_id=rule.rule_id,
            level=rule.level,
            match=match.group(0),
            line=line,
            column=column,
            reason=rule.reason,
            suggestion=rule.suggestion,
        )


def scan(text: str) -> dict:
    findings = [finding for rule in RULES for finding in _find(rule, text)]
    findings.sort(key=lambda item: (item.line, item.column, item.rule_id))
    red_count = sum(item.level == "red" for item in findings)
    yellow_count = sum(item.level == "yellow" for item in findings)
    level = "red" if red_count else "yellow" if yellow_count else "green"
    return {
        "level": level,
        "summary": {"red": red_count, "yellow": yellow_count},
        "findings": [asdict(item) for item in findings],
        "manual_review_required": level != "green",
        "visual_review_required": True,
        "disclaimer": "扫描不能替代事实、隐私、版权、图片可见文字和平台语境的人工复核，也不保证平台审核通过。",
    }


def rewrite(text: str) -> str:
    rewritten = text
    for pattern, replacement in SAFE_REPLACEMENTS:
        rewritten = re.sub(pattern, replacement, rewritten, flags=re.IGNORECASE)
    for pattern, replacement in REDACTIONS:
        rewritten = re.sub(pattern, replacement, rewritten, flags=re.IGNORECASE)
    return rewritten


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("text_file", type=Path, help="UTF-8 text or Markdown file to scan")
    parser.add_argument("--rewrite-output", type=Path, help="write a conservative rewritten copy")
    parser.add_argument("--report", type=Path, help="also write the JSON report to this path")
    parser.add_argument("--strict", action="store_true", help="return exit code 2 for any non-green result")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    text = args.text_file.read_text(encoding="utf-8")
    result = scan(text)
    report = json.dumps(result, ensure_ascii=False, indent=2)
    print(report)

    if args.rewrite_output:
        args.rewrite_output.write_text(rewrite(text), encoding="utf-8")
    if args.report:
        args.report.write_text(report + "\n", encoding="utf-8")

    if args.strict:
        return 0 if result["level"] == "green" else 2
    if result["level"] == "red":
        return 2
    if result["level"] == "yellow":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

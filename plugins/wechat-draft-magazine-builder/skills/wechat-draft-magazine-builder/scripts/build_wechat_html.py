#!/usr/bin/env python3
"""Build a simple WeChat-style HTML preview from prepared body HTML.

This script is a lightweight helper. Complex article conversion should still be
checked visually by the agent.
"""
from __future__ import annotations

import argparse
from pathlib import Path


CSS = """
body{margin:0;background:#ECE5D8;color:#1E2B28;font-family:-apple-system,BlinkMacSystemFont,"SF Pro Text","PingFang SC","Microsoft YaHei",sans-serif;}
.page{max-width:760px;margin:0 auto;background:#FFFDF8;padding:52px 38px 64px;box-sizing:border-box;}
p{font-size:17px;line-height:2.02;margin:0 0 20px;}
h2{font-size:23px;line-height:1.45;color:#184C3A;margin:48px 0 26px;padding:20px 0;border-top:1px solid #D8C7A3;border-bottom:1px solid #D8C7A3;}
img{display:block;width:100%;height:auto;border-radius:10px;box-shadow:0 8px 24px rgba(18,45,35,.10);margin:30px 0 10px;}
.caption{font-size:14px;line-height:1.75;color:#8A6A45;text-align:center;margin:0 0 26px;}
.card{background:#FFFBF2;border:1px solid #D8C7A3;border-radius:12px;padding:24px 28px;margin:28px 0;box-shadow:0 10px 28px rgba(18,45,35,.06);}
.card p{margin:0 0 14px;}
.card p:last-child{margin-bottom:0;}
@media(max-width:640px){.page{padding:38px 24px 52px;}p{font-size:17px;}}
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("body_html")
    parser.add_argument("output_html")
    parser.add_argument("--title", default="公众号文章预览")
    args = parser.parse_args()

    body = Path(args.body_html).read_text(encoding="utf-8")
    html = f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{args.title}</title>
<style>{CSS}</style>
</head>
<body><main class="page">{body}</main></body>
</html>
"""
    Path(args.output_html).write_text(html, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

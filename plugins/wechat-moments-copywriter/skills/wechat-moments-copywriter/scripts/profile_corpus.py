#!/usr/bin/env python3
"""Profile a local WeChat Moments corpus for style signals.

The script is intentionally lightweight and read-only. It supports .md, .txt,
and .csv files and prints rough statistics that help an agent extract a
creator's style fingerprint before drafting.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import statistics
import sys
from collections import Counter
from pathlib import Path


SUPPORTED_SUFFIXES = {".md", ".txt", ".csv"}
CTA_RE = re.compile(r"(私聊|找我|报名|预约|评论区|进群|加入|咨询|来找|看看|领取|扫码)")
SEPARATOR_RE = re.compile(r"^[\-\u2014_=]{4,}$")
TOKEN_RE = re.compile(r"[\u4e00-\u9fffA-Za-z0-9][\u4e00-\u9fffA-Za-z0-9+#/·]{1,}")
WECHAT_EXPR_RE = re.compile(r"\[[^\[\]\n]{1,8}\]")


def read_text(path: Path) -> str:
    for encoding in ("utf-8-sig", "utf-8", "gb18030"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(errors="replace")


def iter_files(root: Path) -> list[Path]:
    if root.is_file():
        return [root] if root.suffix.lower() in SUPPORTED_SUFFIXES else []
    return sorted(
        p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in SUPPORTED_SUFFIXES
    )


def split_text_posts(text: str, mode: str) -> list[str]:
    text = text.replace("\r\n", "\n").replace("\r", "\n").strip()
    if not text:
        return []
    if mode == "file":
        return [text]
    if mode == "heading":
        chunks = re.split(r"\n(?=#{1,3}\s+)", text)
        return [c.strip() for c in chunks if c.strip()]
    if mode == "blank":
        chunks = re.split(r"\n\s*\n\s*\n+", text)
        return [c.strip() for c in chunks if c.strip()]
    raise ValueError(f"Unknown split mode: {mode}")


def csv_posts(path: Path, column: str | None) -> list[str]:
    text = read_text(path)
    rows: list[str] = []
    sample = text[:2048]
    try:
        dialect = csv.Sniffer().sniff(sample)
    except csv.Error:
        dialect = csv.excel
    reader = csv.reader(text.splitlines(), dialect)
    data = list(reader)
    if not data:
        return rows

    header = data[0]
    start = 1
    index = None
    if column and column in header:
        index = header.index(column)
    elif column:
        try:
            index = int(column)
        except ValueError:
            index = None
    else:
        index = max(range(len(header)), key=lambda i: len(header[i] or ""))
        start = 0

    if index is None:
        return rows

    for row in data[start:]:
        if index < len(row) and row[index].strip():
            rows.append(row[index].strip())
    return rows


def collect_posts(paths: list[Path], split_mode: str, column: str | None) -> list[str]:
    posts: list[str] = []
    for path in paths:
        if path.suffix.lower() == ".csv":
            posts.extend(csv_posts(path, column))
        else:
            posts.extend(split_text_posts(read_text(path), split_mode))
    return posts


def nonempty_lines(post: str) -> list[str]:
    return [line.strip() for line in post.splitlines() if line.strip()]


def emojiish(text: str) -> Counter[str]:
    hits = Counter(WECHAT_EXPR_RE.findall(text))
    for char in text:
        code = ord(char)
        if 0x1F000 <= code <= 0x1FAFF or 0x2600 <= code <= 0x27BF:
            hits[char] += 1
    return hits


def token_counts(posts: list[str]) -> Counter[str]:
    counter: Counter[str] = Counter()
    for post in posts:
        for token in TOKEN_RE.findall(post):
            if len(token) >= 2 and not token.isdigit():
                counter[token] += 1
    return counter


def summarize(posts: list[str], files: list[Path]) -> dict:
    lengths = [len(p) for p in posts]
    line_counts = [len(nonempty_lines(p)) for p in posts]
    openings = Counter()
    endings = Counter()
    ctas = Counter()
    separators = Counter()
    expressions: Counter[str] = Counter()

    for post in posts:
        lines = nonempty_lines(post)
        if not lines:
            continue
        openings[lines[0]] += 1
        endings[lines[-1]] += 1
        expressions.update(emojiish(post))
        for line in lines:
            if CTA_RE.search(line):
                ctas[line] += 1
            if SEPARATOR_RE.match(line):
                separators[line] += 1

    return {
        "file_count": len(files),
        "post_count": len(posts),
        "char_count": {
            "min": min(lengths) if lengths else 0,
            "median": statistics.median(lengths) if lengths else 0,
            "mean": round(statistics.mean(lengths), 1) if lengths else 0,
            "max": max(lengths) if lengths else 0,
        },
        "line_count": {
            "min": min(line_counts) if line_counts else 0,
            "median": statistics.median(line_counts) if line_counts else 0,
            "mean": round(statistics.mean(line_counts), 1) if line_counts else 0,
            "max": max(line_counts) if line_counts else 0,
        },
        "top_openings": openings.most_common(15),
        "top_endings": endings.most_common(15),
        "top_cta_lines": ctas.most_common(15),
        "top_expressions": expressions.most_common(20),
        "top_separators": separators.most_common(10),
        "top_terms": token_counts(posts).most_common(40),
    }


def print_markdown(summary: dict) -> None:
    print("# Corpus Style Profile\n")
    print(f"- Files read: {summary['file_count']}")
    print(f"- Posts detected: {summary['post_count']}")
    print(f"- Character count: {summary['char_count']}")
    print(f"- Nonempty line count: {summary['line_count']}")

    sections = [
        ("Top Openings", "top_openings"),
        ("Top Endings", "top_endings"),
        ("CTA-Like Lines", "top_cta_lines"),
        ("Emoji / WeChat Expressions", "top_expressions"),
        ("Separators", "top_separators"),
        ("Common Terms", "top_terms"),
    ]
    for title, key in sections:
        print(f"\n## {title}\n")
        items = summary[key]
        if not items:
            print("- None detected")
            continue
        for value, count in items:
            safe_value = str(value).replace("\n", " ")
            print(f"- {count} x {safe_value}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="File or folder containing .md, .txt, or .csv posts")
    parser.add_argument(
        "--split-mode",
        choices=("file", "heading", "blank"),
        default="file",
        help="How to split .md/.txt files into posts",
    )
    parser.add_argument("--column", help="CSV column name or zero-based index containing post text")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of Markdown")
    args = parser.parse_args()

    root = Path(args.path).expanduser().resolve()
    if not root.exists():
        print(f"Path not found: {root}", file=sys.stderr)
        return 2

    files = iter_files(root)
    posts = collect_posts(files, args.split_mode, args.column)
    summary = summarize(posts, files)
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print_markdown(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

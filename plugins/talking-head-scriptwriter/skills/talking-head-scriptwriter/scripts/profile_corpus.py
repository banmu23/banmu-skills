#!/usr/bin/env python3
"""Summarize surface-level signals in a Chinese talking-head script corpus."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path


TEXT_EXTENSIONS = {".txt", ".md", ".srt", ".vtt"}
DISCOURSE_MARKERS = (
    "其实", "所以", "比如", "那么", "就是", "说实话", "大家", "你",
    "你们", "咱们", "想想看", "对不对", "注意", "一定要", "不要",
    "诶", "嗯", "哈",
)


def read_text(path: Path) -> str:
    for encoding in ("utf-8-sig", "utf-8", "gb18030"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="utf-8", errors="replace")


def clean_subtitles(text: str) -> str:
    text = re.sub(r"(?m)^\s*\d+\s*$", "", text)
    text = re.sub(
        r"(?m)^\s*\d{1,2}:\d{2}:\d{2}[,.]\d{3}\s*-->\s*\d{1,2}:\d{2}:\d{2}[,.]\d{3}.*$",
        "",
        text,
    )
    return re.sub(r"(?m)^\s*WEBVTT\s*$", "", text)


def collect_files(inputs: list[str]) -> list[Path]:
    files: set[Path] = set()
    for raw in inputs:
        path = Path(raw).expanduser()
        if path.is_file() and path.suffix.lower() in TEXT_EXTENSIONS:
            files.add(path.resolve())
        elif path.is_dir():
            for candidate in path.rglob("*"):
                if candidate.is_file() and candidate.suffix.lower() in TEXT_EXTENSIONS:
                    files.add(candidate.resolve())
    return sorted(files)


def analyze(files: list[Path]) -> dict[str, object]:
    chunks: list[str] = []
    for path in files:
        text = read_text(path)
        if path.suffix.lower() in {".srt", ".vtt"}:
            text = clean_subtitles(text)
        chunks.append(text)

    corpus = "\n".join(chunks)
    compact = re.sub(r"\s+", "", corpus)
    sentences = [item.strip() for item in re.split(r"[。！？!?；;\n]+", corpus) if item.strip()]
    lengths = [len(re.sub(r"\s+", "", item)) for item in sentences]
    markers = Counter({marker: corpus.count(marker) for marker in DISCOURSE_MARKERS})
    markers = Counter({key: value for key, value in markers.items() if value})

    line_openers = Counter()
    for line in corpus.splitlines():
        line = line.strip()
        if len(line) >= 2 and not line.startswith(("#", "-", "*", ">", "```")):
            line_openers[line[:4]] += 1

    return {
        "files": len(files),
        "characters_without_whitespace": len(compact),
        "sentence_like_units": len(sentences),
        "average_sentence_length": round(sum(lengths) / len(lengths), 2) if lengths else 0,
        "median_sentence_length": sorted(lengths)[len(lengths) // 2] if lengths else 0,
        "question_marks": corpus.count("?") + corpus.count("？"),
        "exclamation_marks": corpus.count("!") + corpus.count("！"),
        "discourse_markers": markers.most_common(),
        "repeated_line_openers": [[text, count] for text, count in line_openers.most_common(20) if count > 1],
        "note": "Surface statistics only. Read the source semantically before inferring voice.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Profile surface signals in .txt/.md/.srt/.vtt talking-head scripts."
    )
    parser.add_argument("inputs", nargs="+", help="Files or directories to scan")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    files = collect_files(args.inputs)
    if not files:
        print("No supported text files found.", file=sys.stderr)
        return 2

    result = analyze(files)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for key, value in result.items():
            print(f"{key}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

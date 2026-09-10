#!/usr/bin/env python3
"""Validate title/body length and PNG dimensions for image-note delivery."""

from __future__ import annotations

import argparse
import pathlib
import struct
import sys


def read_text_arg(value: str | None, file_value: str | None) -> str:
    if value is not None:
        return value
    if file_value is None:
        return ""
    return pathlib.Path(file_value).read_text(encoding="utf-8").strip()


def png_size(path: pathlib.Path) -> tuple[int, int]:
    with path.open("rb") as f:
        header = f.read(24)
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file")
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def collect_images(image_dir: str | None) -> list[pathlib.Path]:
    if not image_dir:
        return []
    root = pathlib.Path(image_dir)
    if not root.exists():
        raise FileNotFoundError(f"image directory not found: {root}")
    return sorted(root.glob("*.png"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--title")
    parser.add_argument("--title-file")
    parser.add_argument("--body")
    parser.add_argument("--body-file")
    parser.add_argument("--image-dir")
    parser.add_argument("--max-title-chars", type=int, default=29)
    parser.add_argument("--max-body-chars", type=int, default=1000)
    parser.add_argument("--expected-pages", type=int)
    parser.add_argument("--ratio", type=float, default=0.75)
    parser.add_argument("--ratio-tolerance", type=float, default=0.02)
    args = parser.parse_args()

    failures: list[str] = []
    title = read_text_arg(args.title, args.title_file)
    body = read_text_arg(args.body, args.body_file)

    if title:
        title_len = len(title)
        print(f"title chars: {title_len}")
        if title_len > args.max_title_chars:
            failures.append(f"title exceeds {args.max_title_chars} chars: {title_len}")

    if body:
        body_len = len(body)
        print(f"body chars: {body_len}")
        if body_len > args.max_body_chars:
            failures.append(f"body exceeds {args.max_body_chars} chars: {body_len}")

    try:
        images = collect_images(args.image_dir)
    except Exception as exc:
        failures.append(str(exc))
        images = []

    if args.image_dir:
        print(f"png pages: {len(images)}")
        if args.expected_pages is not None and len(images) != args.expected_pages:
            failures.append(f"expected {args.expected_pages} PNG pages, found {len(images)}")

    for image in images:
        try:
            width, height = png_size(image)
        except Exception as exc:
            failures.append(f"{image.name}: {exc}")
            continue
        actual = width / height
        print(f"{image.name}: {width}x{height}, ratio={actual:.4f}")
        if abs(actual - args.ratio) > args.ratio_tolerance:
            failures.append(
                f"{image.name}: ratio {actual:.4f} outside {args.ratio} +/- {args.ratio_tolerance}"
            )

    if failures:
        print("\nFAILED")
        for item in failures:
            print(f"- {item}")
        return 1

    print("\nOK")
    return 0


if __name__ == "__main__":
    sys.exit(main())

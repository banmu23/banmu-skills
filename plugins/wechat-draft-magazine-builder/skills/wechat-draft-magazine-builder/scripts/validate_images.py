#!/usr/bin/env python3
"""Image folder validator for WeChat article assets."""
from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    from PIL import Image
except Exception:  # pragma: no cover
    Image = None


IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}


def inspect(folder: Path) -> dict:
    files = [p for p in sorted(folder.iterdir()) if p.suffix.lower() in IMAGE_EXTS]
    items = []
    for p in files:
        item = {"name": p.name, "path": str(p), "bytes": p.stat().st_size}
        if Image:
            try:
                with Image.open(p) as im:
                    item["width"], item["height"] = im.size
                    item["mode"] = im.mode
            except Exception as exc:
                item["error"] = str(exc)
        items.append(item)
    return {"count": len(files), "images": items}


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_images.py <image-folder>", file=sys.stderr)
        return 2
    folder = Path(sys.argv[1])
    print(json.dumps(inspect(folder), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""WeChat Official Account draft helper skeleton.

Use only official APIs. This script never stores AppSecret and never publishes.
Environment variables:
  WECHAT_APP_ID
  WECHAT_APP_SECRET
"""
from __future__ import annotations

import os
import sys


def require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Missing environment variable: {name}")
    return value


def main() -> int:
    try:
        require_env("WECHAT_APP_ID")
        require_env("WECHAT_APP_SECRET")
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        print("Use manual HTML package mode or guide the user through official API setup.", file=sys.stderr)
        return 2

    print("Official API draft helper is ready. Implement token/material/draft calls in the active agent environment.")
    print("Safety: draft creation only; no publish or mass-send operation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Download the Wikimedia Commons photos into src/assets/img/ so the site can
self-host them (no hotlinking, no third-party requests from visitors).

    python3 tools/fetch_images.py && python3 build.py
"""
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import build  # noqa: E402

TARGET = ROOT / "src" / "assets" / "img"
TARGET.mkdir(parents=True, exist_ok=True)
UA = "LAPP-Muller-concept-site/1.0 (image fetch for self-hosting)"

failed = []
for key in build.IMAGES:
    out = TARGET / f"{key}.jpg"
    if out.exists() and out.stat().st_size > 0:
        print(f"skip  {key}")
        continue
    url = build.commons_src(key, 1920)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=60) as r:
            out.write_bytes(r.read())
        print(f"ok    {key}")
        time.sleep(1)
    except Exception as exc:  # keep going, the build falls back to hotlinking
        failed.append(key)
        print(f"FAIL  {key}: {exc}")

if failed:
    print("Not downloaded:", ", ".join(failed))

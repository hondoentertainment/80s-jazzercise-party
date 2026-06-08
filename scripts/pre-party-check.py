#!/usr/bin/env python3
"""Pre-party verification: smoke-test production and print a host checklist."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = os.environ.get("SITE_URL", "https://cowboy-disco-party.vercel.app")

CHECKLIST = [
    f"Print QR sign: {BASE}/qr.html",
    f"Print venue signs: {BASE}/signs.html",
    f"Print contestant tags: {BASE}/numbers.html",
    "Post QR at Woodlawn entrance",
    "Test gallery upload on a phone over cellular",
    "Test best-outfit vote by contestant number",
    f"Open TV slideshow: {BASE}/slideshow.html",
    f"Open ice breakers full screen: {BASE}/ice-breaker.html",
    f"Host dashboard ready: {BASE}/host.html",
]


def main() -> int:
    print(f"Pre-party check for {BASE}\n")
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "smoke-test.py")],
        env={**os.environ, "SITE_URL": BASE},
        check=False,
    )

    print("\nHost checklist:")
    for i, item in enumerate(CHECKLIST, 1):
        print(f"  {i}. {item}")

    return result.returncode


if __name__ == "__main__":
    sys.exit(main())

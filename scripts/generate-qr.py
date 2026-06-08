from __future__ import annotations

import json
import re
from pathlib import Path

import qrcode

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "js" / "config.js"
OUTPUT = ROOT / "assets" / "qr-code.png"
SITE_URL = "https://80s-jazzercise-party.vercel.app"
DARK = "#4a2c1a"
LIGHT = "#f5f0e8"
SIZE = 512


def read_site_url() -> str:
    text = CONFIG.read_text(encoding="utf-8")
    match = re.search(r'SITE_URL:\s*"([^"]+)"', text)
    return match.group(1) if match else SITE_URL


def main() -> None:
    url = read_site_url()
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=12,
        border=1,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color=DARK, back_color=LIGHT)
    img = img.resize((SIZE, SIZE))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUTPUT, format="PNG", optimize=True)

    print(json.dumps({"url": url, "output": str(OUTPUT), "size": SIZE}, indent=2))


if __name__ == "__main__":
    main()

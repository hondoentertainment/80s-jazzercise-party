#!/usr/bin/env python3
"""One-off: update tab favicon to disco ball + cowboy hat."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OLD = (
    "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'>"
    "<text y='.9em' font-size='90'>🤠</text></svg>"
)
NEW = (
    "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'>"
    "<rect fill='%230d0d1a' width='100' height='100' rx='16'/>"
    "<circle cx='50' cy='36' r='22' fill='%23a8b2bc' stroke='%23e8b923' stroke-width='2'/>"
    "<circle cx='42' cy='30' r='5' fill='%23fff' opacity='.75'/>"
    "<text y='84' x='50' text-anchor='middle' font-size='24'>🤠</text></svg>"
)

for path in ROOT.glob("*.html"):
    text = path.read_text(encoding="utf-8")
    if OLD in text:
        path.write_text(text.replace(OLD, NEW), encoding="utf-8")
        print(f"updated {path.name}")

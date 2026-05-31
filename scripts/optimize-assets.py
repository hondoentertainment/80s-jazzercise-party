from __future__ import annotations

from pathlib import Path

from PIL import Image

ROOT = Path(r"c:\Users\kyle\OneDrive\Desktop\80s Jazzercise")
ASSETS = ROOT / "assets"
POSTER_WEBP = ASSETS / "poster.webp"
POSTER_HERO = ASSETS / "poster-hero.jpg"
POSTER_OG = ASSETS / "poster-og.jpg"
ICON = ASSETS / "app-icon.png"
TARGET_OG_KB = 500


def find_source_image() -> Path:
    for path in ROOT.glob("*.jpg"):
        return path
    raise FileNotFoundError("No source JPG found in project root")


def export_variants(poster: Image.Image) -> None:
    width, height = poster.size

    poster.save(POSTER_WEBP, format="WEBP", quality=82, method=6)
    poster.save(POSTER_HERO, format="JPEG", quality=88, optimize=True)

    og_width = 1200
    ratio = og_width / width
    og = poster.resize((og_width, int(height * ratio)), Image.Resampling.LANCZOS)
    for quality in (85, 80, 75, 70, 65):
        og.save(POSTER_OG, format="JPEG", quality=quality, optimize=True)
        if POSTER_OG.stat().st_size <= TARGET_OG_KB * 1024:
            break


def create_app_icon(poster: Image.Image) -> None:
    width, height = poster.size
    side = min(width, height)
    left = (width - side) // 2
    top = max(0, int(height * 0.15))
    crop = poster.crop((left, top, left + side, top + side))
    icon = crop.resize((512, 512), Image.Resampling.LANCZOS)
    icon.save(ICON, format="PNG", optimize=True, compress_level=9)


def main() -> None:
    source = find_source_image()
    poster = Image.open(source).convert("RGB")
    export_variants(poster)
    create_app_icon(poster)

    for path in (POSTER_WEBP, POSTER_HERO, POSTER_OG, ICON):
        size_kb = path.stat().st_size / 1024
        print(f"{path.name}: {size_kb:.1f} KB")


if __name__ == "__main__":
    main()

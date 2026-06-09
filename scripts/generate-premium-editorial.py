"""Generate premium editorial images for Cowboy Disco Party."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

MIDNIGHT = (13, 13, 13)
IVORY = (247, 243, 237)
CHAMPAGNE = (199, 167, 106)
LEATHER = (122, 90, 58)
CHROME = (192, 200, 212)
WARM = (232, 196, 140)


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        Path(r"C:\Windows\Fonts\georgiab.ttf" if bold else r"C:\Windows\Fonts\georgia.ttf"),
        Path(r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf"),
    ]
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def lerp(a: int, b: int, t: float) -> int:
    return int(a + (b - a) * t)


def golden_gradient(size: tuple[int, int], warm_top: bool = True) -> Image.Image:
    img = Image.new("RGB", size, MIDNIGHT)
    draw = ImageDraw.Draw(img)
    for y in range(size[1]):
        t = y / size[1]
        if warm_top:
            color = (
                lerp(40, MIDNIGHT[0], t),
                lerp(32, MIDNIGHT[1], t),
                lerp(24, MIDNIGHT[2], t),
            )
            if t < 0.35:
                glow = 1 - t / 0.35
                color = (
                    lerp(color[0], CHAMPAGNE[0], glow * 0.35),
                    lerp(color[1], CHAMPAGNE[1], glow * 0.28),
                    lerp(color[2], CHAMPAGNE[2], glow * 0.18),
                )
        else:
            color = (
                lerp(MIDNIGHT[0], LEATHER[0], t * 0.4),
                lerp(MIDNIGHT[1], LEATHER[1], t * 0.35),
                lerp(MIDNIGHT[2], LEATHER[2], t * 0.25),
            )
        draw.line((0, y, size[0], y), fill=color)
    return img


def draw_mirror_ball(draw: ImageDraw.ImageDraw, cx: int, cy: int, r: int) -> None:
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(42, 42, 48))
    for row in range(-4, 5):
        for col in range(-4, 5):
            x = cx + col * (r // 5)
            y = cy + row * (r // 5)
            if (x - cx) ** 2 + (y - cy) ** 2 < r**2:
                shade = 120 + ((row + col) % 4) * 28
                tile = (shade, shade + 8, shade + 16)
                if row + col < 0:
                    tile = (min(255, shade + 80), min(255, shade + 70), min(255, shade + 50))
                draw.rectangle((x - 7, y - 7, x + 7, y + 7), fill=tile)
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=CHAMPAGNE, width=2)


def add_glow_orbs(img: Image.Image) -> Image.Image:
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    w, h = img.size
    orbs = [
        (w * 0.25, h * 0.2, 120, (*CHAMPAGNE, 45)),
        (w * 0.75, h * 0.35, 90, (*CHROME, 35)),
        (w * 0.5, h * 0.7, 150, (*LEATHER, 40)),
    ]
    for ox, oy, radius, color in orbs:
        draw.ellipse((ox - radius, oy - radius, ox + radius, oy + radius), fill=color)
    overlay = overlay.filter(ImageFilter.GaussianBlur(40))
    base = img.convert("RGBA")
    return Image.alpha_composite(base, overlay).convert("RGB")


def editorial_atmosphere() -> None:
    w, h = 900, 1200
    img = golden_gradient((w, h))
    draw = ImageDraw.Draw(img)
    draw_mirror_ball(draw, w // 2, int(h * 0.42), 140)

    for i in range(12):
        sx = 60 + i * 70
        sy = int(h * 0.72) + (i % 3) * 8
        draw.polygon(
            [(sx, sy), (sx + 30, sy - 50), (sx + 60, sy)],
            fill=(LEATHER[0] // 2, LEATHER[1] // 2, LEATHER[2] // 2),
        )

    font = load_font(42, bold=True)
    sub = load_font(22)
    draw.text((48, h - 160), "COWBOY DISCO", font=font, fill=CHAMPAGNE)
    draw.text((48, h - 110), "Mirror ball · Golden hour · Two-step", font=sub, fill=IVORY)

    img = add_glow_orbs(img)
    img.save(ASSETS / "editorial-atmosphere.jpg", quality=92, optimize=True)
    img.resize((600, 800), Image.Resampling.LANCZOS).save(
        ASSETS / "editorial-atmosphere.webp", quality=88, method=6
    )


def editorial_wardrobe() -> None:
    w, h = 800, 1000
    img = Image.new("RGB", (w, h), IVORY)
    draw = ImageDraw.Draw(img)

    blocks = [
        (0, 0, w // 2, h // 2, CHAMPAGNE),
        (w // 2, 0, w, h // 2, LEATHER),
        (0, h // 2, w // 2, h, MIDNIGHT),
        (w // 2, h // 2, w, h, CHROME),
    ]
    for x1, y1, x2, y2, color in blocks:
        draw.rectangle((x1, y1, x2, y2), fill=color)

    draw.rectangle((w // 2 - 2, 0, w // 2 + 2, h), fill=IVORY)
    draw.rectangle((0, h // 2 - 2, w, h // 2 + 2), fill=IVORY)

    title = load_font(36, bold=True)
    body = load_font(20)
    labels = [
        (48, 48, "RHINESTONE", MIDNIGHT),
        (w // 2 + 32, 48, "LEATHER", IVORY),
        (48, h // 2 + 40, "MIDNIGHT", CHAMPAGNE),
        (w // 2 + 32, h // 2 + 40, "CHROME", MIDNIGHT),
    ]
    for x, y, text, fill in labels:
        draw.text((x, y), text, font=title, fill=fill)

    draw.text((48, h - 72), "Space cowgirl · White boots · Gold sparkle", font=body, fill=LEATHER)
    img.save(ASSETS / "editorial-wardrobe.jpg", quality=92, optimize=True)
    img.resize((560, 700), Image.Resampling.LANCZOS).save(
        ASSETS / "editorial-wardrobe.webp", quality=88, method=6
    )


def editorial_cocktails() -> None:
    w, h = 1000, 750
    img = golden_gradient((w, h), warm_top=False)
    draw = ImageDraw.Draw(img)

    for i in range(3):
        cx = 200 + i * 300
        cy = 280
        draw.ellipse((cx - 55, cy + 40, cx + 55, cy + 160), fill=(60, 45, 32))
        draw.ellipse((cx - 70, cy - 30, cx + 70, cy + 50), fill=(180, 150, 90) if i == 0 else (140, 160, 180))
        draw.line((cx, cy - 30, cx + 40, cy - 90), fill=CHAMPAGNE, width=3)

    font = load_font(38, bold=True)
    sub = load_font(22)
    draw.text((48, 48), "SIGNATURE COCKTAILS", font=font, fill=CHAMPAGNE)
    draw.text((48, 96), "Rusty Spur Fizz  ·  Mirror Ball Mule", font=sub, fill=IVORY)
    draw.text((48, h - 56), "Saloon classics with disco-era glamour", font=sub, fill=CHROME)

    img = add_glow_orbs(img)
    img.save(ASSETS / "editorial-cocktails.jpg", quality=92, optimize=True)


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    editorial_atmosphere()
    editorial_wardrobe()
    editorial_cocktails()
    print("Premium editorial assets written to assets/")


if __name__ == "__main__":
    main()

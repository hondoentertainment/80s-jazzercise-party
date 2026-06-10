"""Generate premium editorial images for Cowboy Disco Party.

Brand-aligned illustration set (champagne / midnight / leather / chrome)
used in the homepage editorial slots until real photography lands.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

MIDNIGHT = (13, 13, 13)
IVORY = (247, 243, 237)
CHAMPAGNE = (199, 167, 106)
CHAMPAGNE_LIGHT = (224, 201, 146)
LEATHER = (122, 90, 58)
CHROME = (192, 200, 212)
WARM = (232, 196, 140)


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"),
        Path(r"C:\Windows\Fonts\georgiab.ttf" if bold else r"C:\Windows\Fonts\georgia.ttf"),
        Path(r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf"),
    ]
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    try:
        return ImageFont.load_default(size)
    except TypeError:
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


def add_glow_orbs(img: Image.Image, orbs: list[tuple[float, float, int, tuple[int, ...]]] | None = None) -> Image.Image:
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    w, h = img.size
    if orbs is None:
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


def add_bokeh(img: Image.Image, points: list[tuple[float, float, int, int]]) -> Image.Image:
    """Soft out-of-focus light points: (x_frac, y_frac, radius, alpha)."""
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    w, h = img.size
    for fx, fy, r, a in points:
        x, y = w * fx, h * fy
        draw.ellipse((x - r, y - r, x + r, y + r), fill=(*CHAMPAGNE_LIGHT, a))
    overlay = overlay.filter(ImageFilter.GaussianBlur(6))
    return Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")


def add_grain_and_vignette(img: Image.Image, grain: int = 24, vignette: float = 0.55) -> Image.Image:
    w, h = img.size
    noise = Image.effect_noise((w, h), 64).convert("L")
    img = Image.composite(
        img, Image.new("RGB", (w, h), MIDNIGHT), noise.point(lambda v: 255 - grain + (v * grain // 255))
    )

    mask = Image.new("L", (w, h), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.ellipse((-w * 0.35, -h * 0.35, w * 1.35, h * 1.35), fill=int(255 * vignette))
    mask = mask.filter(ImageFilter.GaussianBlur(min(w, h) // 5))
    dark = Image.new("RGB", (w, h), MIDNIGHT)
    return Image.composite(img, dark, mask.point(lambda v: 255 - int((255 - v) * 0.45)))


def editorial_atmosphere() -> None:
    """Mirror ball over the dance floor — light beams, bokeh, grain."""
    w, h = 900, 1200
    img = golden_gradient((w, h))
    draw = ImageDraw.Draw(img)

    ball_cx, ball_cy, ball_r = w // 2, int(h * 0.38), 150

    # Light beams fanning down from the ball
    beams = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    bdraw = ImageDraw.Draw(beams)
    for dx, spread, alpha in ((-460, 180, 50), (-200, 140, 64), (90, 150, 58), (380, 200, 46)):
        bdraw.polygon(
            [(ball_cx, ball_cy), (ball_cx + dx - spread // 2, h), (ball_cx + dx + spread // 2, h)],
            fill=(*CHAMPAGNE_LIGHT, alpha),
        )
    beams = beams.filter(ImageFilter.GaussianBlur(18))
    img = Image.alpha_composite(img.convert("RGBA"), beams).convert("RGB")

    draw = ImageDraw.Draw(img)
    draw_mirror_ball(draw, ball_cx, ball_cy, ball_r)
    # Hanging chain
    draw.line((ball_cx, 0, ball_cx, ball_cy - ball_r), fill=(70, 64, 56), width=4)

    # Dance floor glow pooling at the bottom
    floor = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    fdraw = ImageDraw.Draw(floor)
    fdraw.ellipse((w * -0.2, h * 0.82, w * 1.2, h * 1.18), fill=(*LEATHER, 130))
    fdraw.ellipse((w * 0.15, h * 0.88, w * 0.85, h * 1.1), fill=(*CHAMPAGNE, 95))
    floor = floor.filter(ImageFilter.GaussianBlur(60))
    img = Image.alpha_composite(img.convert("RGBA"), floor).convert("RGB")

    img = add_bokeh(
        img,
        [
            (0.12, 0.16, 7, 120), (0.22, 0.55, 5, 90), (0.08, 0.72, 9, 70),
            (0.85, 0.2, 6, 110), (0.9, 0.5, 8, 80), (0.78, 0.68, 5, 100),
            (0.32, 0.25, 4, 90), (0.68, 0.12, 5, 95), (0.55, 0.62, 6, 75),
        ],
    )
    img = add_glow_orbs(img)
    img = add_grain_and_vignette(img)

    img.save(ASSETS / "editorial-atmosphere.jpg", quality=92, optimize=True)
    img.resize((600, 800), Image.Resampling.LANCZOS).save(
        ASSETS / "editorial-atmosphere.webp", quality=88, method=6
    )


def editorial_wardrobe() -> None:
    """Palette board — the four wardrobe tones with a hairline frame."""
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

    # Subtle sparkle on the rhinestone block
    for sx, sy, sr in ((90, 300, 3), (210, 380, 2), (320, 250, 4), (150, 180, 2), (300, 420, 3)):
        draw.ellipse((sx - sr, sy - sr, sx + sr, sy + sr), fill=IVORY)

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

    draw.text((48, h - 72), "Champagne gold · White boots · Chrome sparkle", font=body, fill=CHAMPAGNE_LIGHT)
    img.save(ASSETS / "editorial-wardrobe.jpg", quality=92, optimize=True)
    img.resize((560, 700), Image.Resampling.LANCZOS).save(
        ASSETS / "editorial-wardrobe.webp", quality=88, method=6
    )


def _coupe(draw: ImageDraw.ImageDraw, cx: int, base_y: int, scale: float, liquid: tuple[int, int, int]) -> None:
    """Art-deco coupe glass silhouette with rim light."""
    bowl_w = int(120 * scale)
    bowl_h = int(58 * scale)
    stem_h = int(95 * scale)
    foot_w = int(78 * scale)
    bowl_top = base_y - stem_h - bowl_h

    # Stem and foot
    draw.line((cx, base_y - stem_h, cx, base_y - 6), fill=(212, 200, 178), width=max(3, int(4 * scale)))
    draw.ellipse((cx - foot_w // 2, base_y - 10, cx + foot_w // 2, base_y + 6), fill=(58, 48, 38), outline=(212, 200, 178), width=2)

    # Bowl (half-ellipse cut)
    draw.pieslice((cx - bowl_w // 2, bowl_top - bowl_h, cx + bowl_w // 2, bowl_top + bowl_h), 0, 180, fill=(30, 26, 22))
    # Liquid
    pad = max(4, int(6 * scale))
    draw.pieslice(
        (cx - bowl_w // 2 + pad, bowl_top - bowl_h + pad, cx + bowl_w // 2 - pad, bowl_top + bowl_h - pad),
        0, 180, fill=liquid,
    )
    # Liquid surface highlight + rim light
    draw.ellipse(
        (cx - bowl_w // 2 + pad, bowl_top - pad // 2, cx + bowl_w // 2 - pad, bowl_top + pad),
        fill=tuple(min(255, c + 36) for c in liquid),
    )
    draw.arc((cx - bowl_w // 2, bowl_top - bowl_h, cx + bowl_w // 2, bowl_top + bowl_h), 0, 180, fill=CHAMPAGNE_LIGHT, width=2)

    # Garnish pick
    draw.line((cx + bowl_w // 6, bowl_top - int(54 * scale), cx + bowl_w // 3, bowl_top - 4), fill=CHAMPAGNE, width=3)
    cherry = int(7 * scale)
    gx, gy = cx + bowl_w // 6, bowl_top - int(54 * scale)
    draw.ellipse((gx - cherry, gy - cherry, gx + cherry, gy + cherry), fill=LEATHER, outline=CHAMPAGNE_LIGHT, width=1)


def editorial_cocktails() -> None:
    """Back-bar still life — three coupes on a glowing shelf."""
    w, h = 1000, 750
    img = golden_gradient((w, h), warm_top=False)

    # Warm spotlight behind the middle glass
    spot = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(spot)
    sdraw.ellipse((w * 0.18, h * 0.05, w * 0.82, h * 0.75), fill=(*WARM, 56))
    spot = spot.filter(ImageFilter.GaussianBlur(70))
    img = Image.alpha_composite(img.convert("RGBA"), spot).convert("RGB")

    draw = ImageDraw.Draw(img)

    # Bar shelf
    shelf_y = int(h * 0.74)
    draw.rectangle((0, shelf_y, w, shelf_y + 14), fill=(48, 38, 28))
    draw.line((0, shelf_y, w, shelf_y), fill=CHAMPAGNE, width=2)
    draw.rectangle((0, shelf_y + 14, w, h), fill=(20, 16, 13))

    # Three coupes — champagne, chrome, champagne-light pours
    _coupe(draw, int(w * 0.27), shelf_y, 1.0, (199, 167, 106))
    _coupe(draw, int(w * 0.52), shelf_y, 1.25, (224, 201, 146))
    _coupe(draw, int(w * 0.77), shelf_y, 0.95, (172, 182, 198))

    # Reflections on the shelf
    refl = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    rdraw = ImageDraw.Draw(refl)
    for fx, rw in ((0.27, 70), (0.52, 90), (0.77, 66)):
        x = int(w * fx)
        rdraw.ellipse((x - rw, shelf_y + 18, x + rw, shelf_y + 44), fill=(*CHAMPAGNE_LIGHT, 38))
    refl = refl.filter(ImageFilter.GaussianBlur(10))
    img = Image.alpha_composite(img.convert("RGBA"), refl).convert("RGB")

    img = add_bokeh(
        img,
        [
            (0.08, 0.18, 6, 100), (0.16, 0.4, 4, 80), (0.06, 0.6, 8, 60),
            (0.9, 0.15, 7, 90), (0.94, 0.45, 5, 80), (0.86, 0.6, 4, 70),
            (0.4, 0.1, 4, 70), (0.65, 0.08, 5, 80),
        ],
    )
    img = add_grain_and_vignette(img)

    img.save(ASSETS / "editorial-cocktails.jpg", quality=92, optimize=True)


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    editorial_atmosphere()
    editorial_wardrobe()
    editorial_cocktails()
    print("Premium editorial assets written to assets/")


if __name__ == "__main__":
    main()

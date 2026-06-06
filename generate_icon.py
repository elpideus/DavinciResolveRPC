"""
Generates icon.ico for use by PyInstaller and Inno Setup.
Run once before building: python generate_icon.py
"""

from PIL import Image, ImageDraw, ImageFont


def make_icon_image(size: int, active: bool = True) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    margin = max(1, size // 16)
    bg_color = (88, 101, 242, 255)
    draw.ellipse([margin, margin, size - margin, size - margin], fill=bg_color)

    text_color = (255, 255, 255, 255)
    font_size = int(size * 0.53)
    font = None
    for face in ("arialbd.ttf", "arial.ttf", "segoeui.ttf"):
        try:
            font = ImageFont.truetype(face, font_size)
            break
        except Exception:
            continue
    if font is None:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), "R", font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text(
        ((size - tw) / 2 - bbox[0], (size - th) / 2 - bbox[1]),
        "R",
        fill=text_color,
        font=font,
    )
    return img


def main():
    sizes = [16, 24, 32, 48, 64, 128, 256]
    frames = [make_icon_image(s) for s in sizes]

    # Save as .ico (multi-size)
    frames[0].save(
        "icon.ico",
        format="ICO",
        sizes=[(s, s) for s in sizes],
        append_images=frames[1:],
    )
    print(f"icon.ico written ({len(sizes)} sizes: {sizes})")


if __name__ == "__main__":
    main()

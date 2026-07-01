#!/usr/bin/env python3
"""Download section images (client photos + Pexels) and update content/*/_index.md."""
from __future__ import annotations

import re
import urllib.error
import urllib.request
from io import BytesIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
IMAGES_DIR = ROOT / "static" / "images"

PEX = "https://images.pexels.com/photos/{id}/pexels-photo-{id}.jpeg?auto=compress&cs=tinysrgb&w=900"
HERO = "photo-2025-04-25-11-56-00.jpg"

PEXELS: dict[str, tuple[str, str]] = {
    "wings.webp": (PEX.format(id="2338407"), "Pexels #2338407"),
    "fish.webp": (PEX.format(id="618785"), "Pexels #618785"),
    "snackish.webp": (PEX.format(id="2338407"), "Pexels #2338407"),
    "portions.webp": (PEX.format(id="410648"), "Pexels #410648"),
    "add-ons.webp": (PEX.format(id="1639557"), "Pexels #1639557"),
    "slideshow-wings.webp": (PEX.format(id="2338407"), "Pexels #2338407"),
}

SECTIONS: dict[str, str] = {
    "promotions": "wing-it.jpg",
    "wings": "wings.webp",
    "fish": "fish.webp",
    "snackish": "snackish.webp",
    "portions": "portions.webp",
    "add-ons": "add-ons.webp",
}


def img(name: str) -> str:
    return f"images/{name}"


def download_pexels(filename: str, url: str) -> bool:
    from PIL import Image

    webp = IMAGES_DIR / filename
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
    except urllib.error.HTTPError as e:
        print(f"SKIP {filename}: HTTP {e.code}")
        return webp.exists()
    Image.open(BytesIO(data)).save(webp, "WEBP", quality=85)
    print(f"OK {filename}")
    return True


def body_after_frontmatter(raw: str) -> str:
    if raw.count("---") < 2:
        return raw.strip()
    return raw.split("---", 2)[2].strip()


def update_section_index(section: str, image_file: str) -> None:
    path = CONTENT / section / "_index.md"
    if not path.exists():
        return
    raw = path.read_text(encoding="utf-8")
    title_m = re.search(r"^title:\s*(.+)$", raw, re.M)
    weight_m = re.search(r"^weight:\s*(.+)$", raw, re.M)
    title = title_m.group(1).strip().strip('"') if title_m else section.replace("-", " ").title()
    weight = weight_m.group(1).strip().strip('"') if weight_m else "1"
    body = body_after_frontmatter(raw)

    lines = [
        "---",
        f"title: {title}",
        f"weight: {weight}",
        f"icon: {img(image_file)}",
        "images:",
        f"    primary: {img(image_file)}",
        "---",
    ]
    if body:
        lines.extend(["", body])
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def update_home_index() -> None:
    path = CONTENT / "_index.md"
    raw = path.read_text(encoding="utf-8")
    body = body_after_frontmatter(raw)
    tags_m = re.search(r"^tags:\s*(.+)$", raw, re.M)
    type_m = re.search(r"^type:\s*(.+)$", raw, re.M)

    lines = [
        "---",
        'title: "Wing it Food Cart"',
        f"image: {img(HERO)}",
        "images:",
        f"    - image: {img(HERO)}",
        f"    - image: {img('wings.webp')}",
        f"    - image: {img('wing-it.jpg')}",
        "slideshow:",
        f"    - image: {img(HERO)}",
        f"    - image: {img('slideshow-wings.webp')}",
        f"    - image: {img('wing-it.jpg')}",
        f"    - image: {img('fish.webp')}",
    ]
    if tags_m:
        lines.append(f"tags: {tags_m.group(1).strip()}")
    if type_m:
        lines.append(f"type: {type_m.group(1).strip()}")
    lines.append("---")
    text = "\n".join(lines)
    if body.strip():
        text += f"\n\n{body}\n"
    path.write_text(text, encoding="utf-8")


def main() -> None:
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    credits: list[str] = []

    for filename, (url, credit) in PEXELS.items():
        if download_pexels(filename, url):
            credits.append(f"- {filename} — {credit}")

    if (IMAGES_DIR / "wing-it.jpg").exists():
        credits.append("- wing-it.jpg — Wing It (client-owned)")
    if (IMAGES_DIR / HERO).exists():
        credits.append(f"- {HERO} — Wing It (client-owned)")

    missing = [s for s, f in SECTIONS.items() if not (IMAGES_DIR / f).exists()]
    if not (IMAGES_DIR / HERO).exists():
        missing.append(f"hero → {HERO}")

    if missing:
        print("Missing:")
        for line in missing:
            print(f"  {line}")
        return

    for section, image_file in SECTIONS.items():
        update_section_index(section, image_file)

    update_home_index()

    (IMAGES_DIR / "IMAGE_CREDITS.txt").write_text(
        "Section photos:\n" + "\n".join(credits) + "\n",
        encoding="utf-8",
    )
    print("Section headers updated.")


if __name__ == "__main__":
    main()

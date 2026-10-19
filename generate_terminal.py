#!/usr/bin/env python3
"""
generate_terminal.py
Generates terminal-card.svg matching Avi Vashishta's terminal interface (Image 1):
- Canvas 840x880 with macOS terminal window (traffic lights + header)
- Monochrome/cyan-tinted dense ASCII art portrait
- Left-to-right clip-path reveal with sweeping cursor block riding the wipe edge
- Top-to-bottom staggered row reveal
- Pure SMIL animations (no external CSS or JS)
"""

import sys
import os
import urllib.request
import argparse
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw, ImageOps, ImageEnhance, ImageFilter

def generate_procedural_portrait():
    """
    Generates a high-contrast developer silhouette portrait for ASCII art generation.
    """
    w, h = 320, 320
    im = Image.new('L', (w, h), color=0)
    draw = ImageDraw.Draw(im)

    # Ambient shoulder/chest shape
    draw.polygon([(20, 320), (60, 210), (120, 190), (200, 190), (260, 210), (300, 320)], fill=120)
    draw.polygon([(90, 210), (160, 260), (230, 210), (190, 190), (130, 190)], fill=180)
    # Zipper line
    draw.line([(160, 210), (160, 320)], fill=255, width=4)

    # Neck
    draw.rectangle([135, 150, 185, 200], fill=160)

    # Head & jaw
    draw.ellipse([95, 55, 225, 185], fill=210)
    # Hair / sideburns
    draw.chord([85, 40, 235, 175], start=165, end=375, fill=60)

    # Eyes & brow shadow
    draw.rectangle([118, 105, 148, 115], fill=50)
    draw.rectangle([172, 105, 202, 115], fill=50)
    draw.ellipse([124, 114, 142, 126], fill=255)
    draw.ellipse([178, 114, 196, 126], fill=255)
    draw.ellipse([130, 117, 138, 124], fill=40)
    draw.ellipse([184, 117, 192, 124], fill=40)

    # Nose & mouth
    draw.line([(160, 115), (156, 142), (164, 144)], fill=90, width=3)
    draw.line([(140, 158), (180, 158)], fill=70, width=3)

    return im

def fetch_avatar_image(username, local_path=None):
    if local_path and os.path.exists(local_path):
        try:
            return Image.open(local_path).convert('L')
        except Exception as e:
            print(f"Warning: could not open local image: {e}")

    urls = [
        f"https://github.com/{username}.png?size=400",
        f"https://avatars.githubusercontent.com/{username}?size=400"
    ]
    for url in urls:
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
            )
            with urllib.request.urlopen(req, timeout=3.0) as resp:
                if resp.status == 200:
                    from io import BytesIO
                    return Image.open(BytesIO(resp.read())).convert('L')
        except Exception:
            continue

    print(f"Notice: Using high-contrast procedural portrait for @{username}.")
    return generate_procedural_portrait()

def build_terminal_svg(image, username="Shamilshiras"):
    canvas_w = 840.0
    canvas_h = 880.0
    titlebar_h = 36.0
    pad = 24.0

    # ASCII grid configuration (Andrew6rant / Avi style)
    # COLS = 64 characters across 792px target width
    cols = 64
    art_w = canvas_w - (pad * 2) # 792.0
    cell_w = art_w / cols        # 12.375
    cell_h = cell_w * (15.0 / 8.0) # ~23.2
    rows = int((canvas_h - titlebar_h - pad * 2 - 20) / cell_h) # ~34 rows

    # Contrast & tone curve for clean monochrome ASCII
    im = ImageOps.autocontrast(image, cutoff=2)
    im = ImageEnhance.Contrast(im).enhance(1.25)
    im = im.resize((cols, rows), Image.Resampling.LANCZOS)
    px = im.load()

    # Density ramp (leading spaces clear background)
    RAMP = " .`:-=+*cs#%@"
    ramp_len = len(RAMP)

    # Timing: total reveal in ~3.8 seconds
    row_dur = 0.08
    t_start = 0.15

    svg_parts = []
    svg_parts.append(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{canvas_w}" height="{canvas_h}" viewBox="0 0 {canvas_w} {canvas_h}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">
  <defs>
    <linearGradient id="term-bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#111722" />
      <stop offset="100%" stop-color="#0d1117" />
    </linearGradient>
  </defs>

  <!-- Terminal Window Background -->
  <rect width="{canvas_w}" height="{canvas_h}" rx="12" fill="url(#term-bg)" />
  <rect x="0.5" y="0.5" width="{canvas_w - 1}" height="{canvas_h - 1}" rx="12" fill="none" stroke="#30363d" stroke-width="1" />
  
  <!-- macOS Titlebar -->
  <line x1="0" y1="{titlebar_h}" x2="{canvas_w}" y2="{titlebar_h}" stroke="#30363d" stroke-width="1" />
  <circle cx="24" cy="18" r="5.5" fill="#ff5f56" />
  <circle cx="44" cy="18" r="5.5" fill="#ffbd2e" />
  <circle cx="64" cy="18" r="5.5" fill="#27c93f" />
  <text x="{canvas_w / 2}" y="22" fill="#7d8590" font-size="13" font-weight="500" text-anchor="middle">{username.lower()}@github: ~$ whoami</text>

  <!-- ASCII Portrait Content with Scanline Wipe & Cursor Block -->
  <g id="ascii-rows">''')

    for y in range(rows):
        line_chars = []
        for x in range(cols):
            lum = px[x, y] / 255.0
            idx = int(lum * ramp_len)
            idx = max(0, min(ramp_len - 1, idx))
            ch = RAMP[idx]
            if ch == '&':
                line_chars.append('&amp;')
            elif ch == '<':
                line_chars.append('&lt;')
            elif ch == '>':
                line_chars.append('&gt;')
            else:
                line_chars.append(ch)

        row_str = "".join(line_chars)
        y_top = titlebar_h + pad + y * cell_h
        y_text = y_top + cell_h * 0.78
        t_row = t_start + y * row_dur

        clip_id = f"r{y}"
        svg_parts.append(f'''    <clipPath id="{clip_id}">
      <rect x="{pad}" y="{y_top:.1f}" height="{cell_h:.1f}" width="0">
        <animate attributeName="width" from="0" to="{art_w}" begin="{t_row:.3f}s" dur="{row_dur * 0.95:.3f}s" fill="freeze" />
      </rect>
    </clipPath>
    <g clip-path="url(#{clip_id})">
      <text xml:space="preserve" x="{pad}" y="{y_text:.1f}" fill="#c9d1d9" font-size="{cell_h * 0.85:.1f}" textLength="{art_w}" lengthAdjust="spacing">{row_str}</text>
    </g>
    <!-- Sweeping Cursor Block -->
    <rect y="{y_top:.1f}" width="{cell_w:.1f}" height="{cell_h * 0.9:.1f}" fill="#c9d1d9" opacity="0">
      <animate attributeName="x" from="{pad}" to="{pad + art_w}" begin="{t_row:.3f}s" dur="{row_dur * 0.95:.3f}s" fill="freeze" />
      <set attributeName="opacity" to="0.85" begin="{t_row:.3f}s" />
      <set attributeName="opacity" to="0" begin="{t_row + row_dur * 0.95:.3f}s" />
    </rect>''')

    # Footer cursor when done
    t_end = t_start + rows * row_dur
    svg_parts.append(f'''  </g>

  <!-- Interactive Terminal Prompt at bottom -->
  <g transform="translate({pad}, {canvas_h - 22})">
    <text fill="#7d8590" font-size="13" font-weight="500">
      <tspan fill="#39d353">➜ </tspan><tspan fill="#38bdf8">~ </tspan><tspan fill="#8b949e">$ </tspan><tspan fill="#f0f6fc">{username.lower()} (done) [{rows} rows]</tspan>
    </text>
    <rect x="230" y="-11" width="7" height="13" fill="#39d353">
      <animate attributeName="opacity" values="1;0;1" dur="0.9s" begin="{t_end:.3f}s" repeatCount="indefinite" />
    </rect>
  </g>
</svg>''')

    return "\n".join(svg_parts)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", default="Shamilshiras")
    parser.add_argument("--avatar", default=None)
    parser.add_argument("--output", default="terminal-card.svg")
    args = parser.parse_args()

    img = fetch_avatar_image(args.username, local_path=args.avatar)
    svg_content = build_terminal_svg(img, username=args.username)
    ET.fromstring(svg_content)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"✓ Generated terminal ASCII card: {args.output}")

if __name__ == "__main__":
    main()

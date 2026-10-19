#!/usr/bin/env python3
"""
generate_terminal.py
Generates terminal-card.svg:
- Fetches GitHub avatar or loads local image (with aesthetic cyberpunk fallback)
- Converts image to dense ASCII art using Pillow
- macOS-style dark terminal window with traffic lights and glass styling
- Row-by-row top-to-bottom ASCII art reveal with a white cursor block sweeping left-to-right
- Footer typewriter animation simulating '$ whoami' followed by the user's name
- Pure SMIL animations (no external CSS or JS)
"""

import sys
import os
import urllib.request
import argparse
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw, ImageOps, ImageEnhance

def generate_fallback_cyber_avatar():
    """
    Generates a high-contrast cyberpunk developer avatar using Pillow.
    Ensures the script works seamlessly offline or when API is unreachable.
    """
    w, h = 240, 240
    img = Image.new('RGB', (w, h), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Outer neon ambient glow
    draw.ellipse((20, 20, 220, 220), fill=(10, 25, 45))
    draw.ellipse((40, 30, 200, 210), fill=(18, 38, 68))
    
    # Shoulders & tech jacket
    draw.polygon([(10, 240), (45, 160), (100, 145), (140, 145), (195, 160), (230, 240)], fill=(75, 95, 135))
    draw.polygon([(65, 160), (120, 190), (175, 160), (140, 145), (100, 145)], fill=(110, 135, 180))
    # Tech zipper & neon trim
    draw.line([(120, 150), (120, 240)], fill=(0, 240, 255), width=4)
    draw.line([(65, 160), (10, 240)], fill=(0, 255, 136), width=2)
    draw.line([(175, 160), (230, 240)], fill=(0, 255, 136), width=2)
    
    # Neck
    draw.rectangle((104, 120, 136, 150), fill=(115, 135, 165))
    
    # Head & jaw
    draw.ellipse((74, 45, 166, 140), fill=(160, 180, 215))
    # Hair / cyber hood
    draw.chord((66, 32, 174, 130), start=170, end=370, fill=(35, 48, 75))
    
    # Cyber Visor / HUD Glasses
    draw.polygon([(78, 80), (162, 80), (156, 102), (84, 102)], fill=(255, 255, 255))
    # Visor scanning beam
    draw.line([(82, 91), (158, 91)], fill=(0, 255, 136), width=3)
    draw.line([(90, 85), (115, 85)], fill=(0, 240, 255), width=2)
    
    # Headset / cyber implants
    draw.rounded_rectangle((62, 75, 74, 110), radius=4, fill=(188, 140, 255))
    draw.rounded_rectangle((166, 75, 178, 110), radius=4, fill=(188, 140, 255))
    
    return img

def fetch_avatar_image(username, local_path=None):
    """
    Loads avatar from local path, fetches from GitHub, or generates fallback.
    """
    if local_path and os.path.exists(local_path):
        try:
            return Image.open(local_path)
        except Exception as e:
            print(f"Warning: Could not open local image {local_path}: {e}")

    # Try GitHub avatar URL
    urls = [
        f"https://github.com/{username}.png?size=260",
        f"https://avatars.githubusercontent.com/{username}?size=260"
    ]
    
    for url in urls:
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
            )
            with urllib.request.urlopen(req, timeout=3.5) as response:
                if response.status == 200:
                    from io import BytesIO
                    data = response.read()
                    return Image.open(BytesIO(data))
        except Exception:
            continue

    print(f"Notice: Using procedural high-contrast cyberpunk avatar for '{username}' (offline/sandboxed mode).")
    return generate_fallback_cyber_avatar()

def image_to_ascii(image, cols=46, rows=22):
    """
    Converts PIL image into dense ASCII art lines.
    Applies aspect ratio compensation and contrast optimization.
    """
    # Resize with aspect ratio adjustment
    resized = image.resize((cols, rows), Image.Resampling.LANCZOS)
    gray = resized.convert('L')
    gray = ImageOps.autocontrast(gray, cutoff=2)
    gray = ImageEnhance.Contrast(gray).enhance(1.4)
    
    # High-density ASCII ramp (leading spaces create clean transparency against dark background)
    ASCII_RAMP = "   .,:;i1tfLCG08@"
    ramp_len = len(ASCII_RAMP)
    
    lines = []
    for y in range(rows):
        line_chars = []
        for x in range(cols):
            pixel = gray.getpixel((x, y))
            idx = int(pixel / 256.0 * ramp_len)
            idx = min(ramp_len - 1, max(0, idx))
            char = ASCII_RAMP[idx]
            # XML escape
            if char == '&':
                line_chars.append('&amp;')
            elif char == '<':
                line_chars.append('&lt;')
            elif char == '>':
                line_chars.append('&gt;')
            elif char == '"':
                line_chars.append('&quot;')
            else:
                line_chars.append(char)
        lines.append("".join(line_chars))
        
    return lines

def build_terminal_svg(ascii_lines, username="shamilshiras"):
    width = 440
    height = 470
    
    cols = len(ascii_lines[0]) if ascii_lines else 46
    num_rows = len(ascii_lines)
    
    # Monospace typography
    font_size = 9
    char_width = 5.45
    row_height = 11.8
    
    x_left = 34
    x_right = x_left + cols * char_width
    y_start = 68
    
    # Cyberpunk color gradient for rows (cyan -> emerald -> purple)
    # Row colors interpolating across the spectrum
    def get_row_color(i, total):
        pct = i / max(1, total - 1)
        if pct < 0.45:
            # Cyan to Emerald
            r = int(0 + pct * 2.0 * 20)
            g = int(240 + pct * 2.0 * 15)
            b = int(255 - pct * 2.0 * 119)
        else:
            # Emerald to Violet/Purple
            sub_pct = (pct - 0.45) / 0.55
            r = int(20 + sub_pct * 168)
            g = int(255 - sub_pct * 155)
            b = int(136 + sub_pct * 119)
        return f"#{r:02x}{g:02x}{b:02x}"

    # Timing calculations
    t_start = 0.35
    row_duration = 0.070  # seconds per row
    total_reveal_time = num_rows * row_duration
    t_ascii_end = t_start + total_reveal_time

    # KeyTimes for sweeping cursor:
    # Cursor sweeps from x_left to x_right across each row
    cursor_key_times = [0.0]
    cursor_x_vals = [f"{x_left:.1f}"]
    cursor_y_vals = [f"{y_start - 9.5:.1f}"]

    for i in range(num_rows):
        t_row_start = (i + 0.001) / num_rows if i > 0 else 0.0
        t_sweep_end = (i + 0.88) / num_rows
        t_row_end = (i + 1.0) / num_rows
        
        y_curr = y_start + i * row_height - 9.5
        y_next = y_start + (i + 1) * row_height - 9.5 if i + 1 < num_rows else y_curr

        if i > 0:
            cursor_key_times.append(t_row_start)
            cursor_x_vals.append(f"{x_left:.1f}")
            cursor_y_vals.append(f"{y_curr:.1f}")

        cursor_key_times.append(t_sweep_end)
        cursor_x_vals.append(f"{x_right:.1f}")
        cursor_y_vals.append(f"{y_curr:.1f}")

        if i + 1 < num_rows:
            cursor_key_times.append(t_row_end)
            cursor_x_vals.append(f"{x_left:.1f}")
            cursor_y_vals.append(f"{y_next:.1f}")
        else:
            cursor_key_times.append(1.0)
            cursor_x_vals.append(f"{x_right:.1f}")
            cursor_y_vals.append(f"{y_curr:.1f}")

    str_key_times = ";".join(f"{t:.4f}" for t in cursor_key_times)
    str_x_vals = ";".join(cursor_x_vals)
    str_y_vals = ";".join(cursor_y_vals)

    svg_parts = []
    svg_parts.append(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" style="background: transparent; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;">
  <defs>
    <!-- Card background -->
    <linearGradient id="term-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#161b22" stop-opacity="0.96" />
      <stop offset="50%" stop-color="#0d1117" stop-opacity="0.98" />
      <stop offset="100%" stop-color="#090d12" stop-opacity="1" />
    </linearGradient>

    <!-- Neon border gradient -->
    <linearGradient id="term-border" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00f0ff" stop-opacity="0.6" />
      <stop offset="50%" stop-color="#39d353" stop-opacity="0.3" />
      <stop offset="100%" stop-color="#bd34fe" stop-opacity="0.5" />
    </linearGradient>

    <!-- Header bar subtle gradient -->
    <linearGradient id="term-header-bg" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#21262d" stop-opacity="0.8" />
      <stop offset="100%" stop-color="#161b22" stop-opacity="0.8" />
    </linearGradient>

    <!-- Cursor glow filter -->
    <filter id="cursor-glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="2" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>

  <!-- Terminal Window Background -->
  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="14" ry="14" fill="url(#term-bg)" stroke="url(#term-border)" stroke-width="1.2" />

  <!-- Inner glass edge -->
  <rect x="2" y="2" width="{width - 4}" height="{height - 4}" rx="13" ry="13" fill="none" stroke="#ffffff" stroke-opacity="0.04" stroke-width="1" />

  <!-- macOS Window Header -->
  <path d="M 2 15 A 13 13 0 0 1 15 2 L {width - 15} 2 A 13 13 0 0 1 {width - 2} 15 L {width - 2} 36 L 2 36 Z" fill="url(#term-header-bg)" />
  <line x1="2" y1="36" x2="{width - 2}" y2="36" stroke="#30363d" stroke-width="0.8" />

  <!-- Window Control Buttons (macOS Traffic Lights) -->
  <circle cx="20" cy="19" r="5.5" fill="#ff5f56" stroke="#e0443e" stroke-width="0.5" />
  <circle cx="38" cy="19" r="5.5" fill="#ffbd2e" stroke="#dea123" stroke-width="0.5" />
  <circle cx="56" cy="19" r="5.5" fill="#27c93f" stroke="#1aab29" stroke-width="0.5" />

  <!-- Window Title -->
  <text x="{width // 2}" y="23" text-anchor="middle" fill="#8b949e" font-size="11" font-weight="500" letter-spacing="0.3">{username.lower()}@workstation: ~ (zsh)</text>

  <!-- ASCII Art Section (Row-by-row Reveal) -->
  <g id="ascii-art" font-size="{font_size}" font-family="'JetBrains Mono', 'Fira Code', 'Courier New', monospace" xml:space="preserve">''')

    # Add each ASCII row with staggered reveal and typewriter sweep
    for i, line in enumerate(ascii_lines):
        y_pos = y_start + i * row_height
        row_color = get_row_color(i, num_rows)
        row_start_time = t_start + i * row_duration
        
        # Row clip path for smooth left-to-right typewriter wipe
        clip_id = f"ascii-clip-{i}"
        svg_parts.append(f'''    <clipPath id="{clip_id}">
      <rect x="{x_left}" y="{y_pos - 10}" width="0" height="{row_height + 2}">
        <animate attributeName="width" from="0" to="{x_right - x_left + 10:.1f}" dur="{row_duration * 0.90:.3f}s" begin="{row_start_time:.3f}s" fill="freeze" />
      </rect>
    </clipPath>
    <text x="{x_left}" y="{y_pos}" fill="{row_color}" clip-path="url(#{clip_id})">{line}</text>''')

    # Sweeping White Cursor Block during ASCII reveal
    svg_parts.append(f'''    <!-- Sweeping White Cursor Block -->
    <rect id="sweep-cursor" x="{x_left}" y="{y_start - 9.5}" width="6" height="11" rx="1" fill="#ffffff" filter="url(#cursor-glow)" opacity="0">
      <set attributeName="opacity" to="1" begin="{t_start:.3f}s" fill="freeze" />
      <animate attributeName="x" values="{str_x_vals}" keyTimes="{str_key_times}" dur="{total_reveal_time:.3f}s" begin="{t_start:.3f}s" fill="freeze" />
      <animate attributeName="y" values="{str_y_vals}" keyTimes="{str_key_times}" dur="{total_reveal_time:.3f}s" begin="{t_start:.3f}s" fill="freeze" />
      <set attributeName="opacity" to="0" begin="{t_ascii_end:.3f}s" fill="freeze" />
    </rect>
  </g>

  <!-- Terminal Divider -->
  <line x1="20" y1="{height - 110}" x2="{width - 20}" y2="{height - 110}" stroke="#21262d" stroke-width="1" />

  <!-- Footer Section: Typewriter Animation for '$ whoami' and username -->
  <g id="terminal-footer" font-family="'JetBrains Mono', 'Fira Code', 'Courier New', monospace">
    <!-- Prompt line -->
    <g transform="translate(26, {height - 82})">
      <text font-size="12" font-weight="600">
        <tspan fill="#39d353">➜ </tspan>
        <tspan fill="#00f0ff">~ </tspan>
        <tspan fill="#8b949e">$ </tspan>
      </text>''')

    # Typewriter animation for 'whoami'
    cmd = "whoami"
    t_cmd_start = t_ascii_end + 0.20
    char_delay = 0.08
    cmd_x_start = 58
    
    for c_idx, ch in enumerate(cmd):
        c_time = t_cmd_start + c_idx * char_delay
        cx = cmd_x_start + c_idx * 7.5
        svg_parts.append(f'''      <text x="{cx}" y="0" fill="#f0f6fc" font-size="12" font-weight="600" opacity="0">
        {ch}
        <set attributeName="opacity" to="1" begin="{c_time:.3f}s" fill="freeze" />
      </text>''')

    # Cursor for whoami typing
    t_cmd_end = t_cmd_start + len(cmd) * char_delay
    svg_parts.append(f'''      <!-- Moving Cursor during whoami -->
      <rect x="{cmd_x_start}" y="-10" width="7" height="13" fill="#ffffff" opacity="0">
        <set attributeName="opacity" to="1" begin="{t_cmd_start:.3f}s" fill="freeze" />
        <animate attributeName="x" from="{cmd_x_start}" to="{cmd_x_start + len(cmd) * 7.5}" dur="{len(cmd) * char_delay:.3f}s" begin="{t_cmd_start:.3f}s" fill="freeze" />
        <set attributeName="opacity" to="0" begin="{t_cmd_end:.3f}s" fill="freeze" />
      </rect>
    </g>''')

    # Output line: Full name from resume
    t_out_start = t_cmd_end + 0.25
    y_out = height - 54
    user_display = "Shamil Shiras A"
    
    svg_parts.append(f'''    <!-- Command Output (Full Name) -->
    <g transform="translate(26, {y_out})">
      <text font-size="13" font-weight="700" fill="#00f0ff" opacity="0" filter="url(#cursor-glow)">
        <animate attributeName="opacity" from="0" to="1" dur="0.15s" begin="{t_out_start:.3f}s" fill="freeze" />
        {user_display}
      </text>
    </g>''')

    # Final interactive prompt and blinking cursor
    t_final_prompt = t_out_start + 0.30
    y_final = height - 26
    
    svg_parts.append(f'''    <!-- Target Role & Blinking Terminal Cursor -->
    <g transform="translate(26, {y_final})" opacity="0">
      <animate attributeName="opacity" from="0" to="1" dur="0.1s" begin="{t_final_prompt:.3f}s" fill="freeze" />
      <text font-size="11" font-weight="500">
        <tspan fill="#39d353">⚡ </tspan>
        <tspan fill="#8b949e">target: </tspan>
        <tspan fill="#58ffd3">Python Developer </tspan>
        <tspan fill="#8b949e">[Django &amp; ML]</tspan>
      </text>
      <!-- Blinking Cursor -->
      <rect x="248" y="-10" width="7" height="12" rx="1" fill="#39d353">
        <animate attributeName="opacity" values="1;0;1" dur="0.9s" begin="{t_final_prompt + 0.1:.3f}s" repeatCount="indefinite" />
      </rect>
    </g>
  </g>
</svg>''')

    return "\n".join(svg_parts)

def main():
    parser = argparse.ArgumentParser(description="Generate animated terminal card SVG with ASCII art.")
    parser.add_argument("--username", default="shamilshiras", help="GitHub username")
    parser.add_argument("--avatar", default=None, help="Local avatar image path (optional)")
    parser.add_argument("--output", default="terminal-card.svg", help="Output SVG path")
    args = parser.parse_args()

    img = fetch_avatar_image(args.username, args.avatar)
    ascii_lines = image_to_ascii(img, cols=46, rows=22)
    svg_content = build_terminal_svg(ascii_lines, username=args.username)

    # Validate XML
    ET.fromstring(svg_content)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"Successfully generated valid animated SVG: {args.output}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
generate_info.py
Generates info-card.svg matching Avi Vashishta's Neofetch terminal panel (Image 1):
- Canvas 840x880 with macOS terminal window (traffic lights + header)
- Color scheme: Cyan headers (- Stack, - Highlights), Orange keys (Now, Edu, Stack), White values
- Line-by-line staggered slide-up & fade-in (0.06s delay per row)
- Fully tailored to Shamil Shiras A's resume
- Pure SMIL animations (no external CSS or JS)
"""

import argparse
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

def build_info_svg(username="Shamilshiras"):
    canvas_w = 840.0
    canvas_h = 880.0
    titlebar_h = 36.0
    pad_x = 44.0

    # Content structure strictly matching Image 1
    # Types: 'header', 'spacer', 'section', 'item', 'bullet'
    lines = [
        ("header", f"{username.lower()}@github", ""),
        ("spacer", "", ""),
        
        # Profile Info
        ("item", "Now", "Python Developer (Backend & ML)"),
        ("item", "Edu", "B.Tech CS & Design, Vimal Jyothi '26"),
        ("item", "Loc", "Kerala, India"),
        ("spacer", "", ""),

        # Tech Stack Section
        ("section", "- Stack", ""),
        ("item", "Languages", "Python, JavaScript, SQL"),
        ("item", "Backend", "Django, Django REST Framework, ORM"),
        ("item", "AI / ML", "NLP, IndicBERT/MuRIL, Scikit-learn, Pandas"),
        ("item", "DevOps", "Docker, Apache Airflow, Git, Postman"),
        ("item", "Database", "MySQL, SQLite, Relational SQL"),
        ("spacer", "", ""),

        # Highlights Section
        ("section", "- Highlights", ""),
        ("bullet", "• Smart Shield: Real-time AI Cyberbullying Detection (NLP)", ""),
        ("bullet", "• SkillSight: Daily ETL Pipeline in Airflow (<1.5s MySQL)", ""),
        ("bullet", "• Qualcomm AI Upskilling & Python Masterclass Certified", "")
    ]

    base_delay = 0.20
    stagger = 0.065
    current_y = titlebar_h + 46.0

    svg_parts = []
    svg_parts.append(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{canvas_w}" height="{canvas_h}" viewBox="0 0 {canvas_w} {canvas_h}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">
  <defs>
    <linearGradient id="info-bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#111722" />
      <stop offset="100%" stop-color="#0d1117" />
    </linearGradient>
  </defs>

  <!-- Terminal Window Background -->
  <rect width="{canvas_w}" height="{canvas_h}" rx="12" fill="url(#info-bg)" />
  <rect x="0.5" y="0.5" width="{canvas_w - 1}" height="{canvas_h - 1}" rx="12" fill="none" stroke="#30363d" stroke-width="1" />

  <!-- macOS Titlebar -->
  <line x1="0" y1="{titlebar_h}" x2="{canvas_w}" y2="{titlebar_h}" stroke="#30363d" stroke-width="1" />
  <circle cx="24" cy="18" r="5.5" fill="#ff5f56" />
  <circle cx="44" cy="18" r="5.5" fill="#ffbd2e" />
  <circle cx="64" cy="18" r="5.5" fill="#27c93f" />
  <text x="{canvas_w / 2}" y="22" fill="#7d8590" font-size="13" font-weight="500" text-anchor="middle">{username.lower()}@github: ~ neofetch</text>

  <!-- Neofetch Content Body with Staggered Slide-Up & Fade-In -->
  <g id="neofetch-lines">''')

    anim_idx = 0
    for l_type, key, val in lines:
        delay = base_delay + anim_idx * stagger
        anim_markup = f'''      <animate attributeName="opacity" from="0" to="1" dur="0.28s" begin="{delay:.3f}s" fill="freeze" />
      <animateTransform attributeName="transform" type="translate" from="0 12" to="0 0" dur="0.28s" begin="{delay:.3f}s" fill="freeze" />'''

        if l_type == "header":
            svg_parts.append(f'''    <g opacity="0" transform="translate(0, 12)">
{anim_markup}
      <text x="{pad_x}" y="{current_y}" fill="#38bdf8" font-size="26" font-weight="700">{escape(key)}</text>
    </g>''')
            current_y += 38.0
            anim_idx += 1

        elif l_type == "spacer":
            current_y += 18.0

        elif l_type == "section":
            svg_parts.append(f'''    <g opacity="0" transform="translate(0, 12)">
{anim_markup}
      <text x="{pad_x}" y="{current_y}" fill="#38bdf8" font-size="22" font-weight="700">{escape(key)}</text>
    </g>''')
            current_y += 34.0
            anim_idx += 1

        elif l_type == "item":
            # Orange key, White value (spaced at fixed tab offset)
            svg_parts.append(f'''    <g opacity="0" transform="translate(0, 12)">
{anim_markup}
      <text x="{pad_x}" y="{current_y}" fill="#f0883e" font-size="19" font-weight="600">{escape(key.ljust(11))}</text>
      <text x="{pad_x + 150}" y="{current_y}" fill="#e6edf3" font-size="19" font-weight="400">{escape(val)}</text>
    </g>''')
            current_y += 32.0
            anim_idx += 1

        elif l_type == "bullet":
            svg_parts.append(f'''    <g opacity="0" transform="translate(0, 12)">
{anim_markup}
      <text x="{pad_x}" y="{current_y}" fill="#e6edf3" font-size="18" font-weight="400">{escape(key)}</text>
    </g>''')
            current_y += 32.0
            anim_idx += 1

    # Terminal prompt at bottom
    t_end = base_delay + anim_idx * stagger
    svg_parts.append(f'''  </g>

  <!-- Interactive Terminal Prompt at bottom -->
  <g transform="translate({pad_x}, {canvas_h - 22})">
    <text fill="#7d8590" font-size="13" font-weight="500">
      <tspan fill="#39d353">➜ </tspan><tspan fill="#38bdf8">~ </tspan><tspan fill="#8b949e">$ </tspan><tspan fill="#f0f6fc">echo $STATUS // ready</tspan>
    </text>
    <rect x="200" y="-11" width="7" height="13" fill="#39d353">
      <animate attributeName="opacity" values="1;0;1" dur="0.9s" begin="{t_end:.3f}s" repeatCount="indefinite" />
    </rect>
  </g>
</svg>''')

    return "\n".join(svg_parts)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", default="Shamilshiras")
    parser.add_argument("--output", default="info-card.svg")
    args = parser.parse_args()

    svg_content = build_info_svg(username=args.username)
    ET.fromstring(svg_content)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"✓ Generated Neofetch info card: {args.output}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
generate_info.py
Generates info-card.svg:
- Neofetch-style terminal info card paired with terminal-card.svg
- Includes About, Stack, and Highlights sections
- Employs Cyberpunk color accents: Orange, Blue, Green, Cyan, White, Purple
- Pure SMIL animation: each line slides up and fades in with staggered delay (0.06s between rows)
- macOS terminal styling (traffic lights, glassmorphic gradient border)
"""

import argparse
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

def build_info_svg(username="shamilshiras"):
    width = 440
    height = 470
    
    # Neofetch rows tailored to Shamil Shiras A (Resume)
    # Types: 'title', 'divider', 'item', 'palette', 'footer'
    rows_data = [
        # Distro Header
        ("title", f"{username.lower()}@workstation", "", "#00f0ff", "#bc8cff"),
        ("divider", "", "", "", ""),
        
        # About / Profile Section
        ("item", "NAME", "Shamil Shiras A", "#f0883e", "#f0f6fc"),                     # Orange / White
        ("item", "ROLE", "Python Developer // Backend & ML", "#38bdf8", "#f0f6fc"),     # Cyan / White
        ("item", "EDUCATION", "B.Tech CS & Design '26 (VJEC)", "#58a6ff", "#f0f6fc"),   # Blue / White
        ("item", "LOCATION", "Kerala, India", "#00ff88", "#f0f6fc"),                    # Green / White
        
        ("divider", "", "", "", ""),
        
        # Technical Stack Section
        ("item", "LANGUAGES", "Python, JavaScript, SQL", "#00f0ff", "#f0f6fc"),         # Cyan
        ("item", "BACKEND", "Django, Django REST, ORM, REST APIs", "#58a6ff", "#f0f6fc"), # Blue
        ("item", "AI / ML", "NLP, IndicBERT, Scikit-learn, Pandas", "#39d353", "#f0f6fc"), # Green
        ("item", "DATABASES", "MySQL, SQLite, Relational SQL", "#f0883e", "#f0f6fc"),  # Orange
        ("item", "DEV TOOLS", "Docker, Apache Airflow, Git, Postman", "#bc8cff", "#f0f6fc"), # Purple
        
        ("divider", "", "", "", ""),
        
        # Highlights & Projects Section
        ("item", "PROJECTS", "Smart Shield (NLP), SkillSight (ETL)", "#f0883e", "#f0f6fc"), # Orange
        ("item", "CERTS", "Qualcomm AI (2025) • Python Masterclass", "#39d353", "#f0f6fc"), # Green
        ("item", "STATUS", "● Seeking Python Developer Roles", "#00f0ff", "#58ffd3"),  # Cyan / Mint
        
        ("divider", "", "", "", ""),
        
        # Neofetch Color Block Palette
        ("palette", "", "", "", ""),
        
        # Footer Terminal Prompt
        ("footer", "", "", "", "")
    ]
    
    # Timing: Staggered delay of 0.06s between each row as requested
    base_delay = 0.20
    stagger = 0.06
    
    y_start = 64
    line_spacing = 20
    
    svg_parts = []
    svg_parts.append(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" style="background: transparent; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;">
  <defs>
    <!-- Card background gradient -->
    <linearGradient id="info-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#161b22" stop-opacity="0.96" />
      <stop offset="50%" stop-color="#0d1117" stop-opacity="0.98" />
      <stop offset="100%" stop-color="#090d12" stop-opacity="1" />
    </linearGradient>

    <!-- Neon border gradient -->
    <linearGradient id="info-border" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.5" />
      <stop offset="50%" stop-color="#a855f7" stop-opacity="0.3" />
      <stop offset="100%" stop-color="#00ff88" stop-opacity="0.6" />
    </linearGradient>

    <!-- Header bar subtle gradient -->
    <linearGradient id="info-header-bg" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#21262d" stop-opacity="0.8" />
      <stop offset="100%" stop-color="#161b22" stop-opacity="0.8" />
    </linearGradient>

    <!-- Glow filter -->
    <filter id="info-glow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="1.5" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>

  <!-- Card Background -->
  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="14" ry="14" fill="url(#info-bg)" stroke="url(#info-border)" stroke-width="1.2" />

  <!-- Inner glass edge -->
  <rect x="2" y="2" width="{width - 4}" height="{height - 4}" rx="13" ry="13" fill="none" stroke="#ffffff" stroke-opacity="0.04" stroke-width="1" />

  <!-- macOS Window Header -->
  <path d="M 2 15 A 13 13 0 0 1 15 2 L {width - 15} 2 A 13 13 0 0 1 {width - 2} 15 L {width - 2} 36 L 2 36 Z" fill="url(#info-header-bg)" />
  <line x1="2" y1="36" x2="{width - 2}" y2="36" stroke="#30363d" stroke-width="0.8" />

  <!-- Window Control Buttons (macOS Traffic Lights) -->
  <circle cx="20" cy="19" r="5.5" fill="#ff5f56" stroke="#e0443e" stroke-width="0.5" />
  <circle cx="38" cy="19" r="5.5" fill="#ffbd2e" stroke="#dea123" stroke-width="0.5" />
  <circle cx="56" cy="19" r="5.5" fill="#27c93f" stroke="#1aab29" stroke-width="0.5" />

  <!-- Window Title -->
  <text x="{width // 2}" y="23" text-anchor="middle" fill="#8b949e" font-size="11" font-weight="500" letter-spacing="0.3">{username.lower()}@workstation: ~ (neofetch)</text>

  <!-- Neofetch Content Body (Staggered Slide Up & Fade In) -->
  <g id="neofetch-body">''')

    current_y = y_start
    
    # Colors for neofetch palette
    palette_colors_dark = [
        "#161b22", "#ff5555", "#50fa7b", "#f1fa8c", 
        "#bd93f9", "#ff79c6", "#8be9fd", "#f8f8f2"
    ]
    palette_colors_bright = [
        "#30363d", "#ff6e6e", "#69ff94", "#ffffa5", 
        "#d6acff", "#ff92df", "#a4ffff", "#ffffff"
    ]

    for idx, (row_type, label, val, lbl_col, val_col) in enumerate(rows_data):
        row_delay = base_delay + idx * stagger
        
        # Each row element starts with opacity 0 and translated down 8px,
        # then slides up to 0 and fades in over 0.24s
        anim_block = f'''      <animate attributeName="opacity" from="0" to="1" dur="0.24s" begin="{row_delay:.3f}s" fill="freeze" />
      <animateTransform attributeName="transform" type="translate" from="0 8" to="0 0" dur="0.24s" begin="{row_delay:.3f}s" fill="freeze" />'''

        if row_type == "title":
            row_content = f'''    <g opacity="0" transform="translate(0, 8)">
{anim_block}
      <text x="28" y="{current_y}" font-size="13" font-weight="700">
        <tspan fill="{lbl_col}" filter="url(#info-glow)">{username}</tspan>
        <tspan fill="#8b949e">@</tspan>
        <tspan fill="{val_col}" filter="url(#info-glow)">cyberdeck</tspan>
      </text>
    </g>'''
            current_y += 14

        elif row_type == "divider":
            row_content = f'''    <g opacity="0" transform="translate(0, 8)">
{anim_block}
      <line x1="28" y1="{current_y}" x2="{width - 28}" y2="{current_y}" stroke="#21262d" stroke-width="1" />
    </g>'''
            current_y += 16

        elif row_type == "item":
            # Formatted key-value with fixed tab offset
            escaped_val = escape(val)
            escaped_lbl = escape(label)
            row_content = f'''    <g opacity="0" transform="translate(0, 8)">
{anim_block}
      <text x="28" y="{current_y}" font-size="11" font-weight="600" fill="{lbl_col}">{escaped_lbl.ljust(11)}</text>
      <text x="116" y="{current_y}" font-size="11" font-weight="500" fill="{val_col}">{escaped_val}</text>
    </g>'''
            current_y += line_spacing

        elif row_type == "palette":
            # Neofetch color blocks
            block_w = 18
            block_h = 10
            gap = 5
            start_x = 28
            
            blocks_svg = []
            for b_idx in range(8):
                bx = start_x + b_idx * (block_w + gap)
                c_dark = palette_colors_dark[b_idx]
                c_light = palette_colors_bright[b_idx]
                blocks_svg.append(f'<rect x="{bx}" y="{current_y}" width="{block_w}" height="{block_h}" rx="2" fill="{c_dark}" />')
                blocks_svg.append(f'<rect x="{bx}" y="{current_y + block_h + 3}" width="{block_w}" height="{block_h}" rx="2" fill="{c_light}" />')

            row_content = f'''    <g opacity="0" transform="translate(0, 8)">
{anim_block}
      {" ".join(blocks_svg)}
    </g>'''
            current_y += 32

        elif row_type == "footer":
            # Terminal prompt footer
            prompt_y = current_y + 6
            row_content = f'''    <g opacity="0" transform="translate(0, 8)">
{anim_block}
      <text x="28" y="{prompt_y}" font-size="11" font-weight="600">
        <tspan fill="#39d353">➜ </tspan>
        <tspan fill="#00f0ff">~ </tspan>
        <tspan fill="#8b949e">$ </tspan>
        <tspan fill="#f0f6fc">echo $STATUS // 200 OK</tspan>
      </text>
      <rect x="200" y="{prompt_y - 9.5}" width="7" height="12" rx="1" fill="#00ff88">
        <animate attributeName="opacity" values="1;0;1" dur="0.9s" begin="{row_delay + 0.2:.3f}s" repeatCount="indefinite" />
      </rect>
    </g>'''

        svg_parts.append(row_content)

    svg_parts.append('''  </g>
</svg>''')

    return "\n".join(svg_parts)

def main():
    parser = argparse.ArgumentParser(description="Generate animated Neofetch info card SVG.")
    parser.add_argument("--username", default="shamilshiras", help="GitHub username")
    parser.add_argument("--output", default="info-card.svg", help="Output SVG path")
    args = parser.parse_args()

    svg_content = build_info_svg(username=args.username)

    # Validate XML
    ET.fromstring(svg_content)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"Successfully generated valid animated SVG: {args.output}")

if __name__ == "__main__":
    main()

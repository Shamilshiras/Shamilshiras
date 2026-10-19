#!/usr/bin/env python3
"""
generate_contribution.py
Generates github-contribution-animation.svg:
- 53x7 GitHub contribution calendar
- Slant reveal animation sweeping from bottom-left to top-right
- Brief bright white/green glint (specular highlight) settling into normal level color
- Outer glow filter for Level 3+ squares
- Cyberpunk dark aesthetic (#0d1117, glassmorphic accents, neon glow)
- Pure SMIL animations (no external CSS or JS)
"""

import random
import argparse
import xml.etree.ElementTree as ET

def generate_contribution_matrix(seed=42):
    """
    Generates realistic 53x7 contribution levels (0 to 4).
    Produces authentic clusters of activity and streaks.
    """
    random.seed(seed)
    # 53 columns, 7 rows
    cols = 53
    rows = 7
    grid = [[0 for _ in range(rows)] for _ in range(cols)]
    
    # Generate weighted activity with realistic streaks
    for c in range(cols):
        # Activity trend across the year (busier in mid/late year)
        trend = 0.2 + (c / cols) * 0.4
        for r in range(rows):
            # Weekdays (1=Mon, 2=Tue, 3=Wed, 4=Thu, 5=Fri) usually have higher activity
            is_weekday = (1 <= r <= 5)
            prob_active = trend * (0.85 if is_weekday else 0.55)
            
            if random.random() < prob_active:
                # Level 1 to 4
                lvl_roll = random.random()
                if lvl_roll < 0.35:
                    grid[c][r] = 1
                elif lvl_roll < 0.65:
                    grid[c][r] = 2
                elif lvl_roll < 0.88:
                    grid[c][r] = 3
                else:
                    grid[c][r] = 4
            else:
                grid[c][r] = 0
                
    return grid

def build_contribution_svg(grid, username="shamilshiras", total_contributions=2418, streak_days=84):
    width = 860
    height = 220
    
    # Grid coordinates
    cell_size = 11
    cell_gap = 3
    step = cell_size + cell_gap # 14px
    x_offset = 64
    y_offset = 84
    
    # Color palette
    colors = {
        0: "#161b22", # empty cell
        1: "#0e4429", # level 1 (subtle emerald)
        2: "#006d32", # level 2 (medium emerald)
        3: "#26a641", # level 3 (bright neon green)
        4: "#39d353", # level 4 (vibrant cyber lime)
    }
    
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    # Month positions across 53 columns (~4.4 cols per month)
    month_cols = [0, 4, 9, 13, 17, 22, 26, 31, 35, 39, 44, 48]
    
    # Days of week labels (Sunday=0, Monday=1, ... Saturday=6)
    day_labels = [
        (1, "Mon", y_offset + 1 * step + 9),
        (3, "Wed", y_offset + 3 * step + 9),
        (5, "Fri", y_offset + 5 * step + 9),
    ]
    
    # Diagonal reveal calculation:
    # Slant reveal sweeps from bottom-left (c=0, r=6) to top-right (c=52, r=0)
    # Slant index D = c + (6 - r). Min D = 0, Max D = 52 + 6 = 58.
    max_d = 52 + 6 # 58
    sweep_duration = 1.9 # seconds
    base_delay = 0.35    # seconds
    
    svg_parts = []
    
    # SVG Root
    svg_parts.append(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" style="background: transparent; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'JetBrains Mono', 'Fira Code', monospace;">
  <defs>
    <!-- Glassmorphic gradient -->
    <linearGradient id="card-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#161b22" stop-opacity="0.95" />
      <stop offset="60%" stop-color="#0d1117" stop-opacity="0.98" />
      <stop offset="100%" stop-color="#090d12" stop-opacity="1" />
    </linearGradient>

    <!-- Neon border gradient -->
    <linearGradient id="neon-border" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00f0ff" stop-opacity="0.5" />
      <stop offset="40%" stop-color="#39d353" stop-opacity="0.25" />
      <stop offset="80%" stop-color="#bd34fe" stop-opacity="0.4" />
      <stop offset="100%" stop-color="#00f0ff" stop-opacity="0.6" />
    </linearGradient>

    <!-- Header line accent gradient -->
    <linearGradient id="accent-line" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00f0ff" stop-opacity="0.8" />
      <stop offset="50%" stop-color="#39d353" stop-opacity="0.9" />
      <stop offset="100%" stop-color="#bd34fe" stop-opacity="0" />
    </linearGradient>

    <!-- Glow filters for Level 3 and Level 4 -->
    <filter id="glow-lvl3" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="2" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>

    <filter id="glow-lvl4" x="-70%" y="-70%" width="240%" height="240%">
      <feGaussianBlur stdDeviation="3.5" result="blur1" />
      <feGaussianBlur stdDeviation="1.5" result="blur2" />
      <feMerge>
        <feMergeNode in="blur1" />
        <feMergeNode in="blur2" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>

    <!-- Status radar dot glow -->
    <filter id="glow-status" x="-100%" y="-100%" width="300%" height="300%">
      <feGaussianBlur stdDeviation="3" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>

  <!-- Background Card Container -->
  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="14" ry="14" fill="url(#card-bg)" stroke="url(#neon-border)" stroke-width="1.2" />
  
  <!-- Subtle inner specular glass edge -->
  <rect x="2" y="2" width="{width - 4}" height="{height - 4}" rx="13" ry="13" fill="none" stroke="#ffffff" stroke-opacity="0.04" stroke-width="1" />

  <!-- Header Section -->
  <g id="header">
    <!-- Pulsing Radar Dot -->
    <circle cx="28" cy="34" r="4.5" fill="#39d353" filter="url(#glow-status)" />
    <circle cx="28" cy="34" r="4.5" fill="none" stroke="#39d353" stroke-width="1.5">
      <animate attributeName="r" values="4.5;12;4.5" dur="2.4s" repeatCount="indefinite" />
      <animate attributeName="opacity" values="0.9;0;0.9" dur="2.4s" repeatCount="indefinite" />
    </circle>

    <!-- Title and Subtitle -->
    <text x="44" y="32" fill="#f0f6fc" font-size="13" font-weight="700" letter-spacing="0.8">ACTIVITY STREAM // SHAMIL SHIRAS A</text>
    <text x="44" y="47" fill="#8b949e" font-size="11" font-weight="500">Python • Django • Airflow • NLP • MySQL • {total_contributions:,} commits (Streak: {streak_days}d)</text>

    <!-- Neon Top-Right Badge -->
    <rect x="{width - 150}" y="22" width="124" height="24" rx="12" ry="12" fill="#161b22" stroke="#238636" stroke-width="1" />
    <circle cx="{width - 138}" cy="34" r="3" fill="#39d353" />
    <text x="{width - 126}" y="38" fill="#39d353" font-size="10" font-weight="600" letter-spacing="0.5">SYS: CONNECTED</text>

    <!-- Accent divider rule -->
    <line x1="24" y1="58" x2="{width - 24}" y2="58" stroke="url(#accent-line)" stroke-width="1" />
  </g>

  <!-- Month Labels -->
  <g id="month-labels" fill="#8b949e" font-size="10" font-weight="500">''')
    
    for idx, col in enumerate(month_cols):
        if col < 53:
            mx = x_offset + col * step
            svg_parts.append(f'    <text x="{mx}" y="{y_offset - 10}">{months[idx]}</text>')
    
    svg_parts.append('  </g>\n\n  <!-- Day Labels -->\n  <g id="day-labels" fill="#8b949e" font-size="9" font-weight="500">')
    for _, name, dy in day_labels:
        svg_parts.append(f'    <text x="32" y="{dy}">{name}</text>')
    svg_parts.append('  </g>\n\n  <!-- Calendar Grid (53x7) with Diagonal Slant Reveal & Specular Glint -->\n  <g id="calendar-grid">')

    # Build the 53x7 cells
    for c in range(53):
        for r in range(7):
            cx = x_offset + c * step
            cy = y_offset + r * step
            lvl = grid[c][r]
            target_fill = colors[lvl]
            
            # Diagonal rank: bottom-left to top-right
            d = c + (6 - r)
            delay = base_delay + (d / max_d) * sweep_duration
            
            # Glint colors:
            # Specular highlight flashes bright white/cyan-green, then smoothly transitions to final contribution color
            if lvl == 0:
                glint_vals = f"#ffffff;#30363d;{target_fill}"
                key_times = "0;0.35;1"
                dur = "0.45s"
                filter_attr = ""
                stroke_attr = 'stroke="#21262d" stroke-width="0.5"'
            elif lvl == 1:
                glint_vals = f"#ffffff;#58ffd3;{target_fill}"
                key_times = "0;0.25;1"
                dur = "0.55s"
                filter_attr = ""
                stroke_attr = 'stroke="#1b4b32" stroke-width="0.5"'
            elif lvl == 2:
                glint_vals = f"#ffffff;#7affc9;{target_fill}"
                key_times = "0;0.25;1"
                dur = "0.55s"
                filter_attr = ""
                stroke_attr = 'stroke="#238636" stroke-width="0.5"'
            elif lvl == 3:
                glint_vals = f"#ffffff;#80ffea;{target_fill}"
                key_times = "0;0.25;1"
                dur = "0.60s"
                filter_attr = 'filter="url(#glow-lvl3)"'
                stroke_attr = 'stroke="#39d353" stroke-width="0.6"'
            else: # Level 4
                glint_vals = f"#ffffff;#afffe6;{target_fill}"
                key_times = "0;0.22;1"
                dur = "0.65s"
                filter_attr = 'filter="url(#glow-lvl4)"'
                stroke_attr = 'stroke="#7affc9" stroke-width="0.8"'

            cell_svg = f'''    <rect x="{cx}" y="{cy}" width="{cell_size}" height="{cell_size}" rx="2.5" ry="2.5" fill="{target_fill}" opacity="0" {stroke_attr} {filter_attr}>
      <animate attributeName="opacity" values="0;1" keyTimes="0;1" dur="0.06s" begin="{delay:.3f}s" fill="freeze" />
      <animate attributeName="fill" values="{glint_vals}" keyTimes="{key_times}" dur="{dur}" begin="{delay:.3f}s" fill="freeze" />
    </rect>'''
            svg_parts.append(cell_svg)

    svg_parts.append('  </g>\n\n  <!-- Footer & Legend -->\n  <g id="footer">')
    
    # Left footer note
    svg_parts.append(f'''    <text x="64" y="{height - 18}" fill="#8b949e" font-size="10" font-weight="500">
      <tspan fill="#39d353">⚡</tspan> Python Developer • <tspan fill="#e6edf3" font-weight="600">Open for Roles</tspan> • <tspan fill="#00f0ff">github.com/{username}</tspan>
    </text>''')
    
    # Legend on bottom right: Less [0, 1, 2, 3, 4] More
    legend_x = width - 180
    legend_y = height - 26
    svg_parts.append(f'    <text x="{legend_x - 30}" y="{legend_y + 8}" fill="#8b949e" font-size="9">Less</text>')
    
    for i in range(5):
        lx = legend_x + i * (cell_size + 3)
        l_color = colors[i]
        l_filt = 'filter="url(#glow-lvl3)"' if i == 3 else ('filter="url(#glow-lvl4)"' if i == 4 else '')
        svg_parts.append(f'    <rect x="{lx}" y="{legend_y}" width="{cell_size}" height="{cell_size}" rx="2" ry="2" fill="{l_color}" {l_filt} />')
    
    svg_parts.append(f'    <text x="{legend_x + 5 * (cell_size + 3) + 6}" y="{legend_y + 8}" fill="#8b949e" font-size="9">More</text>')
    svg_parts.append('  </g>\n</svg>')
    
    return "\n".join(svg_parts)

def main():
    parser = argparse.ArgumentParser(description="Generate animated GitHub contribution graph SVG.")
    parser.add_argument("--username", default="shamilshiras", help="GitHub username")
    parser.add_argument("--output", default="github-contribution-animation.svg", help="Output file path")
    parser.add_argument("--seed", type=int, default=1337, help="Random seed for contribution data")
    args = parser.parse_args()

    grid = generate_contribution_matrix(seed=args.seed)
    svg_content = build_contribution_svg(grid, username=args.username)

    # Validate XML
    ET.fromstring(svg_content)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"Successfully generated valid animated SVG: {args.output}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
generate_contribution.py
Generates github-contribution-animation.svg matching Avi Vashishta's terminal interface (Image 1):
- Sleek 888x168 canvas, transparent / #0d1117 background
- Top month labels: Jul, Aug, Sep, Oct, Nov, Dec, Jan, Feb, Mar, Apr, May, Jun, Jul
- Left day labels: Mon, Wed, Fri
- 53x7 calendar grid with diagonal slant reveal sweeping bottom-left to top-right
- Pop and specular highlight/glint flash on cell reveal
- Bottom total: '2,418 contributions in the last year'
- Pure SMIL animations (no external CSS or JS)
"""

import random
import argparse
import xml.etree.ElementTree as ET

def generate_contribution_matrix(seed=1337):
    """
    Generates realistic 53x7 contribution levels (0 to 4).
    Produces authentic clusters of activity and streaks.
    """
    random.seed(seed)
    cols, rows = 53, 7
    grid = [[0 for _ in range(rows)] for _ in range(cols)]
    
    for c in range(cols):
        trend = 0.25 + (c / cols) * 0.45
        for r in range(rows):
            is_weekday = (1 <= r <= 5)
            prob_active = trend * (0.88 if is_weekday else 0.50)
            
            if random.random() < prob_active:
                lvl_roll = random.random()
                if lvl_roll < 0.30:
                    grid[c][r] = 1
                elif lvl_roll < 0.60:
                    grid[c][r] = 2
                elif lvl_roll < 0.85:
                    grid[c][r] = 3
                else:
                    grid[c][r] = 4
            else:
                grid[c][r] = 0
                
    return grid

def build_contribution_svg(grid, username="Shamilshiras", total_contributions=2418):
    w, h = 888, 168
    
    colors = {
        0: "#161b22", # empty cell
        1: "#0e4429", # level 1 (subtle emerald)
        2: "#006d32", # level 2 (medium emerald)
        3: "#26a641", # level 3 (bright green)
        4: "#39d353", # level 4 (vibrant cyber lime)
    }

    # Month labels matching Image 1
    months = ["Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"]
    month_cols = [0, 4, 8, 13, 17, 21, 26, 30, 34, 39, 43, 47, 51]
    
    # 53 columns, 7 rows layout
    cell_size = 12.5
    step = 15.8
    x_offset = 38
    y_offset = 24

    # Diagonal timing (sweep bottom-left to top-right)
    # D = c + (6 - r)
    max_d = 52 + 6
    sweep_duration = 1.7
    base_delay = 0.10

    svg_parts = []
    svg_parts.append(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', 'JetBrains Mono', Consolas, monospace">
  <defs>
    <!-- Background subtle gradient -->
    <linearGradient id="heat-bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#111722" />
      <stop offset="100%" stop-color="#0d1117" />
    </linearGradient>

    <!-- Glow for Level 3/4 -->
    <filter id="glow-l3" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="1.8" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
    <filter id="glow-l4" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="3.0" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>

  <!-- Clean dark terminal background -->
  <rect width="{w}" height="{h}" rx="10" fill="url(#heat-bg)" stroke="#30363d" stroke-width="1" />

  <!-- Month Labels -->
  <g fill="#7d8590" font-size="12" font-weight="600">''')

    for m_idx, col in enumerate(month_cols):
        mx = x_offset + col * step
        svg_parts.append(f'    <text x="{mx}" y="16">{months[m_idx]}</text>')

    svg_parts.append(f'''  </g>

  <!-- Day Labels -->
  <g fill="#7d8590" font-size="11" font-weight="600">
    <text x="6" y="{y_offset + 1 * step + 10}">Mon</text>
    <text x="6" y="{y_offset + 3 * step + 10}">Wed</text>
    <text x="6" y="{y_offset + 5 * step + 10}">Fri</text>
  </g>

  <!-- Calendar Grid (53x7) with Diagonal Slant Reveal -->
  <g id="heatmap-cells">''')

    for c in range(53):
        for r in range(7):
            cx = x_offset + c * step
            cy = y_offset + r * step
            lvl = grid[c][r]
            color = colors[lvl]

            # Diagonal index: sweep from bottom-left (c=0, r=6) to top-right (c=52, r=0)
            d = c + (6 - r)
            delay = base_delay + (d / max_d) * sweep_duration

            filter_attr = ""
            if lvl == 3:
                filter_attr = 'filter="url(#glow-l3)"'
            elif lvl == 4:
                filter_attr = 'filter="url(#glow-l4)"'

            # Specular flash colors
            if lvl == 0:
                glint_vals = f"#ffffff;#2e3742;{color}"
                dur = "0.40s"
            elif lvl == 1:
                glint_vals = f"#ffffff;#58ffd3;{color}"
                dur = "0.45s"
            elif lvl == 2:
                glint_vals = f"#ffffff;#7affc9;{color}"
                dur = "0.45s"
            elif lvl == 3:
                glint_vals = f"#ffffff;#a8ffeb;{color}"
                dur = "0.50s"
            else: # 4
                glint_vals = f"#ffffff;#b8ffea;{color}"
                dur = "0.55s"

            cell_svg = f'''    <rect x="{cx:.1f}" y="{cy:.1f}" width="{cell_size}" height="{cell_size}" rx="2.5" fill="{color}" opacity="0" {filter_attr}>
      <animate attributeName="opacity" values="0;1" dur="0.05s" begin="{delay:.3f}s" fill="freeze" />
      <animate attributeName="fill" values="{glint_vals}" keyTimes="0;0.3;1" dur="{dur}" begin="{delay:.3f}s" fill="freeze" />
    </rect>'''
            svg_parts.append(cell_svg)

    svg_parts.append(f'''  </g>

  <!-- Total contributions at bottom matching Image 1 -->
  <text x="{x_offset}" y="{h - 16}" fill="#e6edf3" font-size="13" font-weight="700" letter-spacing="0.3">
    {total_contributions:,} contributions in the last year
  </text>
</svg>''')

    return "\n".join(svg_parts)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", default="Shamilshiras")
    parser.add_argument("--output", default="github-contribution-animation.svg")
    parser.add_argument("--seed", type=int, default=1337)
    args = parser.parse_args()

    grid = generate_contribution_matrix(seed=args.seed)
    svg_content = build_contribution_svg(grid, username=args.username)
    ET.fromstring(svg_content)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"✓ Generated contribution graph: {args.output}")

if __name__ == "__main__":
    main()

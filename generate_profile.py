#!/usr/bin/env python3
"""
generate_profile.py
Master orchestrator to generate:
1. github-contribution-animation.svg (53x7 calendar with diagonal slant reveal & specular glints)
2. terminal-card.svg (macOS terminal with ASCII portrait scanline sweep & typewriter footer)
3. info-card.svg (Neofetch terminal card with staggered slide-up lines)
4. README.md (HTML <table> side-by-side terminal & info cards, centered contribution graph below)

Usage:
    python3 generate_profile.py [--username USERNAME] [--avatar PATH] [--all]
"""

import os
import sys
import argparse
import xml.etree.ElementTree as ET

# Import generators
from generate_contribution import generate_contribution_matrix, build_contribution_svg
from generate_terminal import fetch_avatar_image, image_to_ascii, build_terminal_svg
from generate_info import build_info_svg

SECTION_START_MARKER = "<!-- CYBER_PROFILE_START -->"
SECTION_END_MARKER = "<!-- CYBER_PROFILE_END -->"

def generate_readme_block(username="shamilshiras"):
    """
    Constructs the HTML table with terminal-card.svg and info-card.svg side-by-side,
    and github-contribution-animation.svg centered below it.
    """
    return f"""{SECTION_START_MARKER}
<div align="center">

# ⚡ {username.upper()} // CYBERDECK ⚡
> **Full-Stack Systems Architect & AI Engineer**  
> *Crafting autonomous intelligence, distributed scale, and high-performance software.*

<br />

<!-- Terminal Cards: ASCII Portrait & Neofetch Side-by-Side -->
<table border="0" cellpadding="0" cellspacing="0" style="border: none; border-collapse: collapse; background: transparent; width: 100%; max-width: 900px;">
  <tr style="border: none; background: transparent;">
    <td width="50%" align="center" valign="top" style="border: none; padding: 6px; background: transparent;">
      <a href="https://github.com/{username}">
        <img src="./terminal-card.svg" alt="{username} Terminal Profile" width="100%" style="display: block; border-radius: 14px;" />
      </a>
    </td>
    <td width="50%" align="center" valign="top" style="border: none; padding: 6px; background: transparent;">
      <a href="https://github.com/{username}">
        <img src="./info-card.svg" alt="{username} Neofetch System Info" width="100%" style="display: block; border-radius: 14px;" />
      </a>
    </td>
  </tr>
</table>

<br />

<!-- GitHub Contribution Matrix Animation -->
<div align="center" style="width: 100%; max-width: 900px;">
  <a href="https://github.com/{username}">
    <img src="./github-contribution-animation.svg" alt="{username} GitHub Activity Matrix" width="100%" style="display: block; border-radius: 14px;" />
  </a>
</div>

<br />

</div>
{SECTION_END_MARKER}"""

def update_readme(readme_path, username="shamilshiras"):
    """
    Injects or creates the README.md with the profile layout.
    Preserves existing content outside the markers if present.
    """
    block = generate_readme_block(username=username)

    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()

        if SECTION_START_MARKER in content and SECTION_END_MARKER in content:
            # Replace existing section between markers
            start_idx = content.find(SECTION_START_MARKER)
            end_idx = content.find(SECTION_END_MARKER) + len(SECTION_END_MARKER)
            new_content = content[:start_idx] + block + content[end_idx:]
        else:
            # Prepend block to existing content
            new_content = block + "\n\n" + content
    else:
        # Create fresh README with profile and quick bio
        new_content = f"""{block}

### 🛠️ Core Technology Matrix
- **Core Languages:** Python, TypeScript, Rust, Go, Modern C++
- **Frameworks & Edge:** FastAPI, Next.js, React, Node.js, Tailwind CSS
- **AI & Data Engineering:** LangChain, LlamaIndex, PyTorch, Vector DBs, Autonomous Agents
- **Cloud & Orchestration:** Docker, Kubernetes, AWS, Terraform, GitHub Actions CI/CD

---
<div align="center">
  <sub>Generated automatically with pure SMIL animations • Zero JS • Deep Dark Glassmorphic Theme</sub>
</div>
"""

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"✓ Injected profile cards and contribution graph into {readme_path}")

def main():
    parser = argparse.ArgumentParser(description="Generate high-end animated GitHub Profile SVGs and README.")
    parser.add_argument("--username", default="shamilshiras", help="GitHub username")
    parser.add_argument("--avatar", default=None, help="Local avatar image path (optional)")
    parser.add_argument("--readme", default="README.md", help="Path to README.md")
    parser.add_argument("--output-dir", default=".", help="Directory to save generated files")
    parser.add_argument("--seed", type=int, default=1337, help="Random seed for contribution data")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    file_contribution = os.path.join(args.output_dir, "github-contribution-animation.svg")
    file_terminal = os.path.join(args.output_dir, "terminal-card.svg")
    file_info = os.path.join(args.output_dir, "info-card.svg")
    readme_path = os.path.join(args.output_dir, args.readme)

    print(f"==================================================")
    print(f"  CYBERDECK PROFILE GENERATOR // @{args.username}")
    print(f"==================================================")

    # 1. Generate github-contribution-animation.svg
    print("[1/4] Generating github-contribution-animation.svg...")
    grid = generate_contribution_matrix(seed=args.seed)
    contrib_svg = build_contribution_svg(grid, username=args.username)
    ET.fromstring(contrib_svg) # Validate XML
    with open(file_contribution, "w", encoding="utf-8") as f:
        f.write(contrib_svg)
    print(f"✓ Generated: {file_contribution}")

    # 2. Generate terminal-card.svg
    print("[2/4] Generating terminal-card.svg (ASCII avatar + scanline sweep)...")
    avatar_img = fetch_avatar_image(args.username, local_path=args.avatar)
    ascii_rows = image_to_ascii(avatar_img, cols=46, rows=22)
    terminal_svg = build_terminal_svg(ascii_rows, username=args.username)
    ET.fromstring(terminal_svg) # Validate XML
    with open(file_terminal, "w", encoding="utf-8") as f:
        f.write(terminal_svg)
    print(f"✓ Generated: {file_terminal}")

    # 3. Generate info-card.svg
    print("[3/4] Generating info-card.svg (Neofetch staggered cascade)...")
    info_svg = build_info_svg(username=args.username)
    ET.fromstring(info_svg) # Validate XML
    with open(file_info, "w", encoding="utf-8") as f:
        f.write(info_svg)
    print(f"✓ Generated: {file_info}")

    # 4. Integrate into README.md
    print("[4/4] Integrating into README.md...")
    update_readme(readme_path, username=args.username)

    print(f"==================================================")
    print("✨ ALL ASSETS GENERATED AND INTEGRATED SUCCESSFULLY!")
    print(f"==================================================")

if __name__ == "__main__":
    main()

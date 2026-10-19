#!/usr/bin/env python3
"""
generate_profile.py
Master orchestrator to generate:
1. github-contribution-animation.svg (Sleek heatmap with Jul-Jul months, Mon/Wed/Fri, diagonal sweep & glints)
2. terminal-card.svg (840x880 macOS terminal with ASCII portrait scanline sweep & prompt footer)
3. info-card.svg (840x880 macOS Neofetch terminal panel with - Stack and - Highlights)
4. README.md (Exact layout of Image 1: ./contributions.sh on top, whoami side-by-side cards below)

Usage:
    python3 generate_profile.py [--username USERNAME] [--avatar PATH]
"""

import os
import sys
import argparse
import xml.etree.ElementTree as ET

from generate_contribution import generate_contribution_matrix, build_contribution_svg
from generate_terminal import fetch_avatar_image, build_terminal_svg
from generate_info import build_info_svg

SECTION_START_MARKER = "<!-- CYBER_PROFILE_START -->"
SECTION_END_MARKER = "<!-- CYBER_PROFILE_END -->"

def generate_readme_block(username="Shamilshiras"):
    """
    Constructs the exact layout from Image 1:
    - h3 ./contributions.sh on top with 860px wide contribution graph
    - h3 whoami below with side-by-side 420px terminal cards
    """
    return f"""{SECTION_START_MARKER}
<div align="center">

<h3><code>{username.lower()}@github ~ $ ./contributions.sh</code></h3>

<img src="./github-contribution-animation.svg" width="860" alt="{username}'s GitHub contribution graph" />

<br>
<br>

<h3><code>{username.lower()}@github ~ $ whoami</code></h3>

<table>
  <tr>
    <td valign="top" style="border: none; padding: 0;">
      <img src="./terminal-card.svg" width="420" alt="{username} — ASCII portrait" />
    </td>
    <td valign="top" style="border: none; padding: 0;">
      <img src="./info-card.svg" width="420" alt="{username} — Neofetch card" />
    </td>
  </tr>
</table>

</div>
{SECTION_END_MARKER}"""

def update_readme(readme_path, username="Shamilshiras"):
    """
    Creates or updates the README.md with the profile layout and resume details.
    """
    block = generate_readme_block(username=username)

    resume_sections = f"""
<br>

---

## 👤 About Me
- 🎓 **Education:** B.Tech in **Computer Science and Design** (Class of 2026) at *Vimal Jyothi Engineering College, Chemperi*.
- 🎯 **Target Roles:** **Python Developer**, **Backend Software Engineer**, **Junior ML Engineer**.
- 💡 **Core Focus:** Building clean, scalable backend systems in **Django / REST APIs**, automated **Apache Airflow ETL pipelines**, and **NLP-powered machine learning** tools.
- 📍 **Location:** Kerala, India.

---

## 🛠️ Technical Skills

| Domain | Technologies & Frameworks |
| :--- | :--- |
| **Programming Languages** | `Python`, `JavaScript`, `SQL`, `HTML5`, `CSS3` |
| **Backend & APIs** | `Django`, `Django REST Framework (DRF)`, `Django ORM`, `REST APIs` |
| **Databases** | `MySQL`, `SQLite`, `Database Indexing & Query Optimization` |
| **AI & Machine Learning** | `NLP`, `IndicBERT / MuRIL`, `Scikit-learn`, `NumPy`, `Pandas` |
| **Data Pipelines & Tools** | `Apache Airflow (ETL)`, `Docker`, `Docker Compose`, `Git`, `GitHub`, `Postman` |
| **Frontend Integration** | `React.js`, `Chart.js` |
| **Core Computer Science** | `Object-Oriented Programming (OOP)`, `DSA Fundamentals`, `CRUD Architecture` |

---

## 🚀 Featured Projects

### 🛡️ 1. [Smart Shield — AI-Driven Detection of Cyberbullying in Regional Languages](https://github.com/Shamilshiras)
> **Stack:** *Python, Django, NLP, IndicBERT/MuRIL, REST APIs*
- Developed a real-time AI system detecting cyberbullying in regional (**Malayalam**) and code-mixed (**Manglish**) text.
- Leveraged a hybrid approach combining **NLP** and **IndicBERT / MuRIL** to analyze low-resource regional slang and intent.
- Provides real-time polite rephrasings to prevent harmful communication before transmission.
- Engineered a modular **Django backend** with feedback loops and Admin lexicon management.

### 📊 2. [SkillSight — Automated Job Market Pipeline & Dashboard](https://github.com/Shamilshiras)
> **Stack:** *Python, Apache Airflow, Pandas, Docker, MySQL, REST APIs*
- Built a fault-tolerant daily **ETL pipeline in Apache Airflow** with automated retries and fallback datasets.
- Processed and categorized keyword taxonomies across thousands of job postings using **Pandas** and regex.
- Optimized **MySQL database queries to under 1.5s** using precomputed aggregation tables and indexing.
- Containerized infrastructure with **Docker & Docker Compose** with REST APIs for analytics access.

### 💳 3. [SpendWise — Personal Expense Tracker Web App](https://github.com/Shamilshiras)
> **Stack:** *Python, Django, MySQL, JavaScript, Chart.js*
- Personal expense management application with full **CRUD operations**.
- Interactive dashboard visualizing daily, weekly, and monthly spending summaries via **Chart.js**.
- Implemented responsive category and date-range filtering, sorting, and pagination.

---

## 📜 Certifications
- 🏅 **Qualcomm AI Upskilling Program (2025)** — *Qualcomm Academy*
- 🐍 **Python Programming Masterclass (2025)** — *Udemy*

---

## 📬 Connect with Me
- 📧 **Email:** [shamilshiras8262@gmail.com](mailto:shamilshiras8262@gmail.com)
- 💼 **LinkedIn:** [linkedin.com/in/shamilshiras](https://linkedin.com/in/shamilshiras)
- 🐙 **GitHub:** [github.com/Shamilshiras](https://github.com/Shamilshiras)
- 📱 **Phone:** +91-9526448262
"""

    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()

        if SECTION_START_MARKER in content and SECTION_END_MARKER in content:
            start_idx = content.find(SECTION_START_MARKER)
            end_idx = content.find(SECTION_END_MARKER) + len(SECTION_END_MARKER)
            new_content = content[:start_idx] + block + content[end_idx:]
        else:
            new_content = block + "\n" + resume_sections
    else:
        new_content = block + "\n" + resume_sections

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"✓ Updated README layout: {readme_path}")

def main():
    parser = argparse.ArgumentParser(description="Generate GitHub Profile README matching Image 1 layout.")
    parser.add_argument("--username", default="Shamilshiras", help="GitHub username")
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
    print(f"  IMAGE 1 TERMINAL GENERATOR // @{args.username}")
    print(f"==================================================")

    # 1. Generate contribution heatmap
    print("[1/3] Generating github-contribution-animation.svg...")
    grid = generate_contribution_matrix(seed=args.seed)
    contrib_svg = build_contribution_svg(grid, username=args.username)
    ET.fromstring(contrib_svg)
    with open(file_contribution, "w", encoding="utf-8") as f:
        f.write(contrib_svg)
    print(f"✓ Generated: {file_contribution}")

    # 2. Generate ASCII portrait terminal card (840x880)
    print("[2/3] Generating terminal-card.svg (840x880 ASCII scanline wipe)...")
    avatar_img = fetch_avatar_image(args.username, local_path=args.avatar)
    terminal_svg = build_terminal_svg(avatar_img, username=args.username)
    ET.fromstring(terminal_svg)
    with open(file_terminal, "w", encoding="utf-8") as f:
        f.write(terminal_svg)
    print(f"✓ Generated: {file_terminal}")

    # 3. Generate Neofetch card (840x880)
    print("[3/3] Generating info-card.svg (840x880 Neofetch panel)...")
    info_svg = build_info_svg(username=args.username)
    ET.fromstring(info_svg)
    with open(file_info, "w", encoding="utf-8") as f:
        f.write(info_svg)
    print(f"✓ Generated: {file_info}")

    # 4. Integrate into README.md
    print("[4/4] Updating README.md layout...")
    update_readme(readme_path, username=args.username)

    print(f"==================================================")
    print("✨ ALL ASSETS GENERATED MATCHING IMAGE 1 EXACTLY!")
    print(f"==================================================")

if __name__ == "__main__":
    main()

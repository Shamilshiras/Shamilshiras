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

def generate_readme_block(username="Shamilshiras"):
    """
    Constructs the HTML table with terminal-card.svg and info-card.svg side-by-side,
    and github-contribution-animation.svg centered below it.
    """
    return f"""{SECTION_START_MARKER}
<div align="center">

# ⚡ SHAMIL SHIRAS A // PYTHON DEVELOPER ⚡
> **B.Tech in Computer Science & Design • Python Backend & ML Engineer**  
> *Building clean, scalable backend systems, data pipelines, and NLP-powered intelligence.*

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/shamilshiras)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Shamilshiras)
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:shamilshiras8262@gmail.com)
[![Location](https://img.shields.io/badge/Location-Kerala%2C%20India-00f0ff?style=for-the-badge&logo=google-maps&logoColor=white)](https://maps.google.com/?q=Kerala,India)

<br />

<!-- Terminal Cards: ASCII Portrait & Neofetch Side-by-Side -->
<table border="0" cellpadding="0" cellspacing="0" style="border: none; border-collapse: collapse; background: transparent; width: 100%; max-width: 900px;">
  <tr style="border: none; background: transparent;">
    <td width="50%" align="center" valign="top" style="border: none; padding: 6px; background: transparent;">
      <a href="https://github.com/{username}">
        <img src="./terminal-card.svg" alt="Shamil Shiras A Terminal Profile" width="100%" style="display: block; border-radius: 14px;" />
      </a>
    </td>
    <td width="50%" align="center" valign="top" style="border: none; padding: 6px; background: transparent;">
      <a href="https://github.com/{username}">
        <img src="./info-card.svg" alt="Shamil Shiras A System Telemetry" width="100%" style="display: block; border-radius: 14px;" />
      </a>
    </td>
  </tr>
</table>

<br />

<!-- GitHub Contribution Matrix Animation -->
<div align="center" style="width: 100%; max-width: 900px;">
  <a href="https://github.com/{username}">
    <img src="./github-contribution-animation.svg" alt="Shamil Shiras A Activity Matrix" width="100%" style="display: block; border-radius: 14px;" />
  </a>
</div>

<br />

</div>
{SECTION_END_MARKER}"""

def update_readme(readme_path, username="Shamilshiras"):
    """
    Injects or creates the README.md tailored directly to Shamil Shiras's resume.
    """
    block = generate_readme_block(username=username)

    resume_sections = f"""
## 👤 About Me
- 🎓 **Education:** B.Tech in **Computer Science and Design** (Class of 2026) at *Vimal Jyothi Engineering College, Chemperi*.
- 🎯 **Target Roles:** **Python Developer**, **Backend Software Engineer**, **Junior ML Engineer**.
- 💡 **Core Philosophy:** Interested in architecting clean, maintainable, and high-performance software solutions with robust SQL database design and seamless machine learning integration.
- 📍 **Based In:** Kerala, India.

---

## 🛠️ Technical Skills

| Domain | Technologies & Frameworks |
| :--- | :--- |
| **Programming Languages** | `Python`, `JavaScript`, `SQL`, `HTML5`, `CSS3` |
| **Backend & APIs** | `Django`, `Django REST Framework (DRF)`, `Django ORM`, `REST APIs` |
| **Databases** | `MySQL`, `SQLite`, `Database Indexing & Optimization` |
| **AI & Machine Learning** | `NLP`, `IndicBERT / MuRIL`, `Scikit-learn`, `NumPy`, `Pandas` |
| **Data Pipelines & Tools** | `Apache Airflow (ETL)`, `Docker`, `Docker Compose`, `Git`, `GitHub`, `Postman` |
| **Frontend Integration** | `React.js`, `Chart.js` |
| **Core Computer Science** | `Object-Oriented Programming (OOP)`, `DSA Fundamentals`, `CRUD Architecture` |

---

## 🚀 Featured Projects

### 🛡️ 1. [Smart Shield — AI-Driven Detection of Cyberbullying in Regional Languages](https://github.com/Shamilshiras)
> **Stack:** *Python, Django, NLP, IndicBERT/MuRIL, REST APIs*
- Developed a real-time AI-powered system to detect cyberbullying in regional (**Malayalam**) and code-mixed (**Manglish**) languages.
- Implemented a hybrid approach combining **Natural Language Processing (NLP)** and transformer classifiers (**IndicBERT/MuRIL**) to decipher slang, nuances, and malicious intent.
- Built a **real-time polite rephrasing engine** that suggests constructive alternatives before transmission.
- Engineered a modular **Django backend** with feedback loops and an Admin Module for continuous lexicon updates.

### 📊 2. [SkillSight — Automated Job Market Pipeline & Dashboard](https://github.com/Shamilshiras)
> **Stack:** *Python, Apache Airflow, Pandas, Docker, MySQL, REST APIs*
- Built a fault-tolerant daily **ETL pipeline in Apache Airflow** featuring automated retries and fallback datasets to ingest tech market postings.
- Parsed and categorized skill taxonomies from thousands of job descriptions using **Pandas** and custom regex rules.
- Optimized **MySQL database queries to under 1.5s** via precomputed aggregation tables and composite indexing.
- Containerized the full-stack infrastructure with **Docker & Docker Compose** and exposed analytics via REST APIs.

### 💳 3. [SpendWise — Personal Expense Tracker Web App](https://github.com/Shamilshiras)
> **Stack:** *Python, Django, MySQL, JavaScript, Chart.js*
- Full-featured expense management application with complete **CRUD operations**.
- Interactive dashboard visualizing daily, weekly, and monthly spending summaries via **Chart.js**.
- Implemented responsive category and date-range filtering, multi-column sorting, and pagination for efficient record navigation.

---

## 📜 Certifications
- 🏅 **Qualcomm AI Upskilling Program (2025)** — *Qualcomm Academy*  
  *Machine learning fundamentals, neural network concepts, and practical edge AI applications.*
- 🐍 **Python Programming Masterclass (2025)** — *Udemy*  
  *Python 3 architecture, Object-Oriented Programming (OOP), GUI development, and relational database integration.*

---

## 📬 Get in Touch
- 📧 **Email:** [shamilshiras8262@gmail.com](mailto:shamilshiras8262@gmail.com)
- 💼 **LinkedIn:** [linkedin.com/in/shamilshiras](https://linkedin.com/in/shamilshiras)
- 🐙 **GitHub:** [github.com/Shamilshiras](https://github.com/Shamilshiras)
- 📱 **Phone:** +91-9526448262
"""

    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()

        if SECTION_START_MARKER in content and SECTION_END_MARKER in content:
            # Replace existing section between markers
            start_idx = content.find(SECTION_START_MARKER)
            end_idx = content.find(SECTION_END_MARKER) + len(SECTION_END_MARKER)
            new_content = content[:start_idx] + block + content[end_idx:]
        else:
            new_content = block + "\n" + resume_sections
    else:
        new_content = block + "\n" + resume_sections

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"✓ Injected profile cards and contribution graph into {readme_path}")

def main():
    parser = argparse.ArgumentParser(description="Generate high-end animated GitHub Profile SVGs and README.")
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

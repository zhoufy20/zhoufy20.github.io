from pathlib import Path
import re
import sys

root = Path(__file__).resolve().parents[1]
nav = (root / "_data/navigation.yml").read_text(encoding="utf-8")
masthead = (root / "_includes/masthead.html").read_text(encoding="utf-8")
about = (root / "_pages/about.md").read_text(encoding="utf-8")

expected = [
    "about-me",
    "news",
    "publications",
    "honors-and-awards",
    "educations",
    "invited-talks",
    "internships",
]

failures = []

if re.search(r'url:\s*["\']?/#', nav):
    failures.append("navigation.yml still contains root-path /# links")

for anchor in expected[1:]:
    if f'url: "#{anchor}"' not in nav and f"url: '#{anchor}'" not in nav:
        failures.append(f"navigation.yml missing pure fragment #{anchor}")

if '{{ domain }}{{ link.url }}' in masthead:
    failures.append("masthead still prefixes navigation fragments with domain")
if 'href="{{ link.url }}"' not in masthead:
    failures.append("masthead does not render navigation href directly from link.url")

for anchor in expected:
    patterns = [
        f"id='{anchor}'",
        f'id="{anchor}"',
    ]
    if not any(p in about for p in patterns):
        failures.append(f"about.md missing explicit anchor id={anchor}")

if failures:
    print("Single-page navigation validation FAILED:")
    for item in failures:
        print(f"- {item}")
    sys.exit(1)

print("Single-page navigation validation passed.")

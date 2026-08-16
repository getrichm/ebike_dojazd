#!/usr/bin/env python3
"""
bump_version.py — automatické zvýšenie verzie index.html
Použitie: python3 bump_version.py [index.html]

Formát verzie: 2.1.x.y
  - y ide 0–9, potom x+1 a y=0
  - x ide 0–9, potom vypíše upozornenie (major/minor treba zmeniť ručne)
"""

import re, sys, datetime

FILE = sys.argv[1] if len(sys.argv) > 1 else "index.html"

with open(FILE, encoding="utf-8") as f:
    src = f.read()

# nájdi aktuálnu verziu
m = re.search(r'Verzia (\d+)\.(\d+)\.(\d+)\.(\d+)', src)
if not m:
    # skús formát bez štvrtého čísla (napr. 2.1.1)
    m = re.search(r'Verzia (\d+)\.(\d+)\.(\d+)', src)
    if not m:
        print("CHYBA: verzia sa nenašla v súbore.")
        sys.exit(1)
    major, minor, x, y = int(m[1]), int(m[2]), int(m[3]), 0
    old_str = m.group(0)
else:
    major, minor, x, y = int(m[1]), int(m[2]), int(m[3]), int(m[4])
    old_str = m.group(0)

# zvýš y; ak presiahne 9, presuň na x
y += 1
if y > 9:
    y = 0
    x += 1
if x > 9:
    print(f"UPOZORNENIE: x dosiahol 10 — zmeňte major/minor verziu ručne.")
    x = 9  # drž na 9 ako krajná poistka

today = datetime.date.today()
MESIAC = ["januára","februára","marca","apríla","mája","júna",
          "júla","augusta","septembra","októbra","novembra","decembra"]
date_sk = f"{today.day}. {MESIAC[today.month-1]} {today.year}"

new_ver = f"{major}.{minor}.{x}.{y}"
new_str = f"Verzia {new_ver}"

src = src.replace(old_str, new_str, 1)

# aktualizuj aj dátum v riadku s verziou
src = re.sub(
    r'(Verzia \d+\.\d+\.\d+\.\d+\s*&nbsp;·&nbsp;\s*)[\d]+\. \w+ \d{4}',
    r'\g<1>' + date_sk,
    src
)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(src)

print(f"✓  {FILE}  {old_str}  →  {new_str}  ({date_sk})")

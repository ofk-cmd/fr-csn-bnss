#!/usr/bin/env python3
"""Sync FairPari bonus amounts from official site (fairpari.com/uz, scraped 2026-06-18)."""
import re
from pathlib import Path

SITES = [
    Path('/Users/vv/Desktop/fairpari-casino-bonus'),
    Path('/Users/vv/Desktop/fairpari-casino-bonuses'),
    Path('/Users/vv/Desktop/casino-bonuses-uz'),
]

# Order matters: longer/more specific first
REPLACEMENTS = [
    # Casino welcome — full forms
    ('19 500 000 UZS + 150 FS', '20 200 000 UZS + 150 FS'),
    ('19 500 000 + 150 FS', '20 200 000 + 150 FS'),
    ('19 500 000 UZS va 150 frispin', '20 200 000 UZS va 150 frispin'),
    ('19 500 000 UZS va 150 frispin', '20 200 000 UZS va 150 frispin'),
    ('19 500 000 UZS', '20 200 000 UZS'),
    ('19,500,000 UZS + 150 FS', '20,200,000 UZS + 150 FS'),
    ('19,500,000 UZS', '20,200,000 UZS'),
    ('19,5 mln UZS + 150 frispin', '20,2 mln UZS + 150 frispin'),
    ('19,5 mln UZS + 150 FS', '20,2 mln UZS + 150 FS'),
    ('19.5 mln UZS + 150 frispin', '20.2 mln UZS + 150 frispin'),
    ('19.5 mln UZS + 150 FS', '20.2 mln UZS + 150 FS'),
    ('19,5 млн UZS + 150 FS', '20,2 млн UZS + 150 FS'),
    ('19,5 млн UZS + 150 фриспинов', '20,2 млн UZS + 150 фриспинов'),
    ('19,5 млн UZS', '20,2 млн UZS'),
    ('19.5M UZS + 150 FS', '20.2M UZS + 150 FS'),
    ('19.5M+150 FS', '20.2M+150 FS'),
    ('19.5M UZS', '20.2M UZS'),
    ('19.5M', '20.2M'),
    ('19,5M UZS + 150 FS', '20,2M UZS + 150 FS'),
    ('19,5M UZS', '20,2M UZS'),
    ('19,5M', '20,2M'),
    ('19.5m UZS', '20.2m UZS'),
    ('до 19 500 000 UZS + 150 FS', 'до 20 200 000 UZS + 150 FS'),
    ('до 19,5 млн UZS + 150 FS', 'до 20,2 млн UZS + 150 FS'),
    ('пакет 19 500 000 UZS + 150 FS', 'пакет 20 200 000 UZS + 150 FS'),
    ('пакет 19,5 млн UZS + 150 FS', 'пакет 20,2 млн UZS + 150 FS'),
    ('Jami paket 19.5M UZS + 150 FS', 'Jami paket 20.2M UZS + 150 FS'),
    ('Итого пакет 19.5M UZS + 150 FS', 'Итого пакет 20.2M UZS + 150 FS'),
    ('Welcome 19,5M UZS + 150 FS', 'Welcome 20,2M UZS + 150 FS'),
    ('welcome 19.5M UZS + 150 FS', 'welcome 20.2M UZS + 150 FS'),
    ('welcome 19,5 млн UZS + 150 FS', 'welcome 20,2 млн UZS + 150 FS'),
    ('welcome 19,5M UZS + 150 FS', 'welcome 20,2M UZS + 150 FS'),
    ('Kazino 19.5M+150 FS', 'Kazino 20.2M+150 FS'),
    ('Казино 19.5M+150 FS', 'Казино 20.2M+150 FS'),
    ('kazino 19.5M+150 FS', 'kazino 20.2M+150 FS'),
    ('19.5M UZS + 150 FS ni', '20.2M UZS + 150 FS ni'),
    ('19.5 mln UZS + 150 FS', '20.2 mln UZS + 150 FS'),
    ('19,5 mln UZS + 150 frispin', '20,2 mln UZS + 150 frispin'),
    ('#1 — 19 500 000 UZS + 150 FS', '#1 — 20 200 000 UZS + 150 FS'),
    ('19 500 000 UZS + 150 frispin', '20 200 000 UZS + 150 frispin'),
    ('19.5M UZS + 150 FS (4 dep.)', '20.2M UZS + 150 FS (4 dep.)'),
    ('FairPari 19.5M UZS + 150 FS', 'FairPari 20.2M UZS + 150 FS'),
    ('FairPari 19,5 млн UZS + 150 FS', 'FairPari 20,2 млн UZS + 150 FS'),
    ('FairPari: 19.5M UZS + 150 FS', 'FairPari: 20.2M UZS + 150 FS'),
    ('FairPari: 19 500 000 UZS + 150 FS', 'FairPari: 20 200 000 UZS + 150 FS'),
    ('19 500 000 UZS + 150 FS paketi', '20 200 000 UZS + 150 FS paketi'),
    ('19.5M UZS + 150 FS tuzilmasi', '20.2M UZS + 150 FS tuzilmasi'),
    ('FairPari da 19 500 000 UZS + 150 FS', 'FairPari da 20 200 000 UZS + 150 FS'),
    ('19,5 mln UZS va 150 FS', '20,2 mln UZS va 150 FS'),
    ('19.5 mln UZS va 150 FS', '20.2 mln UZS va 150 FS'),
    ('19,5 млн UZS и 150 FS', '20,2 млн UZS и 150 FS'),
    ('19,5 млн UZS и 150 фриспин', '20,2 млн UZS и 150 фриспин'),
    ('19,5 млн UZS и 150 FS', '20,2 млн UZS и 150 FS'),
    ('19,5 mln', '20,2 mln'),
    ('19.5 mln', '20.2 mln'),
    # Sport welcome
    ('1 300 000 UZS gacha', '1 400 000 UZS gacha'),
    ('1 300 000 UZS', '1 400 000 UZS'),
    ('1,300,000 UZS', '1,400,000 UZS'),
    ('1.3M UZS', '1.4M UZS'),
    ('1,3M UZS', '1,4M UZS'),
    ('1.3M', '1.4M'),
    ('1,3M', '1,4M'),
    ('~1.3M UZS', '~1.4M UZS'),
    ('sport 1.3M', 'sport 1.4M'),
    ('sport ~1.3M UZS', 'sport ~1.4M UZS'),
    ('sport 1.3M —', 'sport 1.4M —'),
    ('Спорт 1,3M UZS', 'Спорт 1,4M UZS'),
    ('спорт 1.3M', 'спорт 1.4M'),
    ('sport 1.3M yoki', 'sport 1.4M yoki'),
    ('sport ~1.3M', 'sport ~1.4M'),
    ('1.3M UZS gacha', '1.4M UZS gacha'),
    ('1 300 000 UZS gacha', '1 400 000 UZS gacha'),
    ('1 300 000 gacha', '1 400 000 gacha'),
    ('до 1,3 млн UZS', 'до 1,4 млн UZS'),
    ('1,3 млн UZS', '1,4 млн UZS'),
]

SKIP_DIRS = {'.git', 'node_modules', 'scripts'}

def apply(text):
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    return text

def main():
    changed = []
    for site in SITES:
        for p in site.rglob('*'):
            if not p.is_file():
                continue
            if any(s in p.parts for s in SKIP_DIRS):
                continue
            if p.suffix not in {'.html', '.json', '.md', '.py', '.xml', '.js'}:
                continue
            try:
                old = p.read_text(encoding='utf-8')
            except (UnicodeDecodeError, IsADirectoryError):
                continue
            new = apply(old)
            if new != old:
                p.write_text(new, encoding='utf-8')
                changed.append(str(p.relative_to(site)))
    print(f'Updated {len(changed)} files')
    for c in changed[:30]:
        print(' ', c)
    if len(changed) > 30:
        print(f'  ... and {len(changed)-30} more')

    # verify no stale casino amounts left
    stale_pat = re.compile(r'19[,. ]?5\s*(млн|mln|M|m)?\s*UZS|19\s*500\s*000|19500000', re.I)
    leftovers = []
    for site in SITES:
        for p in site.rglob('*.html'):
            if '.git' in str(p):
                continue
            t = p.read_text(encoding='utf-8')
            if stale_pat.search(t):
                leftovers.append(str(p))
    print('Stale 19.5M references:', len(leftovers))
    for x in leftovers[:15]:
        print(' ', x)

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Restore Latin URL slugs corrupted by phrase replacement."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FIXES = [
    # cyrillic in paths
    ('skaчат', 'skachat'),
    ('промокод', 'promokod'),
    ('бездепозитный-bonus', 'bonus-bez-depozita'),
    ('бездепозитный', 'bonus-bez-depozita'),
    ('лицензия', 'litsenziya'),
    ('платёж', 'tolov'),
    ('использование-условия', 'foydalanish-shartlari'),
    ('конфиденциальность-политика', 'maxfiylik-siyosati'),
    ('cookie-политика', 'cookie-siyosati'),
    ('sport-бонусыi', 'sport-bonuslari'),
    ('sport-бонусы', 'sport-bonuslari'),
    ('bonus-bez-депозитa', 'bonus-bez-depozita'),
    ('pul-вывод', 'pul-yechish'),
    ('верификация', 'registratsiya'),
    ('hero-banner-платёж', 'hero-banner-tolov'),
    ('hero-banner-лицензия', 'hero-banner-litsenziya'),
    ('data-слот', 'data-slot'),
    # en paths if corrupted
    ('../skaчат/', '../app/'),
]

# hreflang uz paths must stay latin
HREFLANG_UZ = {
    'https://fairpari-casino-bonuses.com/использование-условия/': 'https://fairpari-casino-bonuses.com/foydalanish-shartlari/',
    'https://fairpari-casino-bonuses.com/конфиденциальность-политика/': 'https://fairpari-casino-bonuses.com/maxfiylik-siyosati/',
    'https://fairpari-casino-bonuses.com/cookie-политика/': 'https://fairpari-casino-bonuses.com/cookie-siyosati/',
    'https://fairpari-casino-bonuses.com/sport-бонусыi/': 'https://fairpari-casino-bonuses.com/sport-bonuslari/',
    'https://fairpari-casino-bonuses.com/sport-бонусы/': 'https://fairpari-casino-bonuses.com/sport-bonuslari/',
    'https://fairpari-casino-bonuses.com/платёж/': 'https://fairpari-casino-bonuses.com/tolov/',
    'https://fairpari-casino-bonuses.com/лицензия/': 'https://fairpari-casino-bonuses.com/litsenziya/',
    'https://fairpari-casino-bonuses.com/ru/промокод/': 'https://fairpari-casino-bonuses.com/ru/promokod/',
    'https://fairpari-casino-bonuses.com/ru/лицензия/': 'https://fairpari-casino-bonuses.com/ru/litsenziya/',
    'https://fairpari-casino-bonuses.com/ru/skaчат/': 'https://fairpari-casino-bonuses.com/ru/skachat/',
}

def fix(html):
    for a, b in FIXES:
        html = html.replace(a, b)
    for a, b in HREFLANG_UZ.items():
        html = html.replace(a, b)
    html = html.replace('responsible-gambling/', 'responsible-gaming/')
    return html

if __name__ == '__main__':
    n = 0
    for p in list((ROOT/'ru').rglob('*.html')) + list((ROOT/'en').rglob('*.html')):
        old = p.read_text(encoding='utf-8')
        new = fix(old)
        if new != old:
            p.write_text(new, encoding='utf-8')
            n += 1
    print(f'Fixed {n} files')

#!/usr/bin/env python3
"""Remove domains from H2; replace with LSI-rich headings per page context."""
import re
from pathlib import Path

SITES = [
    Path('/Users/vv/Desktop/fairpari-casino-bonus'),
    Path('/Users/vv/Desktop/fairpari-casino-bonuses'),
    Path('/Users/vv/Desktop/casino-bonuses-uz'),
]

DOMAINS = (
    'fairpari-casino-bonus.com',
    'fairpari-casino-bonuses.com',
    'casino-bonuses-uz.com',
)

# Global exact H2 text replacements (any site)
GLOBAL_H2 = {
    'fairpari-casino-bonuses.com — welcome, FS va keshbek': None,  # page-specific below
    'fairpari-casino-bonuses.com — asosiy raqamlar va aksiyalar': 'FairPari bonus ko\'rsatkichlari — UZS, slotlar va sport liniyasi',
    'fairpari-casino-bonuses.com afzalliklari — O\'zbekiston uchun': 'Bonus afzalliklari — Humo, Click, Payme va mobil faollashtirish',
    'fairpari-casino-bonuses.com xavfsizligi va 18+': 'FairPari bonus xavfsizligi — SSL, litsenziya va mas\'uliyatli o\'yin 18+',
    'fairpari-casino-bonuses.com safeligi and 18+': 'FairPari bonus safety — license, KYC and responsible play 18+',
    "Bog'liq kazino bo'limlari": "FairPari bonus bo'limlari — promo, welcome va wagering",
    "Bog'liq casino sections": 'Related FairPari bonus topics — promo, welcome and wagering',
    'Ishonch ko\'rsatkichlari': 'FairPari ishonchlilik — litsenziya, SSL va 18+',
    'Trust indicators': 'FairPari trust signals — license, SSL and 18+',
    'Welcome bonus kalkulyatori': 'Welcome bonus kalkulyatori — 4 depozit va 150 FS',
}

# block9.title per relative path (UZ)
UZ_BLOCK9 = {
    'index.html': 'FairPari bonuslari hub — welcome 20.2M UZS, FS va keshbek',
    'kazino-bonuslari/index.html': 'Kazino welcome paketi — 20.2M UZS + 150 FS, wagering ×35',
    'promo-kod/index.html': 'Promo kod fa_1635 — bonus va depozit faollashtirish',
    'bonus-kodi/index.html': 'Bonus kodi fa_1635 — ro\'yxat, kassa va wagering',
    'free-spins/index.html': 'Free spins 150 FS — qoidalar, slotlar va muddat',
    'depozitsiz-bonus/index.html': 'Depozitsiz bonus — rasmiy holat va minimal depozit yo\'li',
    'royxatdan-otish/index.html': 'Registratsiya va welcome — 4 depozit paketi UZS',
    'faq/index.html': 'Bonus FAQ — promo kod, wagering va yechish',
    'mobil/index.html': 'Mobil bonus — APK, PWA va ilovada 50 FS',
    'sport-bonuslari/index.html': 'Sport welcome bonus — 1.4M UZS va ekspress ×5',
    'kirish/index.html': 'Kirish va bonus profili — login, UZS va PROMO',
    'tolov/index.html': 'Bonus depoziti — Humo, Click, Payme va yechish',
}

RU_BLOCK9 = {
    'ru/index.html': 'Бонусы казино FairPari — welcome 20,2 млн UZS, FS и кешбэк',
    'ru/bonusy-kazino/index.html': 'Казино welcome — 20,2 млн UZS + 150 FS, вейджер ×35',
    'ru/promokod/index.html': 'Промокод fa_1635 — активация бонуса и депозита',
    'ru/bonus-kod/index.html': 'Бонус-код fa_1635 — регистрация, касса и отыгрыш',
    'ru/free-spins/index.html': 'Фриспины 150 FS — правила, слоты и срок',
    'ru/bonus-bez-depozita/index.html': 'Бездепозитный бонус — официальный статус и альтернатива',
    'ru/registratsiya/index.html': 'Регистрация и welcome — пакет на 4 депозита UZS',
    'ru/faq/index.html': 'FAQ по бонусам — промокод, вейджер и вывод',
    'ru/skachat/index.html': 'Мобильный бонус — APK, PWA и 50 FS в приложении',
    'ru/sport-bonusy/index.html': 'Спорт welcome — до 1,4 млн UZS и экспресс ×5',
    'ru/vhod/index.html': 'Вход и бонус-профиль — login, UZS и PROMO',
    'ru/oplata/index.html': 'Депозит бонуса — Humo, Click, Payme и вывод',
}

EN_BLOCK9 = {
    'en/index.html': 'FairPari casino bonuses hub — welcome 20.2M UZS, FS and cashback',
    'en/casino-bonuses/index.html': 'Casino welcome package — 20.2M UZS + 150 FS, wagering ×35',
    'en/promo-code/index.html': 'Promo code fa_1635 — bonus and deposit activation',
    'en/bonus-code/index.html': 'Bonus code fa_1635 — registration, cashier and wagering',
    'en/free-spins/index.html': 'Free spins 150 FS — rules, slots and deadline',
    'en/no-deposit-bonus/index.html': 'No deposit bonus — official status and min-deposit path',
    'en/registration/index.html': 'Registration and welcome — 4-deposit UZS package',
    'en/faq/index.html': 'Bonus FAQ — promo code, wagering and withdrawal',
    'en/app/index.html': 'Mobile bonus — APK, PWA and 50 FS in-app',
    'en/sports-bonuses/index.html': 'Sports welcome bonus — up to 1.4M UZS, express ×5',
    'en/login/index.html': 'Login and bonus profile — UZS account and PROMO',
    'en/payments/index.html': 'Bonus deposit — Humo, Click, Payme and withdrawal',
}

RU_RELATED_H2 = 'Связанные разделы бонусов — promo, welcome и вейджер'


def strip_domain_from_h2_inner(inner: str) -> str:
    low = inner.lower()
    for d in DOMAINS:
        if d in low:
            # remove domain and leading punctuation
            inner = re.sub(re.escape(d), '', inner, flags=re.I)
            inner = re.sub(r'^\s*[—–-]\s*', '', inner.strip())
            inner = re.sub(r'^\s+', '', inner)
            if inner:
                return f'FairPari bonus — {inner[0].upper()}{inner[1:]}' if not inner.lower().startswith('fairpari') else inner
            return 'FairPari bonus — welcome, FS va keshbek'
    return inner


def fix_h2_content(inner: str, relpath: str) -> str:
    plain = re.sub(r'<[^>]+>', '', inner).strip()

    for mapping in (UZ_BLOCK9, RU_BLOCK9, EN_BLOCK9):
        if relpath in mapping:
            domain_block9 = 'fairpari-casino-bonuses.com — welcome, FS va keshbek'
            generic_ru = 'Бонусы казино FairPari — пакет, FS и кешбэк'
            generic_en = 'FairPari casino bonuses — package, free spins and cashback'
            if plain in (domain_block9, generic_ru, generic_en):
                return mapping[relpath]

    if plain in GLOBAL_H2:
        repl = GLOBAL_H2[plain]
        if repl:
            if relpath.startswith('ru/') and repl == "FairPari bonus bo'limlari — promo, welcome va wagering":
                return RU_RELATED_H2
            return repl

    if relpath.startswith('ru/') and plain == "Bog'liq kazino bo'limlari":
        return RU_RELATED_H2

    if any(d in plain.lower() for d in DOMAINS):
        return strip_domain_from_h2_inner(plain)
    return plain


def patch_file(path: Path, site: Path) -> int:
    relpath = str(path.relative_to(site)).replace('\\', '/')
    text = path.read_text(encoding='utf-8')
    n = 0

    def repl(m):
        nonlocal n
        tag_open, inner, tag_close = m.group(1), m.group(2), m.group(3)
        plain = re.sub(r'<[^>]+>', '', inner).strip()
        new_plain = fix_h2_content(inner, relpath)
        if new_plain != plain:
            n += 1
            return f'{tag_open}{new_plain}{tag_close}'
        return m.group(0)

    new_text = re.sub(r'(<h2\b[^>]*>)(.*?)(</h2>)', repl, text, flags=re.I | re.S)
    if n:
        path.write_text(new_text, encoding='utf-8')
    return n


def main():
    total = 0
    leftovers = []
    for site in SITES:
        site_n = 0
        for html in site.rglob('*.html'):
            site_n += patch_file(html, site)
        total += site_n
        print(f'{site.name}: {site_n} H2 updated')

    for site in SITES:
        for html in site.rglob('*.html'):
            text = html.read_text(encoding='utf-8')
            for m in re.finditer(r'<h2\b[^>]*>(.*?)</h2>', text, re.I | re.S):
                plain = re.sub(r'<[^>]+>', '', m.group(1)).strip()
                if any(d in plain.lower() for d in DOMAINS):
                    leftovers.append((str(html.relative_to(site)), plain))

    print(f'Total: {total} H2 updated')
    print(f'Leftover domain in H2: {len(leftovers)}')
    for f, h in leftovers:
        print(f'  {f}: {h}')


if __name__ == '__main__':
    main()

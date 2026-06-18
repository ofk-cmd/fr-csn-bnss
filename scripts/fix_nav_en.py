#!/usr/bin/env python3
"""Fix EN nav/footer corruption and legal page breadcrumbs."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

EN_FIX = [
    ('Mobileeee menu', 'Mobile menu'),
    ('Mobileee app', 'Mobile app'),
    ('Mobileee casino', 'Mobile casino'),
    ('Mobileee login', 'Mobile login'),
    ('Mobileee promo', 'Mobile promo'),
    ('Mobileee live', 'Mobile live'),
    ('Mobileee slot', 'Mobile slots'),
    ('Mobileee payments', 'Mobile payments'),
    ('Mobileee kassa', 'Mobile cashier'),
    ('Mobileee zerkalo', 'Mobile mirror'),
    ('Mobileee guide', 'Mobile guide'),
    ('Mobileee funksiyalar', 'Mobile features'),
    ('Mobileee safelik', 'Mobile security'),
    ('Mobileee versiya', 'Mobile version'),
    ('Mobileee', 'Mobile app'),
    ('<h4>Yana</h4>', '<h4>More</h4>'),
    ('Securelik', 'Security'),
    ('deadlinelar', 'deadlines'),
    ('Yangi account', 'New account'),
    ('Sign up 4 usul', 'Sign up — 4 methods'),
    ('APK sessiya', 'APK session'),
    ('4 stepsli welcome', '4-stage welcome'),
    ('Kod enter', 'Enter code'),
    ('Frispin slot', 'Free spin slots'),
    ('Kod appda', 'Code in app'),
    ('Provayder turnirlari', 'Provider tournaments'),
    ('iOS PWA o\'rnatish', 'iOS PWA install'),
    ('Tizim talablari', 'System requirements'),
    ('Biometriya and 2FA', 'Biometrics and 2FA'),
    ('Working address', 'Working mirror URL'),
    ('and and more', 'and more'),
    ('appda', 'in the app'),
    ('kassa', 'cashier'),
    ('zerkalo', 'mirror'),
]

RU_FIX = [
    ('<h4>Ещё</h4>', '<h4>Ещё</h4>'),  # keep
    ('Mobileee', 'Мобильное'),
]

LEGAL_BREADCRUMB = {
    'en/responsible-gaming/index.html': 'Responsible gaming',
    'en/privacy-policy/index.html': 'Privacy policy',
    'en/cookie-policy/index.html': 'Cookie policy',
    'en/terms-of-use/index.html': 'Terms of use',
    'ru/otvetstvennaya-igra/index.html': 'Ответственная игра',
    'ru/politika-konfidentsialnosti/index.html': 'Политика конфиденциальности',
    'ru/politika-cookie/index.html': 'Политика cookie',
    'ru/usloviya-ispolzovaniya/index.html': 'Условия использования',
}

FOOTER_LEGAL = {
    'en/responsible-gaming/index.html': [
        ('<a href="../responsible-gaming/">Privacy policy</a>', '<a href="../privacy-policy/">Privacy policy</a>'),
    ],
}

if __name__ == '__main__':
    for p in (ROOT/'en').rglob('*.html'):
        h = p.read_text(encoding='utf-8')
        for a, b in EN_FIX:
            h = h.replace(a, b)
        rel = str(p.relative_to(ROOT))
        if rel in LEGAL_BREADCRUMB:
            label = LEGAL_BREADCRUMB[rel]
            import re
            h = re.sub(r'(<nav class="breadcrumbs"[^>]*>.*?</span>)', lambda m: re.sub(r'<span>[^<]+</span>', f'<span>{label}</span>', m.group(1), count=1), h, count=1, flags=re.S)
        if rel in FOOTER_LEGAL:
            for a, b in FOOTER_LEGAL[rel]:
                h = h.replace(a, b)
        p.write_text(h, encoding='utf-8')
    for p in (ROOT/'ru').rglob('*.html'):
        h = p.read_text(encoding='utf-8')
        for a, b in RU_FIX:
            h = h.replace(a, b)
        rel = str(p.relative_to(ROOT))
        if rel in LEGAL_BREADCRUMB:
            label = LEGAL_BREADCRUMB[rel]
            import re
            h = re.sub(r'(<nav class="breadcrumbs"[^>]*>.*?</span>)', lambda m: re.sub(r'<span>[^<]+</span>', f'<span>{label}</span>', m.group(1), count=1), h, count=1, flags=re.S)
        p.write_text(h, encoding='utf-8')
    print('Nav/footer fix done')

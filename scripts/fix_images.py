#!/usr/bin/env python3
"""Fix broken image refs: map missing files to existing assets, fix Cyrillic paths."""
import re
from pathlib import Path
from typing import Optional

SITES = [
    Path('/Users/vv/Desktop/fairpari-casino-bonus'),
    Path('/Users/vv/Desktop/fairpari-casino-bonuses'),
    Path('/Users/vv/Desktop/casino-bonuses-uz'),
]

IMG_EXT = {'.webp', '.svg', '.png', '.jpg', '.jpeg', '.gif'}

# Cyrillic / corrupt filename → existing asset (site-relative)
EXACT_REPLACEMENTS = {
    'assets/banners/hero-banner-kazino-бонусы.webp': 'assets/banners/casino-bonus.webp',
    'assets/banners/hero-banner-регистрация-otish.webp': 'assets/registration-illustration.webp',
    'assets/banners/kazino-бонусы-s05.webp': 'assets/banners/casino-bonus.webp',
    'fairpari/assets/logo-fairpari.svg': 'assets/logo-fairpari.svg',
    'fairpari/assets/hero-bonus-light.webp': 'assets/hero-bonus-light.webp',
}

CYRILLIC_IN_PATH = re.compile(r'[а-яА-ЯёЁіІ]')


def existing_files(site: Path) -> set[str]:
    return {
        p.relative_to(site).as_posix()
        for p in site.rglob('*')
        if p.is_file() and p.suffix.lower() in IMG_EXT
    }


def fallback_asset(path: str) -> str:
    """Pick best existing fallback for a missing asset path."""
    low = path.lower()
    if 'logo-fairpari' in low:
        return 'assets/logo-fairpari.svg'
    if 'hero-bonus-light' in low:
        return 'assets/hero-bonus-light.webp'
    if 'favicon' in low or 'apple-touch' in low:
        return 'assets/favicon.svg'
    if 'hero-banner' in low or '/hero-' in low:
        if any(x in low for x in ('sport', 'express', 'stavka')):
            return 'assets/banners/sports-bonus.webp'
        if any(x in low for x in ('mobil', 'app', 'skachat', 'apk')):
            return 'assets/app-install-illustration.webp'
        if any(x in low for x in ('promo', 'kod', 'code')):
            return 'assets/promo-code-illustration.webp'
        if any(x in low for x in ('royxat', 'registr', 'registration', 'otish')):
            return 'assets/registration-illustration.webp'
        if any(x in low for x in ('tolov', 'payment', 'oplata', 'pul')):
            return 'assets/banners/payments-uz.webp'
        if any(x in low for x in ('litsenz', 'license', 'security')):
            return 'assets/banners/security.webp'
        if any(x in low for x in ('legal', 'privacy', 'cookie', 'terms')):
            return 'assets/banners/legal-privacy.webp'
        if any(x in low for x in ('faq', 'kirish', 'login', 'vhod')):
            return 'assets/banners/hero-banner-home.webp'
        if any(x in low for x in ('casino', 'kazino', 'bonus', 'slot', 'vip', 'cashback')):
            return 'assets/banners/casino-bonus.webp'
        return 'assets/banners/hero-banner-home.webp'
    if any(x in low for x in ('express-win', 'sports-bonus', 'sport')):
        return 'assets/banners/sports-bonus.webp'
    if any(x in low for x in ('mobile-app', 'app-dual', 'app-install', 'mobil')):
        return 'assets/app-install-illustration.webp'
    if any(x in low for x in ('payments-uz', 'tolov', 'payment')):
        return 'assets/banners/payments-uz.webp'
    if any(x in low for x in ('wagering', 'vip-cashback')):
        return 'assets/banners/wagering-info.webp'
    if any(x in low for x in ('rating', 'top')):
        return 'assets/banners/rating-top.webp'
    if any(x in low for x in ('legal', 'privacy')):
        return 'assets/banners/legal-privacy.webp'
    if '/games/' in low:
        return 'assets/games/sweet-bonanza.webp'
    if '/screenshots/' in low:
        return 'assets/screenshots/20260520-135040-utc-fairpari.com-main.webp'
    # section banners *-sNN.webp
    if re.search(r'-[sS]\d+\.webp$', low) or '-s0' in low:
        if 'mobil' in low:
            return 'assets/app-install-illustration.webp'
        if 'sport' in low:
            return 'assets/banners/sports-bonus.webp'
        return 'assets/banners/casino-bonus.webp'
    return 'assets/banners/casino-bonus.webp'


def resolve_to_site_path(ref: str, html: Path, site: Path) -> Optional[str]:
    if ref.startswith('data:'):
        return None
    if ref.startswith('http'):
        for domain in ('fairpari-casino-bonus.com', 'fairpari-casino-bonuses.com', 'casino-bonuses-uz.com'):
            marker = f'{domain}/'
            if marker in ref:
                return ref.split(marker, 1)[1]
        return None
    if ref.startswith('/'):
        return ref.lstrip('/')
    p = (html.parent / ref).resolve()
    try:
        return p.relative_to(site.resolve()).as_posix()
    except ValueError:
        return None


def relpath_from_html(site_path: str, html: Path, site: Path) -> str:
    target = site / site_path
    rel = Path(os_relpath(target, html.parent))
    return rel.as_posix()


def os_relpath(target: Path, start: Path) -> str:
    import os
    return os.path.relpath(target, start)


def fix_ref(ref: str, html: Path, site: Path, existing: set[str]) -> str:
    site_path = resolve_to_site_path(ref, html, site)
    if not site_path:
        return ref

    # exact replacements (also partial URL paths)
    for old, new in EXACT_REPLACEMENTS.items():
        if site_path == old or site_path.endswith(old):
            site_path = new
            break

    if CYRILLIC_IN_PATH.search(site_path):
        site_path = fallback_asset(site_path)

    if site_path not in existing:
        site_path = fallback_asset(site_path)
        # ensure fallback exists
        if site_path not in existing:
            for candidate in (
                'assets/banners/casino-bonus.webp',
                'assets/banners/hero-banner-home.webp',
                'assets/hero-bonus-light.webp',
            ):
                if candidate in existing:
                    site_path = candidate
                    break

    if ref.startswith('http'):
        domain = ref.split('//', 1)[1].split('/', 1)[0]
        return f'https://{domain}/{site_path}'

    return relpath_from_html(site_path, html, site)


def patch_html(text: str, html: Path, site: Path, existing: set[str]) -> tuple[str, int]:
    changes = 0

    def replace_ref(ref: str) -> str:
        nonlocal changes
        new_ref = fix_ref(ref, html, site, existing)
        if new_ref != ref:
            changes += 1
        return new_ref

    pat = re.compile(
        r'((?:src|href|content)=["\'])([^"\']+\.(?:webp|svg|png|jpg|jpeg|gif))(["\'])',
        re.I,
    )

    def repl_attr(m):
        prefix, ref, suffix = m.group(1), m.group(2), m.group(3)
        return prefix + replace_ref(ref) + suffix

    text = pat.sub(repl_attr, text)

    # JSON-LD and inline absolute image URLs
    url_pat = re.compile(
        r'(https?://(?:fairpari-casino-bonus\.com|fairpari-casino-bonuses\.com|casino-bonuses-uz\.com)/[^"\s]+\.(?:webp|svg|png|jpg|jpeg|gif))',
        re.I,
    )

    def repl_url(m):
        return replace_ref(m.group(1))

    text = url_pat.sub(repl_url, text)
    return text, changes


def fix_favicon_ru_legal(site: Path) -> int:
    n = 0
    for html in (site / 'ru').glob('*.html'):
        text = html.read_text(encoding='utf-8')
        new = text.replace('href="assets/favicon', 'href="../assets/favicon')
        new = new.replace('href="assets/apple-touch', 'href="../assets/apple-touch')
        if new != text:
            html.write_text(new, encoding='utf-8')
            n += 1
    return n


def add_og_tags_casino_uz(site: Path) -> int:
  """Add og:image to pages missing social meta."""
  domain = 'https://casino-bonuses-uz.com'
  og_block = '''  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="Casino Bonuses UZ" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:url" content="{url}" />
  <meta property="og:image" content="{img}" />
  <meta property="og:image:alt" content="{alt}" />
  <meta property="og:locale" content="{locale}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{title}" />
  <meta name="twitter:description" content="{desc}" />
  <meta name="twitter:image" content="{img}" />
  <meta name="twitter:image:alt" content="{alt}" />
'''
  pages = {
    'index.html': {
      'title': "O'zbekistonda eng yaxshi kazino bonuslari — 2026 reyting",
      'desc': "Kazino bonuslari O'zbekiston 2026: TOP-5 reyting, welcome paketlar, wagering, Humo/Payme. FairPari #1 — 20.2M UZS + 150 FS.",
      'url': f'{domain}/',
      'img': f'{domain}/assets/hero-bonus-light.webp',
      'alt': "Kazino bonuslari O'zbekiston — reyting banneri",
      'locale': 'uz_UZ',
    },
    'ru/index.html': {
      'title': 'Лучшие бонусы казино Узбекистан — рейтинг 2026',
      'desc': 'Рейтинг казино-бонусов Узбекистан 2026: welcome-пакеты, wagering, Humo/Payme. FairPari #1.',
      'url': f'{domain}/ru/',
      'img': f'{domain}/assets/hero-bonus-light.webp',
      'alt': 'Бонусы казино Узбекистан — баннер рейтинга',
      'locale': 'ru_UZ',
    },
  }
  n = 0
  for rel, meta in pages.items():
    p = site / rel
    if not p.exists():
      continue
    text = p.read_text(encoding='utf-8')
    if 'og:image' in text:
      continue
    insert = og_block.format(**meta)
    marker = '<link rel="canonical"'
    if marker in text:
      text = text.replace(marker, insert + '  ' + marker, 1)
      p.write_text(text, encoding='utf-8')
      n += 1
  return n


def main():
    total = 0
    for site in SITES:
        existing = existing_files(site)
        site_changes = 0
        for html in site.rglob('*.html'):
            if '.git' in html.parts:
                continue
            text = html.read_text(encoding='utf-8')
            new, n = patch_html(text, html, site, existing)
            if n:
                html.write_text(new, encoding='utf-8')
                site_changes += n
        if site.name == 'fairpari-casino-bonus':
            fix_favicon_ru_legal(site)
        if site.name == 'casino-bonuses-uz':
            add_og_tags_casino_uz(site)
        print(f'{site.name}: {site_changes} image ref fixes')
        total += site_changes

    # verify
    for site in SITES:
        existing = existing_files(site)
        missing = []
        for html in site.rglob('*.html'):
            text = html.read_text(encoding='utf-8')
            for m in re.finditer(r'(?:src|href|content)=["\']([^"\']+\.(?:webp|svg|png|jpg|jpeg|gif))["\']', text, re.I):
                sp = resolve_to_site_path(m.group(1), html, site)
                if sp and sp not in existing and not sp.startswith('http'):
                    missing.append((sp, str(html.relative_to(site))))
        print(f'{site.name}: {len(missing)} missing after fix')
        for sp, f in missing[:8]:
            print(f'  {sp} <- {f}')


if __name__ == '__main__':
    main()

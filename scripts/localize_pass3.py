#!/usr/bin/env python3
"""Pass 3: fix broken URLs, replace mixed seo-expansion with clean RU/EN."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

GLOBAL_FIX = [
    ('responsible-gambling/', 'responsible-gaming/'),
    ('../вход/', '../vhod/'),
    ('../верификация/', '../registratsiya/'),
    ('../kazino-бонусы/', '../bonusy-kazino/'),
    ('sport-бонусы/', 'sport-bonuslari/'),
    ('использование-условия/', 'foydalanish-shartlari/'),
    ('hero-banner-вход.webp', 'hero-banner-kirish.webp'),
    ('вход-s', 'kirish-s'),
    ('../вход/', '../login/'),  # en after ru fix - order matters
]

EN_EXTRA_HREF = [
    ('../vhod/', '../login/'),
    ('../registratsiya/', '../registration/'),
    ('../bonusy-kazino/', '../casino-bonuses/'),
    ('../sport-bonusy/', '../sports-bonuses/'),
    ('../promokod/', '../promo-code/'),
    ('../bonus-bez-depozita/', '../no-deposit-bonus/'),
    ('../oplata/', '../payments/'),
    ('../skachat/', '../app/'),
    ('../litsenziya/', '../license/'),
]

def block_ru(slug):
    """Clean Russian seo-expansion blocks per page."""
    common = f'''<article class="seo-block seo-block--rich">
<h2 id="seo-block-1">Обзор бонусного портала</h2>
<p>fairpari-casino-bonuses.com — независимый каталог бонусов FairPari для Узбекистана. Мы не оператор: информация о welcome, фриспинах и спорт-акциях, промокоде <strong>fa_1635</strong> и правилах отыгрыша.</p>
</article>'''
    pages = {
        'index': common + '''<article class="seo-block seo-block--rich">
<h2 id="seo-block-2">Казино welcome 2026</h2>
<p>Пакет до <strong>20 200 000 UZS + 150 FS</strong> на четыре депозита, wagering ×35. Отдельно — <a class="text-link" href="bonusy-kazino/">спорт-бонус</a> с другими условиями.</p>
</article>
<article class="seo-block seo-block--rich">
<h2 id="seo-block-3">Платежи UZS</h2>
<p>Humo, Uzcard, Click, Payme и крипто. Депозит для активации бонуса — в разделе <a class="text-link" href="oplata/">оплата</a>.</p>
</article>''',
        'bonusy-kazino': '''<article class="seo-block seo-block--rich">
<h2 id="seo-block-1">Welcome казино — 4 этапа</h2>
<p>До <strong>20 200 000 UZS + 150 FS</strong> на первые четыре депозита. Wagering ×35, срок и список игр — в PROMO кабинета.</p>
</article>
<article class="seo-block seo-block--rich">
<h2 id="seo-block-2">Активация</h2>
<p>Промокод <strong><a class="text-link" href="../promokod/">fa_1635</a></strong> при <a class="text-link" href="../registratsiya/">регистрации</a> или в кассе. Без кода welcome может не начислиться.</p>
</article>''',
        'promokod': '''<article class="seo-block seo-block--rich">
<h2 id="seo-block-1">Промокод fa_1635</h2>
<p>Вводите при регистрации или в кассе до депозита. Код привязывает welcome к аккаунту.</p>
</article>
<article class="seo-block seo-block--rich">
<h2 id="seo-block-2">Частые ошибки</h2>
<p>Опечатка, просроченная акция, повторная активация на том же аккаунте — бонус не начисляется. Проверяйте раздел PROMO после <a class="text-link" href="../vhod/">входа</a>.</p>
</article>''',
        'registratsiya': '''<article class="seo-block seo-block--rich">
<h2 id="seo-block-1">Регистрация и бонус</h2>
<p>Email, телефон, соцсети или 1-click. Валюта UZS. Промокод <strong><a class="text-link" href="../promokod/">fa_1635</a></strong> — на этом шаге.</p>
</article>
<article class="seo-block seo-block--rich">
<h2 id="seo-block-2">После регистрации</h2>
<p>Подтвердите контакт, пройдите <a class="text-link" href="../registratsiya/">верификацию</a> перед выводом, сделайте депозит в <a class="text-link" href="../oplata/">кассе</a>.</p>
</article>''',
        'vhod': '''<article class="seo-block seo-block--rich">
<h2 id="seo-block-1">Вход в аккаунт</h2>
<p>Email или телефон + пароль. Восстановление пароля по SMS/email. Рекомендуем 2FA.</p>
</article>
<article class="seo-block seo-block--rich">
<h2 id="seo-block-2">Безопасность</h2>
<p>Только официальный домен fairpari.com/uz. Не сохраняйте пароль на общих устройствах. Прогресс бонуса — в PROMO после <a class="text-link" href="../vhod/">входа</a>.</p>
</article>
<article class="seo-block seo-block--rich">
<h2 id="seo-block-3">Мобильный вход</h2>
<p>Один логин на сайте и в <a class="text-link" href="../skachat/">приложении</a>. Баланс и бонусы синхронизируются.</p>
</article>''',
        'oplata': '''<article class="seo-block seo-block--rich">
<h2 id="seo-block-1">Депозит для бонуса</h2>
<p>Humo, Uzcard, Click, Payme, крипто. Минимум зависит от метода — проверьте кассу перед пополнением.</p>
</article>
<article class="seo-block seo-block--rich">
<h2 id="seo-block-2">Вывод</h2>
<p>KYC при первом выводе. Сроки 1–24 ч для карт UZS. Бонусный баланс отыгрывается до вывода.</p>
</article>''',
        'skachat': '''<article class="seo-block seo-block--rich">
<h2 id="seo-block-1">Android APK и iOS PWA</h2>
<p>Скачивайте только с fairpari.com/uz/mobile. В Google Play и App Store официального приложения нет.</p>
</article>
<article class="seo-block seo-block--rich">
<h2 id="seo-block-2">Бонус в приложении</h2>
<p>Тот же welcome и промокод <strong><a class="text-link" href="../promokod/">fa_1635</a></strong>. Один баланс UZS с сайтом.</p>
</article>''',
        'litsenziya': '''<article class="seo-block seo-block--rich">
<h2 id="seo-block-1">Лицензия оператора</h2>
<p>FairPari указывает номер <strong>OGL/2024/1143/0865</strong>. Портал бонусов — информационный, не оператор.</p>
</article>
<article class="seo-block seo-block--rich">
<h2 id="seo-block-2">KYC и безопасность</h2>
<p>Верификация перед выводом. SSL, ответственная игра 18+ — в <a class="text-link" href="../otvetstvennaya-igra/">отдельном разделе</a>.</p>
</article>''',
    }
    return pages.get(slug, common)

def block_en(slug):
    common = f'''<article class="seo-block seo-block--rich">
<h2 id="seo-block-1">Bonus portal overview</h2>
<p>fairpari-casino-bonuses.com is an independent FairPari bonus catalog for Uzbekistan. We are not the operator: welcome offers, free spins, sports promos, promo code <strong>fa_1635</strong> and wagering rules.</p>
</article>'''
    pages = {
        'index': common + '''<article class="seo-block seo-block--rich">
<h2 id="seo-block-2">Casino welcome 2026</h2>
<p>Up to <strong>20,200,000 UZS + 150 FS</strong> across four deposits, wagering ×35. Sports bonus has separate terms — see <a class="text-link" href="casino-bonuses/">casino bonuses</a>.</p>
</article>
<article class="seo-block seo-block--rich">
<h2 id="seo-block-3">UZS payments</h2>
<p>Humo, Uzcard, Click, Payme and crypto. Deposit to activate bonus — <a class="text-link" href="payments/">payments</a> page.</p>
</article>''',
        'casino-bonuses': '''<article class="seo-block seo-block--rich">
<h2 id="seo-block-1">Casino welcome — 4 stages</h2>
<p>Up to <strong>20,200,000 UZS + 150 FS</strong> on first four deposits. Wagering ×35; game list and deadline in PROMO.</p>
</article>
<article class="seo-block seo-block--rich">
<h2 id="seo-block-2">Activation</h2>
<p>Promo code <strong><a class="text-link" href="../promo-code/">fa_1635</a></strong> at <a class="text-link" href="../registration/">registration</a> or cashier. Without code welcome may not apply.</p>
</article>''',
        'promo-code': '''<article class="seo-block seo-block--rich">
<h2 id="seo-block-1">Promo code fa_1635</h2>
<p>Enter at signup or cashier before deposit. Code links welcome to your account.</p>
</article>
<article class="seo-block seo-block--rich">
<h2 id="seo-block-2">Common mistakes</h2>
<p>Typos, expired promo, duplicate activation — bonus won't credit. Check PROMO after <a class="text-link" href="../login/">login</a>.</p>
</article>''',
        'registration': '''<article class="seo-block seo-block--rich">
<h2 id="seo-block-1">Sign up and bonus</h2>
<p>Email, phone, social or 1-click. Currency UZS. Promo <strong><a class="text-link" href="../promo-code/">fa_1635</a></strong> at this step.</p>
</article>
<article class="seo-block seo-block--rich">
<h2 id="seo-block-2">After signup</h2>
<p>Verify contact, complete KYC before withdrawal, deposit via <a class="text-link" href="../payments/">cashier</a>.</p>
</article>''',
        'login': '''<article class="seo-block seo-block--rich">
<h2 id="seo-block-1">Account login</h2>
<p>Email or phone + password. Reset via SMS/email. 2FA recommended.</p>
</article>
<article class="seo-block seo-block--rich">
<h2 id="seo-block-2">Security</h2>
<p>Use only fairpari.com/uz. Don't save passwords on shared devices. Bonus progress in PROMO after <a class="text-link" href="../login/">login</a>.</p>
</article>
<article class="seo-block seo-block--rich">
<h2 id="seo-block-3">Mobile login</h2>
<p>Same credentials on site and <a class="text-link" href="../app/">app</a>. Balance and bonuses sync.</p>
</article>''',
        'payments': '''<article class="seo-block seo-block--rich">
<h2 id="seo-block-1">Deposit for bonus</h2>
<p>Humo, Uzcard, Click, Payme, crypto. Minimum depends on method — check cashier.</p>
</article>
<article class="seo-block seo-block--rich">
<h2 id="seo-block-2">Withdrawal</h2>
<p>KYC on first cashout. UZS cards 1–24h. Bonus balance must be wagered first.</p>
</article>''',
        'app': '''<article class="seo-block seo-block--rich">
<h2 id="seo-block-1">Android APK and iOS PWA</h2>
<p>Download only from fairpari.com/uz/mobile. No official app in Google Play or App Store.</p>
</article>
<article class="seo-block seo-block--rich">
<h2 id="seo-block-2">Bonus in app</h2>
<p>Same welcome and promo <strong><a class="text-link" href="../promo-code/">fa_1635</a></strong>. One UZS balance with the website.</p>
</article>''',
        'license': '''<article class="seo-block seo-block--rich">
<h2 id="seo-block-1">Operator license</h2>
<p>FairPari lists <strong>OGL/2024/1143/0865</strong>. This bonus portal is informational, not the operator.</p>
</article>
<article class="seo-block seo-block--rich">
<h2 id="seo-block-2">KYC and safety</h2>
<p>Verification before withdrawal. SSL, responsible gaming 18+ — see <a class="text-link" href="../responsible-gaming/">dedicated page</a>.</p>
</article>''',
    }
    return pages.get(slug, common)

SEO_HEADERS_RU = {
    'vhod': ('Руководство по входу', 'FairPari — вход и бонусный кабинет', '2FA и официальный домен'),
    'skachat': ('Мобильное приложение', 'FairPari APK и iOS PWA', 'Бонус с телефона'),
    'registratsiya': ('Регистрация', 'FairPari — создать аккаунт', 'Промокод fa_1635'),
    'oplata': ('Платежи', 'FairPari UZ — депозит и вывод', 'Humo, Click, Payme'),
    'promokod': ('Промокод', 'FairPari fa_1635', 'Активация welcome'),
    'litsenziya': ('Лицензия', 'FairPari — правовая информация', 'KYC и 18+'),
    'bonusy-kazino': ('Казино бонус', 'Welcome FairPari', '4 депозита, ×35'),
    'index': ('Справочник бонусов', 'FairPari UZ 2026', 'Казино и спорт'),
}

SEO_HEADERS_EN = {
    'login': ('Login guide', 'FairPari account access', '2FA and official domain'),
    'app': ('Mobile app', 'FairPari APK and iOS PWA', 'Bonus on phone'),
    'registration': ('Registration', 'FairPari sign up', 'Promo fa_1635'),
    'payments': ('Payments', 'FairPari UZ deposit', 'Humo, Click, Payme'),
    'promo-code': ('Promo code', 'FairPari fa_1635', 'Welcome activation'),
    'license': ('License', 'FairPari legal info', 'KYC and 18+'),
    'casino-bonuses': ('Casino bonus', 'FairPari welcome', '4 deposits, ×35'),
    'index': ('Bonus guide', 'FairPari UZ 2026', 'Casino and sports'),
}

def slug_from_path(path, lang):
    rel = path.relative_to(ROOT / lang)
    if rel.name == 'index.html' and str(rel.parent) == '.':
        return 'index'
    return rel.parent.name

def apply_global(html, is_en=False):
    for a, b in GLOBAL_FIX:
        html = html.replace(a, b)
    if is_en:
        for a, b in EN_EXTRA_HREF:
            html = html.replace(a, b)
    return html

def replace_seo_expansion(html, body):
    return re.sub(
        r'(<div class="seo-expansion__body">).*?(</div>\s*</section>\s*<section|\</div>\s*</section>\s*<div class="related|\</div>\s*</section>\s*<footer|\</div>\s*</section>\s*</main)',
        lambda m: m.group(1) + body + m.group(2),
        html, count=1, flags=re.S
    )

def fix_seo_header(html, eyebrow, title, subtitle):
    html = re.sub(r'(<span class="section__eyebrow">)[^<]+(</span>)', lambda m: m.group(1)+eyebrow+m.group(2), html, count=1)
    html = re.sub(r'(<h2 class="section__title">)[^<]+(</h2>)', lambda m: m.group(1)+title+m.group(2), html, count=1)
    html = re.sub(r'(<p class="section__subtitle">)[^<]+(</p>)', lambda m: m.group(1)+subtitle+m.group(2), html, count=1)
    return html

def fix_en_registration_hero(html):
    html = html.replace('Casino ro&#x27;yxatfrom o&#x27;tish banneri', 'FairPari registration banner')
    html = html.replace('>✅ Ro\'yxat<', '>✅ Sign up<')
    html = html.replace('>Casino akkaunti<', '>Casino account<')
    html = html.replace('xush kelibsiz paket', 'welcome package')
    html = html.replace('registration banneri', 'registration banner')
    html = html.replace('casino bonusesi banneri', 'casino bonus banner')
    return html

UZ_PAT = re.compile(
    r"(?<![\w/])(siyosati|shartlari|qanday|birinchi|depozit|ekspre|kabineti|ilova|faollashtirish|kiritish|frispinlar|bonuslari|mas'uliyatli|foydalanish|maxfiylik|xavfsiz|mavjud|beriladi|uchun|bilan|haqida|o'yin|o'zbekiston|gacha|aksiyalari|katalogi|holat|rasmiy|depositsiz|qo'llanma|nuqtasi|foydalaning|ishlaydi|tavsiya|yuklang|o'rnatish|bildirishnomalar|qulay|tez|yordam|muammo|javob|qoida|tekshir|himoya|ishga|tushir|saqlan|qayta|parol|tiklash|bloklangan|mumkin|kerak|bo'lishi|qilish|qiling|qo'sh|o'ch|yangilan|boshq|havola|manba|xavf|virus|torrent|noma'lum|ruxsat|sozlamalar|qurilma|sessiya|cookie|brauzer|sayt|akkaunt|balans|promo|kesh|tozalash|chat|skrinshot|wifi|almashtirish|uzilsa|qayta|biometrik|face id|push|ikonka|o'rnatishsiz|cheklangan|play protect|ogohlantirish|do'kon|qimor|cheklaydi|operator|translyatsiya|studiyasi|barqaror|oqim|yetkazib|beruvchi|kontenti|stol|igra|jarayon|valyuta|konvertatsiya|odatda|tez|tushadi|qo'shimcha|vaqt|hamyon|daqiqa|pasport|tekshiruv|bosqich|firibgarlik|nazorat|byudjet|limit|cheklash|shaffoflik|raqam|huquqiy|qayd|mahalliy|kassa|ommabop|usullar|saralash|filtr|klassik|mini-games|formatlar|auditoriyasi|yo'nalish|platforma|tushuntiriladi|paket|olishda|qo'llanadi|talabi|bo'limida|yangilanib|turadi|ko'rsatkich|tavsif|yetkazib|demo|rejim|sertifikatlangan|RNG|translyatsiya|sifati|boshqalar|zerkalo|ishchi|manzil|to'lov|slot|bosh|kelib|ro'yxat|akkaunti|banneri)(?![\w/])",
    re.I
)

def scan(html):
    # ignore href/src paths and asset filenames with uz latin
    text = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', html, flags=re.S|re.I)
    text = re.sub(r'\b(href|src)="[^"]*"', '', text)
    return sorted(set(UZ_PAT.findall(text)))

def process(path, lang):
    html = path.read_text(encoding='utf-8')
    slug = slug_from_path(path, lang)
    is_en = lang == 'en'
    html = apply_global(html, is_en)

    if 'seo-expansion__body' in html:
        body = block_en(slug) if is_en else block_ru(slug)
        html = replace_seo_expansion(html, body)
        headers = (SEO_HEADERS_EN if is_en else SEO_HEADERS_RU).get(slug)
        if headers:
            html = fix_seo_header(html, *headers)

    if is_en and 'registration' in str(path):
        html = fix_en_registration_hero(html)

    # footer legal link text
    if is_en:
        html = html.replace('Responsible gambling', 'Responsible gaming')
    else:
        html = html.replace('Конфиденциальность политика', 'Политика конфиденциальности')
        html = html.replace('Ответственная игра политика', 'Ответственная игра')

    path.write_text(html, encoding='utf-8')
    return scan(html)

if __name__ == '__main__':
    ru_bad, en_bad = [], []
    for p in sorted((ROOT/'ru').rglob('*.html')):
        left = process(p, 'ru')
        if left: ru_bad.append((str(p.relative_to(ROOT)), left[:8]))
    for p in sorted((ROOT/'en').rglob('*.html')):
        left = process(p, 'en')
        if left: en_bad.append((str(p.relative_to(ROOT)), left[:8]))
    print('RU remaining:', len(ru_bad))
    for x in ru_bad: print(' ', x)
    print('EN remaining:', len(en_bad))
    for x in en_bad: print(' ', x)

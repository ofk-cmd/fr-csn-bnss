#!/usr/bin/env python3
"""Pass 2: fix broken hrefs, legal bodies, remaining uz tokens in RU/EN."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

RU_HREF_FIX = {
    '../промокод/': '../promokod/',
    '../бездепозитный-bonus/': '../bonus-bez-depozita/',
    '../лицензия/': '../litsenziya/',
    '../pul-вывод/': '../oplata/',
    '../слоты/': '../bonusy-kazino/',
    '../live-kazino/': '../bonusy-kazino/',
    '../sharhlar/': '../faq/',
    'href="../../politika-konfidentsialnosti/"': 'href="../politika-konfidentsialnosti/"',
    'href="../../usloviya-ispolzovaniya/"': 'href="../usloviya-ispolzovaniya/"',
    'href="../../politika-cookie/"': 'href="../politika-cookie/"',
    'href="../../otvetstvennaya-igra/"': 'href="../otvetstvennaya-igra/"',
    'href="../../../"': 'href="../"',
}

EN_HREF_FIX = {
    '../промокод/': '../promo-code/',
    '../бездепозитный-bonus/': '../no-deposit-bonus/',
    '../лицензия/': '../license/',
    '../pul-вывод/': '../payments/',
    '../promokod/': '../promo-code/',
    '../depozitsiz-bonus/': '../no-deposit-bonus/',
    '../litsenziya/': '../license/',
    '../royxatdan-otish/': '../registration/',
    '../tolov/': '../payments/',
    '../mobil/': '../app/',
    '../kazino-bonuslari/': '../casino-bonuses/',
    '../sport-bonuslari/': '../sports-bonuses/',
    '../kirish/': '../login/',
    '../pul-yechish/': '../payments/',
    '../slotlar/': '../casino-bonuses/',
    '../live-kazino/': '../casino-bonuses/',
    '../sharhlar/': '../faq/',
}

RU_EXTRA = [
    ('sport aksiyalari', 'спортивные акции'),
    ('bonus katalogi', 'каталог бонусов'),
    ('Konfidensialnost siyosati', 'Политика конфиденциальности'),
    ('Foydalanish shartlari', 'Условия использования'),
    ('mas\'uliyatli игра', 'ответственная игра'),
    ('mas\'uliyatli o\'yin', 'ответственная игра'),
    ('депозитsiz', 'без депозита'),
    ('спорт-бонусda', 'спорт-бонусе'),
    ('dan ', 'от '),
    ('aksiyasida', 'в акции'),
    ('promoda', 'в промо'),
    ('keshbekdan', 'из кешбэка'),
    ('Birinchi', 'Первый'),
    ('birinchi', 'первый'),
    ('Mavjud', 'Доступно'),
    ('mavjud', 'доступно'),
    ('Xavfsiz', 'Безопасно'),
    ('Ilova', 'Приложение'),
    ('ilova', 'приложение'),
    ('Tolov', 'Платёж'),
    ('tolov', 'платёж'),
    ('foydalanish', 'использование'),
    ('maxfiylik', 'конфиденциальность'),
    ('shartlari', 'условия'),
    ('siyosati', 'политика'),
    ('qanday', 'как'),
    ('haqida', 'о'),
    ('uchun', 'для'),
    ('bilan', 'с'),
    ('kiritish', 'ввод'),
    ('faollashtirish', 'активация'),
    ('Faollashtirish', 'Активация'),
    ("O'yin", 'Игра'),
    ("o'yin", 'игра'),
    ("O'yinchilar", 'Игроки'),
    ("o'yinchilar", 'игроки'),
    ('cho\'ntakda', 'в кармане'),
    ('katalogi', 'каталог'),
    ('janr', 'жанр'),
    ('provayder', 'провайдер'),
    ("bo'yicha", 'по'),
    ('stollari', 'столы'),
    ('tajribasi', 'опыт'),
    ('sрокlar', 'сроки'),
    ('Ma\'lumotlardan foydalanish', 'Использование данных'),
    ('Ma\'lumotlar', 'Данные'),
    ('ma\'lumotlar', 'данные'),
    ('Cookie va kuzatuv', 'Cookie и отслеживание'),
    ('Saqlash срокi va huquqlar', 'Срок хранения и права'),
    ('Qo\'llab-quvvatlash', 'Поддержка'),
    ('qo\'llab-quvvatlash', 'поддержка'),
    ('Sayt onlayn kazino о axborot beradi', 'Сайт предоставляет информацию об онлайн-казино'),
    ('bu materiallar o\'ynashga chaqiruv emas', 'эти материалы не призывают к игре'),
    ('Qarorlar o\'z mas\'uliyatingizda', 'Решения вы принимаете на свой страх и риск'),
    ('qimor moliyaviy xavf tug\'diradi', 'азартные игры несут финансовый риск'),
    ('bosh sahifaga qaytish', 'вернуться на главную'),
    ('eCOGRA sertifikat belgisi', 'сертификат eCOGRA'),
    ('DMCA himoya belgisi', 'знак защиты DMCA'),
    ('sport aksiyalari', 'спортивные акции'),
    ('verifikatsiya', 'верификация'),
    ('barqaror ishlash', 'стабильная работа'),
    ('tug\'ilgan sana', 'дата рождения'),
    ('to\'lov rekvizitlari', 'платёжные реквизиты'),
    ('ochishda', 'при открытии'),
    ('ochish', 'открытие'),
    ('hisob', 'счёт'),
    ('faol bo\'lguncha', 'пока активен'),
    ('qonun talab qilgan', 'требует закон'),
    ('sрокдо', 'срока'),
    ('O\'z ma\'lumotlaringiz', 'Свои данные'),
    ('cheklash mumkin', 'можно ограничить'),
    ('ishlamasligi mumkin', 'может не работать'),
    ('tanlovi', 'выбора'),
    ('statistika', 'статистика'),
    ('sessiyani saqlash', 'сохранение сессии'),
    ('Brauzer sozlamalarida', 'В настройках браузера'),
    ('Brauzer turi', 'тип браузера'),
    ('tashrifi vaqtida', 'во время посещения'),
    ('avtomatik yozilishi mumkin', 'может записываться автоматически'),
    ('so\'ralishi mumkin', 'может запрашиваться'),
    ('uchinchi shaxslarga', 'третьим лицам'),
    ('reklama maqsadida', 'в рекламных целях'),
    ('sotilmaydi', 'не продаются'),
    ('tasdiqlash', 'подтверждение'),
    ('bonuslar', 'бонусы'),
    ('Operator (FairPari) maxfiylik siyosati uchun', 'Политику конфиденциальности оператора (FairPari) смотрите на'),
    ('murojaat qiling', 'обратитесь'),
    ('O\'zgarishlar', 'Изменения'),
    ('nashr etiladi', 'публикуются'),
    ('fairpari.com/uz manziliga', 'fairpari.com/uz'),
    ('Sahifalarda', 'На страницах'),
    ('hamkor havolalar', 'партнёрские ссылки'),
    ('jumladan', 'включая'),
    ('o\'tgach', 'после перехода'),
    ('ularning shartlarini alohida', 'их условия отдельно'),
    ('прочитайте', 'прочитайте'),
    ('brendi bo\'yicha', 'бренда'),
    ('mustaqil ma\'lumot va sharh sayti', 'независимый информационный и обзорный сайт'),
    ('rasmiy operator emasmiz', 'мы не официальный оператор'),
    ('не принимаем депозиты', 'не принимаем депозиты'),
    ('to\'g\'ridan-to\'g\'ri', 'напрямую'),
    ('не предоставляем азартные услуги', 'не предоставляем азартные услуги'),
    ('Ushbu maxfiylik siyosati faqat', 'Настоящая политика конфиденциальности действует только'),
    ('domenidagi kontent va texnik jurnal uchun amal qiladi', 'для контента и технических журналов на домене'),
    ('himoyasi banneri', 'защиты данных, баннер'),
    ('Ma\'lumotlardan foydalanish', 'Использование данных'),
    ('Konfidensialnost siyosati va ma\'lumotlar himoyasi banneri', 'Политика конфиденциальности и защита данных — баннер'),
]

EN_EXTRA = [
    ('sport aksiyalari', 'sports promotions'),
    ('bonus katalogi', 'bonus catalog'),
    ('Litsenziya', 'License'),
    ('litsenziya', 'license'),
    ('Rasmiy', 'Official'),
    ('rasmiy', 'official'),
    ('Birinchi', 'First'),
    ('birinchi', 'first'),
    ('Mavjud', 'Available'),
    ('mavjud', 'available'),
    ('Xavfsiz', 'Secure'),
    ('Bonus kodi', 'Bonus code'),
    ('siyosati', 'policy'),
    ('shartlari', 'terms'),
    ('foydalanish', 'use'),
    ('maxfiylik', 'privacy'),
    ('qanday', 'how'),
    ('brauzerda ularni how boshqarish mumkin', 'how to manage them in the browser'),
    ('qaysi cookie fayllar ishlatiladi', 'which cookie files are used'),
    ('kiritish', 'enter'),
    ('ilova', 'app'),
    ('ekspress', 'express'),
    ('promokod', 'promo code'),
    ('depozitsiz', 'no deposit'),
    ('depositsiz', 'no deposit'),
    ('kabineti', 'account'),
    ('frispinlar', 'free spins'),
    ('gacha', 'up to'),
    ('uchun', 'for'),
    ('bilan', 'with'),
    ('haqida', 'about'),
    ('va ', 'and '),
    ('dan ', 'from '),
    ('bo\'yicha', 'by'),
    ('katalogi', 'catalog'),
    ('janr', 'genre'),
    ('provayder', 'provider'),
    ('stollari', 'tables'),
    ('cho\'ntakda', 'in your pocket'),
    ('tajribasi', 'experience'),
    ('sрокlar', 'deadlines'),
    ('O\'yinchilar fikri', 'Player opinions'),
    ('Slotlar katalogi', 'Slots catalog'),
    ('Live kazino', 'Live casino'),
    ('Mobil kazino', 'Mobile casino'),
    ('Pul yechish', 'Withdrawal'),
    ('yechish qoidalari', 'withdrawal rules'),
    ('Sayt onlayn kazino haqida axborot beradi', 'This site provides information about online casino'),
    ('o\'ynashga chaqiruv emas', 'not an invitation to play'),
    ('Qarorlar o\'z mas\'uliyatingizda', 'Decisions are your own responsibility'),
    ('qimor moliyaviy xavf tug\'diradi', 'gambling carries financial risk'),
    ('bosh sahifaga qaytish', 'back to home'),
    ('sertifikat belgisi', 'certificate badge'),
    ('himoya belgisi', 'protection badge'),
    ('mas\'uliyatli o\'yin', 'responsible gaming'),
    ('eCOGRA sertifikat belgisi', 'eCOGRA certificate badge'),
    ('DMCA himoya belgisi', 'DMCA protection badge'),
    ('aksiyasida', 'in promo'),
    ('promoda', 'in promo'),
    ('keshbekdan', 'from cashback'),
    ('sport bonusda', 'sports bonus'),
    ('kazino welcome dan', 'casino welcome from'),
    ('free spin aksiyasida', 'free spin promo'),
]

LEGAL_RU = {
    'politika-konfidentsialnosti': '''<h2 id="data-collected">Какие данные собираются</h2><p>При открытии аккаунта FairPari могут запрашиваться email, телефон, дата рождения и платёжные реквизиты. При посещении сайта могут автоматически записываться технические журналы (IP, тип браузера, сессия) — для безопасности и стабильной работы.</p>
<h2 id="data-use">Использование данных</h2><p>Персональные данные используются для подтверждения аккаунта, платежей, бонусов и поддержки. Данные не продаются третьим лицам в рекламных целях.</p>
<h2 id="cookies">Cookie и отслеживание</h2><p>Файлы cookie применяются для сохранения сессии, выбора языка и статистики. В настройках браузера cookie можно ограничить; часть функций может перестать работать.</p>
<h2 id="retention">Срок хранения и права</h2><p>Данные хранятся, пока счёт активен, или в срок, требуемый законом. Вы можете запросить доступ, исправление или удаление своих данных через поддержку.</p>''',
    'politika-cookie': '''<h2 id="what-cookies">Что такое cookie</h2><p>Cookie — небольшие файлы в браузере, которые помогают сайту запоминать настройки и сессию.</p>
<h2 id="types">Какие cookie мы используем</h2><p>Технические cookie (сессия, безопасность), функциональные (язык) и аналитические (обезличенная статистика).</p>
<h2 id="manage">Как управлять</h2><p>Ограничьте или удалите cookie в настройках браузера. Подробнее — в <a href="../politika-konfidentsialnosti/">политике конфиденциальности</a>.</p>''',
    'usloviya-ispolzovaniya': '''<h2 id="scope">Область действия</h2><p>Условия распространяются на портал fairpari-casino-bonuses.com — независимый информационный сайт о бонусах FairPari. Мы не оператор и не принимаем депозиты.</p>
<h2 id="affiliate">Партнёрские ссылки</h2><p>Кнопки могут вести на сайт оператора. Мы не гарантируем качество услуг оператора. Проверяйте официальный адрес (fairpari.com/uz).</p>
<h2 id="liability">Ограничение ответственности</h2><p>Материалы носят информационный характер и не являются призывом к игре. Решения вы принимаете самостоятельно; азартные игры рискованны.</p>''',
    'otvetstvennaya-igra': '''<h2 id="18-rule">Правило 18+</h2><p>Бонусный портал: FairPari только для лиц 18+. Аккаунты несовершеннолетних закрываются, средства могут быть возвращены.</p>
<h2 id="self-limits">Инструменты самоограничения</h2><p>Лимиты депозита, ограничение сессии, тайм-аут и самоисключение доступны в настройках аккаунта или через поддержку.</p>
<h2 id="help">Ресурсы помощи</h2><p>Если игра выходит из-под контроля, обратитесь к специалисту или организациям вроде BeGambleAware. Азартные игры могут привести к долгам — просить помощь нормально.</p>''',
}

LEGAL_EN = {
    'privacy-policy': '''<h2 id="data-collected">What data is collected</h2><p>When opening a FairPari account, email, phone, date of birth and payment details may be requested. Site visits may log technical data (IP, browser type, session) for security and stability.</p>
<h2 id="data-use">How data is used</h2><p>Personal data is used for account verification, payments, bonuses and support. Data is not sold to third parties for advertising.</p>
<h2 id="cookies">Cookies and tracking</h2><p>Cookies store sessions, language preferences and statistics. You can limit cookies in browser settings; some features may stop working.</p>
<h2 id="retention">Retention and rights</h2><p>Data is kept while the account is active or as required by law. You may request access, correction or deletion via support.</p>''',
    'cookie-policy': '''<h2 id="what-cookies">What are cookies</h2><p>Cookies are small browser files that help the site remember settings and sessions.</p>
<h2 id="types">Cookies we use</h2><p>Technical (session, security), functional (language) and analytics (anonymized statistics).</p>
<h2 id="manage">How to manage</h2><p>Limit or delete cookies in browser settings. See also our <a href="../privacy-policy/">privacy policy</a>.</p>''',
    'terms-of-use': '''<h2 id="scope">Scope</h2><p>These terms apply to fairpari-casino-bonuses.com — an independent FairPari bonus information portal. We are not the operator and do not accept deposits.</p>
<h2 id="affiliate">Affiliate links</h2><p>Buttons may lead to the operator site. We do not guarantee operator service quality. Verify the official address (fairpari.com/uz).</p>
<h2 id="liability">Disclaimer</h2><p>Content is informational only, not an invitation to gamble. You are responsible for your decisions; gambling carries financial risk.</p>''',
    'responsible-gaming': '''<h2 id="18-rule">18+ rule</h2><p>Bonus portal: FairPari is for adults 18+ only. Underage accounts are closed; funds may be returned.</p>
<h2 id="self-limits">Self-limitation tools</h2><p>Deposit limits, session time limits, timeouts and self-exclusion are available in account settings or via support.</p>
<h2 id="help">Help resources</h2><p>If gambling feels out of control, contact a professional or organizations such as BeGambleAware. Gambling can cause debt — asking for help is normal.</p>''',
}

PAGE_CONTEXT_RU = 'каталог бонусов fairpari-casino-bonuses.com — welcome, FS и спортивные акции.'
PAGE_CONTEXT_EN = 'fairpari-casino-bonuses.com bonus catalog — welcome, FS and sports promotions.'

LIVE_WINS_RU = '''<span class="live-wins__item">Ulug'bek D. — 2 050 000 UZS с casino welcome</span><span class="live-wins__item">Maftuna S. — 630 000 UZS в акции free spin</span><span class="live-wins__item">Javohir B. — 1 110 000 UZS на спорт-бонусе</span><span class="live-wins__item">Laylo K. — 390 000 UZS в промо без депозита</span><span class="live-wins__item">Anvar R. — 1 670 000 UZS из VIP кешбэка</span>'''

LIVE_WINS_EN = '''<span class="live-wins__item">Ulug'bek D. — 2,050,000 UZS from casino welcome</span><span class="live-wins__item">Maftuna S. — 630,000 UZS in free spin promo</span><span class="live-wins__item">Javohir B. — 1,110,000 UZS on sports bonus</span><span class="live-wins__item">Laylo K. — 390,000 UZS in no deposit promo</span><span class="live-wins__item">Anvar R. — 1,670,000 UZS from VIP cashback</span>'''

FOOTER_DISC_RU = '18+. Сайт предоставляет информацию об онлайн-казино; материалы не призывают к игре. Решения на вашей ответственности; азартные игры рискованны.'
FOOTER_DISC_EN = '18+. This site provides online casino information; content is not an invitation to play. You are responsible for your decisions; gambling carries financial risk.'

def fix_file(path, href_fix, extra_phrases, lang):
    html = path.read_text(encoding='utf-8')
    for a, b in href_fix.items():
        html = html.replace(a, b)
    extra_phrases.sort(key=lambda x: len(x[0]), reverse=True)
    for a, b in extra_phrases:
        html = html.replace(a, b)

    if lang == 'ru':
        html = re.sub(r'<p class="page-context"[^>]*>.*?</p>', f'<p class="page-context" data-uniquify="bonuses">{PAGE_CONTEXT_RU}</p>', html, count=1)
        html = html.replace(FOOTER_DISC_RU, FOOTER_DISC_RU)  # noop anchor
        html = re.sub(r'<p class="footer-disclaimer">.*?</p>', f'<p class="footer-disclaimer">{FOOTER_DISC_RU}</p>', html, count=1)
        # live wins
        if 'live-wins__track' in html:
            html = re.sub(r'<div class="live-wins__track">.*?</div>', f'<div class="live-wins__track">{LIVE_WINS_RU}{LIVE_WINS_RU}</div>', html, count=1)
        for key, body in LEGAL_RU.items():
            if key in str(path):
                html = re.sub(r'<h1 class="section__title">[^<]+</h1>.*?</div></section>', lambda m: m.group(0).split('</h1>')[0]+'</h1>'+body+'</div></section>', html, count=1, flags=re.S)
                # simpler: replace between h1 and end section
                pat = r'(<h1 class="section__title">[^<]+</h1>)(.*?)(</div></section>)'
                html = re.sub(pat, r'\1'+body+r'\3', html, count=1, flags=re.S)
        html = html.replace('Конфиденциальность политика', 'Политика конфиденциальности')
        html = html.replace('/ <span>Конфиденциальность политика</span>', '/ <span>Политика конфиденциальности</span>')
        html = html.replace('"name": "Privacy policy"', '"name": "Ответственная игра"')
        html = html.replace('"name": "Политика конфиденциальности siyosati"', '"name": "Политика конфиденциальности"')
    else:
        html = re.sub(r'<p class="page-context"[^>]*>.*?</p>', f'<p class="page-context" data-uniquify="bonuses">{PAGE_CONTEXT_EN}</p>', html, count=1)
        html = re.sub(r'<p class="footer-disclaimer">.*?</p>', f'<p class="footer-disclaimer">{FOOTER_DISC_EN}</p>', html, count=1)
        if 'live-wins__track' in html:
            html = re.sub(r'<div class="live-wins__track">.*?</div>', f'<div class="live-wins__track">{LIVE_WINS_EN}{LIVE_WINS_EN}</div>', html, count=1)
        for key, body in LEGAL_EN.items():
            if key in str(path):
                pat = r'(<h1 class="section__title">[^<]+</h1>)(.*?)(</div></section>)'
                html = re.sub(pat, r'\1'+body+r'\3', html, count=1, flags=re.S)
        html = html.replace('"name": "Privacy policy"', '"name": "Responsible gaming"')

    path.write_text(html, encoding='utf-8')

def scan_uz(path, lang):
    html = path.read_text(encoding='utf-8')
    uz_pat = re.compile(r"\b(siyosati|shartlari|qanday|birinchi|depozit|ekspre|kabineti|ilova|faollashtirish|kiritish|frispinlar|bonuslari|promokod|mas'uliyatli|foydalanish|maxfiylik|royxatdan|tolov|litsenziya|xavfsiz|mavjud|beriladi|uchun|bilan|haqida|o'yin|o'zbekiston|gacha|aksiyalari|katalogi|holat|rasmiy|depositsiz|va ekspress|sport bonusi|bonus kodi)\b", re.I)
    return sorted(set(uz_pat.findall(html)))

if __name__ == '__main__':
    ru_issues = []
    en_issues = []
    for p in sorted((ROOT/'ru').rglob('*.html')):
        fix_file(p, RU_HREF_FIX, RU_EXTRA, 'ru')
        f = scan_uz(p, 'ru')
        if f: ru_issues.append((str(p.relative_to(ROOT)), f[:6]))
    for p in sorted((ROOT/'en').rglob('*.html')):
        fix_file(p, EN_HREF_FIX, EN_EXTRA, 'en')
        f = scan_uz(p, 'en')
        if f: en_issues.append((str(p.relative_to(ROOT)), f[:6]))
    print('RU issues:', len(ru_issues))
    for i in ru_issues: print(' ', i)
    print('EN issues:', len(en_issues))
    for i in en_issues: print(' ', i)

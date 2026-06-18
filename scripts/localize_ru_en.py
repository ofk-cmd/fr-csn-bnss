#!/usr/bin/env python3
"""Localize fairpari-casino-bonuses.com RU and EN pages — remove Uzbek cross-contamination."""
import re
import html as html_lib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOMAIN = 'fairpari-casino-bonuses.com'

LEGAL_HREFLANG = {
    'masuliyatli-oyin': ('/masuliyatli-oyin/', '/ru/otvetstvennaya-igra/', '/en/responsible-gaming/'),
    'maxfiylik-siyosati': ('/maxfiylik-siyosati/', '/ru/politika-konfidentsialnosti/', '/en/privacy-policy/'),
    'cookie-siyosati': ('/cookie-siyosati/', '/ru/politika-cookie/', '/en/cookie-policy/'),
    'foydalanish-shartlari': ('/foydalanish-shartlari/', '/ru/usloviya-ispolzovaniya/', '/en/terms-of-use/'),
}

def M(title, desc, h1, og_alt=None):
    og_alt = og_alt or 'FairPari UZ — casino and sportsbook platform'
    return dict(title=title, description=desc, h1=h1, og_title=title, og_desc=desc,
                tw_title=title, tw_desc=desc, og_alt=og_alt, tw_alt=og_alt)

RU_META = {
    'index.html': M(
        'FairPari бонусы — казино и спорт welcome 2026',
        'Бонусы FairPari в Узбекистане: казино welcome 19,5 млн UZS + 150 FS, спорт-бонус, промокод fa_1635. Таблицы и FAQ, 18+.',
        'Бонусы FairPari — обзор 2026',
        'Бонусы FairPari — слоты, live и crash, баннер'),
    'bonusy-kazino/index.html': M(
        'FairPari бонус казино — welcome и фриспины',
        'Казино welcome FairPari: 19,5 млн UZS + 150 FS, 4 депозита, wagering ×35. Правила и активация, 18+.',
        'FairPari казино welcome — пакет из 4 этапов',
        'Welcome-бонус казино FairPari — баннер'),
    'sport-bonusy/index.html': M(
        'FairPari спорт-бонус — welcome и экспресс',
        'Спортивный welcome FairPari: до 1,3 млн UZS, экспресс-акции, wagering ×5. Отдельно от казино, 18+.',
        'FairPari спорт-бонус — первый депозит и экспресс',
        'Спортивный бонус FairPari — баннер'),
    'promokod/index.html': M(
        'FairPari промокод fa_1635 — активация',
        'Промокод FairPari fa_1635: где вводить, казино welcome и условия. Регистрация и касса, 18+.',
        'FairPari промокод — как активировать',
        'Промокод FairPari — баннер'),
    'bonus-bez-depozita/index.html': M(
        'FairPari бездепозитный бонус — официальный статус',
        'Бонус без депозита FairPari: что реально доступно, бесплатные вращения и альтернативы welcome. 18+.',
        'FairPari бонус без депозита — официальный статус',
        'Бонус без депозита — баннер'),
    'free-spins/index.html': M(
        'FairPari фриспины — правила welcome',
        'Фриспины FairPari: когда начисляются, wagering и срок. Welcome 150 FS на 4 депозита, 18+.',
        'FairPari фриспины — когда начисляются',
        'Фриспины FairPari — баннер'),
    'bonus-kod/index.html': M(
        'FairPari промокод казино — код fa_1635',
        'Бонус-код FairPari fa_1635: где ввести и как активировать welcome. Ошибки и проверка, 18+.',
        'FairPari бонус-код — код казино',
        'Бонус-код FairPari — баннер'),
    'registratsiya/index.html': M(
        'FairPari регистрация — получить бонус',
        'Как зарегистрироваться в FairPari и получить welcome: 4 способа, промокод fa_1635, верификация. 18+.',
        'Как получить бонус — регистрация',
        'Регистрация FairPari — баннер'),
    'vhod/index.html': M(
        'FairPari вход — бонусный кабинет',
        'Вход в FairPari: логин, восстановление пароля, бонусный кабинет и PROMO. 18+.',
        'FairPari вход — бонусный кабинет',
        'Вход FairPari — баннер'),
    'oplata/index.html': M(
        'FairPari платежи — депозит для бонуса',
        'Платежи FairPari UZ: Humo, Uzcard, Payme, Click, крипто. Депозит для активации welcome, 18+.',
        'Платежи — активация бонуса',
        'Платежи FairPari UZ — баннер'),
    'skachat/index.html': M(
        'FairPari мобильное — бонус в APK',
        'Скачать FairPari APK Android и PWA iOS. Мобильные бонусы, один баланс с сайтом. 18+.',
        'Мобильное приложение и бонус — APK и iOS',
        'Мобильное приложение FairPari — баннер'),
    'litsenziya/index.html': M(
        'FairPari лицензия — безопасность бонусов',
        'Лицензия FairPari OGL/2024/1143/0865: безопасность бонусов, KYC и ответственная игра. 18+.',
        'Безопасность, лицензия и ответственная игра',
        'Лицензия и безопасность FairPari — баннер'),
    'faq/index.html': M(
        'FairPari бонусы — частые вопросы',
        'FAQ по бонусам FairPari: промокод, wagering, два welcome, без депозита, вывод. 18+.',
        'FAQ по бонусам FairPari',
        'FAQ FairPari — баннер'),
    'politika-cookie/index.html': M(
        'Политика файлов cookie — FairPari UZ',
        'Политика cookie FairPari UZ: какие файлы используются и как управлять ими в браузере. 18+.',
        'Политика cookie',
        'Политика cookie FairPari — баннер'),
    'politika-konfidentsialnosti/index.html': M(
        'Политика конфиденциальности — FairPari UZ',
        'Политика конфиденциальности FairPari UZ: какие данные собираются, cookie, срок хранения и права пользователя. 18+.',
        'Политика конфиденциальности',
        'Конфиденциальность FairPari — баннер'),
    'usloviya-ispolzovaniya/index.html': M(
        'Условия использования — FairPari UZ',
        'Условия использования портала бонусов FairPari UZ: 18+, отказ от ответственности, ссылки на оператора. 18+.',
        'Условия использования',
        'Условия использования — баннер'),
    'otvetstvennaya-igra/index.html': M(
        'Ответственная игра — FairPari UZ',
        'Ответственная игра FairPari UZ: правило 18+, лимиты, самоисключение и ресурсы помощи. 18+.',
        'Ответственная игра',
        'Ответственная игра — баннер'),
}

EN_META = {
    'index.html': M(
        'FairPari bonuses — casino & sports welcome 2026',
        'All FairPari bonuses in Uzbekistan: casino welcome 19.5M UZS + 150 FS, sports, promo fa_1635, no deposit, free spins. Independent guide, 18+.',
        'FairPari bonuses — 2026 overview',
        'FairPari bonuses — slots, live and crash banner'),
    'casino-bonuses/index.html': M(
        'FairPari casino bonus — welcome & free spins',
        'FairPari casino welcome: 19.5M UZS + 150 FS, 4 deposits, wagering ×35. Rules and activation, 18+.',
        'FairPari casino welcome — 4-step package',
        'FairPari casino welcome bonus banner'),
    'sports-bonuses/index.html': M(
        'FairPari sports bonus — welcome & express',
        'FairPari sports welcome: up to 1.3M UZS, express promos, wagering ×5. Separate from casino, 18+.',
        'FairPari sports bonus — first deposit & express',
        'FairPari sports bonus banner'),
    'promo-code/index.html': M(
        'FairPari promo code fa_1635 — activation',
        'FairPari promo code fa_1635: where to enter, casino welcome and terms. Registration and cashier, 18+.',
        'FairPari promo code — how to activate',
        'FairPari promo code banner'),
    'no-deposit-bonus/index.html': M(
        'FairPari no deposit bonus — official status',
        'FairPari no deposit bonus: what is actually available, free spins and welcome alternatives. 18+.',
        'FairPari no deposit bonus — official status',
        'No deposit bonus banner'),
    'free-spins/index.html': M(
        'FairPari free spins — welcome rules',
        'FairPari free spins: when credited, wagering and deadline. Welcome 150 FS across 4 deposits, 18+.',
        'FairPari free spins — when they are credited',
        'FairPari free spins banner'),
    'bonus-code/index.html': M(
        'FairPari casino bonus code — fa_1635',
        'FairPari bonus code fa_1635: where to enter and how to activate welcome. Common mistakes, 18+.',
        'FairPari bonus code — casino code',
        'FairPari bonus code banner'),
    'registration/index.html': M(
        'FairPari registration — claim your bonus',
        'How to register at FairPari and claim welcome: 4 methods, promo fa_1635, verification. 18+.',
        'How to claim a bonus — registration',
        'FairPari registration banner'),
    'login/index.html': M(
        'FairPari login — account and bonuses',
        'FairPari login: sign in, password recovery, bonus account and PROMO section. 18+.',
        'FairPari login — bonus account',
        'FairPari login banner'),
    'payments/index.html': M(
        'FairPari payments — Humo, Payme, Click, UZS',
        'FairPari payments in Uzbekistan: Humo, Uzcard, Payme, Click, crypto. Deposit to activate welcome, 18+.',
        'Payments — bonus activation',
        'FairPari payments UZ banner'),
    'app/index.html': M(
        'FairPari app — APK & mobile bonuses',
        'Download FairPari APK for Android and PWA for iPhone. Mobile bonuses, one balance with the website. 18+.',
        'Mobile app and bonus — APK & iOS',
        'FairPari mobile app banner'),
    'license/index.html': M(
        'FairPari license — bonus safety',
        'FairPari license OGL/2024/1143/0865: bonus safety, KYC and responsible gaming. 18+.',
        'Security, license and responsible gaming',
        'FairPari license and security banner'),
    'faq/index.html': M(
        'FairPari Bonuses FAQ — Casino & Sports',
        'FairPari bonus FAQ: promo code, wagering, dual welcome, no deposit, withdrawal. 18+.',
        'FairPari bonuses FAQ',
        'FairPari FAQ banner'),
    'cookie-policy/index.html': M(
        'Cookie policy — FairPari UZ',
        'FairPari UZ cookie policy: which cookies are used and how to manage them in your browser. 18+.',
        'Cookie policy',
        'FairPari cookie policy banner'),
    'privacy-policy/index.html': M(
        'Privacy policy — FairPari UZ',
        'FairPari UZ privacy policy: what data is collected, cookies, retention and user rights. 18+.',
        'Privacy policy',
        'FairPari privacy policy banner'),
    'terms-of-use/index.html': M(
        'Terms of use — FairPari UZ',
        'Terms of use for FairPari UZ bonus portal: 18+, disclaimer, affiliate links to operator. 18+.',
        'Terms of use',
        'Terms of use banner'),
    'responsible-gaming/index.html': M(
        'Responsible Gaming — FairPari Bonus Portal',
        'Responsible gaming on FairPari bonus portal: 18+ rule, limits, self-exclusion and help resources. 18+.',
        'Responsible gaming',
        'Responsible gaming banner'),
}

# Longest-first phrase replacements
RU_PHRASES = [
    ("FairPari bonuslari — slotlar, live va crash o'yinlar banneri", "Бонусы FairPari — слоты, live и crash, баннер"),
    ("FairPari UZ — kazino va bukmeker platformasi", "FairPari UZ — платформа казино и букмекера"),
    ("kazino va bukmeker platformasi", "платформа казино и букмекера"),
    ("Mustaqil sharh · operator emas", "Независимый обзор · не оператор"),
    ("Onlayn kazino xavfsizligi va mas'uliyatli o'yin banneri", "Безопасность онлайн-казино и ответственная игра — баннер"),
    ("FairPari — Узбекистан uchun onlayn kazino platformasi.", "FairPari — онлайн-казино платформа для Узбекистана."),
    ("FairPari — O'zbekiston uchun onlayn kazino platformasi.", "FairPari — онлайн-казино платформа для Узбекистана."),
    ("bonus portali — welcome, FS va sport aksiyalari.", "бонусный портал — welcome, FS и спортивные акции."),
    ("fairpari-casino-bonuses.com bonus katalogi", "каталог бонусов fairpari-casino-bonuses.com"),
    ("Bosh sahifa", "Главная"),
    ("Kazino bonus", "Бонус казино"),
    ("Sport bonus", "Спорт-бонус"),
    ("Promo kod", "Промокод"),
    ("Depozitsiz", "Без депозита"),
    ("Free spins", "Фриспины"),
    ("Ro'yxatdan", "Регистрация"),
    ("To'lov", "Платежи"),
    ("Mobil", "Мобильное"),
    ("Kirish", "Вход"),
    ("Boshlash", "Начать"),
    ("Faollashtirish", "Активировать"),
    ("Yopish", "Закрыть"),
    ("Yuqoriga", "Наверх"),
    ("Asosiy menyu", "Основное меню"),
    ("Mobil menyu", "Мобильное меню"),
    ("Menyu", "Меню"),
    ("Til", "Язык"),
    ("Huquqiy bo'limlar", "Юридические разделы"),
    ("Maxfiylik siyosati", "Политика конфиденциальности"),
    ("Foydalanish shartlari", "Условия использования"),
    ("Cookie siyosati", "Политика cookie"),
    ("Mas'uliyatli o'yin", "Ответственная игра"),
    ("Maxfiylik", "Конфиденциальность"),
    ("Shartlar", "Условия"),
    ("Bo'limlar", "Разделы"),
    ("Yana", "Ещё"),
    ("Zerkalo", "Зеркало"),
    ("Litsenziya", "Лицензия"),
    ("Yechish", "Вывод"),
    ("Birinchi depozit bonusi", "Бонус первого депозита"),
    ("Start paketi:", "Стартовый пакет:"),
    ("sport bonusi", "спорт-бонус"),
    ("Sport bonusi", "Спорт-бонус"),
    ("bonus kodi", "бонус-код"),
    ("Bonus kodi", "Бонус-код"),
    ("kazino welcome", "казино welcome"),
    ("Kazino welcome", "Казино welcome"),
    ("depozitsiz bonus", "бонус без депозита"),
    ("Depozitsiz bonus", "Бонус без депозита"),
    ("rasmiy holat", "официальный статус"),
    ("frispinlar", "фриспины"),
    ("Frispinlar", "Фриспины"),
    ("qoidalari", "правила"),
    ("qachon beriladi", "когда начисляются"),
    ("qanday faollashtirish", "как активировать"),
    ("qanday activation", "как активировать"),
    ("kiritish joyi", "место ввода"),
    ("xatolardan qochish", "избежание ошибок"),
    ("xavfsiz bonus", "безопасность бонусов"),
    ("xavfsizlik", "безопасность"),
    ("Xavfsizlik", "Безопасность"),
    ("litsenziya", "лицензия"),
    ("mas'uliyatli o'yin", "ответственная игра"),
    ("bonus kabineti", "бонусный кабинет"),
    ("mobil ilova", "мобильное приложение"),
    ("Mobil ilova", "Мобильное приложение"),
    ("ilova va bonus", "приложение и бонус"),
    ("ekspress", "экспресс"),
    ("birinchi depozit", "первый депозит"),
    ("birinchi deposit", "первый депозит"),
    ("welcome va ekspress", "welcome и экспресс"),
    ("nima mavjud", "что доступно"),
    ("nima yo'q", "чего нет"),
    ("Bepul aylantirishlar", "Бесплатные вращения"),
    ("Ro'yxatdan o'tishda", "При регистрации"),
    ("kassada", "в кассе"),
    ("wagering ×35", "wagering ×35"),
    ("O'zbekiston", "Узбекистан"),
    ("o'yinchilari", "игроков"),
    ("o'yinlar", "игры"),
    ("o'yin", "игра"),
    ("slotlar", "слоты"),
    ("Slotlar", "Слоты"),
    ("Sport", "Спорт"),
    ("Kazino", "Казино"),
    ("Bonuslar", "Бонусы"),
    ("To'lovlar", "Платежи"),
    ("Promokod", "Промокод"),
    ("promokod", "промокод"),
    ("depozit", "депозит"),
    ("Depozit", "Депозит"),
    ("депозитsiz", "бездепозитный"),
    ("FairPari депозитsiz bonus", "FairPari бонус без депозита"),
    ("casino code", "код казино"),
    ("Asosiy kontentga o'tish", "Перейти к основному содержанию"),
    ("18+ qoidasi", "Правило 18+"),
    ("O'zini cheklash vositalari", "Инструменты самоограничения"),
    ("Yordam resurslari", "Ресурсы помощи"),
    ("fairpari.com/uz da Kirish", "вход на fairpari.com/uz"),
    ("fairpari bonuslari", "бонусы FairPari"),
    ("bonuslari", "бонусы"),
    ("va ", "и "),
    ("uchun ", "для "),
    ("bilan ", "с "),
    ("haqida ", "о "),
    ("mavjud", "доступно"),
    ("beriladi", "начисляется"),
    ("kiritiladi", "вводится"),
    ("tekshiring", "проверьте"),
    ("olish", "получить"),
    ("Olish", "Получить"),
    ("yechish", "вывод"),
    ("yechib olish", "вывод"),
    ("to'ldirish", "пополнение"),
    ("hisob", "счёт"),
    ("akkaunt", "аккаунт"),
    ("muddat", "срок"),
    ("shartlar", "условия"),
    ("shartlari", "условия"),
    ("qoidalari", "правила"),
    ("afzallik", "преимущество"),
    ("cheklov", "ограничение"),
    ("operator emas", "не оператор"),
    ("mustaqil", "независимый"),
    ("Mustaqil", "Независимый"),
    ("qisqa", "краткий"),
    ("batafsil", "подробно"),
    ("taqqoslash", "сравнение"),
    ("reytingda", "в рейтинге"),
    ("gacha", "до"),
    ("ko'p", "много"),
    ("kam", "мало"),
    ("faqat", "только"),
    ("har doim", "всегда"),
    ("Har doim", "Всегда"),
]

EN_PHRASES = [
    ("FairPari bonusesi — slots, live va crash o'yinlar banneri", "FairPari bonuses — slots, live and crash games banner"),
    ("FairPari bonuslari — slotlar, live va crash o'yinlar banneri", "FairPari bonuses — slots, live and crash games banner"),
    ("FairPari UZ — kazino va bukmeker platformasi", "FairPari UZ — casino and sportsbook platform"),
    ("kazino va bukmeker platformasi", "casino and sportsbook platform"),
    ("Mobile ilova va bonus — APK va iOS", "Mobile app and bonus — APK & iOS"),
    ("FairPari bonus kodi — casino code", "FairPari bonus code — casino code"),
    ("FairPari sport bonusi — birinchi deposit va ekspress", "FairPari sports bonus — first deposit & express"),
    ("FairPari sport bonusi — welcome va ekspress", "FairPari sports bonus — welcome & express"),
    ("FairPari litsenziya — xavfsiz bonus", "FairPari license — bonus safety"),
    ("Xavfsizlik, litsenziya va mas'uliyat", "Security, license and responsible gaming"),
    ("FairPari depositsiz bonus — rasmiy holat", "FairPari no deposit bonus — official status"),
    ("FairPari free spins — qachon beriladi", "FairPari free spins — when credited"),
    ("FairPari free spins — free spins qoidalari", "FairPari free spins — welcome rules"),
    ("FairPari promokod — qanday activation", "FairPari promo code — how to activate"),
    ("FairPari login — bonus kabineti", "FairPari login — bonus account"),
    ("FairPari casino bonus code: fa_1635, kiritish joyi va xatolardan qochish.", "FairPari casino bonus code fa_1635: where to enter and how to avoid mistakes."),
    ("Welcome faollashtirish", "Welcome activation"),
    ("FairPari casino welcome: 19.5M UZS + 150 FS, 4 deposit, wagering ×35. Frispinlar", "FairPari casino welcome: 19.5M UZS + 150 FS, 4 deposits, wagering ×35. Free spins"),
    ("FairPari UZ maxfiylik siyosati: qanday ma'lumotlar to'planadi, cookie, saqlash muddati va foydalanuvchi huquqlari.", "FairPari UZ privacy policy: what data is collected, cookies, retention and user rights."),
    ("FairPari UZ cookie siyosati: qaysi cookie fayllar ishlatiladi va brauzerda ularni boshqarish.", "FairPari UZ cookie policy: which cookie files are used and how to manage them in the browser."),
    ("FairPari bonus FAQ: promokod, wagering, ikki welcome, depositsiz, withdrawal.", "FairPari bonus FAQ: promo code, wagering, dual welcome, no deposit, withdrawal."),
    ("FairPari sport welcome: 1.3M UZS gacha, ekspress aksiyalar, wagering ×5.", "FairPari sports welcome: up to 1.3M UZS, express promos, wagering ×5."),
    ("FairPari promo kod fa_1635: qayerda kiritish, casino welcome va shartlar.", "FairPari promo code fa_1635: where to enter, casino welcome and terms."),
    ("Download FairPari APK for Android and PWA for iPhone. Mobile bonuses, one balanc", "Download FairPari APK for Android and PWA for iPhone. Mobile bonuses, one balance"),
    ("one balans", "one balance"),
    ("Bosh sahifa", "Home"),
    ("Kazino bonus", "Casino bonus"),
    ("Sport bonus", "Sports bonus"),
    ("Promo kod", "Promo code"),
    ("Depozitsiz", "No deposit"),
    ("Ro'yxatdan", "Registration"),
    ("To'lov", "Payments"),
    ("Mobil", "Mobile"),
    ("Kirish", "Login"),
    ("Boshlash", "Get started"),
    ("Faollashtirish", "Activate"),
    ("Yopish", "Close"),
    ("Mas'uliyatli o'yin", "Responsible gaming"),
    ("Maxfiylik siyosati", "Privacy policy"),
    ("Foydalanish shartlari", "Terms of use"),
    ("Cookie siyosati", "Cookie policy"),
    ("frispinlar", "free spins"),
    ("Frispinlar", "Free spins"),
    ("litsenziya", "license"),
    ("promokod", "promo code"),
    ("depozitsiz", "no deposit"),
    ("depositsiz", "no deposit"),
    ("rasmiy holat", "official status"),
    ("qoidalari", "rules"),
    ("qachon", "when"),
    ("beriladi", "credited"),
    ("qanday", "how"),
    ("kiritish", "enter"),
    ("xavfsiz", "safe"),
    ("kabineti", "account"),
    ("ilova", "app"),
    ("ekspress", "express"),
    ("birinchi", "first"),
    ("va ", "and "),
    ("uchun ", "for "),
    ("bilan ", "with "),
    ("gacha", "up to"),
    ("O'zbekiston", "Uzbekistan"),
    ("o'yin", "game"),
    ("o'yinlar", "games"),
    ("slotlar", "slots"),
    ("bonuslari", "bonuses"),
    ("bonus kodi", "bonus code"),
    ("sport bonusi", "sports bonus"),
    ("nima mavjud", "what is available"),
    ("mavjud", "available"),
    ("shartlar", "terms"),
    ("muddat", "deadline"),
    ("hisob", "account"),
    ("depozit", "deposit"),
    ("yechish", "withdrawal"),
    ("mustaqil", "independent"),
    ("operator emas", "not an operator"),
]

RU_PHRASES.sort(key=lambda x: len(x[0]), reverse=True)
EN_PHRASES.sort(key=lambda x: len(x[0]), reverse=True)

RU_NAV_FOOTER = [
    ('aria-label="Asosiy menyu"', 'aria-label="Основное меню"'),
    ('aria-label="Mobil menyu"', 'aria-label="Мобильное меню"'),
    ('aria-label="Til"', 'aria-label="Язык"'),
    ('aria-label="Huquqiy bo\'limlar"', 'aria-label="Юридические разделы"'),
    ('aria-label="Breadcrumb"><a href="../">Bosh sahifa</a>', 'aria-label="Хлебные крошки"><a href="../">Главная</a>'),
    ('aria-label="Breadcrumb"><a href="../../">Bosh sahifa</a>', 'aria-label="Хлебные крошки"><a href="../../">Главная</a>'),
    ('footer-lang" href="../">Русская версия</a>', 'footer-lang" href="../">Узбекская версия</a>'),
    ('footer-lang" href="../ru/">Русская версия</a>', 'footer-lang" href="../">Узбекская версия</a>'),
]

EN_NAV_FOOTER = [
    ('aria-label="Asosiy menyu"', 'aria-label="Main menu"'),
    ('aria-label="Mobil menyu"', 'aria-label="Mobile menu"'),
    ('aria-label="Til"', 'aria-label="Language"'),
    ('aria-label="Huquqiy bo\'limlar"', 'aria-label="Legal sections"'),
    ('aria-label="Breadcrumb"><a href="../">Bosh sahifa</a>', 'aria-label="Breadcrumb"><a href="../">Home</a>'),
    ('>Kirish<', '>Login<'),
    ('>Boshlash<', '>Get started<'),
    ('>Faollashtirish<', '>Activate<'),
    ('>Yopish<', '>Close<'),
    ('Start paketi:', 'Welcome pack:'),
    ('Birinchi depozit bonusi', 'First deposit bonus'),
]

def esc_attr(s):
    return html_lib.escape(s, quote=True)

def apply_meta(html, meta):
    html = re.sub(r'<title>.*?</title>', f'<title>{meta["title"]}</title>', html, count=1, flags=re.S)
    html = re.sub(r'<meta name="description" content="[^"]*"', f'<meta name="description" content="{esc_attr(meta["description"])}"', html, count=1)
    html = re.sub(r'property="og:title" content="[^"]*"', f'property="og:title" content="{esc_attr(meta["og_title"])}"', html)
    html = re.sub(r'property="og:description" content="[^"]*"', f'property="og:description" content="{esc_attr(meta["og_desc"])}"', html)
    html = re.sub(r'name="twitter:title" content="[^"]*"', f'name="twitter:title" content="{esc_attr(meta["tw_title"])}"', html)
    html = re.sub(r'name="twitter:description" content="[^"]*"', f'name="twitter:description" content="{esc_attr(meta["tw_desc"])}"', html)
    html = re.sub(r'property="og:image:alt" content="[^"]*"', f'property="og:image:alt" content="{esc_attr(meta["og_alt"])}"', html)
    html = re.sub(r'name="twitter:image:alt" content="[^"]*"', f'name="twitter:image:alt" content="{esc_attr(meta["tw_alt"])}"', html)
    # H1
    html = re.sub(r'(<h1[^>]*>)(.*?)(</h1>)', lambda m: m.group(1) + meta['h1'] + m.group(3), html, count=1, flags=re.S)
    # JSON-LD name/headline/description
    html = html.replace('"inLanguage": "uz-UZ"', '"inLanguage": "ru-UZ"')
    for field in ('name', 'headline', 'description'):
        # only replace in webpage article block roughly
        pass
    html = re.sub(r'"name": "Mas\'uliyatli o\'yin"', '"name": "Ответственная игра"', html)
    html = re.sub(r'"headline": "Mas\'uliyatli o\'yin[^"]*"', f'"headline": "{meta["title"]}"', html)
    return html

def apply_phrases(html, phrases):
    for uz, target in phrases:
        html = html.replace(uz, target)
    return html

def fix_hreflang_legal(html, uz, ru, en):
    block = f'''    <link rel="alternate" hreflang="uz-UZ" href="https://{DOMAIN}{uz}" />
    <link rel="alternate" hreflang="ru-UZ" href="https://{DOMAIN}{ru}" />
    <link rel="alternate" hreflang="en-UZ" href="https://{DOMAIN}{en}" />
    <link rel="alternate" hreflang="x-default" href="https://{DOMAIN}{uz}" />'''
    html = re.sub(r'\s*<link rel="alternate" hreflang="[^"]*" href="[^"]*" />\s*', '\n', html)
    html = re.sub(r'(<link rel="canonical" href="[^"]*" />)', r'\1\n\n\n\n' + block, html, count=1)
    # fix wrong en responsible-gambling -> responsible-gaming
    html = html.replace('/en/responsible-gambling/', '/en/responsible-gaming/')
    return html

def detect_uz_in_ru_en(text, lang):
    """Flag latin uz patterns in ru/en pages"""
    if lang.startswith('ru'):
        # cyrillic should dominate; flag common uz latin
        uz_pat = re.compile(r"\b(siyosati|shartlari|qanday|birinchi|depozit|ekspre|kabineti|ilova|faollashtirish|kiritish|frispinlar|bonuslari|promokod|mas'uliyatli|foydalanish|maxfiylik|royxatdan|tolov|litsenziya|xavfsiz|mavjud|beriladi|uchun|bilan|haqida|o'yin|o'zbekiston|gacha|va ekspress)\b", re.I)
    else:
        uz_pat = re.compile(r"\b(siyosati|shartlari|qanday|birinchi|ilova|kabineti|kiritish|frispinlar|litsenziya|xavfsiz|promokod|depozitsiz|rasmiy|holat|ekspress|sport bonusi|bonus kodi|mas'uliyatli|o'yin|gacha|beriladi|mavjud)\b", re.I)
    return uz_pat.findall(text)

def process_lang(lang_prefix, meta_dict, phrases, nav_footer):
    issues_after = []
    for rel, meta in meta_dict.items():
        path = ROOT / lang_prefix / rel
        if not path.exists():
            print('MISSING', path)
            continue
        html = path.read_text(encoding='utf-8')
        lang = re.search(r'lang="([^"]+)"', html)
        lang = lang.group(1) if lang else lang_prefix + '-UZ'

        html = apply_meta(html, meta)
        html = apply_phrases(html, phrases)
        for a, b in nav_footer:
            html = html.replace(a, b)

        # legal hreflang
        for key, (uz, ru, en) in LEGAL_HREFLANG.items():
            if key.replace('-', '') in rel.replace('/', '') or key in rel:
                target = uz if lang_prefix == 'masuliyatli' else None
            if 'politika-cookie' in rel or 'cookie-policy' in rel:
                html = fix_hreflang_legal(html, *LEGAL_HREFLANG['cookie-siyosati'])
            elif 'politika-konfidentsialnosti' in rel or 'privacy-policy' in rel:
                html = fix_hreflang_legal(html, *LEGAL_HREFLANG['maxfiylik-siyosati'])
            elif 'usloviya' in rel or 'terms-of-use' in rel:
                html = fix_hreflang_legal(html, *LEGAL_HREFLANG['foydalanish-shartlari'])
            elif 'otvetstvennaya' in rel or 'responsible-gaming' in rel:
                html = fix_hreflang_legal(html, *LEGAL_HREFLANG['masuliyatli-oyin'])

        # responsible gaming body fix EN
        if rel == 'responsible-gaming/index.html':
            html = re.sub(r'<h1[^>]*>.*?</h1>', '<h1 class="section__title">Responsible gaming</h1>', html, count=1, flags=re.S)
            body = '''<h2 id="18-rule">18+ rule</h2><p>Bonus portal: FairPari is for adults 18+ only. Underage accounts are closed; funds may be returned.</p>
<h2 id="self-limits">Self-limitation tools</h2><p>Deposit limits, session time limits, timeouts and self-exclusion are available in account settings or via support.</p>
<h2 id="help">Help resources</h2><p>If gambling feels out of control, contact a professional or organizations such as BeGambleAware. Gambling can cause debt and family problems — asking for help is normal.</p>'''
            html = re.sub(r'<h1 class="section__title">Responsible gaming</h1>.*?</div></section>', f'<h1 class="section__title">Responsible gaming</h1>{body}</div></section>', html, count=1, flags=re.S)

        if rel == 'otvetstvennaya-igra/index.html':
            body = '''<h2 id="18-rule">Правило 18+</h2><p>Бонусный портал: FairPari только для лиц 18+. Аккаунты несовершеннолетних закрываются, средства могут быть возвращены.</p>
<h2 id="self-limits">Инструменты самоограничения</h2><p>Лимиты депозита, ограничение сессии, тайм-аут и самоисключение доступны в настройках аккаунта или через поддержку.</p>
<h2 id="help">Ресурсы помощи</h2><p>Если игра выходит из-под контроля, обратитесь к специалисту или организациям вроде BeGambleAware. Азартные игры могут привести к долгам — просить помощь нормально.</p>'''
            html = re.sub(r'<h1 class="section__title">Ответственная игра</h1>.*?</div></section>', f'<h1 class="section__title">Ответственная игра</h1>{body}</div></section>', html, count=1, flags=re.S)
            html = html.replace('"inLanguage": "uz-UZ"', '"inLanguage": "ru-UZ"')

        path.write_text(html, encoding='utf-8')
        found = detect_uz_in_ru_en(html, lang_prefix)
        if found:
            issues_after.append((rel, sorted(set(found))[:8]))
        print('OK', lang_prefix, rel)

    return issues_after

def fix_uz_hreflang_en():
  for uz_path, (_, _, en) in LEGAL_HREFLANG.items():
    p = ROOT / uz_path / 'index.html'
    if p.exists():
      html = p.read_text(encoding='utf-8')
      html = html.replace('/en/responsible-gambling/', '/en/responsible-gaming/')
      p.write_text(html, encoding='utf-8')

if __name__ == '__main__':
    fix_uz_hreflang_en()
    ru_issues = process_lang('ru', RU_META, RU_PHRASES, RU_NAV_FOOTER)
    en_issues = process_lang('en', EN_META, EN_PHRASES, EN_NAV_FOOTER)
    print('\n=== RU remaining uz tokens ===')
    for i in ru_issues:
        print(i)
    print('\n=== EN remaining uz tokens ===')
    for i in en_issues:
        print(i)
    print(f'\nRU files with issues: {len(ru_issues)}')
    print(f'EN files with issues: {len(en_issues)}')

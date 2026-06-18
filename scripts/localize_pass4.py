#!/usr/bin/env python3
"""Pass 4: alt texts, FAQ schema, feature cards, remaining mixed phrases."""
import re
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

RU_PHRASES = [
    (' banneri', ' — баннер'),
    ('banneri:', 'баннер:'),
    ('Xush kelibsiz paket', 'Welcome-пакет'),
    ('xush kelibsiz paket', 'welcome-пакет'),
    ('frispin', 'фриспин'),
    ('Mahalliy касса', 'Локальная касса'),
    ('Himoya', 'Защита'),
    ('Rasmiy manzil', 'Официальный адрес'),
    ('Rasmiy UZ sayti qaysi?', 'Какой официальный сайт UZ?'),
    ('FairPari Узбекистанda ishlaydimi?', 'Работает ли FairPari в Узбекистане?'),
    ('Brend xalqaro лицензия asosida faoliyat yuritishini ko\'rsatadi. Mahalliy qonun-qoidalarni независимый проверьте.', 'Бренд указывает международную лицензию. Местные правила проверяйте самостоятельно.'),
    ('Login как?', 'Как войти?'),
    ('fairpari.com/uz da Вход — email/telefon yoki ijtimoiy tarmoq. APK/PWA da bir xil.', 'На fairpari.com/uz вход по email/телефону или соцсетям. В APK/PWA то же.'),
    ('APK qayerdan?', 'Откуда скачать APK?'),
    ('fairpari.com/uz/mobile — boshqa manbalarот yuklamang.', 'fairpari.com/uz/mobile — не скачивайте из других источников.'),
    ('Промокод qayerda?', 'Где ввести промокод?'),
    ('Регистрацияda yoki в кассе; только rasmiy PROMO.', 'При регистрации или в кассе; только официальный PROMO.'),
    ('Qaysi welcome?', 'Какой welcome?'),
    ('Казино 19.5M+150 FS yoki sport 1.3M — bir vaqtda bittasi.', 'Казино 19,5M+150 FS или спорт 1,3M — одновременно один.'),
    ('To\'ldirish usullari?', 'Способы пополнения?'),
    ('Wagering ×35 — ~7 kun; max bet cheklangan', 'Wagering ×35 — ~7 дней; макс. ставка ограничена'),
    ('Keshbek и reload — alohida PROMO', 'Кешбэк и reload — отдельный PROMO'),
    ('amal qilish срокi FairPari da tekshiriladi', 'срок действия проверяйте в FairPari'),
    ('Jami paket', 'Итого пакет'),
    ('o\'yinlar banneri', 'игры — баннер'),
    ('crash o&#x27;yinlar banneri', 'crash-игры — баннер'),
    ('crash игры banneri', 'crash-игры — баннер'),
    ('mobil kazino banneri', 'мобильное казино — баннер'),
    ('VIP cashback banneri', 'VIP кешбэк — баннер'),
    ('11 foiz kazino qaytarimi', '11% казино кешбэк'),
    ('Вход qo\'llanma', 'Руководство по входу'),
    ('FairPari kazino', 'FairPari казино'),
    ('Zerkalo', 'Зеркало'),
    ('Ro\'yxat', 'Регистрация'),
    ('Akkaunt', 'Аккаунт'),
    ('Ruxsat', 'Разрешение'),
    ('Pasport', 'Паспорт'),
    ('Kassa', 'Касса'),
    ('Balans', 'Баланс'),
    ('Parol', 'Пароль'),
    ('Tez', 'Быстро'),
    ('Ishchi', 'Рабочий'),
    ('Noma\'lum', 'Неизвестный'),
    ('O\'rnatish', 'Установка'),
    ('Push', 'Push-уведомления'),
    ('Translyatsiya', 'Трансляция'),
    ('cheklangan', 'ограничено'),
    ('mumkin', 'возможно'),
    ('qilish', 'сделать'),
    ('paket', 'пакет'),
    ('bosh', 'главная'),
    ('himoya', 'защита'),
    ('limit', 'лимит'),
    ('chat', 'чат'),
    ('slot', 'слот'),
    ('operator', 'оператор'),
]

EN_PHRASES = [
    (' banneri', ' banner'),
    ('banneri:', 'banner:'),
    ('Xush kelibsiz paket', 'Welcome package'),
    ('xush kelibsiz paket', 'welcome package'),
    ('frispin', 'free spin'),
    ('Mahalliy', 'Local'),
    ('Himoya', 'Security'),
    ('Rasmiy', 'Official'),
    ('rasmiy', 'official'),
    ('Zerkalo', 'Mirror'),
    ('Ro\'yxat', 'Sign up'),
    ('Akkaunt', 'Account'),
    ('akkaunt', 'account'),
    ('Ruxsat', 'Permission'),
    ('Pasport', 'Passport'),
    ('Kassa', 'Cashier'),
    ('Balans', 'Balance'),
    ('Parol', 'Password'),
    ('Tez', 'Fast'),
    ('Ishchi', 'Working'),
    ('Noma\'lum', 'Unknown'),
    ('O\'rnatish', 'Install'),
    ('Translyatsiya', 'Stream'),
    ('cheklangan', 'limited'),
    ('mumkin', 'possible'),
    ('qilish', 'do'),
    ('paket', 'package'),
    ('himoya', 'protection'),
    ('Wagering ×35 — ~7 kun', 'Wagering ×35 — ~7 days'),
    ('Keshbek', 'Cashback'),
    ('alohida', 'separate'),
    ('amal qilish', 'validity'),
    ('Jami paket', 'Total package'),
    ('o\'yinlar', 'games'),
    ('mobil kazino', 'mobile casino'),
    ('foiz kazino qaytarimi', '% casino cashback'),
    ('FairPari Узбекистанda ishlaydimi?', 'Does FairPari work in Uzbekistan?'),
    ('Brend xalqaro', 'The brand operates under international'),
    ('Mahalliy qonun', 'Check local laws'),
    ('Login как?', 'How to log in?'),
    ('ijtimoiy tarmoq', 'social networks'),
    ('bir xil', 'the same'),
    ('APK qayerdan?', 'Where to download APK?'),
    ('boshqa manbalarот yuklamang', 'do not download from other sources'),
    ('Промокод qayerda?', 'Where to enter promo code?'),
    ('Регистрацияda', 'At registration'),
    ('Qaysi welcome?', 'Which welcome?'),
    ('bir vaqtda bittasi', 'only one at a time'),
    ('To\'ldirish usullari?', 'Deposit methods?'),
    ('casino ro\'yxatfrom o\'tish', 'casino registration'),
    ('Casino akkaunti', 'Casino account'),
    ('xush kelibsiz', 'welcome'),
    ('bonusesi banneri', 'bonus banner'),
    ('registration banneri', 'registration banner'),
]

def apply_phrases(html, phrases):
    phrases = sorted(phrases, key=lambda x: len(x[0]), reverse=True)
    for a, b in phrases:
        # skip replacements inside href/src attributes for path-like strings
        if '/' in a and 'http' not in a:
            continue
        html = html.replace(a, b)
    return html

def fix_related_links_ru(html):
    html = html.replace('Слоты katalogi', 'Каталог слотов')
    html = html.replace('janr и provayder bo\'yicha', 'по жанру и провайдеру')
    html = html.replace('Live kazino', 'Live-казино')
    html = html.replace('Ruletka, blackjack и game show stollari', 'Рулетка, блэкджек и game show')
    html = html.replace('Мобильное kazino', 'Мобильное казино')
    html = html.replace('slot cho\'ntakda', 'слоты в кармане')
    html = html.replace('sрокlar и Humo/Click', 'сроки и Humo/Click')
    html = html.replace('O\'yinchilar fikri', 'Мнения игроков')
    html = html.replace('Slot и вывод tajribasi', 'Слоты и опыт вывода')
    html = html.replace('boshqalar', 'и другие')
    html = html.replace('Translyatsiya sifati', 'Качество трансляции')
    html = html.replace('Мобильное to\'lov', 'Мобильные платежи')
    html = html.replace('Click/Payme приложениеda', 'Click/Payme в приложении')
    html = html.replace('Мобильное login', 'Мобильный вход')
    html = html.replace('Biometriya и 2FA', 'Биометрия и 2FA')
    html = html.replace('Мобильное zerkalo', 'Мобильное зеркало')
    html = html.replace('Ishchi manzil', 'Рабочий адрес')
    html = html.replace('Мобильное slot', 'Мобильные слоты')
    html = html.replace('Sweet Bonanza и boshqalar', 'Sweet Bonanza и другие')
    return html

def fix_related_links_en(html):
    html = html.replace('katalogi', 'catalog')
    html = html.replace('bo\'yicha', 'by')
    html = html.replace('stollari', 'tables')
    html = html.replace('cho\'ntakda', 'in your pocket')
    html = html.replace('tajribasi', 'experience')
    html = html.replace('sрокlar', 'deadlines')
    html = html.replace('boshqalar', 'and more')
    html = html.replace('sifati', 'quality')
    html = html.replace('to\'lov', 'payments')
    html = html.replace('ilovada', 'in the app')
    html = html.replace('manzil', 'address')
    return html

if __name__ == '__main__':
    for p in sorted((ROOT/'ru').rglob('*.html')):
        h = p.read_text(encoding='utf-8')
        h = apply_phrases(h, RU_PHRASES)
        h = fix_related_links_ru(h)
        p.write_text(h, encoding='utf-8')
    for p in sorted((ROOT/'en').rglob('*.html')):
        h = p.read_text(encoding='utf-8')
        h = apply_phrases(h, EN_PHRASES)
        h = fix_related_links_en(h)
        p.write_text(h, encoding='utf-8')
    print('Pass 4 done')

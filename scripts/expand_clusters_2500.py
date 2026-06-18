#!/usr/bin/env python3
"""Expand FairPari cluster index.html pages to >=2520 visible words (stdlib only)."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parent.parent
TARGET_WORDS = 2520
WORD_BUFFER = 100
LEGAL_FRAGMENTS = (
    "cookie",
    "politika",
    "maxfiylik",
    "foydalanish",
    "masuliyat",
    "terms",
    "privacy",
    "responsible",
)

SLUGS: dict[str, dict[str, str]] = {
    "uz": {
        "kazino": "kazino-bonuslari",
        "sport": "sport-bonuslari",
        "depozitsiz": "depozitsiz-bonus",
        "free-spins": "free-spins",
        "bonus-kod": "bonus-kodi",
        "faq": "faq",
        "registratsiya": "royxatdan-otish",
        "kirish": "kirish",
        "mobil": "mobil",
        "tolov": "tolov",
        "litsenziya": "litsenziya",
        "promo": "promo-kod",
        "index": "",
    },
    "ru": {
        "kazino": "bonusy-kazino",
        "sport": "sport-bonusy",
        "depozitsiz": "bonus-bez-depozita",
        "free-spins": "free-spins",
        "bonus-kod": "bonus-kod",
        "faq": "faq",
        "registratsiya": "registratsiya",
        "kirish": "vhod",
        "mobil": "skachat",
        "tolov": "oplata",
        "litsenziya": "litsenziya",
        "promo": "promokod",
        "index": "",
    },
    "en": {
        "kazino": "casino-bonuses",
        "sport": "sports-bonuses",
        "depozitsiz": "no-deposit-bonus",
        "free-spins": "free-spins",
        "bonus-kod": "bonus-code",
        "faq": "faq",
        "registratsiya": "registration",
        "kirish": "login",
        "mobil": "app",
        "tolov": "payments",
        "litsenziya": "license",
        "promo": "promo-code",
        "index": "",
    },
}

PATH_TO_META: dict[str, tuple[str, str]] = {
    "index.html": ("index", "uz"),
    "ru/index.html": ("index", "ru"),
    "en/index.html": ("index", "en"),
    "kazino-bonuslari/index.html": ("kazino", "uz"),
    "ru/bonusy-kazino/index.html": ("kazino", "ru"),
    "en/casino-bonuses/index.html": ("kazino", "en"),
    "sport-bonuslari/index.html": ("sport", "uz"),
    "ru/sport-bonusy/index.html": ("sport", "ru"),
    "en/sports-bonuses/index.html": ("sport", "en"),
    "depozitsiz-bonus/index.html": ("depozitsiz", "uz"),
    "ru/bonus-bez-depozita/index.html": ("depozitsiz", "ru"),
    "en/no-deposit-bonus/index.html": ("depozitsiz", "en"),
    "free-spins/index.html": ("free-spins", "uz"),
    "ru/free-spins/index.html": ("free-spins", "ru"),
    "en/free-spins/index.html": ("free-spins", "en"),
    "bonus-kodi/index.html": ("bonus-kod", "uz"),
    "ru/bonus-kod/index.html": ("bonus-kod", "ru"),
    "en/bonus-code/index.html": ("bonus-kod", "en"),
    "promo-kod/index.html": ("promo", "uz"),
    "ru/promokod/index.html": ("promo", "ru"),
    "en/promo-code/index.html": ("promo", "en"),
    "royxatdan-otish/index.html": ("registratsiya", "uz"),
    "ru/registratsiya/index.html": ("registratsiya", "ru"),
    "en/registration/index.html": ("registratsiya", "en"),
    "kirish/index.html": ("kirish", "uz"),
    "ru/vhod/index.html": ("kirish", "ru"),
    "en/login/index.html": ("kirish", "en"),
    "mobil/index.html": ("mobil", "uz"),
    "ru/skachat/index.html": ("mobil", "ru"),
    "en/app/index.html": ("mobil", "en"),
    "tolov/index.html": ("tolov", "uz"),
    "ru/oplata/index.html": ("tolov", "ru"),
    "en/payments/index.html": ("tolov", "en"),
    "litsenziya/index.html": ("litsenziya", "uz"),
    "ru/litsenziya/index.html": ("litsenziya", "ru"),
    "en/license/index.html": ("litsenziya", "en"),
    "faq/index.html": ("faq", "uz"),
    "ru/faq/index.html": ("faq", "ru"),
    "en/faq/index.html": ("faq", "en"),
}

SECTION_HEADERS: dict[tuple[str, str], tuple[str, str, str]] = {
    ("index", "uz"): ("Bonus markazi", "FairPari O'zbekiston bonuslari", "Welcome, sport va promo fa_1635"),
    ("index", "ru"): ("Бонусный центр", "Бонусы FairPari Узбекистан", "Welcome, спорт и промокод fa_1635"),
    ("index", "en"): ("Bonus hub", "FairPari Uzbekistan bonuses", "Welcome, sports and promo fa_1635"),
    ("kazino", "uz"): ("Kazino qo'llanma", "FairPari kazino bonuslari", "20.2M UZS + 150 FS, wagering ×35"),
    ("kazino", "ru"): ("Гид по казино", "Бонусы казино FairPari", "20,2 млн UZS + 150 FS, отыгрыш ×35"),
    ("kazino", "en"): ("Casino guide", "FairPari casino bonuses", "20.2M UZS + 150 FS, wagering ×35"),
    ("sport", "uz"): ("Sport qo'llanma", "FairPari sport bonuslari", "1.4M UZS, ekspress ×5"),
    ("sport", "ru"): ("Спорт-гид", "Спорт-бонусы FairPari", "1,4 млн UZS, экспресс ×5"),
    ("sport", "en"): ("Sports guide", "FairPari sports bonuses", "1.4M UZS, accumulator ×5"),
    ("depozitsiz", "uz"): ("Depozitsiz", "FairPari depozitsiz bonus", "Alternativa va welcome"),
    ("depozitsiz", "ru"): ("Бездепозит", "Бонус без депозита FairPari", "Альтернатива и welcome"),
    ("depozitsiz", "en"): ("No deposit", "FairPari no-deposit bonus", "Alternatives and welcome"),
    ("free-spins", "uz"): ("Frispinlar", "FairPari bepul aylantirishlar", "150 FS welcome tarkibida"),
    ("free-spins", "ru"): ("Фриспины", "Бесплатные вращения FairPari", "150 FS в welcome"),
    ("free-spins", "en"): ("Free spins", "FairPari free spins", "150 FS in welcome pack"),
    ("bonus-kod", "uz"): ("Bonus kodi", "FairPari bonus kodi", "fa_1635 faollashtirish"),
    ("bonus-kod", "ru"): ("Бонус-код", "Бонус-код FairPari", "Активация fa_1635"),
    ("bonus-kod", "en"): ("Bonus code", "FairPari bonus code", "Activating fa_1635"),
    ("promo", "uz"): ("Promo kod", "FairPari promo-kod fa_1635", "Ro'yxatdan o'tish va depozit"),
    ("promo", "ru"): ("Промокод", "Промокод FairPari fa_1635", "Регистрация и депозит"),
    ("promo", "en"): ("Promo code", "FairPari promo code fa_1635", "Registration and deposit"),
    ("registratsiya", "uz"): ("Ro'yxatdan o'tish", "FairPari akkaunt ochish", "Bonus tanlash va fa_1635"),
    ("registratsiya", "ru"): ("Регистрация", "Создание аккаунта FairPari", "Выбор бонуса и fa_1635"),
    ("registratsiya", "en"): ("Registration", "FairPari account signup", "Bonus choice and fa_1635"),
    ("kirish", "uz"): ("Kirish", "FairPari akkauntga kirish", "Balans va bonus kuzatuvi"),
    ("kirish", "ru"): ("Вход", "Вход в аккаунт FairPari", "Баланс и отслеживание бонуса"),
    ("kirish", "en"): ("Login", "FairPari account login", "Balance and bonus tracking"),
    ("mobil", "uz"): ("Mobil", "FairPari mobil ilova", "Bonuslar telefonda"),
    ("mobil", "ru"): ("Мобильное", "Мобильное приложение FairPari", "Бонусы на телефоне"),
    ("mobil", "en"): ("Mobile", "FairPari mobile app", "Bonuses on your phone"),
    ("tolov", "uz"): ("To'lov", "FairPari to'lov va yechish", "Humo, Uzcard, Payme, Click"),
    ("tolov", "ru"): ("Оплата", "Пополнение и вывод FairPari", "Humo, Uzcard, Payme, Click"),
    ("tolov", "en"): ("Payments", "FairPari deposits and withdrawals", "Humo, Uzcard, Payme, Click"),
    ("litsenziya", "uz"): ("Litsenziya", "FairPari litsenziya va xavfsizlik", "Mas'uliyatli o'yin 18+"),
    ("litsenziya", "ru"): ("Лицензия", "Лицензия и безопасность FairPari", "Ответственная игра 18+"),
    ("litsenziya", "en"): ("Licence", "FairPari licence and safety", "Responsible play 18+"),
    ("faq", "uz"): ("FAQ", "FairPari bonus savollari", "Welcome, wagering, to'lov"),
    ("faq", "ru"): ("FAQ", "Вопросы о бонусах FairPari", "Welcome, отыгрыш, оплата"),
    ("faq", "en"): ("FAQ", "FairPari bonus questions", "Welcome, wagering, payments"),
}


def href(lang: str, page_key: str, target: str) -> str:
    prefix = "" if page_key == "index" else "../"
    slug = SLUGS[lang][target]
    if not slug:
        return "./" if page_key == "index" else "../"
    return f"{prefix}{slug}/"


def link(lang: str, page_key: str, target: str, text: str) -> str:
    return f'<a class="text-link" href="{href(lang, page_key, target)}">{text}</a>'


def strip_scripts(html: str) -> str:
    return re.sub(r"<script[^>]*>.*?</script>", " ", html, flags=re.I | re.S)


def strip_tags(html: str) -> str:
    return re.sub(r"<[^>]+>", " ", html)


def count_words(html: str) -> int:
    text = strip_tags(strip_scripts(html))
    return len(text.split())


def is_legal(rel: str) -> bool:
    low = rel.lower()
    return any(fragment in low for fragment in LEGAL_FRAGMENTS)


def find_injection_index(text: str) -> int | None:
    marker = 'id="related-pages"'
    idx = text.find(marker)
    if idx == -1:
        return None
    sec = text.rfind("<section", 0, idx)
    return sec if sec != -1 else None


def article_html(h2: str, paragraphs: list[str], block_id: int) -> str:
    paras = "".join(f"<p>{p}</p>" for p in paragraphs)
    return (
        f'<article class="seo-block seo-block--rich">'
        f'<h2 id="seo-exp-{block_id}">{h2}</h2>{paras}</article>'
    )


ArticleFn = Callable[[str, str, Callable[[str], str]], tuple[str, list[str]]]


def _h(lang: str, pk: str) -> Callable[[str], str]:
    return lambda t: link(lang, pk, t, {
        "kazino": {"uz": "kazino bonuslari", "ru": "бонусы казино", "en": "casino bonuses"}[lang],
        "sport": {"uz": "sport bonuslari", "ru": "спорт-бонусы", "en": "sports bonuses"}[lang],
        "depozitsiz": {"uz": "depozitsiz bonus", "ru": "бонус без депозита", "en": "no-deposit bonus"}[lang],
        "free-spins": {"uz": "frispinlar", "ru": "фриспины", "en": "free spins"}[lang],
        "bonus-kod": {"uz": "bonus kodi", "ru": "бонус-код", "en": "bonus code"}[lang],
        "promo": {"uz": "promo-kod", "ru": "промокод", "en": "promo code"}[lang],
        "registratsiya": {"uz": "ro'yxatdan o'tish", "ru": "регистрация", "en": "registration"}[lang],
        "kirish": {"uz": "kirish", "ru": "вход", "en": "login"}[lang],
        "mobil": {"uz": "mobil ilova", "ru": "приложение", "en": "mobile app"}[lang],
        "tolov": {"uz": "to'lov usullari", "ru": "оплата", "en": "payments"}[lang],
        "litsenziya": {"uz": "litsenziya", "ru": "лицензия", "en": "licence"}[lang],
        "faq": {"uz": "FAQ", "ru": "FAQ", "en": "FAQ"}[lang],
    }.get(t, t))


# ---------------------------------------------------------------------------
# Shared article factories (topic-tagged)
# ---------------------------------------------------------------------------

def _art_welcome_casino(lang: str, pk: str, h: Callable[[str], str]) -> tuple[str, list[str]]:
    if lang == "uz":
        return (
            "Kazino welcome — 20.2M UZS va 150 frispin",
            [
                f"FairPari kazino welcome paketi O'zbekiston o'yinchilari uchun eng katta takliflardan biri: "
                f"birinchi to'rt depozitda jami <strong>20 200 000 UZS + 150 bepul aylantirish</strong>. "
                f"Har bir bosqich PROMO kartochkasida alohida foiz va FS soni bilan ko'rsatiladi. "
                f"Promokod <strong>fa_1635</strong> {h('registratsiya')} yoki depozitda kiritilishi kerak.",
                f"Welcome faqat slot yo'nalishi uchun mo'ljallangan: sport paketi "
                f"({h('sport')}) bilan birinchi depozitda bir vaqtda tanlab bo'lmaydi. "
                f"Wagering kazino bonusida <strong>×35</strong> — ya'ni bonus summasini "
                f"qoidalarga mos slotlarda aylantirish talab etiladi. Muddat odatda 7–30 kun.",
                f"150 frispin odatda belgilangan o'yinlarga bo'linadi; ularning yutug'i bonus balansiga "
                f"tushadi va alohida aylantirish talab qilinishi mumkin. Max bet va taqiqlangan o'yinlar "
                f"ro'yxati PROMO footnote da. {h('free-spins')} sahifasida FS mexanikasi batafsil.",
                f"Depozit {h('tolov')} orqali Humo, Uzcard, Payme yoki Click bilan amalga oshiriladi. "
                f"Minimal summa taxminan 130 000 UZS atrofida. Bonus faollashgach {h('kirish')} orqali "
                f"progressni kuzating; savollar uchun {h('faq')} bo'limiga murojaat qiling.",
            ],
        )
    if lang == "ru":
        return (
            "Казино welcome — 20,2 млн UZS и 150 FS",
            [
                f"Приветственный пакет казино FairPari для Узбекистана: на первые четыре депозита до "
                f"<strong>20 200 000 UZS + 150 фриспинов</strong>. Каждый этап указан в карточке PROMO. "
                f"Промокод <strong>fa_1635</strong> вводится при {h('registratsiya')} или депозите.",
                f"Welcome только для казино: со {h('sport')} на первом депозите выбирается одно направление. "
                f"Отыгрыш казино — <strong>×35</strong> на слотах, срок обычно 7–30 дней.",
                f"150 FS начисляются на выбранные слоты; выигрыш с них идёт на бонусный баланс. "
                f"Max bet и исключённые игры — в footnote PROMO. Подробнее на странице {h('free-spins')}.",
                f"Пополнение через {h('tolov')}: Humo, Uzcard, Payme, Click. Минимум около 130 000 UZS. "
                f"Следите за прогрессом через {h('kirish')}; вопросы — в {h('faq')}.",
            ],
        )
    return (
        "Casino welcome — 20.2M UZS and 150 FS",
        [
            f"FairPari casino welcome for Uzbekistan spans the first four deposits: up to "
            f"<strong>20,200,000 UZS + 150 free spins</strong>. Each stage is shown on the PROMO card. "
            f"Enter promo code <strong>fa_1635</strong> at {h('registratsiya')} or deposit.",
            f"Welcome is casino-only: you cannot combine it with the {h('sport')} pack on the first deposit. "
            f"Casino wagering is <strong>×35</strong> on eligible slots, usually within 7–30 days.",
            f"The 150 FS are split across designated games; winnings credit the bonus balance. "
            f"Max bet and excluded titles are listed in PROMO footnotes. See {h('free-spins')} for mechanics.",
            f"Fund via {h('tolov')} using Humo, Uzcard, Payme, or Click. Minimum is around 130,000 UZS. "
            f"Track progress after {h('kirish')}; use {h('faq')} for common questions.",
        ],
    )


def _art_welcome_sport(lang: str, pk: str, h: Callable[[str], str]) -> tuple[str, list[str]]:
    if lang == "uz":
        return (
            "Sport welcome — 1.4M UZS gacha 100%",
            [
                f"FairPari sport bonusi birinchi depozit uchun <strong>100% gacha 1 400 000 UZS</strong> "
                f"taklif qiladi. Bu {h('kazino')} welcome dan mustaqil yo'nalish: ro'yxatdan o'tishda "
                f"yoki PROMO bo'limida sport paketini tanlang. Promokod <strong>fa_1635</strong> kiritish unutmang.",
                f"Sport welcome faqat pre-match va live stavkalar uchun. Wagering <strong>×5</strong> "
                f"ekspress kuponlarda: har bir hodisa odatda minimal <strong>1.40</strong> koeffitsient bilan "
                f"hisoblanadi. Virtual sport va ba'zi maxsus bozorlar hisobga olinmasligi mumkin.",
                f"Ekspress — kamida uchta hodisali kupon. Turnirlar va booster aksiyalari PROMO da "
                f"e'lon qilinadi. Freebet va cashback alohida shartlarga ega; har safar kartochkani o'qing.",
                f"Depozit {h('tolov')} orqali tez o'tkaziladi. Wagering tugagach yechish ochiladi; "
                f"{h('registratsiya')} va {h('faq')} sahifalarida sport-kazino tanlovi qoidalari bor.",
            ],
        )
    if lang == "ru":
        return (
            "Спорт welcome — до 1,4 млн UZS 100%",
            [
                f"Спортивный welcome FairPari на первый депозит: <strong>до 1 400 000 UZS</strong> 100%. "
                f"Это отдельно от {h('kazino')} welcome — выберите спорт в PROMO. Код <strong>fa_1635</strong>.",
                f"Бонус на прематч и live. Отыгрыш <strong>×5</strong> экспрессами, минимальный коэффициент "
                f"события обычно <strong>1.40</strong>. Виртуальный спорт может не учитываться.",
                f"Экспресс — минимум три события. Турниры и бустеры в PROMO. Freebet — отдельные правила.",
                f"Пополнение через {h('tolov')}. После отыгрыша доступен вывод; см. {h('registratsiya')} и {h('faq')}.",
            ],
        )
    return (
        "Sports welcome — up to 1.4M UZS 100%",
        [
            f"FairPari sports welcome on the first deposit: <strong>up to 1,400,000 UZS</strong> at 100%. "
            f"Separate from {h('kazino')} welcome — pick sports in PROMO. Code <strong>fa_1635</strong>.",
            f"Valid on pre-match and live bets. Wagering <strong>×5</strong> on accumulators; each leg "
            f"usually needs odds of at least <strong>1.40</strong>. Virtual sports may be excluded.",
            f"Accumulator means three or more selections. Tournaments and boosters appear in PROMO. "
            f"Freebets carry their own terms.",
            f"Deposit via {h('tolov')}. Withdraw after wagering; see {h('registratsiya')} and {h('faq')}.",
        ],
    )


def _art_promo_code(lang: str, pk: str, h: Callable[[str], str]) -> tuple[str, list[str]]:
    if lang == "uz":
        return (
            "Promokod fa_1635 — qayerda va qachon",
            [
                f"FairPari O'zbekiston uchun asosiy promokod <strong>fa_1635</strong>. "
                f"U {h('registratsiya')} formasida yoki birinchi {h('tolov')} oynasida kiritiladi. "
                f"Kodsiz welcome bonusi faollashmasligi mumkin — har doim tekshiring.",
                f"Kod katta va kichik harflarga sezgir bo'lishi mumkin; bo'sh joy qoldirmang. "
                f"Agar promo maydoni ko'rinmasa, {h('mobil')} ilovasini yangilang yoki brauzer keshini tozalang. "
                f"Batafsil: {h('promo')} va {h('bonus-kod')} sahifalari.",
                f"fa_1635 faqat bir marta va yangi akkaunt uchun amal qiladi. Ikkinchi akkaunt ochish "
                f"bonusni bekor qilishi mumkin. Birinchi depozitda kazino yoki sport tanlovi qaytarilmas.",
                f"Vaqtinchalik aksiyalar alohida kodlar talab qilishi mumkin; ular PROMO da ko'rsatiladi. "
                f"Asosiy welcome shartlari o'zgarmasa, fa_1635 standart kod hisoblanadi.",
            ],
        )
    if lang == "ru":
        return (
            "Промокод fa_1635 — где и когда вводить",
            [
                f"Основной промокод FairPari для Узбекистана — <strong>fa_1635</strong>. "
                f"Вводится при {h('registratsiya')} или первом {h('tolov')}. Без кода welcome может не начислиться.",
                f"Проверьте регистр символов и отсутствие пробелов. Нет поля — обновите {h('mobil')} "
                f"или очистите кеш. См. {h('promo')} и {h('bonus-kod')}.",
                f"Код обычно один раз на новый аккаунт. Второй аккаунт аннулирует бонус. "
                f"Выбор казино или спорта на первом депозите окончателен.",
                f"Временные акции могут требовать другие коды в PROMO. fa_1635 — стандарт для welcome.",
            ],
        )
    return (
        "Promo code fa_1635 — where and when",
        [
            f"The main FairPari promo for Uzbekistan is <strong>fa_1635</strong>. "
            f"Enter it at {h('registratsiya')} or the first {h('tolov')}. Welcome may not apply without it.",
            f"Watch letter case and avoid spaces. No field? Update the {h('mobil')} app or clear cache. "
            f"See {h('promo')} and {h('bonus-kod')}.",
            f"Typically one use per new account. Duplicate accounts void the bonus. "
            f"Casino vs sports choice on first deposit is final.",
            f"Temporary promos may need other codes in PROMO. fa_1635 remains the standard welcome code.",
        ],
    )


def _art_wagering(lang: str, pk: str, h: Callable[[str], str]) -> tuple[str, list[str]]:
    if lang == "uz":
        return (
            "Wagering ×35 kazino va ×5 sport",
            [
                f"FairPari da ikki asosiy wagering modeli bor: kazino <strong>×35</strong>, sport <strong>×5</strong>. "
                f"Ularni aralashtirish mumkin emas — birinchi depozitda {h('kazino')} yoki {h('sport')} tanlang.",
                f"Kazino wageringida slotlar odatda 100% hissa qo'shadi; ruletka, blackjack va live "
                f"past foiz yoki nol hisoblanishi mumkin. Max bet cheklovi bonus bekor qilinishiga olib keladi.",
                f"Sportda ekspress shartlari: minimal uch hodisa, har biri ≥1.40. Muddat sportda qisqaroq "
                f"(7–14 kun). Progress {h('kirish')} kabinetida ko'rinadi.",
                f"Savollar: {h('faq')}. To'lov va yechish: {h('tolov')}. {h('litsenziya')} bo'limida "
                f"mas'uliyatli o'yin qoidalari.",
            ],
        )
    if lang == "ru":
        return (
            "Отыгрыш ×35 казино и ×5 спорт",
            [
                f"Два режима отыгрыша FairPari: казино <strong>×35</strong>, спорт <strong>×5</strong>. "
                f"На первом депозите — {h('kazino')} или {h('sport')}, не оба.",
                f"В казино слоты обычно 100%; рулетка, блэкджек, live — меньше или 0%. Превышение max bet отменяет бонус.",
                f"В спорте экспресс: ≥3 события, коэфф. ≥1.40. Срок короче. Прогресс в кабинете {h('kirish')}.",
                f"Вопросы: {h('faq')}. {h('tolov')}, {h('litsenziya')}.",
            ],
        )
    return (
        "Wagering ×35 casino and ×5 sports",
        [
            f"FairPari uses casino <strong>×35</strong> and sports <strong>×5</strong> wagering. "
            f"Pick {h('kazino')} or {h('sport')} on the first deposit — not both.",
            f"Slots usually count 100% in casino; roulette, blackjack, live may count less or zero. "
            f"Exceeding max bet can void the bonus.",
            f"Sports: accumulator with ≥3 legs at ≥1.40 odds. Shorter deadline. Track in {h('kirish')}.",
            f"See {h('faq')}, {h('tolov')}, {h('litsenziya')}.",
        ],
    )


def _art_payments(lang: str, pk: str, h: Callable[[str], str]) -> tuple[str, list[str]]:
    if lang == "uz":
        return (
            "Humo, Uzcard, Payme va Click",
            [
                f"O'zbekiston o'yinchilari FairPari hisobini {h('tolov')} bo'limidagi mahalliy tizimlar orqali "
                f"to'ldiradi: <strong>Humo</strong>, <strong>Uzcard</strong>, <strong>Payme</strong>, "
                f"<strong>Click</strong>. Tranzaksiya odatda bir necha daqiqa.",
                f"Minimal depozit welcome uchun taxminan 130 000 UZS. Birinchi to'ldirishda "
                f"<strong>fa_1635</strong> va kazino/sport tanlovini tasdiqlang. Valyuta — UZS.",
                f"Yechish shaxsiy kabinet orqali; KYC talab qilinsa, hujjatlarni vaqtida yuboring. "
                f"Bonus wagering tugamaguncha yechish cheklanishi mumkin.",
                f"{h('mobil')} ilovada ham xuddi shu usullar mavjud. {h('faq')} da limitlar va muddatlar.",
            ],
        )
    if lang == "ru":
        return (
            "Humo, Uzcard, Payme и Click",
            [
                f"Игроки из Узбекистана пополняют счёт через {h('tolov')}: <strong>Humo</strong>, "
                f"<strong>Uzcard</strong>, <strong>Payme</strong>, <strong>Click</strong>. Обычно несколько минут.",
                f"Минимум для welcome около 130 000 UZS. При первом пополнении — <strong>fa_1635</strong> "
                f"и выбор казино/спорт. Валюта UZS.",
                f"Вывод через кабинет; KYC при необходимости. До отыгрыша вывод может быть ограничен.",
                f"Те же методы в {h('mobil')}. Лимиты в {h('faq')}.",
            ],
        )
    return (
        "Humo, Uzcard, Payme and Click",
        [
            f"Uzbekistan players fund accounts via {h('tolov')}: <strong>Humo</strong>, <strong>Uzcard</strong>, "
            f"<strong>Payme</strong>, <strong>Click</strong>. Usually a few minutes.",
            f"Minimum for welcome around 130,000 UZS. On first top-up confirm <strong>fa_1635</strong> "
            f"and casino/sports choice. Currency: UZS.",
            f"Withdraw in the cashier; complete KYC if asked. Withdrawal may be limited until wagering ends.",
            f"Same methods in the {h('mobil')}. Limits in {h('faq')}.",
        ],
    )


def _art_registration(lang: str, pk: str, h: Callable[[str], str]) -> tuple[str, list[str]]:
    if lang == "uz":
        return (
            "Ro'yxatdan o'tish va bonus tanlovi",
            [
                f"Yangi akkaunt {h('registratsiya')} sahifasida: telefon yoki email, parol, valyuta UZS. "
                f"Promokod <strong>fa_1635</strong> shu bosqichda kiritiladi. 18+ talab qilinadi.",
                f"Birinchi depozitda kazino welcome (20.2M UZS + 150 FS) yoki sport (1.4M UZS) tanlang. "
                f"Keyinroq yo'nalishni almashtirib bo'lmaydi. {h('kazino')} va {h('sport')} sahifalarini solishtiring.",
                f"Tasdiqlash SMS yoki email orqali. Keyin {h('kirish')} va {h('tolov')} bilan davom eting. "
                f"{h('mobil')} ilovada ham ro'yxatdan o'tish mumkin.",
                f"Shaxsiy ma'lumotlarni to'g'ri kiriting — KYC va yechish uchun muhim. {h('litsenziya')} "
                f"va mas'uliyatli o'yin qoidalarini o'qing.",
            ],
        )
    if lang == "ru":
        return (
            "Регистрация и выбор бонуса",
            [
                f"Новый аккаунт на {h('registratsiya')}: телефон или email, пароль, UZS. "
                f"Промокод <strong>fa_1635</strong> здесь. Только 18+.",
                f"На первом депозите — казино (20,2 млн + 150 FS) или спорт (1,4 млн). "
                f"Сравните {h('kazino')} и {h('sport')}.",
                f"Подтверждение SMS/email. Затем {h('kirish')} и {h('tolov')}. Регистрация в {h('mobil')}.",
                f"Верные данные для KYC. {h('litsenziya')}.",
            ],
        )
    return (
        "Registration and bonus choice",
        [
            f"Create an account on {h('registratsiya')}: phone or email, password, UZS. "
            f"Enter <strong>fa_1635</strong>. 18+ only.",
            f"On first deposit choose casino (20.2M + 150 FS) or sports (1.4M). "
            f"Compare {h('kazino')} and {h('sport')}.",
            f"Verify via SMS/email. Then {h('kirish')} and {h('tolov')}. Also via {h('mobil')}.",
            f"Accurate data for KYC. Read {h('litsenziya')}.",
        ],
    )


def _art_free_spins(lang: str, pk: str, h: Callable[[str], str]) -> tuple[str, list[str]]:
    if lang == "uz":
        return (
            "150 frispin — taqsimot va qoidalar",
            [
                f"FairPari kazino welcome tarkibidagi <strong>150 bepul aylantirish</strong> bir necha depozit "
                f"bosqichiga bo'linadi. Har bir partiya belgilangan slotlarda faollashadi — ro'yxat PROMO da.",
                f"FS dan olingan yutuq bonus balansiga tushadi va <strong>×35</strong> wagering talab qiladi. "
                f"Frispin muddatini o'tkazib yubormang; odatda kunlar bilan cheklangan.",
                f"Qo'shimcha FS aksiyalari turnirlar va reload bonuslarida bo'lishi mumkin. "
                f"{h('kazino')} va {h('promo')} bo'limlarini kuzatib boring.",
                f"{h('depozitsiz')} takliflar doimiy emas; 150 FS asosan depozitli welcome qismidir. "
                f"Savollar: {h('faq')}.",
            ],
        )
    if lang == "ru":
        return (
            "150 фриспинов — распределение и правила",
            [
                f"<strong>150 бесплатных вращений</strong> в казино welcome делятся на этапы депозитов. "
                f"Слоты указаны в PROMO.",
                f"Выигрыш с FS на бонусный баланс с отыгрышем <strong>×35</strong>. Срок FS ограничен.",
                f"Дополнительные FS в турнирах и reload. Следите за {h('kazino')} и {h('promo')}.",
                f"{h('depozitsiz')} не заменяет welcome FS. {h('faq')}.",
            ],
        )
    return (
        "150 free spins — split and rules",
        [
            f"The <strong>150 free spins</strong> in casino welcome are split across deposit stages. "
            f"Eligible slots are listed in PROMO.",
            f"FS winnings go to the bonus balance with <strong>×35</strong> wagering. FS expire after a set period.",
            f"Extra FS may appear in tournaments and reloads. Watch {h('kazino')} and {h('promo')}.",
            f"{h('depozitsiz')} offers differ; 150 FS are mainly part of deposit welcome. {h('faq')}.",
        ],
    )


def _art_no_deposit(lang: str, pk: str, h: Callable[[str], str]) -> tuple[str, list[str]]:
    if lang == "uz":
        return (
            "Depozitsiz bonus va welcome alternativasi",
            [
                f"Doimiy <strong>depozitsiz bonus</strong> har kuni e'lon qilinmasligi mumkin. "
                f"Agar PROMO da kartochka yo'q bo'lsa, minimal depozit bilan welcome — eng ishonchli yo'l: "
                f"{h('kazino')} yoki {h('sport')}.",
                f"Vaqtinchalik depozitsiz aksiyalar — turnir sovrinlari, cashback, alohida FS. "
                f"Har birining wageringi alohida; ×35 va ×5 qoidalarini aralashtirmang.",
                f"Minimal depozit ~130 000 UZS, {h('tolov')} orqali Humo/Uzcard/Payme/Click. "
                f"<strong>fa_1635</strong> bilan faollashtiring.",
                f"Aldamchi «bepul bonus» havolalaridan qoching. Faqat rasmiy sayt va {h('mobil')} ilova. "
                f"{h('litsenziya')} ma'lumotlarini tekshiring.",
            ],
        )
    if lang == "ru":
        return (
            "Бездепозитный бонус и альтернатива welcome",
            [
                f"Постоянный <strong>бездепозитный бонус</strong> не всегда в PROMO. "
                f"Минимальный депозит и welcome — надёжная альтернатива: {h('kazino')} или {h('sport')}.",
                f"Временные бездепозиты — турниры, кэшбэк, FS. Отдельный отыгрыш; не смешивайте ×35 и ×5.",
                f"Минимум ~130 000 UZS через {h('tolov')}. Код <strong>fa_1635</strong>.",
                f"Избегайте мошеннических ссылок. Официальный сайт и {h('mobil')}. {h('litsenziya')}.",
            ],
        )
    return (
        "No-deposit bonus and welcome alternative",
        [
            f"A permanent <strong>no-deposit bonus</strong> is not always in PROMO. "
            f"Minimum deposit welcome is the reliable path: {h('kazino')} or {h('sport')}.",
            f"Temporary no-deposit promos include tournaments, cashback, FS. Separate wagering; "
            f"do not mix ×35 and ×5 rules.",
            f"Minimum ~130,000 UZS via {h('tolov')}. Code <strong>fa_1635</strong>.",
            f"Avoid scam links. Official site and {h('mobil')}. Check {h('litsenziya')}.",
        ],
    )


def _art_mobile(lang: str, pk: str, h: Callable[[str], str]) -> tuple[str, list[str]]:
    if lang == "uz":
        return (
            "Mobil ilovada bonuslar",
            [
                f"FairPari {h('mobil')} ilovasi Android va iOS uchun: slotlar, live, sport liniyasi va "
                f"PROMO bo'limi telefonda. Welcome <strong>fa_1635</strong> ilovada ham kiritiladi.",
                f"Push-bildirishnomalar vaqtinchalik aksiyalar haqida xabar beradi. Depozit {h('tolov')} "
                f"usullari mobil kassada mavjud: Humo, Uzcard, Payme, Click.",
                f"Frispinlar va wagering progressi kabinetda ko'rinadi — {h('kirish')} bilan sinxron. "
                f"Ilovani faqat rasmiy manbadan yuklab oling.",
                f"{h('faq')} da mobilga oid savollar; {h('bonus-kod')} va {h('promo')} sahifalari "
                f"brauzer bilan bir xil kodlarni ishlatadi.",
            ],
        )
    if lang == "ru":
        return (
            "Бонусы в мобильном приложении",
            [
                f"Приложение FairPari {h('mobil')}: слоты, live, спорт, PROMO. Код <strong>fa_1635</strong> в приложении.",
                f"Push о акциях. Пополнение {h('tolov')}: Humo, Uzcard, Payme, Click.",
                f"Прогресс FS и отыгрыша в кабинете {h('kirish')}. Скачивайте только официально.",
                f"{h('faq')}, {h('bonus-kod')}, {h('promo')}.",
            ],
        )
    return (
        "Bonuses in the mobile app",
        [
            f"FairPari {h('mobil')}: slots, live, sports, PROMO. Enter <strong>fa_1635</strong> in-app.",
            f"Push alerts for promos. Deposit via {h('tolov')}: Humo, Uzcard, Payme, Click.",
            f"FS and wagering progress in {h('kirish')}. Download only from official sources.",
            f"See {h('faq')}, {h('bonus-kod')}, {h('promo')}.",
        ],
    )


def _art_login(lang: str, pk: str, h: Callable[[str], str]) -> tuple[str, list[str]]:
    if lang == "uz":
        return (
            "Kabinetda bonus progressi",
            [
                f"{h('kirish')} orqali shaxsiy kabinetga kiring: asosiy balans, bonus balansi va wagering "
                f"ko'rsatkichlari. Kazino <strong>×35</strong> yoki sport <strong>×5</strong> qolgan summani kuzating.",
                f"Parolni unutganda tiklash SMS/email orqali. Ikki faktorli himoya mavjud bo'lsa, yoqing. "
                f"Bir akkauntda bir nechta welcome olish mumkin emas.",
                f"PROMO bo'limi kabinetda: faol bonuslar, muddatlar, max bet. Yangi depozit oldidan "
                f"{h('tolov')} limitlarini tekshiring.",
                f"Muammo bo'lsa {h('faq')} yoki qo'llab-quvvatlash. {h('registratsiya')} yangi foydalanuvchilar uchun.",
            ],
        )
    if lang == "ru":
        return (
            "Прогресс бонуса в кабинете",
            [
                f"Через {h('kirish')}: основной и бонусный баланс, отыгрыш ×35 или ×5.",
                f"Восстановление пароля по SMS/email. Один welcome на аккаунт.",
                f"PROMO в кабинете: сроки, max bet. Перед депозитом — {h('tolov')}.",
                f"Проблемы: {h('faq')}. {h('registratsiya')} для новых.",
            ],
        )
    return (
        "Bonus progress in the account",
        [
            f"After {h('kirish')}: main and bonus balance, ×35 or ×5 wagering left.",
            f"Password reset via SMS/email. One welcome per account.",
            f"PROMO in the cabinet: deadlines, max bet. Check {h('tolov')} before deposit.",
            f"Issues: {h('faq')}. {h('registratsiya')} for new users.",
        ],
    )


def _art_licence(lang: str, pk: str, h: Callable[[str], str]) -> tuple[str, list[str]]:
    if lang == "uz":
        return (
            "Litsenziya va mas'uliyatli o'yin",
            [
                f"FairPari {h('litsenziya')} ma'lumotlari va o'yin provayderlari haqida sahifada. "
                f"Bonuslar qo'shimcha imkoniyat, daromad kafolati emas. <strong>18+</strong> qat'iy.",
                f"Shaxsiy limitlar, tanaffus va o'z-o'zini cheklash vositalari kabinetda bo'lishi mumkin. "
                f"Wagering shartlarini bajarmasdan yechishga urinmang — bonus bekor qilinadi.",
                f"Faqat rasmiy domen va {h('mobil')} ilova. Telegramdagi «bepul bonus» havolalari xavfli.",
                f"To'lovlar {h('tolov')} bo'limida; bonus savollari {h('faq')}. {h('promo')} fa_1635 — rasmiy kod.",
            ],
        )
    if lang == "ru":
        return (
            "Лицензия и ответственная игра",
            [
                f"Данные о {h('litsenziya')} FairPari на странице. Бонусы — не гарантия дохода. <strong>18+</strong>.",
                f"Лимиты и самоисключение в кабинете. Не выводите до отыгрыша — бонус аннулируют.",
                f"Только официальный сайт и {h('mobil')}. Остерегайтесь ссылок в мессенджерах.",
                f"{h('tolov')}, {h('faq')}, {h('promo')} fa_1635.",
            ],
        )
    return (
        "Licence and responsible play",
        [
            f"FairPari {h('litsenziya')} details on this page. Bonuses are not income guarantees. <strong>18+</strong>.",
            f"Limits and self-exclusion may be in the cabinet. Do not withdraw before wagering completes.",
            f"Use only the official site and {h('mobil')}. Beware messenger «free bonus» links.",
            f"{h('tolov')}, {h('faq')}, official {h('promo')} code fa_1635.",
        ],
    )


def _art_faq_topics(lang: str, pk: str, h: Callable[[str], str]) -> tuple[str, list[str]]:
    if lang == "uz":
        return (
            "Tez-tez so'raladigan bonus savollari",
            [
                f"Ko'p savollar {h('faq')} da jamlangan: welcome hajmi, fa_1635, wagering muddatlari, "
                f"Humo/Uzcard/Payme/Click cheklovlari. Kazino 20.2M UZS + 150 FS, sport 1.4M UZS.",
                f"Sport va kazino welcome birinchi depozitda bir vaqtda emas. FS depozitsiz emas — "
                f"ular welcome tarkibida. {h('depozitsiz')} vaqtinchalik bo'lishi mumkin.",
                f"Max bet va taqiqlangan o'yinlar PROMO da. Progress {h('kirish')} kabinetida. "
                f"{h('bonus-kod')} va {h('promo')} kod farqi haqida ham o'qing.",
                f"Yechish wagering tugagach; KYC talab qilinsa, hujjatlar kerak. {h('tolov')} va "
                f"{h('litsenziya')} bo'limlariga qarang.",
            ],
        )
    if lang == "ru":
        return (
            "Частые вопросы о бонусах",
            [
                f"В {h('faq')}: welcome, fa_1635, сроки, лимиты Humo/Uzcard/Payme/Click. "
                f"Казино 20,2 млн + 150 FS, спорт 1,4 млн.",
                f"Спорт и казино не вместе на первом депозите. FS — часть welcome, не бездепозит. "
                f"{h('depozitsiz')} временный.",
                f"Max bet в PROMO. Прогресс в {h('kirish')}. {h('bonus-kod')} и {h('promo')}.",
                f"Вывод после отыгрыша. {h('tolov')}, {h('litsenziya')}.",
            ],
        )
    return (
        "Frequently asked bonus questions",
        [
            f"{h('faq')} covers welcome size, fa_1635, deadlines, Humo/Uzcard/Payme/Click limits. "
            f"Casino 20.2M + 150 FS, sports 1.4M.",
            f"Sports and casino not together on first deposit. FS are part of welcome, not no-deposit. "
            f"{h('depozitsiz')} may be temporary.",
            f"Max bet in PROMO. Progress in {h('kirish')}. {h('bonus-kod')} vs {h('promo')}.",
            f"Withdraw after wagering. See {h('tolov')}, {h('litsenziya')}.",
        ],
    )


def _art_bonus_code_page(lang: str, pk: str, h: Callable[[str], str]) -> tuple[str, list[str]]:
    if lang == "uz":
        return (
            "Bonus kodi va promo-kod farqi",
            [
                f"<strong>fa_1635</strong> — FairPari welcome uchun asosiy kod. {h('bonus-kod')} sahifasi "
                f"kodni qayerda kiritishni tushuntiradi; {h('promo')} bo'limi vaqtinchalik aksiyalarni ko'rsatadi.",
                f"Kodni faqat ro'yxatdan o'tish yoki depozitda kiriting. Uchinchi tomon saytlaridagi "
                f"«yangi kodlar» ishonchsiz bo'lishi mumkin.",
                f"Kazino welcome: 20.2M UZS + 150 FS, wagering ×35. Sport: 1.4M UZS, ×5. "
                f"{h('kazino')} va {h('sport')} ni solishtiring.",
                f"{h('registratsiya')} → {h('tolov')} → {h('kirish')} ketma-ketligi standart jarayon.",
            ],
        )
    if lang == "ru":
        return (
            "Бонус-код и промокод — в чём разница",
            [
                f"<strong>fa_1635</strong> — основной welcome-код. {h('bonus-kod')} — как вводить; "
                f"{h('promo')} — временные акции.",
                f"Ввод только при регистрации или депозите. Сторонние «новые коды» ненадёжны.",
                f"Казино 20,2 млн + 150 FS, ×35. Спорт 1,4 млн, ×5. {h('kazino')}, {h('sport')}.",
                f"Цепочка: {h('registratsiya')} → {h('tolov')} → {h('kirish')}.",
            ],
        )
    return (
        "Bonus code vs promo code",
        [
            f"<strong>fa_1635</strong> is the main welcome code. {h('bonus-kod')} explains entry; "
            f"{h('promo')} lists temporary promos.",
            f"Enter only at signup or deposit. Third-party «new codes» may be unreliable.",
            f"Casino 20.2M + 150 FS, ×35. Sports 1.4M, ×5. Compare {h('kazino')} and {h('sport')}.",
            f"Flow: {h('registratsiya')} → {h('tolov')} → {h('kirish')}.",
        ],
    )


def _art_index_hub(lang: str, pk: str, h: Callable[[str], str]) -> tuple[str, list[str]]:
    if lang == "uz":
        return (
            "FairPari bonus ekotizimi — qisqa xarita",
            [
                f"Ushbu sayt FairPari bonuslarini O'zbekiston kontekstida tushuntiradi: "
                f"{h('kazino')} welcome 20.2M UZS + 150 FS, {h('sport')} 1.4M UZS, promokod fa_1635.",
                f"Wagering: kazino ×35, sport ×5. To'lov: {h('tolov')} — Humo, Uzcard, Payme, Click. "
                f"{h('registratsiya')}, {h('kirish')}, {h('mobil')} — amaliy qadamlar.",
                f"{h('depozitsiz')}, {h('free-spins')}, {h('bonus-kod')}, {h('promo')} — maxsus mavzular. "
                f"{h('faq')} va {h('litsenziya')} — xavfsizlik va savollar.",
                f"Barcha ma'lumotlar 18+ o'yinchilar uchun. Bonus shartlari PROMO da yangilanishi mumkin — "
                f"depozitdan oldin kartochkani o'qing.",
            ],
        )
    if lang == "ru":
        return (
            "Экосистема бонусов FairPari — карта",
            [
                f"Сайт объясняет бонусы FairPari для Узбекистана: {h('kazino')} 20,2 млн + 150 FS, "
                f"{h('sport')} 1,4 млн, fa_1635.",
                f"Отыгрыш ×35 / ×5. {h('tolov')}: Humo, Uzcard, Payme, Click. "
                f"{h('registratsiya')}, {h('kirish')}, {h('mobil')}.",
                f"{h('depozitsiz')}, {h('free-spins')}, {h('bonus-kod')}, {h('promo')}, {h('faq')}, {h('litsenziya')}.",
                f"Только 18+. Условия в PROMO перед депозитом.",
            ],
        )
    return (
        "FairPari bonus ecosystem — map",
        [
            f"This site explains FairPari bonuses for Uzbekistan: {h('kazino')} 20.2M + 150 FS, "
            f"{h('sport')} 1.4M, fa_1635.",
            f"Wagering ×35 / ×5. {h('tolov')}: Humo, Uzcard, Payme, Click. "
            f"{h('registratsiya')}, {h('kirish')}, {h('mobil')}.",
            f"{h('depozitsiz')}, {h('free-spins')}, {h('bonus-kod')}, {h('promo')}, {h('faq')}, {h('litsenziya')}.",
            f"18+ only. Read PROMO before each deposit.",
        ],
    )


# Topic-specific extra articles (unique angles per page_key)
def _extra_kazino(lang: str, pk: str, h: Callable[[str], str]) -> tuple[str, list[str]]:
    t = {
        "uz": ("Kazino reload va keshbek", [
            "FairPari kazino bo'limida welcome dan keyin reload bonuslari va haftalik keshbek bo'lishi mumkin. "
            "Ularning wageringi welcome bilan bir xil bo'lmasligi mumkin — har kartochkani o'qing.",
            "Slot turnirlari UZS sovrin fondi va FS bilan o'tkaziladi. Ishtirok uchun minimal stavka va "
            "ro'yxatdagi o'yinlar talab qilinadi.",
            f"Welcome 20.2M UZS + 150 FS ni {h('promo')} fa_1635 bilan faollashtiring. {h('tolov')} orqali depozit.",
            f"Savollar: {h('faq')}. {h('sport')} alternativasi birinchi depozitda mavjud.",
        ]),
        "ru": ("Reload и кэшбэк казино", [
            "После welcome возможны reload и еженедельный кэшбэк. Отыгрыш может отличаться — читайте карточку.",
            "Турниры слотов с призами в UZS и FS. Минимальная ставка и список игр в условиях.",
            f"Welcome 20,2 млн + 150 FS с {h('promo')} fa_1635. Депозит через {h('tolov')}.",
            f"{h('faq')}. Альтернатива — {h('sport')} на первом депозите.",
        ]),
        "en": ("Casino reload and cashback", [
            "After welcome, reload bonuses and weekly cashback may appear. Wagering can differ — read each card.",
            "Slot tournaments with UZS prizes and FS. Min bet and game list in terms.",
            f"Activate 20.2M + 150 FS with {h('promo')} fa_1635. Deposit via {h('tolov')}.",
            f"See {h('faq')}. {h('sport')} alternative on first deposit.",
        ]),
    }
    return t[lang]


def _extra_sport(lang: str, pk: str, h: Callable[[str], str]) -> tuple[str, list[str]]:
    t = {
        "uz": ("Live stavka va sport wagering", [
            "Live bo'limida koeffitsientlar o'yin davomida yangilanadi. Sport welcome wagering uchun "
            "ekspress shartlari bajarilishi kerak — bitta oddiy stavka yetarli bo'lmasligi mumkin.",
            "Futbol, basketbol, tennis, kibersport — asosiy bozorlar. Ba'zi past koeffitsientli bozorlar "
            "hisobga olinmaydi.",
            f"1.4M UZS gacha sport bonus {h('registratsiya')} va fa_1635 bilan. {h('kazino')} bilan solishtirmang — tanlov bir marta.",
            f"{h('tolov')} va {h('faq')} yordam beradi.",
        ]),
        "ru": ("Live-ставки и отыгрыш спорта", [
            "В live коэффициенты меняются. Для отыгрыша спорт welcome нужны экспрессы с условиями.",
            "Футбол, баскетбол, теннис, киберспорт. Низкие коэфф. могут не считаться.",
            f"До 1,4 млн спорт с {h('registratsiya')} и fa_1635. Не {h('kazino')} — выбор один раз.",
            f"{h('tolov')}, {h('faq')}.",
        ]),
        "en": ("Live betting and sports wagering", [
            "Live odds update in play. Sports welcome wagering needs qualifying accumulators.",
            "Football, basketball, tennis, esports. Low odds markets may not count.",
            f"Up to 1.4M sports with {h('registratsiya')} and fa_1635. Not {h('kazino')} — one-time choice.",
            f"{h('tolov')}, {h('faq')}.",
        ]),
    }
    return t[lang]


def _extra_tolow(lang: str, pk: str, h: Callable[[str], str]) -> tuple[str, list[str]]:
    t = {
        "uz": ("Yechish va bonus balansi", [
            "Bonus mablag'ini wagering tugamaguncha yechib bo'lmaydi. Asosiy balans va bonus balansi "
            "kabinetda alohida ko'rsatiladi.",
            "Humo va Uzcard orqali yechish odatiy; Payme va Click ham qo'llab-quvvatlanishi mumkin. "
            "Komissiya va minimal summa PROMO yoki kassada.",
            f"Birinchi yechishda KYC — pasport yoki ID. {h('registratsiya')} ma'lumotlari mos bo'lishi kerak.",
            f"{h('faq')} va {h('litsenziya')} qo'shimcha tafsilotlar.",
        ]),
        "ru": ("Вывод и бонусный баланс", [
            "Бонус нельзя вывести до отыгрыша. Балансы раздельно в кабинете.",
            "Вывод на Humo, Uzcard; Payme, Click возможны. Комиссия в кассе.",
            f"KYC при первом выводе. Данные {h('registratsiya')} должны совпадать.",
            f"{h('faq')}, {h('litsenziya')}.",
        ]),
        "en": ("Withdrawal and bonus balance", [
            "Bonus funds cannot be withdrawn until wagering completes. Balances are shown separately.",
            "Withdraw to Humo, Uzcard; Payme, Click may be supported. Fees in the cashier.",
            f"KYC on first withdrawal. Match {h('registratsiya')} details.",
            f"{h('faq')}, {h('litsenziya')}.",
        ]),
    }
    return t[lang]


PAGE_ARTICLE_POOLS: dict[str, list[ArticleFn]] = {
    "index": [
        _art_index_hub, _art_welcome_casino, _art_welcome_sport, _art_promo_code,
        _art_wagering, _art_payments, _art_registration, _art_free_spins,
        _art_no_deposit, _art_mobile, _art_login, _art_licence, _art_faq_topics,
    ],
    "kazino": [
        _art_welcome_casino, _extra_kazino, _art_free_spins, _art_wagering,
        _art_promo_code, _art_payments, _art_registration, _art_no_deposit,
        _art_mobile, _art_login, _art_faq_topics, _art_bonus_code_page, _art_licence,
    ],
    "sport": [
        _art_welcome_sport, _extra_sport, _art_wagering, _art_promo_code,
        _art_payments, _art_registration, _art_welcome_casino, _art_mobile,
        _art_login, _art_faq_topics, _art_licence, _art_index_hub,
    ],
    "depozitsiz": [
        _art_no_deposit, _art_welcome_casino, _art_welcome_sport, _art_promo_code,
        _art_payments, _art_registration, _art_wagering, _art_free_spins,
        _art_mobile, _art_faq_topics, _art_licence, _art_bonus_code_page,
    ],
    "free-spins": [
        _art_free_spins, _art_welcome_casino, _art_wagering, _art_promo_code,
        _art_no_deposit, _art_payments, _art_registration, _art_mobile,
        _art_login, _art_faq_topics, _art_bonus_code_page, _art_licence,
    ],
    "bonus-kod": [
        _art_bonus_code_page, _art_promo_code, _art_welcome_casino, _art_welcome_sport,
        _art_registration, _art_payments, _art_wagering, _art_free_spins,
        _art_mobile, _art_faq_topics, _art_no_deposit, _art_licence,
    ],
    "promo": [
        _art_promo_code, _art_bonus_code_page, _art_welcome_casino, _art_welcome_sport,
        _art_registration, _art_payments, _art_wagering, _art_free_spins,
        _art_mobile, _art_login, _art_faq_topics, _art_licence,
    ],
    "registratsiya": [
        _art_registration, _art_promo_code, _art_welcome_casino, _art_welcome_sport,
        _art_payments, _art_wagering, _art_mobile, _art_login,
        _art_free_spins, _art_faq_topics, _art_bonus_code_page, _art_licence,
    ],
    "kirish": [
        _art_login, _art_wagering, _art_promo_code, _art_welcome_casino,
        _art_welcome_sport, _art_payments, _art_mobile, _art_registration,
        _art_faq_topics, _art_free_spins, _art_licence, _art_bonus_code_page,
    ],
    "mobil": [
        _art_mobile, _art_promo_code, _art_welcome_casino, _art_welcome_sport,
        _art_payments, _art_login, _art_registration, _art_wagering,
        _art_free_spins, _art_faq_topics, _art_bonus_code_page, _art_licence,
    ],
    "tolov": [
        _art_payments, _extra_tolow, _art_wagering, _art_promo_code,
        _art_welcome_casino, _art_welcome_sport, _art_registration,
        _art_login, _art_mobile, _art_faq_topics, _art_licence, _art_no_deposit,
    ],
    "litsenziya": [
        _art_licence, _art_faq_topics, _art_wagering, _art_payments,
        _art_promo_code, _art_registration, _art_mobile, _art_no_deposit,
        _art_welcome_casino, _art_welcome_sport, _art_login, _art_bonus_code_page,
    ],
    "faq": [
        _art_faq_topics, _art_welcome_casino, _art_welcome_sport, _art_wagering,
        _art_promo_code, _art_payments, _art_no_deposit, _art_free_spins,
        _art_registration, _art_mobile, _art_licence, _art_bonus_code_page,
    ],
}


def build_expansion_html(page_key: str, lang: str, words_needed: int) -> str:
    eyebrow, title, subtitle = SECTION_HEADERS[(page_key, lang)]
    h = _h(lang, page_key)
    pool = PAGE_ARTICLE_POOLS[page_key]
    articles: list[str] = []
    added_words = 0
    block_id = 1
    idx = 0
    cycles = 0
    while added_words < words_needed and cycles < 50:
        fn = pool[idx % len(pool)]
        h2, paras = fn(lang, page_key, h)
        art = article_html(h2, paras, block_id)
        articles.append(art)
        added_words += count_words(art)
        block_id += 1
        idx += 1
        if idx % len(pool) == 0:
            cycles += 1
    body = "\n".join(articles)
    return (
        f'<section class="section section--alt section--seo-expansion" id="seo-guide-2500" '
        f'data-expand-2500="v1">\n'
        f'<div class="container">\n'
        f'<header class="section__header">\n'
        f'<span class="section__eyebrow">{eyebrow}</span>\n'
        f'<h2 class="section__title">{title}</h2>\n'
        f'<p class="section__subtitle">{subtitle}</p>\n'
        f'</header>\n'
        f'<div class="seo-expansion__body">\n'
        f'{body}\n'
        f'</div>\n'
        f'</div>\n'
        f'</section>'
    )


def expand_file(path: Path) -> tuple[bool, str]:
    rel = path.relative_to(ROOT).as_posix()
    if rel not in PATH_TO_META:
        return False, f"skip (unmapped): {rel}"
    page_key, lang = PATH_TO_META[rel]
    text = path.read_text(encoding="utf-8")
    if 'data-expand-2500="v1"' in text:
        return False, f"skip (already expanded): {rel}"
    current = count_words(text)
    if current >= TARGET_WORDS:
        return False, f"skip (>= {TARGET_WORDS} words): {rel} ({current})"
    words_needed = TARGET_WORDS - current + WORD_BUFFER
    injection = build_expansion_html(page_key, lang, words_needed)
    pos = find_injection_index(text)
    if pos is None:
        return False, f"error (no related-pages marker): {rel}"
    new_text = text[:pos] + injection + text[pos:]
    path.write_text(new_text, encoding="utf-8")
    new_count = count_words(new_text)
    return True, f"expanded: {rel} ({current} -> {new_count} words)"


def main() -> int:
    expanded: list[str] = []
    skipped: list[str] = []
    errors: list[str] = []
    still_short: list[str] = []

    for path in sorted(ROOT.glob("**/index.html")):
        rel = path.relative_to(ROOT).as_posix()
        if is_legal(rel):
            continue
        ok, msg = expand_file(path)
        if ok:
            expanded.append(msg)
        elif msg.startswith("error"):
            errors.append(msg)
        else:
            skipped.append(msg)

    for path in sorted(ROOT.glob("**/index.html")):
        rel = path.relative_to(ROOT).as_posix()
        if is_legal(rel):
            continue
        wc = count_words(path.read_text(encoding="utf-8"))
        if wc < TARGET_WORDS:
            still_short.append(f"{rel} ({wc} words)")

    print(f"Expanded {len(expanded)} file(s).")
    for line in expanded:
        print(f"  {line}")
    if skipped:
        print(f"Skipped {len(skipped)} file(s).")
    if errors:
        print(f"Errors {len(errors)}:")
        for line in errors:
            print(f"  {line}")
    if still_short:
        print(f"Still under {TARGET_WORDS} words ({len(still_short)}):")
        for line in still_short:
            print(f"  {line}")
    else:
        print(f"All non-legal pages are >= {TARGET_WORDS} words.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Expand content blocks (~500-700 words) for injection before related-pages section.

Provides get_expand_html(page_key, lang) returning HTML wrapped in section--expand-1000.
No imports from other project files.
"""

from __future__ import annotations

PAGE_FILES: dict[str, list[tuple[str, str]]] = {
    "depozitsiz": [
        ("depozitsiz-bonus", "uz"),
        ("ru/bonus-bez-depozita", "ru"),
        ("en/no-deposit-bonus", "en"),
    ],
    "free-spins": [
        ("free-spins", "uz"),
        ("ru/free-spins", "ru"),
        ("en/free-spins", "en"),
    ],
    "bonus-kod": [
        ("bonus-kodi", "uz"),
        ("ru/bonus-kod", "ru"),
        ("en/bonus-code", "en"),
    ],
    "faq": [
        ("faq", "uz"),
        ("ru/faq", "ru"),
        ("en/faq", "en"),
    ],
    "sport": [
        ("sport-bonuslari", "uz"),
        ("ru/sport-bonusy", "ru"),
        ("en/sports-bonuses", "en"),
    ],
    "kazino": [
        ("kazino-bonuslari", "uz"),
        ("ru/bonusy-kazino", "ru"),
        ("en/casino-bonuses", "en"),
    ],
    "registratsiya": [
        ("royxatdan-otish", "uz"),
        ("ru/registratsiya", "ru"),
        ("en/registration", "en"),
    ],
    "kirish": [
        ("kirish", "uz"),
        ("ru/vhod", "ru"),
        ("en/login", "en"),
    ],
    "mobil": [
        ("mobil", "uz"),
        ("ru/skachat", "ru"),
        ("en/app", "en"),
    ],
    "tolov": [
        ("tolov", "uz"),
        ("ru/oplata", "ru"),
        ("en/payments", "en"),
    ],
    "litsenziya": [
        ("litsenziya", "uz"),
        ("ru/litsenziya", "ru"),
        ("en/license", "en"),
    ],
    "promo": [
        ("promo-kod", "uz"),
        ("ru/promokod", "ru"),
        ("en/promo-code", "en"),
    ],
    "index": [
        ("index.html", "uz"),
        ("ru/index.html", "ru"),
        ("en/index.html", "en"),
    ],
}

_SLUGS: dict[str, dict[str, str]] = {
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
    },
}

_DISCLAIMER = {
    "uz": (
        '<p class="disclaimer"><strong>18+.</strong> Qimor o\'yinlari moliyaviy xavf '
        "tug'diradi. Mas'uliyat bilan o'ynang.</p>"
    ),
    "ru": (
        '<p class="disclaimer"><strong>18+.</strong> Азартные игры связаны с финансовым '
        "риском. Играйте ответственно.</p>"
    ),
    "en": (
        '<p class="disclaimer"><strong>18+.</strong> Gambling involves financial risk. '
        "Play responsibly.</p>"
    ),
}


def _href(lang: str, page_key: str, target: str) -> str:
    prefix = "" if page_key == "index" else "../"
    return prefix + _SLUGS[lang][target] + "/"


def _wrap(body: str) -> str:
    return (
        '<section class="section section--content section--expand-1000" '
        'data-expand-1000="v1" id="content-expand-1000">\n'
        '  <div class="container prose">\n'
        + body
        + "\n  </div>\n</section>"
    )


def _table(rows: list[tuple[str, str, str]]) -> str:
    head = rows[0]
    body = "".join(
        f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in rows[1:]
    )
    return (
        '<table class="data-table"><thead><tr>'
        f"<th>{head[0]}</th><th>{head[1]}</th><th>{head[2]}</th>"
        f"</tr></thead><tbody>{body}</tbody></table>"
    )


def _ol(items: list[str]) -> str:
    return "<ol>" + "".join(f"<li>{i}</li>" for i in items) + "</ol>"


def _ul(items: list[str]) -> str:
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def _faq(pairs: list[tuple[str, str]]) -> str:
    return (
        '<dl class="faq-list">'
        + "".join(f"<dt>{q}</dt><dd>{a}</dd>" for q, a in pairs)
        + "</dl>"
    )


# ---------------------------------------------------------------------------
# Content builders — one function per page_key, branches on lang
# ---------------------------------------------------------------------------

def _content_depozitsiz(lang: str, pk: str, h) -> str:
    if lang == "uz":
        return (
            "<h2 id=\"exp-dep\">FairPari depozitsiz bonus — joriy holat va alternativalar</h2>"
            "<p>O'zbekiston o'yinchilari tez-tez <strong>depozitsiz bonus</strong> qidiradi: "
            "balansni to'ldirmasdan bepul aylantirish yoki stavka olish istagi tushunarli. "
            "FairPari da doimiy klassik no-deposit paket har kuni e'lon qilinmasligi mumkin, "
            "biroq <strong>minimal depozit</strong> (taxminan <strong>130 000 UZS</strong>) bilan "
            "birinchi to'ldirishda katta welcome ochiladi — kazino "
            "<strong>20 200 000 UZS + 150 FS</strong>, sport <strong>1 400 000 UZS</strong> gacha. "
            "Promokod <strong>fa_1635</strong> ro'yxatdan o'tish yoki depozitda kiritiladi.</p>"
            "<p>Vaqtinchalik depozitsiz aksiyalar — turnir sovrinlari, cashback, alohida slotlarda FS — "
            "mavjud bo'lishi mumkin. Biz faqat tekshirilgan summalar va wagering "
            "(kazino <strong>×35</strong>, sport <strong>×5</strong>) haqida yozamiz. "
            "Agar depozitsiz kartochka ko'rinmasa, minimal depozitli welcome eng ishonchli yo'l.</p>"
            "<h3>Minimal depozit — amaliy alternativa</h3>"
            "<p>130 000 UZS atrofidagi to'ldirish "
            f"<a href=\"{h('tolov')}\">Humo, Uzcard, Payme, Click</a> orqali bir necha daqiqada "
            "amalga oshadi. Birinchi depozitda faqat bitta yo'nalish tanlanadi: kazino yoki sport welcome. "
            "Kazino paketidagi 150 bepul aylantirish bosqichlarga bo'linadi; ularning yutug'i bonus "
            "balansiga tushadi va slotlarda ×35 aylantirish talab etiladi.</p>"
            + _table([
                ("Taklif", "Hajm", "Wagering"),
                ("Kazino welcome", "20 200 000 UZS + 150 FS", "×35 slotlar"),
                ("Sport welcome", "1 400 000 UZS gacha", "×5 ekspress"),
                ("Depozitsiz (vaqtinchalik)", "PROMO bo'limi", "Alohida"),
                ("Min. depozit", "~130 000 UZS", "—"),
            ])
            + "<h3>Qadamlar: depozitsiz yoki welcome</h3>"
            + _ol([
                f"<a href=\"{h('registratsiya')}\">Ro'yxatdan o'ting</a> — telefon yoki email, UZS.",
                "PROMO bo'limida depozitsiz kartochka bormi — tekshiring.",
                "Agar yo'q bo'lsa, <strong>fa_1635</strong> bilan minimal depozit kiriting.",
                f"Kazino: <a href=\"{h('kazino')}\">kazino bonuslari</a>; sport: "
                f"<a href=\"{h('sport')}\">sport bonuslari</a>.",
                f"Wagering muddatini <a href=\"{h('faq')}\">FAQ</a> va "
                f"<a href=\"{h('promo')}\">promo-kod</a> bo'limida aniqlang.",
            ])
            + "<h3>Xavfsizlik va mas'uliyatli o'yin</h3>"
            "<p>Bonus qo'shimcha imkoniyat, daromad kafolati emas. Shaxsiy limitlar va "
            f"<a href=\"{h('litsenziya')}\">litsenziya</a> ma'lumotlarini o'rganing. Faqat rasmiy "
            f"FairPari sayti yoki <a href=\"{h('mobil')}\">mobil ilova</a>dan foydalaning. "
            "Telegramdagi «bepul bonus» havolalaridan qoching. KYC talab qilinsa, hujjatlarni "
            "o'z vaqtida yuboring — yechish kechikmasin.</p>"
            "<p>Har safar depozitdan oldin PROMO kartochkasidagi matnni o'qing: minimal koeffitsient, "
            "max bet va o'yinlar ro'yxati o'sha yerda. Sport va kazino wageringlari aralashmaydi; "
            "bitta yo'nalishni tanlang va shu bo'yicha reja tuzing. Depozitsiz bonus olishga "
            "urinayotganda operator shartlarni o'zgartirishi mumkin — joriy holatni faqat PROMO "
            "orqali tasdiqlang.</p>"
            + _faq([
                ("Hozir depozitsiz bonus bormi?", "Doimiy paket har doim e'lon qilinmaydi; PROMO da tekshiring."),
                ("150 FS depozitsizmi?", "Yo'q — ular birinchi depozit kazino welcome qismidir."),
                ("fa_1635 qayerga?", f"Ro'yxatdan o'tish yoki depozit oynasida; batafsil <a href=\"{h('promo')}\">promo-kod</a>."),
                ("Wagering muddati?", "Kazino ×35 — 7–30 kun; sport ×5 — qisqaroq."),
                ("Welcome va depozitsiz birga?", "Yo'q — birinchi depozitda bitta welcome tanlanadi."),
            ])
            + _DISCLAIMER["uz"]
        )
    if lang == "ru":
        return (
            "<h2 id=\"exp-dep\">Бездепозитный бонус FairPari — статус и альтернативы</h2>"
            "<p>Игроки из Узбекистана часто ищут <strong>бонус без депозита</strong>. "
            "На FairPari постоянный no-deposit пакет может не отображаться каждый день, однако при "
            "<strong>минимальном депозите</strong> (около <strong>130 000 UZS</strong>) открывается welcome: "
            "казино <strong>20 200 000 UZS + 150 FS</strong>, спорт <strong>до 1 400 000 UZS</strong>. "
            "Промокод <strong>fa_1635</strong> вводится при регистрации или депозите.</p>"
            "<p>Временные бездепозитные акции могут появляться периодически. Мы пишем только о проверенных "
            "суммах и отыгрыше (казино <strong>×35</strong>, спорт <strong>×5</strong>). "
            "Если карточки бездепозита нет, welcome с минимальным депозитом — надёжный путь.</p>"
            "<h3>Минимальный депозит как альтернатива</h3>"
            "<p>Пополнение от 130 000 UZS через "
            f"<a href=\"{h('tolov')}\">Humo, Uzcard, Payme, Click</a> занимает минуты. "
            "При первом депозите выбирается казино или спорт welcome — оба одновременно недоступны.</p>"
            + _table([
                ("Предложение", "Объём", "Отыгрыш"),
                ("Казино welcome", "20 200 000 UZS + 150 FS", "×35 слоты"),
                ("Спорт welcome", "до 1 400 000 UZS", "×5 экспресс"),
                ("Бездепозит", "раздел PROMO", "Отдельный"),
                ("Мин. депозит", "~130 000 UZS", "—"),
            ])
            + "<h3>Шаги: бездепозит или welcome</h3>"
            + _ol([
                f"<a href=\"{h('registratsiya')}\">Зарегистрируйтесь</a> в UZS.",
                "Проверьте PROMO на карточку бездепозита.",
                "Внесите минимальный депозит с <strong>fa_1635</strong>, если бездепозита нет.",
                f"Казино: <a href=\"{h('kazino')}\">бонусы казино</a>; спорт: <a href=\"{h('sport')}\">спорт-бонусы</a>.",
                f"Сроки в <a href=\"{h('faq')}\">FAQ</a> и <a href=\"{h('promo')}\">промокод</a>.",
            ])
            + "<h3>Безопасность</h3>"
            "<p>Бонус — возможность, не гарантия дохода. Изучите "
            f"<a href=\"{h('litsenziya')}\">лицензию</a> и используйте "
            f"<a href=\"{h('mobil')}\">официальное приложение</a>. Избегайте ссылок в мессенджерах.</p>"
            "<p>Перед депозитом читайте карточку PROMO: минимальный коэффициент, max bet, список игр. "
            "Отыгрыш казино и спорта не смешивается.</p>"
            + _faq([
                ("Есть бездепозит сейчас?", "Не всегда; проверьте PROMO."),
                ("150 FS бездепозитные?", "Нет — часть казино welcome."),
                ("Куда fa_1635?", f"Регистрация или депозит; <a href=\"{h('promo')}\">промокод</a>."),
                ("Срок отыгрыша?", "Казино ×35 — 7–30 дней; спорт ×5 — короче."),
                ("Совместить с welcome?", "Нет — один welcome на первый депозит."),
            ])
            + _DISCLAIMER["ru"]
        )
    return (
        "<h2 id=\"exp-dep\">FairPari no-deposit bonus — status and alternatives</h2>"
        "<p>Players in Uzbekistan often search for a <strong>no-deposit bonus</strong>. FairPari may not "
        "list a permanent no-deposit package daily, yet a <strong>minimum deposit</strong> "
        "(around <strong>130,000 UZS</strong>) unlocks welcome: casino <strong>20,200,000 UZS + 150 FS</strong>, "
        "sports up to <strong>1,400,000 UZS</strong>. Promo code <strong>fa_1635</strong> is entered at "
        "registration or deposit.</p>"
        "<p>Temporary no-deposit promos may appear periodically. We only report verified amounts and "
        "wagering (casino <strong>×35</strong>, sports <strong>×5</strong>). If no no-deposit card is "
        "shown, welcome with minimum deposit is the reliable path.</p>"
        "<h3>Minimum deposit as alternative</h3>"
        "<p>Topping up from 130,000 UZS via "
        f"<a href=\"{h('tolov')}\">Humo, Uzcard, Payme, Click</a> takes minutes. "
        "On first deposit you choose casino or sports welcome — not both.</p>"
        + _table([
            ("Offer", "Volume", "Wagering"),
            ("Casino welcome", "20,200,000 UZS + 150 FS", "×35 slots"),
            ("Sports welcome", "up to 1,400,000 UZS", "×5 accumulator"),
            ("No-deposit", "PROMO section", "Separate"),
            ("Min. deposit", "~130,000 UZS", "—"),
        ])
        + "<h3>Steps: no-deposit or welcome</h3>"
        + _ol([
            f"<a href=\"{h('registratsiya')}\">Register</a> in UZS.",
            "Check PROMO for a no-deposit card.",
            "Deposit minimum with <strong>fa_1635</strong> if none.",
            f"Casino: <a href=\"{h('kazino')}\">casino bonuses</a>; sports: <a href=\"{h('sport')}\">sports bonuses</a>.",
            f"Deadlines in <a href=\"{h('faq')}\">FAQ</a> and <a href=\"{h('promo')}\">promo code</a>.",
        ])
        + "<h3>Safety</h3>"
        "<p>A bonus is opportunity, not guaranteed income. Review "
        f"<a href=\"{h('litsenziya')}\">licence</a> info and use the "
        f"<a href=\"{h('mobil')}\">official app</a>. Avoid messenger links.</p>"
        "<p>Before each deposit read the PROMO card: minimum odds, max bet, eligible games. "
        "Casino and sports wagering do not mix.</p>"
        + _faq([
            ("No-deposit available now?", "Not always; check PROMO."),
            ("Are 150 FS no-deposit?", "No — part of casino welcome."),
            ("Where to enter fa_1635?", f"Registration or deposit; <a href=\"{h('promo')}\">promo code</a>."),
            ("Wagering period?", "Casino ×35 — 7–30 days; sports ×5 — shorter."),
            ("Combine with welcome?", "No — one welcome on first deposit."),
        ])
        + _DISCLAIMER["en"]
    )


# PLACEHOLDER_FOR_REMAINING_BUILDERS

_BUILDERS: dict[str, object] = {
    "depozitsiz": _content_depozitsiz,
}

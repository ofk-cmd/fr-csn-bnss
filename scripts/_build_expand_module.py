#!/usr/bin/env python3
"""Build page_expand_1000_content.py with all 39 content blocks."""
from pathlib import Path
import json

OUT = Path(__file__).parent / "page_expand_1000_content.py"

SLUGS = {
    "uz": {
        "kazino": "kazino-bonuslari", "sport": "sport-bonuslari",
        "depozitsiz": "depozitsiz-bonus", "free-spins": "free-spins",
        "bonus-kod": "bonus-kodi", "faq": "faq",
        "registratsiya": "royxatdan-otish", "kirish": "kirish",
        "mobil": "mobil", "tolov": "tolov", "litsenziya": "litsenziya",
        "promo": "promo-kod",
    },
    "ru": {
        "kazino": "bonusy-kazino", "sport": "sport-bonusy",
        "depozitsiz": "bonus-bez-depozita", "free-spins": "free-spins",
        "bonus-kod": "bonus-kod", "faq": "faq",
        "registratsiya": "registratsiya", "kirish": "vhod",
        "mobil": "skachat", "tolov": "oplata", "litsenziya": "litsenziya",
        "promo": "promokod",
    },
    "en": {
        "kazino": "casino-bonuses", "sport": "sports-bonuses",
        "depozitsiz": "no-deposit-bonus", "free-spins": "free-spins",
        "bonus-kod": "bonus-code", "faq": "faq",
        "registratsiya": "registration", "kirish": "login",
        "mobil": "app", "tolov": "payments", "litsenziya": "license",
        "promo": "promo-code",
    },
}

PAGE_FILES = {
    "depozitsiz": [
        ("depozitsiz-bonus", "uz"), ("ru/bonus-bez-depozita", "ru"),
        ("en/no-deposit-bonus", "en"),
    ],
    "free-spins": [
        ("free-spins", "uz"), ("ru/free-spins", "ru"), ("en/free-spins", "en"),
    ],
    "bonus-kod": [
        ("bonus-kodi", "uz"), ("ru/bonus-kod", "ru"), ("en/bonus-code", "en"),
    ],
    "faq": [("faq", "uz"), ("ru/faq", "ru"), ("en/faq", "en")],
    "sport": [
        ("sport-bonuslari", "uz"), ("ru/sport-bonusy", "ru"),
        ("en/sports-bonuses", "en"),
    ],
    "kazino": [
        ("kazino-bonuslari", "uz"), ("ru/bonusy-kazino", "ru"),
        ("en/casino-bonuses", "en"),
    ],
    "registratsiya": [
        ("royxatdan-otish", "uz"), ("ru/registratsiya", "ru"),
        ("en/registration", "en"),
    ],
    "kirish": [("kirish", "uz"), ("ru/vhod", "ru"), ("en/login", "en")],
    "mobil": [("mobil", "uz"), ("ru/skachat", "ru"), ("en/app", "en")],
    "tolov": [("tolov", "uz"), ("ru/oplata", "ru"), ("en/payments", "en")],
    "litsenziya": [
        ("litsenziya", "uz"), ("ru/litsenziya", "ru"), ("en/license", "en"),
    ],
    "promo": [
        ("promo-kod", "uz"), ("ru/promokod", "ru"), ("en/promo-code", "en"),
    ],
    "index": [
        ("index.html", "uz"), ("ru/index.html", "ru"), ("en/index.html", "en"),
    ],
}


def href(lang, page_key, target):
    prefix = "" if page_key == "index" else "../"
    return f"{prefix}{SLUGS[lang][target]}/"


def tbl(rows):
    head = rows[0]
    body = "".join(
        f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in rows[1:]
    )
    return (
        f'<table class="data-table"><thead><tr>'
        f"<th>{head[0]}</th><th>{head[1]}</th><th>{head[2]}</th>"
        f"</tr></thead><tbody>{body}</tbody></table>"
    )


def ol(items):
    return "<ol>" + "".join(f"<li>{i}</li>" for i in items) + "</ol>"


def ul(items):
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def faq(pairs):
    return '<dl class="faq-list">' + "".join(
        f"<dt>{q}</dt><dd>{a}</dd>" for q, a in pairs
    ) + "</dl>"


def disc(lang):
    if lang == "uz":
        return '<p class="disclaimer"><strong>18+.</strong> Qimor o\'yinlari moliyaviy xavf tug\'diradi. Mas\'uliyat bilan o\'ynang.</p>'
    if lang == "ru":
        return '<p class="disclaimer"><strong>18+.</strong> Азартные игры связаны с финансовым риском. Играйте ответственно.</p>'
    return '<p class="disclaimer"><strong>18+.</strong> Gambling involves financial risk. Play responsibly.</p>'


# Unique content per (page_key, lang) — each ~500-700 words
def build_all():
    C = {}

    # ---- DEPOZITSIZ ----
    for lang in ("uz", "ru", "en"):
        h = lambda t, l=lang, pk="depozitsiz": href(l, pk, t)
        if lang == "uz":
            C[("depozitsiz", "uz")] = f"""
        <h2 id="exp-dep-holat">FairPari depozitsiz bonus — joriy holat va alternativalar</h2>
        <p>O'zbekiston o'yinchilari tez-tez <strong>depozitsiz bonus</strong> qidiradi: balansni to'ldirmasdan bepul aylantirish yoki stavka olish istagi tushunarli. FairPari da doimiy klassik no-deposit paket har kuni e'lon qilinmasligi mumkin, biroq <strong>minimal depozit</strong> (taxminan <strong>130 000 UZS</strong>) bilan birinchi to'ldirishda katta welcome ochiladi — kazino <strong>20 200 000 UZS + 150 FS</strong>, sport <strong>1 400 000 UZS</strong> gacha. Promokod <strong>fa_1635</strong> ro'yxatdan o'tish yoki depozitda kiritiladi; shartlar PROMO bo'limida yangilanadi.</p>
        <p>Vaqtinchalik depozitsiz aksiyalar — turnir sovrinlari, cashback, alohida slotlarda FS — mavjud bo'lishi mumkin. Sahifadagi «yo'q» holati aldamchi reklamadan farq qiladi: biz faqat tekshirilgan summalar va wagering (kazino <strong>×35</strong>, sport <strong>×5</strong>) haqida yozamiz. Agar depozitsiz kartochka ko'rinmasa, minimal depozitli welcome eng ishonchli yo'l hisoblanadi.</p>
        <h3 id="exp-dep-alt">Minimal depozit — amaliy alternativa</h3>
        <p>130 000 UZS atrofidagi to'ldirish <a href="{h('tolov')}">Humo, Uzcard, Payme, Click</a> orqali bir necha daqiqada amalga oshadi. Birinchi depozitda faqat bitta yo'nalish tanlanadi: kazino welcome yoki sport welcome — ikkalasi bir vaqtda berilmaydi. Kazino paketidagi 150 bepul aylantirish bosqichlarga bo'linadi; ularning yutug'i bonus balansiga tushadi va slotlarda ×35 aylantirish talab etiladi.</p>
        {tbl([
            ("Taklif", "Hajm", "Wagering"),
            ("Kazino welcome", "20 200 000 UZS + 150 FS", "×35 slotlar"),
            ("Sport welcome", "1 400 000 UZS gacha", "×5 ekspress"),
            ("Depozitsiz (vaqtinchalik)", "PROMO bo'limi", "Alohida"),
            ("Min. depozit", "~130 000 UZS", "—"),
        ])}
        <h3 id="exp-dep-steps">Qadamlar: depozitsiz yoki welcome</h3>
        {ol([
            f'<a href="{h("registratsiya")}">Ro\'yxatdan o\'ting</a> — telefon yoki email, parol, valyuta UZS.',
            'PROMO yoki «Aksiyalar» bo\'limida depozitsiz kartochka bormi — tekshiring.',
            'Agar yo\'q bo\'lsa, <strong>fa_1635</strong> bilan minimal depozit kiriting.',
            f'Kazino uchun <a href="{h("kazino")}">kazino bonuslari</a>, sport uchun <a href="{h("sport")}">sport bonuslari</a> sahifalarini o\'qing.',
            f'<a href="{h("faq")}">FAQ</a> va <a href="{h("promo")}">promo-kod</a> bo\'limlarida wagering muddatini aniqlang.',
        ])}
        <h3 id="exp-dep-risk">Xavfsizlik va mas'uliyatli o'yin</h3>
        <p>Bonus qo'shimcha imkoniyat, daromad kafolati emas. Shaxsiy limitlar, tanaffus va <a href="{h('litsenziya')}">litsenziya</a> ma'lumotlarini o'rganing. Faqat rasmiy FairPari sayti yoki <a href="{h('mobil')}">mobil ilova</a>dan foydalaning; Telegramdagi «bepul bonus» havolalaridan qoching. KYC talab qilinsa, hujjatlarni o'z vaqtida yuboring — yechish kechikmasin.</p>
        <p>Depozitsiz bonus olishga urinayotganda shuni yodda tuting: operator shartlarni o'zgartirishi mumkin. Har safar depozitdan oldin PROMO kartochkasidagi matnni o'qing — minimal koeffitsient, max bet va o'yinlar ro'yxati o'sha yerda. Sport va kazino wageringlari aralashmaydi; bitta yo'nalishni tanlang va shu bo'yicha reja tuzing.</p>
        {faq([
            ("Hozir depozitsiz bonus bormi?", "Doimiy paket har doim e'lon qilinmaydi; joriy ro'yxat PROMO da. Minimal depozit welcome barqaror alternativadir."),
            ("150 FS depozitsiz hisoblanadimi?", "Yo'q — ular odatda birinchi depozit bilan bog'liq kazino welcome qismidir."),
            ("fa_1635 qayerga yoziladi?", f"Ro'yxatdan o'tishda yoki depozit oynasida; batafsil <a href=\"{h('promo')}\">promo-kod</a> sahifasida."),
            ("Wagering qancha kun beriladi?", "Kazino ×35 — odatda 7–30 kun; sport ×5 — qisqaroq. Aniq muddat PROMO kartochkasida ko'rsatiladi."),
            ("Depozitsiz va welcome birga olinadimi?", "Yo'q — birinchi depozitda bitta welcome tanlanadi; keyingi aksiyalar alohida PROMO da."),
        ])}
        {disc("uz")}"""
        elif lang == "ru":
            C[("depozitsiz", "ru")] = f"""
        <h2 id="exp-dep-holat">Бездепозитный бонус FairPari — статус и альтернативы</h2>
        <p>Игроки из Узбекистана часто ищут <strong>бонус без депозита</strong>: желание получить бесплатные вращения или ставки без пополнения счёта понятно. На FairPari постоянный классический no-deposit пакет может не отображаться каждый день, однако при <strong>минимальном депозите</strong> (около <strong>130 000 UZS</strong>) открывается крупный welcome — казино <strong>20 200 000 UZS + 150 фриспинов</strong>, спорт <strong>до 1 400 000 UZS</strong>. Промокод <strong>fa_1635</strong> вводится при регистрации или депозите; условия обновляются в разделе PROMO.</p>
        <p>Временные бездепозитные акции — турнирные призы, кэшбэк, FS на отдельных слотах — могут появляться периодически. Статус «недоступно» на странице отличается от мошеннической рекламы: мы пишем только о проверенных суммах и отыгрыше (казино <strong>×35</strong>, спорт <strong>×5</strong>). Если карточки бездепозита нет, welcome с минимальным депозитом — самый надёжный путь.</p>
        <h3 id="exp-dep-alt">Минимальный депозит как практичная альтернатива</h3>
        <p>Пополнение от 130 000 UZS через <a href="{h('tolov')}">Humo, Uzcard, Payme, Click</a> занимает несколько минут. При первом депозите выбирается одно направление: казино welcome или спорт welcome — оба одновременно недоступны. 150 фриспинов в казино-пакете начисляются поэтапно; выигрыш с них идёт на бонусный баланс с отыгрышем ×35 на слотах.</p>
        {tbl([
            ("Предложение", "Объём", "Отыгрыш"),
            ("Казино welcome", "20 200 000 UZS + 150 FS", "×35 слоты"),
            ("Спорт welcome", "до 1 400 000 UZS", "×5 экспресс"),
            ("Бездепозит (временный)", "раздел PROMO", "Отдельный"),
            ("Мин. депозит", "~130 000 UZS", "—"),
        ])}
        <h3 id="exp-dep-steps">Шаги: бездепозит или welcome</h3>
        {ol([
            f'<a href="{h("registratsiya")}">Зарегистрируйтесь</a> — телефон или email, пароль, валюта UZS.',
            'Проверьте раздел PROMO на карточку бездепозита.',
            'Если её нет — внесите минимальный депозит с кодом <strong>fa_1635</strong>.',
            f'Для казино читайте <a href="{h("kazino")}">бонусы казино</a>, для спорта — <a href="{h("sport")}">спорт-бонусы</a>.',
            f'Сроки отыгрыша уточните в <a href="{h("faq")}">FAQ</a> и на странице <a href="{h("promo")}">промокод</a>.',
        ])}
        <h3 id="exp-dep-risk">Безопасность и ответственная игра</h3>
        <p>Бонус — дополнительная возможность, а не гарантия дохода. Изучите лимиты, перерывы и сведения о <a href="{h('litsenziya')}">лицензии</a>. Используйте только официальный сайт FairPari или <a href="{h('mobil')}">мобильное приложение</a>; избегайте ссылок «бесплатный бонус» в мессенджерах. При запросе KYC отправьте документы вовремя — это ускорит вывод.</p>
        <p>Перед попыткой получить бездепозит помните: оператор может менять условия. Каждый раз перед депозитом читайте текст карточки PROMO — минимальный коэффициент, max bet и список игр указаны там. Отыгрыш казино и спорта не смешивается; выберите одно направление и действуйте по плану.</p>
        {faq([
            ("Есть ли сейчас бездепозитный бонус?", "Постоянный пакет не всегда объявлен; актуальный список в PROMO. Welcome с мин. депозитом — стабильная альтернатива."),
            ("150 FS считаются бездепозитными?", "Нет — они обычно часть казино welcome при первом депозите."),
            ("Куда вводить fa_1635?", f"При регистрации или в окне депозита; подробнее на странице <a href=\"{h('promo')}\">промокод</a>."),
            ("Сколько дней на отыгрыш?", "Казино ×35 — обычно 7–30 дней; спорт ×5 — короче. Точный срок на карточке PROMO."),
            ("Можно ли совместить бездепозит и welcome?", "Нет — при первом депозите выбирается один welcome; дальнейшие акции отдельно в PROMO."),
        ])}
        {disc("ru")}"""
        else:
            C[("depozitsiz", "en")] = f"""
        <h2 id="exp-dep-holat">FairPari no-deposit bonus — current status and alternatives</h2>
        <p>Players in Uzbekistan often search for a <strong>no-deposit bonus</strong>: the wish to receive free spins or bets without funding an account is understandable. FairPari may not list a permanent classic no-deposit package every day, yet a <strong>minimum deposit</strong> (around <strong>130,000 UZS</strong>) unlocks a large welcome — casino <strong>20,200,000 UZS + 150 free spins</strong>, sports up to <strong>1,400,000 UZS</strong>. Promo code <strong>fa_1635</strong> is entered at registration or deposit; terms are updated in the PROMO section.</p>
        <p>Temporary no-deposit promos — tournament prizes, cashback, FS on selected slots — may appear from time to time. A «not available» status on this page differs from scam ads: we only report verified amounts and wagering (casino <strong>×35</strong>, sports <strong>×5</strong>). If no no-deposit card is shown, welcome with minimum deposit is the most reliable path.</p>
        <h3 id="exp-dep-alt">Minimum deposit as a practical alternative</h3>
        <p>Topping up from 130,000 UZS via <a href="{h('tolov')}">Humo, Uzcard, Payme, Click</a> takes a few minutes. On the first deposit you choose one direction: casino welcome or sports welcome — both cannot be taken together. The 150 free spins in the casino pack are credited in stages; winnings go to the bonus balance with ×35 wagering on slots.</p>
        {tbl([
            ("Offer", "Volume", "Wagering"),
            ("Casino welcome", "20,200,000 UZS + 150 FS", "×35 slots"),
            ("Sports welcome", "up to 1,400,000 UZS", "×5 accumulator"),
            ("No-deposit (temporary)", "PROMO section", "Separate"),
            ("Min. deposit", "~130,000 UZS", "—"),
        ])}
        <h3 id="exp-dep-steps">Steps: no-deposit or welcome</h3>
        {ol([
            f'<a href="{h("registratsiya")}">Register</a> — phone or email, password, currency UZS.',
            'Check the PROMO section for an active no-deposit card.',
            'If none — make a minimum deposit with code <strong>fa_1635</strong>.',
            f'For casino read <a href="{h("kazino")}">casino bonuses</a>; for sports see <a href="{h("sport")}">sports bonuses</a>.',
            f'Confirm wagering deadlines in <a href="{h("faq")}">FAQ</a> and on the <a href="{h("promo")}">promo code</a> page.',
        ])}
        <h3 id="exp-dep-risk">Safety and responsible play</h3>
        <p>A bonus is extra opportunity, not guaranteed income. Review limits, cool-off tools, and <a href="{h('litsenziya')}">licence</a> information. Use only the official FairPari site or <a href="{h('mobil')}">mobile app</a>; avoid «free bonus» links in messengers. If KYC is requested, submit documents promptly to avoid withdrawal delays.</p>
        <p>When trying to claim a no-deposit offer, remember the operator may change terms. Before each deposit read the PROMO card text — minimum odds, max bet, and eligible games are listed there. Casino and sports wagering do not mix; pick one direction and plan accordingly.</p>
        {faq([
            ("Is a no-deposit bonus available now?", "A permanent package is not always advertised; check PROMO. Welcome with min. deposit is the stable alternative."),
            ("Are the 150 FS no-deposit?", "No — they are typically part of casino welcome on first deposit."),
            ("Where do I enter fa_1635?", f"At registration or in the deposit window; details on the <a href=\"{h('promo')}\">promo code</a> page."),
            ("How many days for wagering?", "Casino ×35 — usually 7–30 days; sports ×5 — shorter. Exact term on the PROMO card."),
            ("Can no-deposit and welcome be combined?", "No — one welcome is chosen on first deposit; further promos are separate in PROMO."),
        ])}
        {disc("en")}"""

    # Continue with remaining page keys - I'll add them in the script
    return C

if __name__ == "__main__":
  print("partial", len(build_all()))

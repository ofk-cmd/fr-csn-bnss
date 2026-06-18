#!/usr/bin/env python3
"""One-off generator for page_expand_1000_content.py — run once then delete."""
from pathlib import Path

OUT = Path(__file__).parent / "page_expand_1000_content.py"

SLUGS = {
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

PAGE_FILES = {
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


def href(lang: str, page_key: str, target: str) -> str:
    prefix = "" if page_key == "index" else "../"
    slug = SLUGS[lang][target]
    if not slug:
        return "./" if page_key == "index" else "../"
    return f"{prefix}{slug}/"


# Content builders — each returns inner HTML (without section wrapper)
CONTENT_BUILDERS = {}


def content_uz_depozitsiz(h):
    return f"""
        <h2 id="depozitsiz-holat">FairPari depozitsiz bonus — joriy holat</h2>
        <p>O'zbekiston o'yinchilari tez-tez <strong>depozitsiz bonus</strong> (no deposit) qidiradi: balansni to'ldirmasdan bepul stavka yoki aylantirish olish istagi tushunarli. FairPari da doimiy klassik depozitsiz paket har kuni ko'rinmasligi mumkin, lekin <strong>minimal depozit</strong> (taxminan <strong>130 000 UZS</strong>) bilan birinchi to'ldirishda katta welcome ochiladi: kazino yo'nalishi <strong>20 200 000 UZS + 150 bepul aylantirish</strong>, sport yo'nalishi esa <strong>1 400 000 UZS</strong> gacha. Promokod <strong>fa_1635</strong> ro'yxatdan o'tishda yoki depozitda kiritiladi — shartlar PROMO bo'limida yangilanadi.</p>
        <p>Depozitsiz takliflar odatda vaqtinchalik: turnir sovrinlari, cashback, ba'zi slotlarda FS aksiyalari. Agar sahifada «depozitsiz yo'q» deb yozilgan bo'lsa, bu rasmiy siyosatni aks ettiradi — aldamchi «100% bepul» reklamalarga ishonmang. Biz faqat tekshirilgan summalar va wagering (kazino <strong>×35</strong>, sport <strong>×5</strong>) haqida yozamiz.</p>

        <h3 id="depozitsiz-alternativa">Minimal depozit — amaliy alternativa</h3>
        <p>130 000 UZS atrofidagi minimal to'ldirish Humo, Uzcard, Payme yoki Click orqali bir necha daqiqada o'tadi. Birinchi depozitda kazino yoki sport welcome tanlanadi — ikkalasini bir vaqtda olish mumkin emas. Kazino paketidagi 150 FS odatda belgilangan slotlarda beriladi; ularning yutug'i bonus balansiga tushadi va ×35 aylantirish talab qilinadi.</p>
        <table class="data-table">
          <thead><tr><th>Taklif turi</th><th>Summa / hajm</th><th>Wagering</th></tr></thead>
          <tbody>
            <tr><td>Kazino welcome</td><td>20 200 000 UZS + 150 FS</td><td>×35 (slotlar)</td></tr>
            <tr><td>Sport welcome</td><td>1 400 000 UZS gacha</td><td>×5 (ekspress)</td></tr>
            <tr><td>Depozitsiz (vaqtinchalik)</td><td>PROMO bo'limida</td><td>Alohida qoidalar</td></tr>
            <tr><td>Min. depozit</td><td>~130 000 UZS</td><td>—</td></tr>
          </tbody>
        </table>

        <h3 id="depozitsiz-qanday">Depozitsiz yoki welcome — qanday tanlash</h3>
        <ol>
          <li><a href="{h('registratsiya')}">Ro'yxatdan o'ting</a> va valyutani UZS qilib belgilang.</li>
          <li>PROMO yoki aksiyalar bo'limida depozitsiz kartochka bormi — tekshiring.</li>
          <li>Agar yo'q bo'lsa, <strong>fa_1635</strong> bilan minimal depozit qiling.</li>
          <li>Kazino uchun <a href="{h('kazino')}">kazino bonuslari</a>, sport uchun <a href="{h('sport')}">sport bonuslari</a> sahifasini o'qing.</li>
          <li><a href="{h('tolov')}">To'lov usullari</a> va <a href="{h('faq')}">FAQ</a> orqali wagering muddatini aniqlang.</li>
        </ol>

        <h3 id="depozitsiz-xavfsizlik">Xavfsizlik va mas'uliyat</h3>
        <p>Bonus — qo'shimcha imkoniyat, daromad kafolati emas. Shaxsiy limitlar, tanaffus va <a href="{h('litsenziya')}">litsenziya</a> ma'lumotlarini o'qing. Faqat rasmiy FairPari ilovasi yoki saytidan foydalaning; Telegramdagi «bepul bonus» havolalaridan qoching.</p>

        <h3 id="depozitsiz-faq">Tez-tez so'raladigan savollar</h3>
        <dl class="faq-list">
          <dt>Hozir depozitsiz bonus bormi?</dt>
          <dd>Doimiy paket har doim e'lon qilinmaydi; joriy ro'yxat PROMO da. Minimal depozit welcome doimiy alternativadir.</dd>
          <dt>150 FS depozitsiz hisoblanadimi?</dt>
          <dd>Yo'q — ular odatda birinchi depozit bilan bog'liq kazino welcome qismidir.</dd>
          <dt>fa_1635 qayerga yoziladi?</dt>
          <dd>Ro'yxatdan o'tishda yoki depozit oynasida; <a href="{h('promo')}">promo-kod</a> bo'limida batafsil.</dd>
          <dt>Wagering qancha kun?</dt>
          <dd>Kazino ×35 — odatda 7–30 kun; sport ×5 — qisqaroq. Aniq muddat PROMO kartochkasida.</dd>
        </dl>
        <p class="disclaimer"><strong>18+.</strong> Qimor o'yinlari moliyaviy xavf tug'diradi. Mas'uliyat bilan o'ynang.</p>"""


def content_ru_depozitsiz(h):
    return f"""
        <h2 id="depozitsiz-holat">Бездепозитный бонус FairPari — актуальный статус</h2>
        <p>Игроки из Узбекистана часто ищут <strong>бонус без депозита</strong>: желание получить бесплатные ставки или вращения без пополнения счёта понятно. На FairPari постоянный классический no-deposit пакет может отсутствовать в конкретный день, зато при <strong>минимальном депозите</strong> (около <strong>130 000 UZS</strong>) открывается крупный welcome: казино <strong>20 200 000 UZS + 150 фриспинов</strong>, спорт <strong>до 1 400 000 UZS</strong>. Промокод <strong>fa_1635</strong> вводится при регистрации или депозите — условия обновляются в разделе PROMO.</p>
        <p>Бездепозитные предложения обычно временные: турнирные призы, кэшбэк, акции FS на отдельных слотах. Если на странице указано, что бездепозитного бонуса нет, это отражает официальную политику — не доверяйте рекламе «100% бесплатно». Мы пишем только о проверенных суммах и отыгрыше (казино <strong>×35</strong>, спорт <strong>×5</strong>).</p>

        <h3 id="depozitsiz-alternativa">Минимальный депозит как практичная альтернатива</h3>
        <p>Пополнение от 130 000 UZS через Humo, Uzcard, Payme или Click занимает несколько минут. При первом депозите выбирается казино или спорт welcome — оба одновременно недоступны. 150 FS в казино-пакете начисляются на выбранные слоты; выигрыш с них идёт на бонусный баланс с отыгрышем ×35.</p>
        <table class="data-table">
          <thead><tr><th>Тип предложения</th><th>Сумма / объём</th><th>Отыгрыш</th></tr></thead>
          <tbody>
            <tr><td>Казино welcome</td><td>20 200 000 UZS + 150 FS</td><td>×35 (слоты)</td></tr>
            <tr><td>Спорт welcome</td><td>до 1 400 000 UZS</td><td>×5 (экспресс)</td></tr>
            <tr><td>Бездепозит (временный)</td><td>в разделе PROMO</td><td>Отдельные правила</td></tr>
            <tr><td>Мин. депозит</td><td>~130 000 UZS</td><td>—</td></tr>
          </tbody>
        </table>

        <h3 id="depozitsiz-qanday">Как выбрать между бездепозитом и welcome</h3>
        <ol>
          <li><a href="{h('registratsiya')}">Зарегистрируйтесь</a> и выберите валюту UZS.</li>
          <li>Проверьте раздел PROMO на карточку бездепозита.</li>
          <li>Если её нет — внесите минимальный депозит с кодом <strong>fa_1635</strong>.</li>
          <li>Для казино читайте <a href="{h('kazino')}">бонусы казино</a>, для спорта — <a href="{h('sport')}">спорт-бонусы</a>.</li>
          <li>Уточните сроки отыгрыша в <a href="{h('tolov')}">оплате</a> и <a href="{h('faq')}">FAQ</a>.</li>
        </ol>

        <h3 id="depozitsiz-xavfsizlik">Безопасность и ответственность</h3>
        <p>Бонус — дополнительная возможность, а не гарантия дохода. Изучите лимиты, перерывы и данные о <a href="{h('litsenziya')}">лицензии</a>. Используйте только официальное приложение или сайт FairPari; избегайте ссылок «бесплатный бонус» в мессенджерах.</p>

        <h3 id="depozitsiz-faq">Частые вопросы</h3>
        <dl class="faq-list">
          <dt>Есть ли сейчас бездепозитный бонус?</dt>
          <dd>Постоянный пакет не всегда объявлен; актуальный список в PROMO. Welcome с минимальным депозитом — стабильная альтернатива.</dd>
          <dt>150 FS считаются бездепозитными?</dt>
          <dd>Нет — они обычно часть казино welcome при первом депозите.</dd>
          <dt>Куда вводить fa_1635?</dt>
          <dd>При регистрации или в окне депозита; подробнее в разделе <a href="{h('promo')}">промокод</a>.</dd>
          <dt>Сколько дней на отыгрыш?</dt>
          <dd>Казино ×35 — обычно 7–30 дней; спорт ×5 — короче. Точный срок на карточке PROMO.</dd>
        </dl>
        <p class="disclaimer"><strong>18+.</strong> Азартные игры связаны с финансовым риском. Играйте ответственно.</p>"""


def content_en_depozitsiz(h):
    return f"""
        <h2 id="depozitsiz-holat">FairPari no-deposit bonus — current status</h2>
        <p>Players in Uzbekistan often search for a <strong>no-deposit bonus</strong>: the wish to receive free bets or spins without funding an account is understandable. FairPari may not list a permanent classic no-deposit package every day, yet a <strong>minimum deposit</strong> (around <strong>130,000 UZS</strong>) unlocks a large welcome: casino <strong>20,200,000 UZS + 150 free spins</strong>, sports up to <strong>1,400,000 UZS</strong>. Promo code <strong>fa_1635</strong> is entered at registration or deposit — terms are updated in the PROMO section.</p>
        <p>No-deposit offers are usually temporary: tournament prizes, cashback, FS promos on selected slots. If this page states that no deposit bonus is unavailable, that reflects official policy — do not trust ads promising «100% free». We only report verified amounts and wagering (casino <strong>×35</strong>, sports <strong>×5</strong>).</p>

        <h3 id="depozitsiz-alternativa">Minimum deposit as a practical alternative</h3>
        <p>Topping up from 130,000 UZS via Humo, Uzcard, Payme, or Click takes a few minutes. On the first deposit you choose casino or sports welcome — both cannot be taken together. The 150 FS in the casino pack are credited on designated slots; winnings go to the bonus balance with ×35 wagering.</p>
        <table class="data-table">
          <thead><tr><th>Offer type</th><th>Amount / volume</th><th>Wagering</th></tr></thead>
          <tbody>
            <tr><td>Casino welcome</td><td>20,200,000 UZS + 150 FS</td><td>×35 (slots)</td></tr>
            <tr><td>Sports welcome</td><td>up to 1,400,000 UZS</td><td>×5 (accumulator)</td></tr>
            <tr><td>No-deposit (temporary)</td><td>in PROMO section</td><td>Separate rules</td></tr>
            <tr><td>Min. deposit</td><td>~130,000 UZS</td><td>—</td></tr>
          </tbody>
        </table>

        <h3 id="depozitsiz-qanday">Choosing between no-deposit and welcome</h3>
        <ol>
          <li><a href="{h('registratsiya')}">Register</a> and set currency to UZS.</li>
          <li>Check PROMO for an active no-deposit card.</li>
          <li>If none — make a minimum deposit with code <strong>fa_1635</strong>.</li>
          <li>For casino read <a href="{h('kazino')}">casino bonuses</a>; for sports see <a href="{h('sport')}">sports bonuses</a>.</li>
          <li>Confirm wagering deadlines via <a href="{h('tolov')}">payments</a> and <a href="{h('faq')}">FAQ</a>.</li>
        </ol>

        <h3 id="depozitsiz-xavfsizlik">Safety and responsibility</h3>
        <p>A bonus is extra opportunity, not guaranteed income. Review limits, cool-off tools, and <a href="{h('litsenziya')}">licence</a> information. Use only the official FairPari app or website; avoid «free bonus» links in messengers.</p>

        <h3 id="depozitsiz-faq">Frequently asked questions</h3>
        <dl class="faq-list">
          <dt>Is a no-deposit bonus available now?</dt>
          <dd>A permanent package is not always advertised; check PROMO. Welcome with minimum deposit is the stable alternative.</dd>
          <dt>Are the 150 FS no-deposit?</dt>
          <dd>No — they are typically part of casino welcome on first deposit.</dd>
          <dt>Where do I enter fa_1635?</dt>
          <dd>At registration or in the deposit window; details on the <a href="{h('promo')}">promo code</a> page.</dd>
          <dt>How many days for wagering?</dt>
          <dd>Casino ×35 — usually 7–30 days; sports ×5 — shorter. Exact term on the PROMO card.</dd>
        </dl>
        <p class="disclaimer"><strong>18+.</strong> Gambling involves financial risk. Play responsibly.</p>"""

# ... I'll continue with all other page keys in the generator

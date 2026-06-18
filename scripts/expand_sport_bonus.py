#!/usr/bin/env python3
"""Expand sport-bonuslari (UZ) and ru/sport-bonusy to 1200+ visible words."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

UZ_BLOCK = '''
    <section class="section section--content" id="sport-bonus-guide">
      <div class="container prose">
        <h2 id="sport-welcome">Sport welcome bonusi — 1 400 000 UZS gacha 100%</h2>
        <p>FairPari sport bonusi <strong>birinchi depozit</strong> uchun alohida yo'nalish: kazino welcome (20 200 000 UZS + 150 FS) bilan bir vaqtda tanlash mumkin emas — ro'yxatdan o'tishda yoki PROMO bo'limida sport paketini belgilang. Maksimal 100% bonus <strong>1 400 000 UZS</strong> gacha (tekshiruv 18.06.2026, fairpari.com/uz PROMO). Minimal depozit va max bet PROMO kartochkasida ko'rsatiladi.</p>
        <p>Sport welcome faqat <strong>pre-match va live</strong> stavkalar uchun: futbol (Premier League, La Liga, Serie A), basketbol (NBA, Evroliga), tennis (ATP/WTA), kibersport va boshqa bozorlar. Virtual sport va ba'zi maxsus bozorlar wagering hisobiga kirmasligi mumkin — har doim qoidalarni o'qing.</p>

        <h2 id="ekspress-bonus">Ekspress va kombinatsiya aksiyalari</h2>
        <p>Ekspress (kombinatsiya) stavkalar — sport bonusining asosiy vositasi: ko'p hodisali kuponlarda koeffitsientlar ko'payadi, shuning uchun operatorlar ekspresslarga alohida <strong>cashback yoki bonus foizi</strong> beradi. FairPari da muntazam «ekspress booster» va turnirlar bo'lishi mumkin; joriy ro'yxat PROMO yoki «Aksiyalar» bo'limida.</p>
        <ul>
          <li><strong>3+ hodisa</strong> — minimal ekspress kupon (odatda wagering hisobiga kiradi)</li>
          <li><strong>Har bir hodisa koeff. ≥ 1.40</strong> — sport welcome wagering sharti (×5)</li>
          <li><strong>Ekspress turnirlari</strong> — haftalik reyting, sovrin fondi UZS</li>
          <li><strong>Freebet</strong> — ba'zi aksiyalarda depozitsiz stavka (alohida shartlar)</li>
        </ul>

        <h2 id="wagering-sport">Wagering sport bonusida — ×5 qoidasi</h2>
        <p>Sport welcome <strong>×5 wagering</strong> talab qiladi: bonus summasini (yoki depozit+bonus — PROMO matniga qarang) ekspress stavkalarda aylantirish kerak. Har bir hodisa odatda <strong>minimal 1.40 koeffitsient</strong> bilan hisoblanadi. Kazino bonusidagi ×35 dan farqli ravishda sportda muddat qisqaroq bo'lishi mumkin (7–14 kun).</p>
        <table class="data-table">
          <thead><tr><th>Parametr</th><th>Sport welcome</th><th>Kazino welcome</th></tr></thead>
          <tbody>
            <tr><td>Maks. bonus</td><td>1 400 000 UZS</td><td>20 200 000 UZS + 150 FS</td></tr>
            <tr><td>Wagering</td><td>×5 (ekspress)</td><td>×35 (slotlar)</td></tr>
            <tr><td>Minimal koeff.</td><td>1.40 / hodisa</td><td>Slotlar 100% (ba'zi istisnolar)</td></tr>
            <tr><td>Tanlov</td><td>Sport yoki kazino</td><td>Bir vaqtda emas</td></tr>
          </tbody>
        </table>

        <h2 id="faollashtirish">Sport bonusini qanday faollashtirish</h2>
        <ol>
          <li><strong>Ro'yxatdan o'ting</strong> — telefon yoki email, parol, valyuta UZS</li>
          <li><strong>Sport welcome tanlang</strong> — birinchi depozitda kazino o'rniga sport paketi</li>
          <li><strong>Depozit kiriting</strong> — Humo, Uzcard, Payme, Click (min. summa PROMO da)</li>
          <li><strong>Ekspress tuzing</strong> — 3+ hodisa, har biri ≥ 1.40</li>
          <li><strong>Wagering tugaguncha</strong> — yechishdan oldin shartlarni bajaring</li>
        </ol>
        <p>Batafsil qo'llanma: <a href="../royxatdan-otish/">ro'yxatdan o'tish</a>, <a href="../tolov/">to'lov usullari</a>, <a href="../kazino-bonuslari/">kazino welcome</a> (alternativa).</p>

        <h2 id="sport-bozorlar">Sport bozorlari va cheklovlar</h2>
        <p>FairPari sport liniyasi O'zbekiston o'yinchilari uchun keng: futbol chempionatlari, xalqaro turnirlar, basketbol, tennis, MMA, kriket, kibersport. Live bo'limida o'yin davomida koeffitsientlar yangilanadi. Ba'zi bozorlar (masalan, «ikki imkoniyat» yoki juda past koeff.) wagering hisobiga kirmaydi — PROMO footnote ni tekshiring.</p>
        <p><strong>Max bet</strong> bonus bilan stavka qilganda cheklangan bo'lishi mumkin (odatda bonusning 10–20%). Limitdan oshish bonus bekor qilinishiga olib keladi.</p>

        <h2 id="sport-faq">Sport bonusi — tez-tez so'raladigan savollar</h2>
        <dl class="faq-list">
          <dt>Sport va kazino bonusini birga olsam bo'ladimi?</dt>
          <dd>Yo'q — birinchi depozitda bitta yo'nalish tanlanadi. Keyingi aksiyalar PROMO da alohida.</dd>
          <dt>Wagering qancha vaqt beriladi?</dt>
          <dd>Odatda 7–14 kun; aniq muddat PROMO kartochkasida.</dd>
          <dt>Live stavka wagering hisoblanadimi?</dt>
          <dd>Ha, agar minimal koeff. va ekspress shartlari bajarilsa.</dd>
          <dt>Yechish qachon ochiladi?</dt>
          <dd>×5 wagering tugagach va KYC (kerak bo'lsa) o'tgach — <a href="../pul-yechish/">yechish qoidalari</a>.</dd>
          <dt>1.4M dan ko'p bonus olish mumkinmi?</dt>
          <dd>Yo'q — sport welcome maksimumi 1 400 000 UZS (100% birinchi depozit).</dd>
        </dl>
      </div>
    </section>'''

RU_BLOCK = '''
    <section class="section section--content" id="sport-bonus-guide">
      <div class="container prose">
        <h2 id="sport-welcome">Приветственный спорт-бонус — до 1 400 000 UZS 100%</h2>
        <p>Спортивный welcome FairPari — <strong>отдельное направление</strong> для первого депозита: пакет казино (20 200 000 UZS + 150 FS) одновременно выбрать нельзя. Максимум <strong>1 400 000 UZS</strong> по проверке 18.06.2026 (fairpari.com/uz PROMO). Минимальный депозит и max bet — в карточке PROMO.</p>
        <p>Бонус действует на <strong>прематч и live</strong>: футбол, баскетбол, теннис, киберспорт и др. Виртуальный спорт может не учитываться в отыгрыше — читайте правила.</p>

        <h2 id="ekspress-bonus">Экспрессы и комбинированные акции</h2>
        <p>Экспресс-ставки — основной инструмент отыгрыша: мультипликаторы коэффициентов, регулярные бустеры и турниры в разделе «Акции». Типичные условия:</p>
        <ul>
          <li><strong>3+ события</strong> в купоне</li>
          <li><strong>Каждое событие ≥ 1.40</strong> — для отыгрыша ×5</li>
          <li><strong>Freebet</strong> — в отдельных промо (свои условия)</li>
        </ul>

        <h2 id="wagering-sport">Отыгрыш спорт-бонуса — ×5</h2>
        <p>Требуется <strong>×5 вейджер</strong> на экспрессах. В казино — ×35 на слотах. Срок обычно 7–14 дней.</p>
        <table class="data-table">
          <thead><tr><th>Параметр</th><th>Спорт welcome</th><th>Казино welcome</th></tr></thead>
          <tbody>
            <tr><td>Макс. бонус</td><td>1 400 000 UZS</td><td>20 200 000 UZS + 150 FS</td></tr>
            <tr><td>Вейджер</td><td>×5 (экспресс)</td><td>×35 (слоты)</td></tr>
            <tr><td>Мин. коэфф.</td><td>1.40 / событие</td><td>Слоты 100%</td></tr>
          </tbody>
        </table>

        <h2 id="faollashtirish">Как активировать спорт-бонус</h2>
        <ol>
          <li>Регистрация — UZS, телефон/email</li>
          <li>Выбор <strong>спорт welcome</strong> при первом депозите</li>
          <li>Депозит Humo, Uzcard, Payme, Click</li>
          <li>Экспресс 3+ события, коэфф. ≥ 1.40</li>
          <li>Отыгрыш ×5, затем вывод</li>
        </ol>
        <p>Подробнее: <a href="../../ru/registratsiya/">регистрация</a>, <a href="../../ru/oplata/">оплата</a>, <a href="../../ru/bonusy-kazino/">казино welcome</a>.</p>

        <h2 id="sport-bozorlar">Линия и ограничения</h2>
        <p>Широкая линия для UZ: футбол, баскетбол, теннис, MMA, киберспорт. Live с обновлением коэффициентов. Max bet при игре с бонусом ограничен — превышение может аннулировать бонус.</p>

        <h2 id="sport-faq">FAQ по спорт-бонусу</h2>
        <dl class="faq-list">
          <dt>Можно ли взять спорт и казино вместе?</dt>
          <dd>Нет — один выбор на первый депозит.</dd>
          <dt>Сколько дней на отыгрыш?</dt>
          <dd>Обычно 7–14 дней по PROMO.</dd>
          <dt>Учитывается ли live?</dt>
          <dd>Да, при соблюдении мин. коэфф. и экспресса.</dd>
          <dt>Когда доступен вывод?</dt>
          <dd>После ×5 и KYC при необходимости.</dd>
        </dl>
      </div>
    </section>'''


def inject(path: Path, block: str, marker: str = 'id="related-pages"'):
    text = path.read_text(encoding='utf-8')
    if 'id="sport-bonus-guide"' in text:
        print(f'  skip (already expanded): {path}')
        return False
    idx = text.find(marker)
    if idx == -1:
        print(f'  ERROR marker not found: {path}')
        return False
    # insert before related section
    sec_start = text.rfind('<section', 0, idx)
    text = text[:sec_start] + block + '\n    ' + text[sec_start:]
    path.write_text(text, encoding='utf-8')
    return True


def main():
    pairs = [
        (ROOT / 'sport-bonuslari/index.html', UZ_BLOCK),
        (ROOT / 'ru/sport-bonusy/index.html', RU_BLOCK),
    ]
    for path, block in pairs:
        if inject(path, block):
            print(f'expanded: {path.relative_to(ROOT)}')


if __name__ == '__main__':
    main()

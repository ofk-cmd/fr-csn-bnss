#!/usr/bin/env python3
"""Final content pass — safe phrases only, no short tokens that break URLs."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent

RU = [
    ('Mundarija', 'Содержание'),
    ('Промокод qayerda вводится', 'Где вводить промокод'),
    ('Provayder turnirlari', 'Турниры провайдеров'),
    ('Operator manzili', 'Адрес оператора'),
    ('Qidiruvdagi nusxa saytlar xavfli bo\'lishi возможно', 'Копии сайтов в поиске могут быть опасны'),
    ('только rasmiy domen yoki ishonchli партнёрские ссылкиiот foydalaning', 'используйте только официальный домен или проверенные партнёрские ссылки'),
    ('депозит qabul qilmaydi', 'не принимает депозиты'),
    ('bu независимый yo\'riqnoma', 'это независимое руководство'),
    ('аккаунт открытие', 'открытие аккаунта'),
    ('bonus условия', 'условия бонуса'),
    ('мобильное приложение', 'мобильное приложение'),
    ('sport и kazino bitta аккаунтda', 'спорт и казино в одном аккаунте'),
    ('отдельный вход не нужен', 'отдельный вход не нужен'),
    ('yuqoridagi jadval', 'таблица выше'),
    ('Haqiqat и miflar', 'Факты и мифы'),
    ('Bonus получить', 'Получить бонус'),
    ('Savollar', 'Вопросы'),
    ('12 000+ avtomat', '12 000+ автоматов'),
    ('жанр и провайдер по', 'по жанру и провайдеру'),
    ('Ruletka, blackjack', 'Рулетка, блэкджек'),
    ('слот в кармане', 'слоты в кармане'),
    ('срокlar', 'сроки'),
    ('Игроки fikri', 'Мнения игроков'),
    ('Slot и вывод опыт', 'Слоты и опыт вывода'),
    ('Bonus jadvali', 'Таблица бонусов'),
    ('4 bosqichli welcome', 'welcome в 4 этапа'),
    ('Kod ввод', 'Ввод кода'),
    ('Регистрация formasi', 'форма регистрации'),
    ('Frispin слот', 'Фриспин-слоты'),
    ('150 FS qaysi игрыda', '150 FS на каких играх'),
    ('Мобильное promo', 'Мобильное промо'),
    ('Kod приложениеda', 'Код в приложении'),
    ('Muddatlar jadvali', 'Таблица сроков'),
    ('Minimal лимит', 'Минимальный лимит'),
    ('Мобильное касса', 'Мобильная касса'),
    ('Bonus депозит', 'Бонусный депозит'),
    ('Welcome активация', 'Активация welcome'),
    ('Безопасно manzil', 'Безопасный адрес'),
    ('Мобильное вход', 'Мобильный вход'),
    ('APK sessiya', 'Сессия в APK'),
    ('Yangi аккаунт', 'Новый аккаунт'),
    ('Регистрация 4 usul', 'Регистрация 4 способами'),
    ('Oldin ro\'yxatот o\'tgan bo\'lsangiz', 'Если уже регистрировались'),
    ('главная sahifasidagi', 'на главной странице'),
    ('orqali kiring', 'войдите через'),
    ('Парольni unutgan bo\'lsangiz', 'Если забыли пароль'),
    ('tiklash', 'восстановление'),
    ('Неизвестный havolalarот', 'Не переходите по сомнительным ссылкам'),
    ('«FairPari вход» linklariga bosmang', 'на «FairPari вход»'),
    ('приложениеda', 'в приложении'),
    ('платежи</a> для qulay', 'платежи</a> для удобства'),
    ('rasmiy', 'официальный'),
    ('Rasmiy', 'Официальный'),
    ('xavfsiz', 'безопасно'),
    ('Xavfsiz', 'Безопасно'),
    ('royxatdan', 'регистрация'),
    ('Royxatdan', 'Регистрация'),
]

EN = [
    ('Mundarija', 'Contents'),
    ('Savollar', 'Questions'),
    ('12 000+ avtomat', '12,000+ machines'),
    ('Ruletka', 'Roulette'),
    ('fikri', 'reviews'),
    ('manzil', 'address'),
    ('jadvali', 'table'),
    ('bosqichli', 'stage'),
    ('formasi', 'form'),
    ('qaysi', 'which'),
    ('игрыda', 'games'),
    ('Muddatlar', 'Deadlines'),
    ('Haqiqat и miflar', 'Facts and myths'),
    ('Bonus получить', 'Get bonus'),
    ('Operator manzili', 'Operator address'),
    ('rasmiy domen', 'official domain'),
    ('ishonchli', 'trusted'),
    ('foydalaning', 'use'),
    ('qabul qilmaydi', 'does not accept'),
    ('yo\'riqnoma', 'guide'),
    ('bitta аккаунтda', 'one account'),
    ('yuqoridagi jadval', 'table above'),
    ('avtomat', 'machines'),
    ('sрокlar', 'deadlines'),
    ('Royxat', 'Sign up'),
    ('ro\'yxat', 'sign up'),
    ('sahifasidagi', 'page'),
    ('orqali kiring', 'log in via'),
    ('unutgan', 'forgot'),
    ('havolalarот', 'from links'),
    ('bosmang', 'do not click'),
    ('ilovada', 'in the app'),
    ('qulay', 'convenience'),
]

def apply(path, phrases):
    h = path.read_text(encoding='utf-8')
    phrases = sorted(phrases, key=lambda x: len(x[0]), reverse=True)
    for a, b in phrases:
        h = h.replace(a, b)
    path.write_text(h, encoding='utf-8')

if __name__ == '__main__':
    for p in (ROOT/'ru').rglob('*.html'):
        apply(p, RU)
    for p in (ROOT/'en').rglob('*.html'):
        apply(p, EN)
    print('Final pass done')

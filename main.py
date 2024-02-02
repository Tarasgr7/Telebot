import telebot
from telebot import types
import json
import requests
import time
import datetime
import os

TOKEN = '6916893480:AAHzRGLmyBa5PxwBx1Vc49q1ppB_mwuCyn0'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    item1 = types.KeyboardButton("Розклад")
    item2 = types.KeyboardButton("Погода")
    item3 = types.KeyboardButton("Викладачі")
    item4 = types.KeyboardButton("Графік пар")
    markup.add(item1, item2, item3, item4)

    bot.send_message(message.chat.id, "Козаче, мені потрібно дізнатись чого ти бажаєш ?", reply_markup=markup)


@bot.message_handler(commands=['materials'])
def send_materials(message):
    try:
        directory = 'materials'
        files = os.listdir(directory)

        for file in files:
            file_path = os.path.join(directory, file)
            with open(file_path, 'rb') as f:
                bot.send_document(message.chat.id, f)

        if not files:
            bot.send_message(message.chat.id, "У папці немає файлів.")

    except Exception as e:
        bot.reply_to(message, "Сталася помилка під час надсилання файлів.")


# Обробник кнопки "Розклад"
@bot.message_handler(func=lambda message: message.text == "Розклад")
def schedule(message):
    with open('data.txt', 'r', encoding='UTF-8') as file:
        schedule_text = file.read()
    bot.send_message(message.chat.id, schedule_text)


# Обробник кнопки "Викладачі"
@bot.message_handler(func=lambda message: message.text == "Викладачі")
def teachers(message):
    markup = types.ReplyKeyboardRemove(selective=False)

    # Створення кнопок для викладачів
    teacher_buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Програмування')
    item2 = types.KeyboardButton('Чисельні методи')
    item9 = types.KeyboardButton('Куратор')
    item4 = types.KeyboardButton('Правознавство')
    item5 = types.KeyboardButton('Комп\'ютерні технології обробки данних')
    item6 = types.KeyboardButton('Схемотехніка та архітектура пк')
    item7 = types.KeyboardButton('Іноземна мова')
    item8 = types.KeyboardButton('Вища математика')
    item3 = types.KeyboardButton('Мережеві технології')
    item10 = types.KeyboardButton("Повернутися")

    # Додайте кнопки для інших предметів

    teacher_buttons.row(item1, item2)
    teacher_buttons.row(item3, item4)
    teacher_buttons.row(item5, item6)
    teacher_buttons.row(item7, item8)
    teacher_buttons.row(item9)
    teacher_buttons.row(item10)

    bot.send_message(message.chat.id, "Виберіть предмет, який веде ваш викладач", reply_markup=teacher_buttons)


# Обробник кнопки предмета викладача
@bot.message_handler(
    func=lambda message: message.text in ['Програмування', 'Чисельні методи', 'Куратор', 'Правознавство',
                                          'Іноземна мова', 'Вища математика', 'Мережеві технології',
                                          'Схемотехніка та архітектура пк', 'Комп\'ютерні технології обробки данних'])
def teacher_subject(message):
    if message.text == 'Програмування':
        teacher_name = 'Гошко Богдан Мирославович'
        teacher_photo = open('.\photo\Goshko.jpg.', 'rb')
    elif message.text == 'Чисельні методи':
        teacher_name = 'Пташник Вадим Вікторович'
        teacher_photo = open('.\photo\Ptashnyk.jpg.', 'rb')
    elif message.text == 'Комп\'ютерні технології обробки данних':
        teacher_name = 'Шувар Богдан Іванович'
        teacher_photo = open('.\photo\Shuvar.jpg', 'rb')
    elif message.text == 'Схемотехніка та архітектура пк':
        teacher_name = 'Падюка Роман Іванович'
        teacher_photo = open('.\photo\Padjuka.jpg', 'rb')
    elif message.text == 'Мережеві технології':
        teacher_name = 'Штогрин Святослав Андрійович '
        teacher_photo = open('.\photo\Shtogryn.jpg', 'rb')
    elif message.text == 'Куратор':
        teacher_name = 'Заплатинський Назар Богданович'
        teacher_photo = open('.\photo\Zaplatynsky.jpg', 'rb')
    elif message.text == 'Вища математика':
        teacher_name = 'Богач Мар\'яна Мирославівна'
        teacher_photo = open('.\photo\Bohach.jpg', 'rb')
    elif message.text == 'Правознавство':
        teacher_name = 'Оліщук Петро Олегович'
        teacher_photo = open('.\photo\Oliwchyk.jpg', 'rb')
    elif message.text == 'Іноземна мова':
        teacher_name = 'Турчин Ірина Михайлівна'
        teacher_photo = open('.\photo\Turchyn.jpg', 'rb')

    bot.send_photo(message.chat.id, teacher_photo, caption=f"{teacher_name}")
    teacher_photo.close()


@bot.message_handler(func=lambda message: message.text == "Повернутися")
def return_to_main_menu(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    item1 = types.KeyboardButton("Розклад")
    item2 = types.KeyboardButton("Погода")
    item3 = types.KeyboardButton("Викладачі")
    item4 = types.KeyboardButton("Графік пар")
    markup.add(item1, item2, item3, item4)

    bot.send_message(message.chat.id, "Вибери потрібну опцію", reply_markup=markup)


# Обробник кнопки "Погода"
@bot.message_handler(func=lambda message: message.text == "Погода")
def weather(message):
    res = requests.get(
        'https://api.openweathermap.org/data/2.5/weather?q=Дубляни&appid=83e4103c7ca0edddfd287e6ca5c3f695&units=metric')
    data = json.loads(res.text)
    today = datetime.date.today()
    todey_reverse = today.strftime('%d-%m-%Y')
    weather_by_now = f'Погода у Дублянах | {todey_reverse} \n \nТемпература:' \
                     f' +{int(data["main"]["temp"])}°C (Відчувається як +{int(data["main"]["feels_like"])}°C)\n' \
                     f'Вологість: {data["main"]["humidity"]}% \nШвидкість вітру: {data["wind"]["speed"]}(м\с)'
    bot.send_message(message.chat.id, weather_by_now)

@bot.message_handler(func=lambda message: message.text == "Графік пар")
def timetable(message):
    with open('timetable.txt', 'r', encoding='UTF-8') as file:
        schedule_text = file.read()
    bot.send_message(message.chat.id, schedule_text)

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        time.sleep(10)

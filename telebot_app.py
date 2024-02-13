import telebot
from telebot import types
from settings import *
from utilities import ConvertionException, CryptoConverter, TextImageReader, QRcodeMaker
from datetime import *
import urllib3

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text_info = (f"Приветствую тебя, {message.chat.username}!\n"
                 "Я - твой электронный бот-помощник!\n"
                 "Мой создатель - Агафонов Е.А.🙂\n\n"
                 "Пока я умею следующее:\n"
                 "1️⃣ <b>Сообщать актуальный курс валют и рассчитывать стоимость ее покупки:</b>\n"
                 "Для запроса курса/стоимости валюты в поле ввода набери и отправь (пример):\n"
                 "'<u>100 USD RUB</u>'\n"
                 "(где 100 - это количество USD (Долларов США) для перевода в RUB (Российские рубли). Для вызова списка"
                 " доступных валют (ISO 4217) в поле ввода набери и отправь команду '/values';\n"
                 "2️⃣ <b>Распознавать текст на изображении(фото) и выводить его в текстовом формате в чат:</b>\n"
                 "<u>Для распознавания просто прикрепи и отправь изображение(фото) текста.</u>\n"
                 "Доступно распознавание текста с кириллическими, латинскими символами либо иероглифами (изображение "
                 "может содержать символы разных языков одновременно).\n"
                 "<u>ВАЖНО:</u>\n"
                 "Изображение должно быть читаемым и без искажений, текст отображается под прямым углом к "
                 "читателю👍🏻.")
    markup = types.ReplyKeyboardMarkup()
    btn_1 = types.KeyboardButton("Распознать текст (OCR)")
    btn_2 = types.KeyboardButton("Курс/Стоимость валюты")
    markup.row(btn_1, btn_2)
    btn_3 = types.KeyboardButton("Создать QR-код")
    btn_4 = types.KeyboardButton("Функция не назначена")
    markup.row(btn_3, btn_4)
    bot.send_message(message.chat.id, text_info, parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=["values"])
def handle_values(message: telebot.types.Message):
    text = "Список валют:\n" + curr_str
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["langs"])
def handle_langs(message: telebot.types.Message):
    text = "Список поддерживаемых языков для распознавания:\n" + langs_str
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=["text"])
def make_QR_code(message: telebot.types.Message):
    if message.text == "Создать QR-код":
        text = (f"{message.chat.username}, вставь в поле ввода url-адрес необходимого веб-сайта для генерации qr-кода.\n"
                f"<b>ВАЖНО:\n1) строка с адресом должна ОБЯЗАТЕЛЬНО содержать полный путь к сайту через 'https://' "
                f"(например):<u>https://www.google.ru/</u>;\n2) лишние пробелы в начале/конце адреса отсутствуют.</b>")
        bot.send_message(message.chat.id, text, parse_mode='html')
        bot.register_next_step_handler(message, crate_qr_code)

    else:
        try:
            values = message.text.split(' ')
            if len(values) != 3:
                raise ConvertionException(
                    f"Ошибка!\n"
                    f"Указано {len(values)} значения(ий) вместо положенных трех.\n"
                    f"ВАЖНО:\n"
                    f"Между строками допускается строго только один пробел!\n"
                    f"Недопустимо использовать пробелы в начале и/или конце строки\n"
                    f"Вот корректный пример ввода: '100 USD RUB'")

            quantity, base_code, target_code = values

            status, result = CryptoConverter.convert(token=API_KEY, quantity=quantity.upper(), base_code=base_code.upper(),
                                                     target_code=target_code.upper())

        except ConvertionException as e:
            bot.reply_to(message, f"{e}")
        except Exception as e:
            bot.reply_to(message, f"{e}")
        else:
            text = f"Стоимость покупки {quantity} {base_code} составит {round(result['conversion_result'], 2)} {target_code}."
            bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=["photo"])
def recognizing_text(message: telebot.types.Message):
    text_pictures = message.photo[-1]
    file_info = bot.get_file(text_pictures.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    save_path = RECOGN_IMAGE_PATH
    with open(save_path, 'wb') as new_file:
        new_file.write(downloaded_file)

    bot.reply_to(message, f"{message.chat.username}, укажи название языка на отправленном тобой  изображении.\n"
                          f"В поле ввода набери и отправь (например):\n"
                          f"'ru' - если изображение содержит символы только одного языка (например только русского);\n"
                          f"'ru en' - если изображение содержит символы нескольких языков (например и русского, и "
                          f"английского).\n"
                          f"Для вызова списка доступных языков в поле ввода набери и отправь команду '/langs';\n"
                          f"ВАЖНО:\n"
                          f"Между названиями языков допускается строго только один пробел!\n"
                          f"Недопустимо использовать пробелы в начале и/или конце строки!\n"
                          f"Вот корректный пример ввода (например): 'ru en', либо только 'ru'")
    bot.register_next_step_handler(message, enter_langs)


def enter_langs(message):
    msg_list = message.text.split(' ')
    langs = []
    for i in msg_list:
        langs.append(i.lower())
    bot.reply_to(message, f"{message.chat.username}, приступаю к распознаванию текста??!\n"
                          f" Потребуется время, просьба чуть-чуть подождать...")
    result = TextImageReader.text_recognition(RECOGN_IMAGE_PATH, langs)
    text = "Готово👌🏻:   "
    bot.send_message(message.chat.id, text)
    bot.send_message(message.chat.id, result)


def crate_qr_code(message):
    html_link = message.text
    qr_code = QRcodeMaker.make_QR_code(html_link)
    text = "Готово👌🏻:"
    bot.send_message(message.chat.id, text)
    bot.send_photo(message.chat.id, qr_code)


bot.polling(none_stop=True)


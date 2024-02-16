import telebot
from telebot import types
from settings import *
from utilities import ConvertionException, CryptoConverter, TextImageReader, QRcodeMaker, RequestsToEGRYUL
import datetime

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text_info = (f"Приветствую тебя, {message.chat.username}!\n"
                 "Я - твой электронный бот-помощник!\n"
                 "Мой создатель - Агафонов Е.А.🙂\n\n"
                 "Пока я умею следующее:\n\n"
                 "1️⃣ Сообщать актуальный курс валют и рассчитывать стоимость ее покупки.\n"
                 "Для запроса нажми кнопку <b><u>'Курс/Стоимость валюты'</u>;</b>\n"
                 "2️⃣ Распознавать текст на изображении(фото) и выводить его в текстовом формате в чат.\n"
                 "Для запроса нажми кнопку <b><u>'Распознать текст (OCR)'</u>;</b>\n"
                 "3️⃣ Сгенерировать QR-код с ссылкой на веб-сайт или зашифрованными данными.\n"
                 "Для запроса нажми кнопку <b><u>'Создать QR-код'</u>;</b>"
                 "4️⃣ Получить сведения о юридическом лице из ЕГРЮЛ.\n"
                 "Для запроса нажми кнопку <b><u>'Реквизиты организации (ЕГРЮЛ)'</u>;</b>"
                 )
    markup = types.ReplyKeyboardMarkup()
    btn_1 = types.KeyboardButton("  Курс/Стоимость валюты")
    btn_2 = types.KeyboardButton("Распознать текст (OCR)")
    markup.row(btn_1, btn_2)
    btn_3 = types.KeyboardButton("Создать QR-код")
    btn_4 = types.KeyboardButton("Реквизиты организации (ЕГРЮЛ)")
    markup.row(btn_3, btn_4)
    bot.send_message(message.chat.id, text_info, parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=["langs"])
def handle_langs(message: telebot.types.Message):
    text = "Список поддерживаемых языков для распознавания:\n" + langs_str
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=["text"])
def text_messages_handler(message: telebot.types.Message):
    if message.text == "Создать QR-код":
        trigger_msg_qrcode = (
            f"{message.chat.username}, вставь в поле ввода url-адрес необходимого веб-сайта для генерации qr-кода.\n"
            f"<b>ВАЖНО:\n"
            f"1) строка с адресом должна ОБЯЗАТЕЛЬНО содержать полный путь к сайту через 'https://'(например):\n"
            f"<u>https://www.google.ru/</u>;\n"
            f"2) лишние пробелы в начале/конце адреса отсутствуют.</b>")
        bot.send_message(message.chat.id, trigger_msg_qrcode, parse_mode='html')
        bot.register_next_step_handler(message, create_qr_code)

    elif message.text == "Распознать текст (OCR)":
        trigger_msg_ocr = (f"{message.chat.username}, готов принять фото для распознавания 🙂!\n"
                           f"<b>Просто прикрепи и отправь изображение(фото) текста.</b>\n"
                           f"Доступно распознавание текста с кириллическими, латинскими символами либо иероглифами "
                           f"(изображение может содержать символы разных языков одновременно).\n"
                           f"<u>ВАЖНО:</u>\n"
                           f"Изображение должно быть читаемым и без искажений, текст отображается под прямым углом к "
                           f"читателю👍🏻.\n"
                           f"Высылай....")
        bot.send_message(message.chat.id, trigger_msg_ocr, parse_mode='html')
        bot.register_next_step_handler(message, set_recogn_langs_handler)

    elif message.text == "Курс/Стоимость валюты":
        trigger_msg_curr = (
            f"{message.chat.username}, для запроса курса/стоимости валюты в поле ввода набери и отправь "
            f"(например):\n"
            f"<b>100 USD RUB</b>\n"
            f"(где 100 - это количество USD (Долларов США) для перевода в RUB (Российские рубли).\n"
            f"Cписок доступных для конвертации валют:\n"
            f"{curr_str}")
        bot.send_message(message.chat.id, trigger_msg_curr, parse_mode="html")
        bot.register_next_step_handler(message, convert_currencies)

    if message.text == "Реквизиты организации (ЕГРЮЛ)":
        trigger_msg_EGRYL = (f"Для предоставления сведений о юридическом лице (ЮЛ) введите и отправьте сообщение с "
                             f"наименованием ЮЛ и/или ИНН. Пример:\n "
                             f"<b>ПАО Газпром</b>;\n"
                             f"либо -\n"
                             f"<b>Сбербанк 7707083893</b>.")
        bot.send_message(message.chat.id, trigger_msg_EGRYL, parse_mode="html")
        bot.register_next_step_handler(message, get_EGRYL_data)

    else:
        text_error = (f"{message.chat.username}, указанная команда не соответствует условиям текущего запроса или "
                      f"введено недопустимое значение😕!\n"
                      f"Через поле ввода сообщения отправь (нажми на экране) '/start' и внимательно следуй "
                      f"инструкциям.\n"
                      f"Все получится😊!")
        bot.send_message(message.chat.id, text_error)


@bot.message_handler(content_types=["photo"])
def set_recogn_langs_handler(message: telebot.types.Message):
    text_pictures = message.photo[-1]
    file_info = bot.get_file(text_pictures.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    save_path = RECOGN_IMAGE_PATH
    with open(save_path, 'wb') as new_file:
        new_file.write(downloaded_file)
    text_msg = (f"{message.chat.username}, укажи название языка на отправленном тобой  изображении.\n"
                f"В поле ввода набери и отправь (например):\n"
                f"<b>ru</b> - если изображение содержит символы букв только одного языка (например только русского);\n"
                f"<b>ru en</b> - если изображение содержит символы букв нескольких языков (например и русского, и "
                f"английского).\n"
                f"Вот корректный пример ввода (например): <b>de fr</b> (или только <b>ru</b>).\n"
                f"Список доступных для распознавания языков:\n"
                f"{langs_str}")
    bot.send_message(message.chat.id, text_msg, parse_mode="html")
    bot.register_next_step_handler(message, image_OCR_recognition)


def image_OCR_recognition(message: telebot.types.Message):
    msg_list = message.text.split(' ')
    langs = []
    for i in msg_list:
        langs.append(i.lower())
    bot.reply_to(message, f"{message.chat.username}, приступаю к распознаванию текста🤓!\n"
                          f" Потребуется время, просьба чуть-чуть подождать...")
    result = TextImageReader.text_recognition(RECOGN_IMAGE_PATH, langs)
    text = "Готово👌🏻:"
    bot.send_message(message.chat.id, text)
    bot.send_message(message.chat.id, text=f"<b>{result}</b>", parse_mode="html")
    bot.send_message(message.chat.id, text="Для продолжения нажми кнопку /start в меню или набери и отправь "
                                           "команду: /start в поле для ввода сообщений😊!")


def create_qr_code(message: telebot.types.Message):
    html_link = message.text
    qr_code = QRcodeMaker.make_QR_code(html_link)
    text = "Готово👌🏻:"
    bot.send_message(message.chat.id, text)
    bot.send_photo(message.chat.id, qr_code)
    bot.send_message(message.chat.id, text="Для продолжения нажми кнопку /start в меню или набери и отправь "
                                           "команду: /start в поле для ввода сообщений😊!")


def get_EGRYL_data(message: telebot.types.Message):
    incoming_msg = message.text
    response = RequestsToEGRYUL.find_org_by_name(incoming_msg)

    result = (f"Полное наимен-ие: <b>{response[0].get('data').get('name').get('full_with_opf')}</b>\n"
              f"Краткое наимен-ие: <b>{response[0].get('data').get('name').get('short_with_opf')}</b>\n"
              f"ИНН: <b>{response[0].get('data').get('inn')}</b>\n"
              f"КПП: <b>{response[0].get('data').get('kpp')}</b>\n"
              f"ОГРН: <b>{response[0].get('data').get('ogrn')}</b>\n"
              f"Дата рег-ии: "
              f"<b>{datetime.datetime.fromtimestamp(((response[0].get('data').get('state').get('registration_date')) / 1000))}</b>\n"
              f"ФИО руков-ля(ЕИО): <b>{response[0].get('data').get('management').get('name')}</b>\n"
              f"Должность руков-ля: <b>{response[0].get('data').get('management').get('post')}</b>\n"
              f"Статус ЮЛ (действ./не действ.): <b>{response[0].get('data').get('state').get('status')}</b>\n"
              f"Код налог-ой инсп-ции: <b>{response[0].get('data').get('address').get('data').get('tax_office')}</b>\n"
              f"Основной ОКВЭД: <b>{response[0].get('data').get('okved')}</b>\n"
              f"Сведения о лицен-ях: <b>{response[0].get('data').get('licenses')}</b>\n"
              f"Адрес госуд-ой рег-ии: <b>{response[0].get('data').get('address').get('value')}</b>\n")

    text = "Готово👌🏻:"
    bot.send_message(message.chat.id, text)
    bot.send_message(message.chat.id, result, parse_mode="html")
    bot.send_message(message.chat.id, text="Для продолжения нажми кнопку /start в меню или набери и отправь "
                                           "команду: /start в поле для ввода сообщений😊!")


def convert_currencies(message: telebot.types.Message):
    try:
        incoming_msg = message.text.split(' ')
        values = []
        for i in incoming_msg:
            i.upper()
            values.append(i)
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
        bot.send_message(message.chat.id, text="Для продолжения нажми кнопку /start в меню или набери и отправь "
                                               "команду: /start в поле для ввода сообщений😊!")


bot.polling(none_stop=True)

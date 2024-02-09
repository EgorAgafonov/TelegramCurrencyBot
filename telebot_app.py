import telebot
from settings import *
from utilities import ConvertionException, CryptoConverter, TextImageReader
from datetime import *

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: telebot.types.Message):
    text_info = (f"Приветствую тебя, {message.chat.username}!\n"
                 "Я - твой электронный бот-помощник🤖!\n"
                 "Мой создатель - Агафонов Е.А.😊.\n"
                 "Пока я умею следующее:\n\n"
                 "1️⃣ Сообщать актуальный курс валют и рассчитывать стоимость ее покупки:\n"
                 "Для запроса курса/стоимости валюты в поле ввода набери и отправь (пример):\n\n"
                 "'100 USD RUB'\n\n"
                 "(где 100 - это количество USD (Долларов США) для перевода в RUB (Российские рубли). Для вызова списка"
                 " доступных валют (ISO 4217) в поле ввода набери и отправь команду '/values';\n\n"
                 "2️⃣ Распознавать текст на изображении(фото) и выводить его в текстовом формате в чат:\n\n"
                 "Для распознавания просто прикрепи и отправь изображение(фото) текста.\n\n"
                 "Доступно распознавание текста с кириллическими, латинскими символами либо иероглифами (изображение "
                 "может содержать символы разных языков одновременно).\n"
                 "ВАЖНО: Изображение должно быть читаемым и без искажений, текст отображается под прямым углом к "
                 "читателю.\n"
                 "При соблюдении этих условий я постараюсь обеспечить хорошее качество распознавания текста 😊👍🏻.")
    bot.send_message(message.chat.id, text_info)


@bot.message_handler(commands=["values"])
def handle_values(message: telebot.types.Message):
    text = "Список валют:\n" + curr_str
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["langs"])
def handle_langs(message: telebot.types.Message):
    text = "Список поддерживаемых языков для распознавания:\n" + langs_str
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=["text"])
def currency_convertor(message: telebot.types.Message):
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
    save_path = os.path.join(IMAGE_PATH, "input_chat_image.bmp")

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

    bot.reply_to(message, f"{message.chat.username}, приступаю к распознаванию текста💪🏻!\n"
                          f" Потребуется время, просьба чуть-чуть подождать...")
    result = TextImageReader.text_recognition(save_path)
    text = "Готово🙂:"
    bot.send_message(message.chat.id, text)
    bot.send_message(message.chat.id, result)


bot.polling(none_stop=True)


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
                 "Для запроса курса/стоимости валюты в поле ввода набери и отправь (пример):\n"
                 "'100 USD RUB'\n"
                 "(где 100 - это количество USD (Долларов США) для перевода в RUB (Российские рубли). Для вызова списка"
                 " доступных валют (ISO 4217) в поле ввода набери и отправь команду '/values';\n\n"
                 "2️⃣ Распознавать текст на изображении(фото) и выводить его в текстовом формате в чат:\n"
                 "Для распознавания текста просто прикрепи и отправь изображение(скан, фото) страницы с текстом. "
                 "Доступно распознавание текста на русском и/или английском языках (изображение может содержать как "
                 "кириллические, так и латинские символы одновременно).\n"
                 "ВАЖНО: Поле ввода текста оставь пустым, изображение должно быть читаемым, текст отображается под "
                 f"прямым углом к читателю. При соблюдении этих условий я постараюсь обеспечить хорошее качество "
                 f"распознавания текста 👍🏻.")
    bot.send_message(message.chat.id, text_info)


@bot.message_handler(commands=["values"])
def handle_values(message: telebot.types.Message):
    text = "Список валют:\n" + curr_str
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=["text"])
def currency_convertor(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConvertionException(
                f"Ошибка!\n"
                f"Указано {len(values)} значения(ий) вместо положенных трех.\n"
                f"ВАЖНО: Между строками допускается строго только один отступ!\n"
                f"Вот корректный пример ввода: '100 USD RUB'")

        quantity, base_code, target_code = values

        status, result = CryptoConverter.convert(token=API_KEY, quantity=quantity, base_code=base_code,
                                                 target_code=target_code)

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
    bot.reply_to(message, f"{message.chat.username}, приступаю к распознаванию текста💪🏻!\n"
                          f" Потребуется время, просьба чуть-чуть подождать,...")
    result = TextImageReader.text_recognition(save_path)
    text = "Готово🙂:"
    bot.send_message(message.chat.id, text)
    bot.send_message(message.chat.id, result)


bot.polling(none_stop=True)


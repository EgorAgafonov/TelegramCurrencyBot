import telebot
from settings import *
from exchange_app import ExchangeRateAPI
import emoji

bot = telebot.TeleBot(TOKEN)
currency_API = ExchangeRateAPI()

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: telebot.types.Message):
    text_info = (f"Приветствую тебя, друг!\n"
                 "Я - твой электронный бот-помощник🤖!\n\n"
                 "1️⃣ Для запроса курса/стоимости валюты в поле ввода набери и отправь (пример):\n"
                 "'100 USD RUB'\n"
                 "(где 100 - это количество USD (Долларов США) для перевода в RUB (Российские рубли).\n"
                 "Для вызова списка доступных валют (ISO 4217) в поле ввода набери и отправь команду '/values';\n\n"
                 "2️⃣ Для распознавания текста просто прикрепи и отправь изображение(скан, фото) страницы с "
                 "текстом.\n"
                 "ВАЖНО: Поле текста оставь пустым, изображение должно быть читаемым, а текст на нем отображен под "
                 f"прямым углом к читателю. При соблюдении этих условий я постараюсь обеспечить максимальное качество "
                 f"распознавания текста 👍🏻.")
    bot.send_message(message.chat.id, text_info)


@bot.message_handler(commands=["values"])
def handle_values(message: telebot.types.Message):
    text = "Cписок доступных валют:"
    for key in currencies.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=["text"])
def voice_message_answer(message: telebot.types.Message):
    status, result = currency_API.conversion_of_currency_pair(api_key, "USD", "RUB", "99.99")
    bot.reply_to(message, "xxxxxxxxxxxxxxxxxxxxxxxx")
#
#
# @bot.message_handler(content_types=["photo"])
# def voice_message_answer(message: telebot.types.Message):
#     bot.reply_to(message, "xxxxxxxxxxxxxxxxxxxxxxxxxx")


bot.polling(none_stop=True)

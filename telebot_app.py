import telebot
from settings import TOKEN
import emoji

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: telebot.types.Message):
    text_info = (f"Приветствую, хозяин!{emoji.emojize(':face_blowing_a_kiss:')}.\n"
                 "Я - твой электронный бот-помощник!\n"
                 "1. Для запроса валюты в поле ввода набери и отправь (пример):\n"
                 "'100 USD RUB'\n"
                 "(где 100 - это количество USD (Долларов США) для перевода в RUB (Российские рубли).\n"
                 "Доступные индексы валют (ISO 4217): RUB, CNY, EUR, USD, BTC;\n\n"
                 "2. Для распознавания текста просто прикрепи и отправь изображение(скан, фото) страницы с "
                 "текстом." +
                 f"\n\nВАЖНО: Поле текста оставь пустым, изображение должно быть читаемым, а текст на нем отображен под "
                 f"прямым углом к читателю. При соблюдении этих условий, дорогой хозяин, я постараюсь обеспечить тебе "
                 f"максимальное качество распознавания текста {emoji.emojize(':smiling_face_with_halo:')}")

    bot.send_message(message.chat.id, text_info)


@bot.message_handler(content_types=["text"])
def voice_message_answer(message: telebot.types.Message):
    print(message.text)
    bot.reply_to(message, "xxxxxxxxxxxxxxxxxxxxxxxx")


@bot.message_handler(content_types=["photo"])
def voice_message_answer(message: telebot.types.Message):
    bot.reply_to(message, "xxxxxxxxxxxxxxxxxxxxxxxxxx")


bot.polling(none_stop=True)

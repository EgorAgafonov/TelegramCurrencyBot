import telebot
from settings import TOKEN

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: telebot.types.Message):
    text_info = ("Привет! Я - твой электронный бот-помощник!\nПомогу распознать текст и/или конвертировать валюту по "
                 "текущему актуальному курсу!\n"
                 "В поле 'Сообщение/Написать сообщение' набери следующее сообщение(команду):\n"
                 "'100 USD RUB' (где 100 - это количество USD (Долларов США) для перевода в RUB (российские рубли)")
    bot.send_message(message.chat.id)


@bot.message_handler(content_types=["voice"])
def voice_message_answer(message: telebot.types.Message):
    bot.reply_to(message, "Как прекрасно ты звучишь ;-)!")


bot.polling(none_stop=True)

import telebot
from settings import TOKEN

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=["voice"])
def voice_message_answer(message: telebot.types.Message):
    bot.send_message(message.chat.id, "Как прекрасно ты звучишь ;-)!")


@bot.message_handler(content_types=["text"])
def text_message_answer(message: telebot.types.Message):
    bot.send_message(message.chat.id, f"Привет, {message.chat.username}!")


@bot.message_handler(content_types=["photo"])
def foto_message_answer(message: telebot.types.Message):
    bot.send_message(message.chat.id, "Замечательное фото!")


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: telebot.types.Message):
    pass


# Обрабатываются все документы и аудиозаписи
@bot.message_handler(content_types=['document', 'audio'])
def handle_docs_audio(message):
    pass


bot.polling(none_stop=True)

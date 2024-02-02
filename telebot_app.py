import telebot
from settings import TOKEN

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: telebot.types.Message):
    bot.send_message(message.chat.id, "РАЗРАБОТЧИКУ: Заполнить документацию для команды /help, /start!!!")


@bot.message_handler(content_types=["voice"])
def voice_message_answer(message: telebot.types.Message):
    bot.reply_to(message, "Как прекрасно ты звучишь ;-)!")


@bot.message_handler(content_types=["text"])
def text_message_answer(message: telebot.types.Message):
    print(message.text.split(' '))
    bot.reply_to(message, f"Привет, {message.chat.username}!")


@bot.message_handler(content_types=["photo"])
def foto_message_answer(message: telebot.types.Message):
    bot.reply_to(message, "Nice meme XDD")




bot.polling(none_stop=True)

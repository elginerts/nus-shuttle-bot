from config import TELEGRAM_TOKEN
import telebot

bot = telebot.TeleBot(token=TELEGRAM_TOKEN)

@bot.message_handler(commands=["start"])
def welcome(message):
    welcome_text = f'user {message.from_user.first_name} Welcome to the Bot!'
    bot.send_message(message.chat.id, welcome_text)


bot.polling() 
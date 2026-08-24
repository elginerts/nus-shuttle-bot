from config import TELEGRAM_TOKEN
import telebot
from telebot import types

bot = telebot.TeleBot(token=TELEGRAM_TOKEN)

@bot.message_handler(commands=["start"])
def welcome(message):
    welcome_text = f'user {message.from_user.first_name} Welcome to the Bot!'
    bot.send_message(message.chat.id, welcome_text)

@bot.message_handler(commands=["stops"])
def show_stops(message):
    # nearest_stops = "Nearby Bus Stops:\n1. Biz2: 30m\n2. HSSML: 40m\n3. Opp. HSSML: 120m"
    
    # bot.send_message(message.chat.id, nearest_stops)

    # Create a set of buttons in the bot's reply message
    keyboard = types.InlineKeyboardMarkup()

    # Add button option for BIZ2 bus stop
    biz2_button = types.InlineKeyboardButton(
        "BIZ2: 30M",
        callback_data="stop_biz2"
    )

    # Add button option for HSSML bus stop
    hssml_button = types.InlineKeyboardButton(
        "HSSML: 45M",
        callback_data="stop_hssml"
    )

    keyboard.add(biz2_button)
    keyboard.add(hssml_button)

    bot.send_message(message.chat.id, "Nearby Bus Stops:", reply_markup=keyboard)


bot.polling() 
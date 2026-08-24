from config import TELEGRAM_TOKEN
import telebot
from telebot import types

bot = telebot.TeleBot(token=TELEGRAM_TOKEN)

@bot.message_handler(commands=["start"])
def welcome(message):
    welcome_text = f'user {message.from_user.first_name} Welcome to the Bot!'
    bot.send_message(message.chat.id, welcome_text)

# When user types /stops, bot will return a list of nearby bus stops
@bot.message_handler(commands=["stops"])
def show_stops(message):

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

@bot.callback_query_handler(func=lambda call: call.data.startswith("stop_"))
def handle_stop_button_click(call):
    if call.data == "stop_biz2":
        reply="BIZ2 Bus Arrivals:\nA1: 3min, 5min, 10min\nD2:ARR, 6min, 12min"
    elif call.data == "stop_hssml":
        reply="HSSML Bus Arrivals:\nD1:2min, 7min, 9min\nR1:3min, 5min, 14min"
    else:
        reply="Error: No Button Clicked!"
    bot.send_message(call.message.chat.id, reply)

bot.polling() 
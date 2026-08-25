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

    # Add button option for HMK bus stop
    heng_mui_keng_button = types.InlineKeyboardButton(
        "Heng Mui Keng Terrace: 30M",
        callback_data="stop_16069"
    )

    # Add button option for Opp. HMK bus stop
    opposite_heng_mui_keng_button = types.InlineKeyboardButton(
        "Opp Heng Mui Keng Terrace: 45M",
        callback_data="stop_16061"
    )

    keyboard.add(heng_mui_keng_button)
    keyboard.add(opposite_heng_mui_keng_button)

    bot.send_message(message.chat.id, "Nearby Bus Stops:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith("stop_"))
def handle_stop_button_click(call):
    if call.data == "stop_16069":
        reply="Heng Mui Keng Terrace Bus Arrivals:\n3min, 5min, 10min"
    elif call.data == "stop_16061":
        reply="Opp Heng Mui Keng Terrace Bus Arrivals:\n2min, 7min, 9min"
    else:
        reply="Error: No Button Clicked!"
    bot.send_message(call.message.chat.id, reply)

bot.polling() 
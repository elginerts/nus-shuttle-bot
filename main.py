from config import TELEGRAM_TOKEN, LTA_API_KEY
import telebot
from telebot import types
import requests

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


# API endpoint for LTA bus arrivals
lta_url = "https://datamall2.mytransport.sg/ltaodataservice/v3/BusArrival"

# Create header for LTA API authentication 
lta_header = {
    "AccountKey": LTA_API_KEY
}

# Create query parameter for LTA API endpoint
lta_params = {
    "BusStopCode": "16069"
}

# Get bus arrival timings for Heng Mui Keng Terrace bus stop
stop_16069_response = requests.get(lta_url, headers=lta_header, params=lta_params)
arrival_data = stop_16069_response.json()
print(arrival_data)

services_16069 = arrival_data["Services"]
# If no arrival data, display no buses in telegram
if len(services_16069) == 0:
    print("No bus arrival information is currently available.")
else:
    print(services)


bot.polling() 
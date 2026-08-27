from config import TELEGRAM_TOKEN, LTA_API_KEY
import telebot
from telebot import types
import requests
import json
from datetime import datetime

bot = telebot.TeleBot(token=TELEGRAM_TOKEN)

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


def get_arrival_time(time_unformatted):
    
    if time_unformatted == "":
        return "Unavailable"
    
    else:
        time_formatted = datetime.fromisoformat(time_unformatted)
        current_time = datetime.now().astimezone()
        seconds_remaining = (time_formatted - current_time).total_seconds()

        arrival_time_mins = round(seconds_remaining / 60)

        if arrival_time_mins <= 0:
            return "Arriving"
        else:
            return f"{arrival_time_mins} min"

def get_bus_arrivals(stop_code):
    
    # API endpoint for LTA bus arrivals
    lta_url = "https://datamall2.mytransport.sg/ltaodataservice/v3/BusArrival"

    # Create header for LTA API authentication 
    lta_header = {
        "AccountKey": LTA_API_KEY
    }

    # Create query parameter for LTA API endpoint
    lta_params = {
        "BusStopCode": stop_code
    }

    # Get bus arrival timings for Heng Mui Keng Terrace bus stop
    try: 
        stop_code_response = requests.get(lta_url, headers=lta_header, params=lta_params, timeout = 10)
        stop_code_response.raise_for_status()
        arrival_data = stop_code_response.json()

    # If LTA API stops working, raise exception and give error message to user
    except requests.RequestException as error:
        print("LTA request failed:", error)

        return ("I couldn't retrieve the bus arrivals right now. Please try again later.")

    services = arrival_data["Services"]

    telegram_reply = ""

    # If no arrival data, display no buses in telegram
    if len(services) == 0:
        telegram_reply = "No bus arrival information is currently available."
    # Else display the bus number and arrival timing
    else:
        for service in services:
            # Get bus number 
            service_no = service["ServiceNo"]

            # Get arrival time in minutes of approaching buses:
            arrival_time_unformatted = service["NextBus"]["EstimatedArrival"]
            arrival_time_formatted = get_arrival_time(arrival_time_unformatted)
            second_arrival_time_unformatted = service["NextBus2"]["EstimatedArrival"]
            second_arrival_time_formatted = get_arrival_time(second_arrival_time_unformatted)
            third_arrival_time_unformatted = service["NextBus3"]["EstimatedArrival"]
            third_arrival_time_formatted = get_arrival_time(third_arrival_time_unformatted)

            telegram_reply += f"Bus {service_no}: {arrival_time_formatted}, {second_arrival_time_formatted}, {third_arrival_time_formatted}\n"

    print(telegram_reply)
    return telegram_reply




@bot.callback_query_handler(func=lambda call: call.data.startswith("stop_"))
def handle_stop_button_click(call):
    # Stops the loading animation on the button
    bot.answer_callback_query(call.id)

    stop_code = call.data.removeprefix("stop_")
    telegram_reply = get_bus_arrivals(stop_code)
    bot.send_message(call.message.chat.id, telegram_reply)


bot.polling() 
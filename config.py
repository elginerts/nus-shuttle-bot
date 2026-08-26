"""
This file serves as the main application settings/configuration
"""

import os
from dotenv import load_dotenv

# Finds .env file and loads the values into program's environment
load_dotenv()

# Retrieve telegram bot API token from .env file
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
LTA_API_KEY = os.getenv("LTA_API_KEY")

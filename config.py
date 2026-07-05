import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
LOG_CHAT_ID = os.getenv("LOG_CHAT_ID")

DELETE_SPAM = True
AUTO_BAN = True
AUTO_MUTE = False

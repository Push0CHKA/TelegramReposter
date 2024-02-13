from os import getenv

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

API_ID = getenv("API_ID")
API_HASH = getenv("API_HASH")
ADMIN_CHAT_ID = int(getenv("ADMIN_CHAT_ID"))
TMP_DIR = getenv("TMP_DIR")
DB_HOST = getenv("DB_HOST")
DB_PORT = getenv("DB_PORT")
DB_USER = getenv("DB_USER")
DB_PASS = getenv("DB_PASS")
DB_NAME = getenv("DB_NAME")
STOP_WORDS = [
    "приватный", "приватном", "приватка", "приватке", "приватку",
    "приватке", "основа", "основе", "основу", "реклама",
]
DONOR_CHATS_IDS = []


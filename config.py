from os import getenv

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


API_ID = getenv("API_ID")
API_HASH = getenv("API_HASH")
FUTURES_DONOR_ID = int(getenv("FUTURES_DONOR_ID"))
FUTURES_ID = int(getenv("FUTURES_ID"))
SPOT_DONOR_ID = int(getenv("SPOT_DONOR_ID"))
SPOT_ID = int(getenv("SPOT_ID"))
WORKING_DIR = getenv("WORKING_DIR")


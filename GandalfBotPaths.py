from sys import platform
from os import getcwd
from logging.handlers import RotatingFileHandler
import logging, json, traceback

if platform == "linux" or platform == "linux2":
    # linux
    SONG_PATH = f"{getcwd()}/Songs/"
    COOKIE_PATH = f"{getcwd()}/cookies.txt"
    JSON_PATH = f"{getcwd()}/keys.json"
    LOG_PATH = f"{getcwd()}/logs.txt"
    IMGPATH = f"{getcwd()}/Imgs/"
elif platform == "win32":
    SONG_PATH = f"{getcwd()}\\Songs\\"
    COOKIE_PATH = f"{getcwd()}\\cookies.txt"
    JSON_PATH = f"{getcwd()}\\keys.json"
    LOG_PATH = f"{getcwd()}\\logs.txt"
    IMGPATH = f"{getcwd()}\\Imgs\\"

with open(JSON_PATH, "r") as f:
    loaded_json = json.load(f)

#logging
logger = logging.getLogger("Rotating Log")
logger.setLevel(logging.ERROR)
handler = RotatingFileHandler(LOG_PATH, maxBytes=10000, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def write_error(error):
    traceback.print_exception(
                    type(error), error, error.__traceback__)
    logger.error(str(error))
    logger.error(traceback.format_exc())

def critical_error(E):
    logging.critical(E)

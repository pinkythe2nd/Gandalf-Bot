from sys import platform
from os import getcwd
import logging
import json

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
logging.basicConfig(filename=LOG_PATH, level=logging.WARNING)

def write_error(E):
    logging.warning(E)

def critical_error(E):
    logging.critical(E)

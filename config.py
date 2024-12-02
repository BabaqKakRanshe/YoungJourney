import os
import logging

from dotenv import load_dotenv
load_dotenv()

uri = os.getenv("database_uri")
TOKEN = os.getenv("TOKEN")



# Модуль для игры в санту
SECRET_SANTA_ENABLED = True

print("Module config successfully loaded.")
logging.info("Module config successfully loaded.")
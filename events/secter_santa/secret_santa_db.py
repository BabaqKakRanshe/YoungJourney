import logging
from datetime import datetime

from database.db import client, collection_users

collection_secret_santa = client.SecretSanta.Leaders

if collection_secret_santa.count_documents({}) == 0:
    print("Collection SecretSanta is empty.")
else:
    print(f"In the SecretSant {collection_secret_santa.count_documents({})} collection of documents.")

def is_in_secret_santa(user_id):
    return collection_secret_santa.find_one({"user_id": user_id}) is not None










#Логирование запуска
print("Module secret_santa_db successfully loaded.")
logging.info("Module secret_santa_db successfully loaded.")
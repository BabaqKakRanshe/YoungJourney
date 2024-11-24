import logging

from database.db import client


collection_secret_santa = client.SecretSanta.SecretSanta

if collection_secret_santa.count_documents({}) == 0:
    print("Collection SecretSanta is empty.")
else:
    print(f"In the SecretSant {collection_secret_santa.count_documents({})} collection of documents.")
def find_user(user_id):
    db = client.Users
    return db.Users.find_one({"user_id": user_id})
def add_to_secret_santa(user_id):

    db = client.SecretSanta
    db.SecretSanta_Collection.insert_one({"user_id": user_id})

def is_in_secret_santa(user_id):
    db = client.SecretSanta
    return db.SecretSanta_Collection.find_one({"user_id": user_id}) is not None

#Логирование запуска
print("Module secret_santa_db successfully loaded.")
logging.info("Module secret_santa_db successfully loaded.")
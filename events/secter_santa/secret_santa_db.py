import logging
from datetime import datetime

from database.db import client, collection_users

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

    # Получаем данные пользователя из коллекции Users
    user_data = client.Users.Users.find_one({"user_id": user_id})

    if user_data:
        # Если пользователь найден, извлекаем имя
        user_name = user_data.get("name", "Неизвестно")
    else:
        # Если пользователь не найден, устанавливаем имя по умолчанию
        user_name = "Неизвестно"

    # Получаем текущую дату и время
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Записываем данные в коллекцию SecretSanta
    db.SecretSanta_Collection.insert_one({
        "user_id": user_id,
        "name": user_name,
        "registration_date": current_time
    })

def is_in_secret_santa(user_id):
    db = client.SecretSanta
    return db.SecretSanta_Collection.find_one({"user_id": user_id}) is not None





















#Логирование запуска
print("Module secret_santa_db successfully loaded.")
logging.info("Module secret_santa_db successfully loaded.")
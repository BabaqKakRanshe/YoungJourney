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


def add_wish_list_to_user(user_id, wish_list, collection):

    try:
        result = collection.update_one(
            {"user_id": user_id},  # Фильтр по user_id
            {"$set": {"wish_list": wish_list}}  # Установка нового поля
        )
        if result.matched_count > 0:
            return True
        else:
            return False
    except Exception as e:
        return False

def get_wish_list_by_user_id(user_id, collection):
    try:
        user = collection.find_one({"user_id": user_id})  # Ищем пользователя по user_id
        if user:
            wish_list = user.get("wish_list", None)  # Получаем wish_list, если он существует
            if wish_list is not None:
                return wish_list
            else:
                return None
        else:
            print(f"Пользователь с user_id {user_id} не найден.")
            return None
    except Exception as e:
        print(f"Ошибка при получении wish list: {e}")
        return None

def get_all_users():
    # Пример получения всех пользователей из базы данных
    # Это зависит от того, как у вас устроена база данных.
    # Возвращаем список пользователей с их user_id.
    return [
        {"user_id": 123456789},
        {"user_id": 987654321},
        # Другие пользователи
    ]





#Логирование запуска
print("Module secret_santa_db successfully loaded.")
logging.info("Module secret_santa_db successfully loaded.")
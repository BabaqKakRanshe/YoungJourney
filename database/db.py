import logging

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

from config import  uri


client = MongoClient(uri, server_api=ServerApi('1'))

collection_users = client.Users.Users
collection_leaders = client.Users.Leaders

# Функция для поиска пользователя по user_id
def get_user_by_id(user_id, collection):
    try:
        user = collection.find_one({"user_id": user_id})

        if user:
            return user
        else:
            return None

    except ConnectionError as e:
        print(f"Database connection error: {e}")
        return None

def get_all_users(collection):
    try:
        # Получаем всех пользователей из коллекции
        users = list(collection.find())  # Преобразуем курсор в список
        return users
    except Exception as e:
        print(f"Error when retrieving users: {e}")
        return []

def add_user_to_collection(user_id, collection, user_name=None, real_first_name=None, real_last_name=None ):
    try:
        # Если имя не указано, заменяем на значение по умолчанию
        if user_name is None:
            user_name = "Без ника"
        if real_first_name is None:
            real_first_name = "Без имени"
        if real_last_name is None:
            real_last_name = "Без фамилии"

        if collection.find_one({"user_id": user_id}):
            print(f"User with ID {user_id} already exists.")
            return

        user_data = {
            "user_id": user_id,
            "real_first_name": real_first_name,
            "real_last_name": real_last_name,
            "nick_name": user_name,
            "date_added": datetime.now()  # Дата добавления
        }

        collection.insert_one(user_data)
        print(user_id, user_name, real_first_name, real_first_name, datetime.now())
    except ConnectionError as e:
        print(f"Database connection error: {e}")
        return


def get_user_role(user_id):

    try:
        user = collection_users.find_one({"user_id": user_id}, {"_id": 0, "user_role": 1})

        if user and "user_role" in user:
            return user["user_role"]
        else:
            return None

    except Exception as e:
        print(f"Error when retrieving user role: {e}")
        return None

print("Module db successfully loaded.")
logging.info("Module db successfully loaded.")
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime


uri = "mongodb+srv://Babaq:3bJjvdRy8zzGivwI@youngjourney.e8m4u.mongodb.net/?retryWrites=true&w=majority&appName=YoungJourney"

client = MongoClient(uri, server_api=ServerApi('1'))

collection_users = client.Users.Users
collection_leaders = client.Users.Leaders

# Функция для поиска пользователя по user_id
def find_user_by_id(user_id):
    try:
        # Поиск одного документа в коллекции Users по user_id
        user = collection_users.find_one({"user_id": user_id})

        if user:
            return user  # Возвращаем найденного пользователя
        else:
            return None  # Если пользователь не найден, возвращаем None
    except ConnectionError as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return None


# Пример использования
user_id = 417925165  # Замените на нужный ID пользователя
user = find_user_by_id(user_id)

if user:
    print("Пользователь найден:", user)
else:
    print("Пользователь с таким ID не найден.")


def add_user(user_id, user_name):
    try:
        if collection_users.find_one({"user_id": user_id}):
            print(f"Пользователь с ID {user_id} уже существует.")
            return  # Если пользователь уже есть, не добавляем его

        # Добавляем нового пользователя с ID, именем и текущей датой
        user_data = {
            "user_id": user_id,
            "name": user_name,
            "date_added": datetime.now()  # Дата добавления
        }

        # Вставляем данные в коллекцию
        collection_users.insert_one(user_data)
        print(f"Пользователь {user_name} с ID {user_id} успешно добавлен.")

    except ConnectionError as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return


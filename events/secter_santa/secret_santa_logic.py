import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import pytz
import random
from datetime import datetime
from faker import Faker

from handlers.handlers import bot
from database.db import get_all_users
from events.secter_santa.secret_santa_db import collection_secret_santa

# Указываем часовой пояс
timezone = pytz.timezone("Asia/Almaty")  # Замените на нужный часовой пояс

#Отправка сообщения
async def send_message(user_id, message):
    try:
        await bot.send_message(user_id, message)
        print(f"Message successfully sent to user {user_id} in {datetime.now(timezone)}")
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")

# Функция для запуска планировщика
async def start_scheduler():
    # Создаем объект планировщика с учетом часового пояса
    scheduler = AsyncIOScheduler(timezone=timezone)

    # Получаем всех пользователей из коллекции Secret Santa
    all_users = get_all_users(collection_secret_santa)

    # Назначаем каждому пользователю его "Тайного Ангела"
    assign_secret_santa(all_users, collection_secret_santa)

    # Добавляем задачу в планировщик: задача будет выполняться по расписанию (в 18:08 по времени в timezone)
    scheduler.add_job(send_secret_santa_to_all_users, 'cron', hour=20, minute=7)  # Время в указанном часовом поясе

    scheduler.start()

    print("Scheduler is up and running")
    print(f"Current time: {datetime.now(timezone)}")


def assign_secret_santa(users, collection):
    # Копируем список пользователей
    shuffled_users = users[:]
    random.shuffle(shuffled_users)

    # Назначаем каждого участника Тайным Ангелом
    secret_santa_map = {}
    for i in range(len(users)):
        # Каждый пользователь получает следующего, а последний получает первого
        secret_santa_map[shuffled_users[i]["user_id"]] = shuffled_users[(i + 1) % len(users)]["user_id"]

        # Обновляем запись в базе данных с ID Тайного Ангела
        collection.update_one(
            {"user_id": shuffled_users[i]["user_id"]},
            {"$set": {"secret_santa_id": secret_santa_map[shuffled_users[i]["user_id"]]}}
        )

    return secret_santa_map

async def send_secret_santa_to_all_users():
    # Получаем всех пользователей из коллекции
    all_users = get_all_users(collection_secret_santa)

    # Проходим по каждому пользователю
    for user in all_users:
        user_id = user["user_id"]

        # Получаем ID тайного Ангела для текущего пользователя
        secret_santa_name = user.get(
            "real_first_name")
        secret_santa_nick_name = user.get(
            "nick_name")
        if secret_santa_name:
            # Формируем сообщение для пользователя
            message = f"😇 Ваш Тайный Ангел — это {secret_santa_name} {secret_santa_nick_name}! 🎁\n" \
                      "Не раскрывайте свою личность, до момента вручения основного подарка! 🙊\n" \
                      "Старайся молиться за этого человека, поддерживай его, а также тайно радуй маленькими подарками ✝️"

            try:
                # Отправляем сообщение пользователю
                await bot.send_message(user_id, message)
                print(f"Сообщение отправлено пользователю {user_id}, Тайный Ангел: {secret_santa_name}")
            except Exception as e:
                print(f"Ошибка при отправке сообщения пользователю {user_id}: {e}")
        else:
            print(f"Для пользователя с ID {user_id} не найден Тайный Ангел.")


fake = Faker()
# Функция для добавления случайных пользователей в коллекцию
def add_random_user_to_collection(collection, num_users):
    print(f"Количество пользователей: {num_users}")
    try:
        # Генерация случайных пользователей
        for _ in range(num_users):
            user_id = random.randint(100000000, 999999999)  # Генерация случайного user_id
            user_name = fake.user_name()  # Генерация случайного ника
            real_first_name = fake.first_name()  # Генерация случайного имени
            real_last_name = fake.last_name()  # Генерация случайной фамилии

            # Проверка на существование пользователя в базе
            if collection.find_one({"user_id": user_id}):
                print(f"User with ID {user_id} already exists.")
                continue

            # Создание данных для пользователя
            user_data = {
                "user_id": user_id,
                "real_first_name": real_first_name,
                "real_last_name": real_last_name,
                "nick_name": user_name,
                "date_added": datetime.now()  # Дата добавления
            }

            # Добавление пользователя в базу данных
            collection.insert_one(user_data)
            print(f"User added: {user_id}, {user_name}, {real_first_name} {real_last_name}")
    except Exception as e:
        print(f"Error occurred: {e}")









# Логирование запуска
print("Module secret_santa_logic successfully loaded.")
logging.info("Module secret_santa_logic successfully loaded.")

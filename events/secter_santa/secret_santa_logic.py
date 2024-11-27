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
async def start_scheduler(year: int, month: int, day: int, hour: int, minute: int):

    scheduler = AsyncIOScheduler(timezone=timezone)

    all_users = get_all_users(collection_secret_santa)

    assign_secret_santa(all_users, collection_secret_santa)

    scheduler.add_job(
        send_secret_santa_to_all_users,
        'date',
        run_date=datetime(year, month, day, hour, minute, tzinfo=timezone),
        misfire_grace_time=3600  # Задача выполнится, если пропустила время выполнения не более чем на 1 час
    )

    scheduler.start()

    print("Scheduler is up and running")
    print(f"Current time: {datetime.now(timezone)}")
    print(f"Task scheduled for {year}-{month:02d}-{day:02d} {hour:02d}:{minute:02d} ({timezone})")


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
        secret_santa_id = user.get("secret_santa_id")  # ID Тайного Ангела

        if secret_santa_id:
            # Получаем данные Тайного Ангела
            secret_santa = collection_secret_santa.find_one({"user_id": secret_santa_id})
            if secret_santa:
                secret_santa_name = secret_santa.get("real_first_name", None)
                secret_santa_nick_name = secret_santa.get("nick_name", None)

                # Получаем список пожеланий Тайного Ангела
                wish_list = secret_santa.get("wish_list", "Нет пожеланий.")  # Можно заменить на пустой список или дефолтное сообщение

                # Если нет ни имени, ни ника, заменяем на "Бессовечный человек"
                if not secret_santa_name and not secret_santa_nick_name:
                    secret_santa_name = "Бессовечный человек"
                    message = f"🎉 Игра в Тайного Ангела началась! 🎉\n" \
                              f"\n😇 Ты стал подаркодарителем для — {secret_santa_name}! 🎁\n" \
                              "Не раскрывай свою личность, до момента вручения основного подарка! 🙊\n" \
                              "Молись за этого человека, поддерживай его, и радуй маленькими подарками ✝️💫\n\n" \
                              f"Твой поддержкаприниматель (или, точнее, {secret_santa_name}) по секрету рассказал мне, что хочет: {wish_list} 🎅✨"

                else:
                    # Формируем стандартное сообщение для пользователя
                    message = f"🎉 Игра в Тайного Ангела началась! 🎉\n" \
                              f"\n😇 Ты стал подаркодарителем для — {secret_santa_name}! 🎁\n" \
                              "Не раскрывай свою личность, до момента вручения основного подарка! 🙊\n" \
                              "Молись за этого человека, поддерживай его, и радуй маленькими подарками ✝️💫\n\n" \
                              f"Твой поддержкаприниматель {secret_santa_name} по секрету рассказал мне, что хочет: {wish_list} 🎅✨"

                    # Если есть никнейм, добавляем ссылку на профиль
                    if secret_santa_nick_name != "Без ника":
                        message += f"\n\nЭто чат с твоим объектом падаркодарения, чтоб не перепутал Яриков: [@{secret_santa_nick_name}](https://t.me/{secret_santa_nick_name})"

                try:
                    # Отправляем сообщение пользователю
                    await bot.send_message(user_id, message, parse_mode="Markdown")
                    print(f"Message sent to user {user_id}, Secret Santa: {secret_santa_name}")
                except Exception as e:
                    print(f"Error sending message to user {user_id}: {e}")
            else:
                print(f"Secret Santa for user {user_id} not found in the database.")
        else:
            print(f"No Secret Santa found for user with ID {user_id}.")



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

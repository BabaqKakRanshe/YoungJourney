import asyncio
import logging
from dotenv import load_dotenv

#Dev
import init_bot
from database import db
from config import SECRET_SANTA_ENABLED

#Handlers
from handlers import *
#Admin
import handlers.admin_handlers

from events.secter_santa.secret_santa_logic import start_scheduler, send_message, add_random_user_to_collection, assign_secret_santa
from events.secter_santa.secret_santa_db import collection_secret_santa
if SECRET_SANTA_ENABLED:
    try:
        import events.secter_santa.secret_santa_main
        print("The Secret Santa module has been successfully uploaded.")
        logging.info("The Secret Santa module has been successfully uploaded.")

    except Exception as e:
        print("Error loading the Secret Santa module.")
        logging.error(f"Error loading the Secret Santa module: {e}")

#Логирование запуска
print("All modules successfully loaded.")
logging.info("All modules successfully loaded.")

# Загрузка переменных из .env
load_dotenv()

async def main():
    # Запускаем планировщик в фоновом режиме
    # scheduler_task = asyncio.create_task(start_scheduler(year=2024, month=11, day=1, hour=19, minute=1))
    # Запускаем polling бота в фоновом режиме
    polling_task = asyncio.create_task(init_bot.dp.start_polling(init_bot.bot))  # Создаем задачу для опроса бота
    # Основной цикл для выполнения других действий, если нужно

    while True:
        await asyncio.sleep(1)  # Ожидание для параллельного выполнения других задач
    print("4")
if __name__ == "__main__":
    asyncio.run(main())




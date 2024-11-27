import asyncio
import logging

#Dev
from database.db import get_all_users
from handlers.handlers import dp,bot
from config import SECRET_SANTA_ENABLED

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


async def main():
    # Запускаем планировщик в фоновом режиме
    scheduler_task = asyncio.create_task(start_scheduler(year=2024, month=11, day=27, hour=16, minute=1))
    # Запускаем polling бота в фоновом режиме
    polling_task = asyncio.create_task(dp.start_polling(bot))  # Создаем задачу для опроса бота
    # Основной цикл для выполнения других действий, если нужно
    while True:
        await asyncio.sleep(1)  # Ожидание для параллельного выполнения других задач
    print("4")
if __name__ == "__main__":
    asyncio.run(main())




import asyncio
import logging

#Dev
import database.db

from config import SECRET_SANTA_ENABLED

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
    logging.basicConfig(level=logging.INFO)
    # Метод start_polling(bot) запускает процесс опроса обновлений от Telegram.

if __name__ == "__main__":
    asyncio.run(main())
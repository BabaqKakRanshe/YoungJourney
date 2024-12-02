import logging

from init_bot import dp, Command, types
from database.db import add_user_to_collection, collection_users

@dp.message(Command("start"))
async def start_command(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.username
    user_first_name = message.from_user.first_name
    user_last_name = message.from_user.last_name

    greeting = f"Привет, {user_name}! 🌟\n\nРады, что ты с нами! 💖 Этот бот здесь, чтобы добавить немного волшебства в твой день! ✨\n\nБудь готов к удивительным приключениям и приятным сюрпризам! 🎁 Мы уже приготовили для тебя много интересного! 😍💬"

    add_user_to_collection(user_id, collection_users, user_name=user_name, real_first_name=user_first_name)
    await message.answer(greeting)

print("Module handlers successfully loaded.")
logging.info("Module handlers successfully loaded.")
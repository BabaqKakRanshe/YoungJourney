from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command

from database.db import add_user_to_collection, collection_users
from config import TOKEN

bot = Bot(token=(TOKEN))
dp = Dispatcher()
router = Router()

@dp.message(Command("start"))
async def start_command(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.username
    user_first_name = message.from_user.first_name
    user_last_name = message.from_user.last_name

    greeting = f"Привет, {user_name}! 🌟\n\nРады, что ты с нами! 💖 Этот бот здесь, чтобы добавить немного волшебства в твой день! ✨\n\nБудь готов к удивительным приключениям и приятным сюрпризам! 🎁 Мы уже приготовили для тебя много интересного! 😍💬"

    add_user_to_collection(user_id, collection_users, user_name=user_name, real_first_name=user_first_name)
    await message.answer(greeting)


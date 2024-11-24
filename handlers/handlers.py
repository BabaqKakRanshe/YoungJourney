from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from config import TOKEN
from database.db import add_user_to_collection, collection_users

bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()

@dp.message(Command("start"))
async def start_command(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username if message.from_user.username else "незнакомец"

    greeting = f"Привет, {username}! 🌟\n\nРады, что ты с нами! 💖 Этот бот здесь, чтобы добавить немного волшебства в твой день! ✨\n\nБудь готов к удивительным приключениям и приятным сюрпризам! 🎁 Мы уже приготовили для тебя много интересного! 😍💬"

    await message.answer(greeting)

    add_user_to_collection(message.from_user.id, collection_users, message.from_user.username)
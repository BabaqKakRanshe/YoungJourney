from aiogram import Bot, Dispatcher, types, Router
from aiogram import Bot, Dispatcher

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()

router = Router()

@dp.message()
async def echo_message(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username if message.from_user.username else "Имя пользователя не задано"

    global userName
    target_user = message.from_user.username

    await message.reply(f"ID пользователя: {message.from_user.id}\nИмя пользователя: {message.from_user.username}")

    if target_user in userName:
        await message.answer(f"Привет: {target_user}, рад видеть лидера")
    else:
        await message.answer(f"Мы еще не знакомы")


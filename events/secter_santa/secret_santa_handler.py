import logging

from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from events.secter_santa.secret_santa_logic import participate_in_secret_santa, get_user_secret_santa_status, is_user_leader



# Обработчик команды для "Тайного Санта"
async def handle_secret_santa(message: types.Message):
    user_id = message.from_user.id

    # Проверяем, является ли пользователь лидером
    if not is_user_leader(user_id):
        await message.reply("Доступ к функции 'Тайный Санта' доступен только лидерам.")
        return

    # Отправляем клавиатуру в зависимости от состояния пользователя
    status = get_user_secret_santa_status(user_id)

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    if status == "Вы уже участвуете в Тайном Санте.":
        keyboard.add(KeyboardButton("Проверить статус"), KeyboardButton("Отказаться"))
    else:
        keyboard.add(KeyboardButton("Принять участие"))

    await message.reply(status, reply_markup=keyboard)

# Обработчик выбора действия пользователя
async def process_santa_choice(message: types.Message):
    user_id = message.from_user.id
    if message.text == "Принять участие":
        response = participate_in_secret_santa(user_id)
        await message.reply(response)
    elif message.text == "Отказаться":
        # Логика для отказа от участия, если требуется
        await message.reply("Вы отказались от участия.")
    elif message.text == "Проверить статус":
        status = get_user_secret_santa_status(user_id)
        await message.reply(status)

#Логирование запуска
print("Module secret_santa_handler successfully loaded.")
logging.info("Module secret_santa_handler successfully loaded.")
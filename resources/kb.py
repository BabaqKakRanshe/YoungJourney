from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Начать")],
        [KeyboardButton(text="Помощь")],
    ],
    resize_keyboard=True
)

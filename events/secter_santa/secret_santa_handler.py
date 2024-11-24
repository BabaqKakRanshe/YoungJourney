import logging

from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import Command

from events.secter_santa.secret_santa_logic import participate_in_secret_santa, get_user_secret_santa_status, is_user_leader
import events.secter_santa.secret_santa_db
from events.secter_santa.secret_santa_db import is_in_secret_santa,add_to_secret_santa, find_user
from handlers.handlers import router,dp


# Список ключевых фраз для активации режима
trigger_phrases = ["Санта", "игра санта", "Секретный санта", "🎅🏻", "🤶🏻", "🧑🏻‍🎄"]

# Обработчик команды Санта
@dp.message(lambda msg: any(phrase.lower() in msg.text.lower() for phrase in trigger_phrases))
async def start_handler(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Конечно хочу! 🤩"),KeyboardButton(text="А что это? 🤔") ]
        ],
        resize_keyboard=True
    )
    await message.answer("Привет, Лидер! 👋 Хочешь сыграть в Тайного Санту 🎅 с командой? 🤔🎁", reply_markup=keyboard)


@dp.message(lambda msg: msg.text in ["Конечно хочу! 🤩", "Я в деле! 👍️"])
async def secret_santa_info(message: types.Message):
    user_id = message.from_user.id

    # Проверяем, есть ли пользователь в базе
    if is_in_secret_santa(user_id):
        # Если пользователь уже зарегистрирован
        await message.answer("Ты уже зарегистрирован в игре! 🙌")
    else:
        # Если пользователя нет, добавляем его в базу
        add_to_secret_santa(user_id)
        await message.answer(
            "Поздравляю! 🎉 Ты записан ✅, ожидай 1 декабря 📅, чтобы получить своего счастливчика 🎁✨!",
            reply_markup=ReplyKeyboardRemove()
        )
@dp.message(lambda msg: msg.text == "А что это? 🤔")
async def secret_santa_info(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Понятно 👍"),KeyboardButton(text="Ничего не понятно ☠️") ]
        ],
        resize_keyboard=True
    )
    # Логика добавления лидера в базу участников
    await message.answer(
        "**🎅 Тайный Санта — это веселая игра, в которой каждый участник тайно дарит подарок другому участнику, не раскрывая своего имени до момента вручения подарка. 🎁✨\n\n"
        "💡 Как играть?\n\n"
        "1. Каждый лидер записывается в игру, и его имя остается скрытым от остальных.\n"
        "2. 1 декабря 🎄 мы отправляем каждому лидеру информацию о том, кому он должен подарить подарок.\n"
        "3. Важно не раскрывать свою личность до самого конца! 🙊\n"
        "4. Подарки можно делать как символическими, так и более персональными — главное, чтобы было весело! 🎉\n"
        "5. В конце игры все участники выясняют, кто их 'Санта'! 🎉",
        reply_markup=keyboard
    )

@dp.message(lambda msg: msg.text == "Ничего не понятно ☠️")
async def start_handler(message: types.Message):
    keyboard = ReplyKeyboardRemove()
    gerbert_chat_link = "https://t.me/GerbertKZ"

    await message.answer(
        "Это очень тяжелый случай 😓, рекомендуем обратиться к профессионалу 👩‍⚕️👨‍⚕️.\n"
        f"[Написать @GerbertKZ]({gerbert_chat_link})",
        reply_markup=keyboard,  # Передаем экземпляр клавиатуры
        parse_mode="Markdown"
    )

@dp.message(lambda msg: msg.text == "Понятно 👍")
async def start_handler(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Я в деле! 👍️"),KeyboardButton(text="Это не для меня 🤡") ]
        ],
        resize_keyboard=True
    )
    await message.answer("Как же приятно работать в одной команде с таким неповторимым и одарённым человеком! 🌟\n"
                         "У нас есть ответ? 🤨", reply_markup=keyboard)

@dp.message(lambda msg: msg.text == "Это не для меня 🤡")
async def start_handler(message: types.Message):
    keyboard = ReplyKeyboardRemove()
    await message.answer("Ох, как же жаль, что тебя не будет 🤦‍♂️😔...", reply_markup=keyboard)

#Логирование запуска
print("Module secret_santa_handler successfully loaded.")
logging.info("Module secret_santa_handler successfully loaded.")
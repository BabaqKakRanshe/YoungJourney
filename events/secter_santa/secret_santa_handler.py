import logging
import random

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from events.secter_santa.secret_santa_db import is_in_secret_santa, collection_secret_santa, add_wish_list_to_user, get_wish_list_by_user_id
from init_bot import dp
from database.db import add_user_to_collection, get_user_by_id, collection_users, get_all_users

import resources.text

# Обработчик команды Санта
@dp.message(lambda msg: any(phrase.lower() in msg.text.lower() for phrase in resources.text.SANTA_TRIGGER_PHRASES))
async def start_handler(message: types.Message):
    welcome_phrase = random.choice(resources.text.WELCOME_LIST_PHRASES)

    LeaderName = get_user_by_id(message.from_user.id, collection_secret_santa)

    if LeaderName:
        # Если пользователь найден, используем его имя
        LeaderName = LeaderName.get("real_first_name", "Имя не найдено")
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Я уже записан? 😬"), KeyboardButton(text="А что это? 🤔"),
                 KeyboardButton(text="Мой wish list 💅🏻")]
            ],
            resize_keyboard=True
        )
        await message.answer(f"Привет, {LeaderName} 👋 " + welcome_phrase,
                             reply_markup=keyboard)
    else:
        # Если пользователь не найден, устанавливаем значение "TEST"
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Конечно хочу! 🤩"), KeyboardButton(text="А что это? 🤔")]
            ],
            resize_keyboard=True
        )
        await message.answer(f"Привет, лидер 👋 Хочешь сыграть в Тайного Ангела с командой? 🤔🎁",
                             reply_markup=keyboard)


@dp.message(lambda msg: msg.text in ["Конечно хочу! 🤩", "Я в деле! 👍️", "Я уже записан? 😬"])
async def secret_santa_info(message: types.Message):
    user_id = message.from_user.id
    user_nickname = message.from_user.username
    user_first_name = message.from_user.first_name

    # Проверяем, есть ли пользователь в базе
    if is_in_secret_santa(user_id):
        # Если пользователь уже зарегистрирован
        await message.answer("Ты уже в моем списке! 🙌")

    else:
        # Если пользователя нет, добавляем его в базу
        user_document = get_user_by_id(user_id, collection_users)

        add_user_to_collection(user_id, collection_secret_santa, user_name=user_nickname, real_first_name=user_first_name)
        await message.answer(
            "Поздравляю! 🎉 Ты записан ✅, ожидай 2 декабря в какое-то время 📅, чтобы получить своего счастливчика 🎁✨!\n"
            "\nНе забудь пополнить свой wish list!💅🏻💅🏻💅🏻",
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
        "❄️ Скоро декабрь, а значит, время для праздников и подарков! Но поскольку наша команда растет, подарить что-то каждому становится сложнее. Поэтому мы продолжаем нашу ежегодную традицию — игру ‘Тайный ангел’! 🎁✨\n\n"
        "💡 Как играть?\n\n"
        "1. Каждый участник записывается в игру, и его имя остается скрытым от остальных.\n"
        "2. 1 декабря мы отправляем каждому участнику информацию о том, за кого он может молится, поддерживать и радовать маленькими подарками в течение месяца. 🎄\n"
        "3. Важно не раскрывать свою личность в процессе! 🙊\n"
        "4. Подарки могут быть символическими — например, кофе, конфетки или приятные мелочи. Главное — радовать друг друга! 🎉\n"
        "5. В конце декабря все участники узнают, кто был их ‘Тайным ангелом’! 🎉\n"
        "\nВажно: мини подарки не должны быть дорогими. Даже небольшие приятности, например, кофе, конфетки, подойдут.",
        reply_markup=keyboard
    )


@dp.message(lambda msg: msg.text == "Ничего не понятно ☠️")
async def start_handler(message: types.Message):
    keyboard = ReplyKeyboardRemove()
    gerbert_chat_link = "https://t.me/@o0lenenok0_o"

    await message.answer(
        "Это очень тяжелый случай 😓, рекомендуем обратиться к профессионалу 👩‍⚕️👨‍⚕️.\n"
        f"[Написать @@o0lenenok0_o]({gerbert_chat_link})",
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
                         "\n У нас есть ответ? 🤨", reply_markup=keyboard)

@dp.message(lambda msg: msg.text == "Это не для меня 🤡")
async def start_handler(message: types.Message):
    keyboard = ReplyKeyboardRemove()
    await message.answer("Ох, как же жаль, что тебя не будет 🤦‍♂️😔...", reply_markup=keyboard)

class WishListStates(StatesGroup):
    waiting_for_wish_list = State()

@dp.message(lambda message: message.text == "Мой wish list 💅🏻")
async def wish_list_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    random_phrase = random.choice(resources.text.WISH_LIST_PHRASES)

    wish_list = get_wish_list_by_user_id (user_id, collection_secret_santa)

    if wish_list is None:
        wish_list = "ничего (это на тебя не похоже)"

    await message.reply(random_phrase + "\n"
                                        "\nБудь так добр, введи полный список своих великих пожеланий одним сообщением, если, конечно, это не слишком сложно 🥺. \n"
                                        "\nИмей в виду, что этот список сотрет тот, который я уже потрясённо запомнил 🤯.\n"
                                        "\nВ прошлый раз ты просил: " + wish_list + ". \n"
                                        "\nСписок изменился? 🤨")

    await state.set_state(WishListStates.waiting_for_wish_list)

@dp.message(WishListStates.waiting_for_wish_list)
async def add_wish_list(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    wish_list = message.text

    # Ответ пользователю
    await message.answer(f"О, так это точно то, что вы хотели?\n"
                         f"Ваш списочек: \n{wish_list}\n"
                         f"\nНу что ж, если это всё верно, добавим в ваш безупречный wish list! 🎉")

    # Добавление в список желаемых
    add_wish_list_to_user(user_id, wish_list, collection_secret_santa)

    # Поиск ангела, чье поле secret_santa_id равно user_id
    all_users = get_all_users(collection_secret_santa)  # Получаем всех пользователей из базы
    angel = None
    for user in all_users:
        if user.get("secret_santa_id") == user_id:
            angel = user
            break  # Прерываем цикл, как только находим ангела

    if angel:
        # Отправка сообщения ангелу
        try:
            await message.bot.send_message(
                chat_id=angel["user_id"],  # Используем ID ангела
                text=f"Твой подопечный внес изменения в свой wish list и вот что он добавил:\n{wish_list}"
            )
        except Exception as e:
            print(f"Не удалось отправить сообщение ангелу {angel['user_id']}: {e}")
    else:
        print(f"Не найден ангел для пользователя с ID {user_id}")

    # Очистка состояния
    await state.clear()

#Логирование запуска
print("Module secret_santa_handler successfully loaded.")
logging.info("Module secret_santa_handler successfully loaded.")
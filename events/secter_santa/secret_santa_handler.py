import logging
import random

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import Command

import events.secter_santa.secret_santa_db
from events.secter_santa.secret_santa_db import is_in_secret_santa, collection_secret_santa, add_wish_list_to_user, get_wish_list_by_user_id
from handlers.handlers import router,dp
from database.db import add_user_to_collection, find_user_by_id, collection_users



# Список ключевых фраз для активации режима
santa_trigger_phrases = ["Тайный ангел", "Ангел", "😇", "👼🏻"]

wish_list_phrases = [
    "Теперь пиши, что хочешь получить, мой сладкий пирожочек 💋✨",
    "Жду твой список желаний, мой сахарный зайчик 🍭💕",
    "Расскажи, что ты хочешь, мой маленький подарочек 🎉💌",
    "Жду твои мечты, мой кролик 🐰💫",
    "Ну-ка, пиши, что тебя порадует, моя конфетка 🍬💎",
    "Открывай тайны своих желаний, моя клубничка 🍓✨",
    "Теперь твой ход, мой тигренок, говори, что хочешь 🐾🎁",
    "Давай, мой кексик, расскажи, что тебя сделает счастливым 🧁❤️",
    "Жду твой волшебный список, мой обаяшка 🪄💝"
]
welcome_list_phrases = [
    "Уже строишь планы, как скрыть подарки? 🎁",
    "Кто ж не жаждет сюрпризов, правда? 😏",
    "Все уже в предвкушении... или ты ещё не выбрал, что хочешь? 🎅",
    "Прямо сейчас начинаешь мечтать о своём подарке? 😜",
    "Когда уже можно начать проверку подарков? 🕵️‍♂️",
    "Мыслишь, что получишь? Или это останется сюрпризом? 🤫",
    "А ты уже решил, что подаришь? Или будешь надеяться на чудо? 🎁",
    "Надеешься, что в этот раз будет не только подарки, но и магия? ✨",
]

# Обработчик команды Санта
@dp.message(lambda msg: any(phrase.lower() in msg.text.lower() for phrase in santa_trigger_phrases))
async def start_handler(message: types.Message):
    welcome_phrase = random.choice(welcome_list_phrases)

    LeaderName = find_user_by_id(message.from_user.id, collection_secret_santa)

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
        user_document = find_user_by_id(user_id, collection_users)

        add_user_to_collection(user_id, collection_secret_santa, user_name=user_nickname, real_first_name=user_first_name)
        await message.answer(
            "Поздравляю! 🎉 Ты записан ✅, ожидай 1 декабря 📅, чтобы получить своего счастливчика 🎁✨!\n"
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
    random_phrase = random.choice(wish_list_phrases)

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

    await message.answer(f"О, так это точно то, что вы хотели?\n"
                         f"Ваш списочек: \n{wish_list}\n"
                         f"\nНу что ж, если это всё верно, добавим в ваш безупречный wish list! 🎉")

    add_wish_list_to_user (user_id, wish_list, collection_secret_santa )
    await state.clear()

#Логирование запуска
print("Module secret_santa_handler successfully loaded.")
logging.info("Module secret_santa_handler successfully loaded.")
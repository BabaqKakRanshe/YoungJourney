import logging

from init_bot import dp, types, Command, StateFilter, FSMContext
from database.db import get_user_role, get_user_by_id, collection_users, get_all_users

# Хэндлер для команды /admin_message
@dp.message(Command("admin_message"))
async def admin_message_command(message: types.Message, state: FSMContext):
    # Получаем роль пользователя
    user_role = get_user_role(message.from_user.id)
    user_id = get_user_by_id(message.from_user.id, collection_users)

    # Проверка, что роль пользователя = "God"
    if user_role != "God":
        logging.info(f"User {user_id} attempted to execute the /admin_message command")
        return

    # Запрос выбора получателя
    await message.reply("Введите `all` для отправки всем или ID пользователя для отправки конкретному.")
    await state.set_state("awaiting_recipient")

# Хэндлер для ввода получателя (состояние awaiting_recipient)
@dp.message(StateFilter("awaiting_recipient"))
async def admin_message_recipient_handler(message: types.Message, state: FSMContext):
    recipient = message.text.strip()
    await state.update_data(recipient=recipient)
    await message.reply("Введите текст сообщения:")
    await state.set_state("awaiting_message_text")

# Хэндлер для ввода текста сообщения (состояние awaiting_message_text)
@dp.message(StateFilter("awaiting_message_text"))
async def admin_message_text_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    recipient = data.get("recipient")
    text = message.text.strip()

    # Отправка сообщения всем пользователям
    if recipient.lower() == "all":
        # Получаем всех пользователей из базы данных
        users = get_all_users(collection_users)  # Замените на правильную коллекцию
        for user in users:
            user_id = user.get("user_id")
            try:
                # Отправляем сообщение каждому пользователю
                await message.bot.send_message(chat_id=user_id, text=text)
                print(f"Отправили сообщение пользователю {user_id}")
            except Exception as e:
                print(f"Не удалось отправить сообщение пользователю {user_id}: {e}")

        await message.reply("Сообщение отправлено всем пользователям.")
    else:
        # Отправка сообщения конкретному пользователю
        try:
            await message.bot.send_message(chat_id=int(recipient), text=text)
            await message.reply(f"Сообщение отправлено пользователю {recipient}.")
        except ValueError:
            await message.reply("Указан неверный ID.")
        except Exception as e:
            await message.reply(f"Ошибка отправки сообщения: {e}")

    # Сброс состояния
    await state.clear()

print("Module admin_handlers successfully loaded.")
logging.info("Module admin_handlers successfully loaded.")
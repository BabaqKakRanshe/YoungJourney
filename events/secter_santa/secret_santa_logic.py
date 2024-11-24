import logging

from  events.secter_santa.secret_santa_db import find_user, is_in_secret_santa, add_to_secret_santa

# Проверяем, является ли пользователь лидером


def is_user_leader(user_id):
    user = find_user(user_id)

    return user and user.get("Position") == "Leader"

# Обрабатываем статус пользователя в Тайном Санте
def get_user_secret_santa_status(user_id):
    if is_in_secret_santa(user_id):
        return "Вы уже участвуете в Тайном Санте."
    else:
        return "Вы не участвуете в Тайном Санте."

# Принять участие в Тайном Санте
def participate_in_secret_santa(user_id):
    if is_in_secret_santa(user_id):
        return "Вы уже участвуете в Тайном Санте."
    else:
        add_to_secret_santa(user_id)
        return "Вы успешно присоединились к Тайному Санте."

#Логирование запуска
print("Module secret_santa_logic successfully loaded.")
logging.info("Module secret_santa_logic successfully loaded.")
import requests
from strenum import StrEnum
from telegram_bot.auth import session


class Field(StrEnum):
    name = "Имя"
    surname = "Фамилия"
    patronymic = "Отчество"
    mobile_phone = "Мобильный телефон"
    birthdate = "Дата рождения"


modify_date = {}
def enter_change_field(message, bot):
    if session[message.chat.id]['is_parent']:
        bot.send_message(message.chat.id, 'Введите поле, которое хотите изменить.'
                                      'Возможные поля для изменения:'
                                        "Имя, Фамилия, Отчество, Мобильный телефон")
    else:
        bot.send_message(message.chat.id, 'Введите поле, которое хотите изменить.'
                                      'Возможные поля для изменения:'
                                        "Имя, Фамилия, Отчество, Мобильный телефон, Дата рождения")

    bot.register_next_step_handler(message, save_field, bot)

def save_field(message, bot):
    edit_field = message.text
    for field in Field:
        if field.value == edit_field:
            modify_date[field.name] = None

    bot.send_message(message.chat.id, f'Введите новое {message.text}')
    bot.register_next_step_handler(message, modify_personal_date, bot)


def modify_personal_date(message, bot):
    edit_field = message.text
    key = list(modify_date.keys())[0]
    modify_date[key] = edit_field
    send_path_request(message, bot)


def send_path_request(message, bot):
    with requests.Session() as s:
        if session[message.chat.id]['is_parent']:
            response = s.get(f'http://0.0.0.0:8000/tg/parent-info?username='
                         f'{session[message.chat.id]["username"]}')
            payload = response.json()
            key_edit_field = list(modify_date.keys())[0]
            payload[key_edit_field] = modify_date[key_edit_field]
            result = s.patch(f'http://0.0.0.0:8000/tg/parent/{payload["id"]}', data=payload)
        else:
            response = s.get(f'http://0.0.0.0:8000/tg/child-info?username='
                             f'{session[message.chat.id]["username"]}')
            payload = response.json()
            key_edit_field = list(modify_date.keys())[0]
            payload[key_edit_field] = modify_date[key_edit_field]
            result = s.patch(f'http://0.0.0.0:8000/tg/child/{payload["id"]}', data=payload)

        if result.status_code == 200:
            bot.send_message(message.chat.id, "Данные успешно изменены ✅")



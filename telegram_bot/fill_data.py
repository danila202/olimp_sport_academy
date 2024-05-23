from telebot.types import Message
import requests

data = {}

API_URL = 'http://0.0.0.0:8000/tg/'

def registrate(message: Message, bot, json_custom_user,user):
    data['user'] = json_custom_user["id"]
    r = requests.post(API_URL + user, data=data)
    data.clear()
    if r.status_code == 201:
        bot.send_message(message.chat.id, "Ваши данные успешно сохранены")


def start_registrate(message: Message, bot, json_custom_user):
    if message.text != "Продолжить":
        parent = requests.get(f'http://0.0.0.0:8000/tg/parent-info?username='+message.text).json()
        data["parent_id"] = parent.get("id")

    bot.send_message(message.chat.id, 'Введите своё имя')
    bot.register_next_step_handler(message, save_name, bot, json_custom_user)


def save_name(message: Message, bot, json_custom_user):
    name = message.text
    data['name'] = name
    surname = bot.send_message(message.chat.id, 'Введите фамилию')
    bot.register_next_step_handler(surname, save_surname, bot,json_custom_user)


def save_surname(message: Message, bot, json_custom_user):
    surname = message.text
    data['surname'] = surname
    patronymic = bot.send_message(message.chat.id, 'Введите отчество')
    bot.register_next_step_handler(patronymic, save_patronymic, bot, json_custom_user)


def save_patronymic(message: Message, bot, json_custom_user):
    patronymic = message.text
    data['patronymic'] = patronymic
    mobile_phone = bot.send_message(message.chat.id, 'Введите мобильный телефон')
    bot.register_next_step_handler(mobile_phone, save_mobile_phone, bot,json_custom_user)


def save_birth_date(message: Message, bot, json_custom_user):
    birthdate = message.text
    data['birthdate'] = birthdate
    registrate(message, bot, json_custom_user, user="child")


def save_mobile_phone(message: Message, bot, json_custom_user):
    mobile_phone = message.text
    data['mobile_phone'] = mobile_phone
    if json_custom_user["is_parent"]:
        registrate(message, bot, json_custom_user, user="parent")
    else:
        birthdate = bot.send_message(message.chat.id, 'Введите дату рождения')
        bot.register_next_step_handler(birthdate,save_birth_date, bot, json_custom_user)












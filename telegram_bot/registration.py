from telebot.types import Message
import requests
API_URL = 'http://0.0.0.0:8000/tg'


def handler_registration(message: Message, bot, user):
    bot.send_message(message.chat.id, 'Придумайте username')
    bot.register_next_step_handler(message, handler_username, bot, user)


def handler_username(message: Message, bot, user):
    username = message.text
    user['username'] = username
    password = bot.send_message(message.chat.id, 'Придумайте пароль')
    bot.register_next_step_handler(password, handler_password, bot, user)


def handler_password(message: Message, bot, user):
    password = message.text
    user['password'] = password
    bot.send_message(message.chat.id, f'Ваш username- {user["username"]}\nПароль - '
                                           f'{user["password"]}')
    send_post_request(message, bot, user)


def send_post_request(message: Message, bot, user):
    r = requests.post(API_URL+'/user', data=user)
    if r.status_code == 201:
        bot.send_message(message.chat.id, f"Поздравляю Вы зарегистрировались")





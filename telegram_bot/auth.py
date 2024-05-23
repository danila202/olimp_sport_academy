import requests
from telebot import types
from telegram_bot.fill_data import start_registrate
payload = {}


def input_username(message, bot):
    msg = bot.send_message(message.chat.id, "Введите ваш username:")
    bot.register_next_step_handler(msg, input_password,bot)


def input_password(message, bot):
    payload["username"] = message.text
    msg = bot.send_message(message.chat.id, "Введите ваш password")
    bot.register_next_step_handler(msg, handler_login, bot)


def handler_login(message, bot):
    payload["password"] = message.text
    with requests.session() as session:
        session.get('http://0.0.0.0:8000/auth/login/')
        csrf_token = session.cookies['csrftoken']
        headers = {
        'X-CSRFToken': csrf_token
        }
        response = session.post('http://0.0.0.0:8000/auth/login/', data=payload, headers=headers)
        if response.url == 'http://0.0.0.0:8000/accounts/profile/':
            msg = bot.send_message(message.chat.id, 'Поздравляю Вы вошли в свой аккаунт!\n'
                                              'Если Вы родитель и регистрируете за ребенка, то '
                                              'укажите свой username, иначе напишите продолжить')

            json_custom_user = session.get(f'http://0.0.0.0:8000/tg/user-info?username='
                                 f'{payload["username"]}').json()


            bot.register_next_step_handler(msg,start_registrate, bot, json_custom_user)













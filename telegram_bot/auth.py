import requests
from telebot import types
from telegram_bot.fill_data import start_registrate
from telegram_bot.user_menu import create_menu, create_login_button, create_registration_button

payload = {}
session = {}


def input_username(message, bot):
    msg = bot.send_message(message.chat.id, "Введите Ваш username:")
    bot.register_next_step_handler(msg, input_password,bot)


def input_password(message, bot):
    payload["username"] = message.text
    msg = bot.send_message(message.chat.id, "Введите Ваш password")
    bot.register_next_step_handler(msg, handler_login, bot)


def handler_login(message,bot):
    payload["password"] = message.text
    with requests.session() as s:
        s.get('http://0.0.0.0:8000/auth/login/')
        csrf_token = s.cookies['csrftoken']
        headers = {
        'X-CSRFToken': csrf_token
        }
        response = s.post('http://0.0.0.0:8000/auth/login/', data=payload, headers=headers)
        if response.url == 'http://0.0.0.0:8000/accounts/profile/':
            bot.send_message(message.chat.id, '🥳<b>Поздравляю Вы вошли в свой аккаунт!</b>\n'
                                              'После того как вы оформите абонемент'
                                              'у Вас будет отображаться информация о расписание'
                                              'и посещение', parse_mode="HTML")
            json_custom_user = s.get(f'http://0.0.0.0:8000/tg/user-info?username='
                                            f'{payload["username"]}').json()
            session[message.chat.id] = json_custom_user
            create_menu(message, bot, json_custom_user['is_parent'])

        else:
            bot.send_message(message.chat.id, 'Неверный username или пароль. Попробуйте снова')
            payload.clear()
            create_login_button(message, bot)
            bot.register_next_step_handler(message, input_username, bot)


def is_login(message, bot):
    if message.chat.id not in session:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        register_parent = types.KeyboardButton("Зарегистрироваться как родитель")
        login_button = types.KeyboardButton("Войти")
        markup.add(register_parent, login_button)
        bot.send_message(message.chat.id, 'Доступны кнопки регистрации и входа', reply_markup=markup)


def logout(message, bot):
    del session[message.chat.id]
    create_login_button(message, bot)
    requests.get('http://0.0.0.0:8000/auth/logout/')


def fill_user_data(message, bot):
    if message.chat.id in session:
        if session[message.chat.id]['is_parent']:
            response = requests.get(f'http://0.0.0.0:8000/tg/parent-info?username='
                         f'{session[message.chat.id]["username"]}')
            if response.status_code==200:
                data = response.json()
                bot.send_message(
                    message.chat.id,
                    f'Имя - <b>{data["name"]}</b>\n'
                    f'Фамилия - <b>{data["surname"]}</b>\n'
                    f'Отчество - <b>{data["patronymic"]}</b>\n'
                    f'Мобильный телефон - <b>{data["mobile_phone"]}</b>',
                    parse_mode='HTML')
            else:
                start_registrate(message, bot,session[message.chat.id], is_parent=True)
        else:
            response = requests.get(f'http://0.0.0.0:8000/tg/child-info?username='
                                    f'{session[message.chat.id]["username"]}')

            if response.status_code==200:
                data = response.json()
                bot.send_message(
                    message.chat.id,
                    f'Имя - <b>{data["name"]}</b>\n'
                    f'Фамилия - <b>{data["surname"]}</b>\n'
                    f'Отчество - <b>{data["patronymic"]}</b>\n'
                    f'Дата рождения - <b>{data["birthdate"]}</b>\n'
                    f'Мобильный телефон - <b>{data["mobile_phone"]}</b>',
                    parse_mode='HTML')
            else:
                msg = bot.send_message(message.chat.id,'Укажите username родителя')
                bot.register_next_step_handler(
                    msg,start_registrate, bot, session[message.chat.id],is_parent=False
                )


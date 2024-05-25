import os
import telebot
from telebot import types
from telebot.types import Message, BotCommand
from dotenv import load_dotenv
from telegram_bot.registration import handler_registration
from telegram_bot.auth import input_username, fill_user_data, logout, is_login
from telegram_bot.handel_schedule import view_schedule
from telegram_bot.user_menu import create_registration_button, create_login_button
from telegram_bot.handel_visitation import view_visitation


load_dotenv()

API_TOKEN = os.environ.get('API_TOKEN')


bot = telebot.TeleBot(API_TOKEN)
user = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Добро пожаловать! Введите кодовое слово")
    bot.register_next_step_handler(message, callback=is_correct_secret_key)


@bot.message_handler(commands=['buttons'])
def create_buttons(message):
    is_login(message, bot)

def set_bot_commands():
    commands = [BotCommand("buttons", 'Кнопки регистрации и входа')]
    bot.set_my_commands(commands)


def is_correct_secret_key(message):
    if message.text == os.environ.get("SECRET_WORD"):
        bot.send_message(message.chat.id, "Верно. Теперь предлагаю Вам зарегестрироваться.\n"
                                          "Перейдите в меню и нажмите команду /buttons")


    else:
        bot.send_message(message.chat.id, "Неверно")
        send_welcome(message)

@bot.message_handler(func=lambda message: message.text == "Зарегистрироваться как родитель"
                     or message.text == "Зарегистрироваться как спортсмен")
def create_register_button(message):
        bot.register_next_step_handler(message, callback=registrate)

def registrate(message):
    if message.text == "Зарегистрироваться как родитель":
        user['is_parent'] = True
        user['is_child'] = False
    elif message.text == "Зарегистрироваться как спортсмен":
        user['is_parent'] = False
        user['is_child'] = True
    handler_registration(message, bot, user)

@bot.message_handler(func=lambda message: message.text=="Войти")
def login(message):
    input_username(message, bot)


@bot.message_handler(func=lambda message: message.text=="👤 Личные данные")
def fill_personal_data(message):
    fill_user_data(message, bot)


@bot.message_handler(func=lambda message: message.text=="📅 Расписание")
def handel_schedule(message):
    view_schedule(message, bot)


@bot.message_handler(func=lambda message: message.text=="✅ Посещения")
def handel_visitation(message):
    view_visitation(message, bot)

@bot.message_handler(func=lambda message: message.text=="👋 Выйти")
def handel_logout(message):
    logout(message, bot)




if __name__ =="__main__":
    set_bot_commands()
    bot.polling()
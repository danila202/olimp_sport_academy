import os
import telebot
from telebot import types
from telebot.types import Message
from dotenv import load_dotenv
from telegram_bot.registration import handler_registration
from telegram_bot.auth import input_username

load_dotenv()

API_TOKEN = os.environ.get('API_TOKEN')


bot = telebot.TeleBot(API_TOKEN)
user = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Добро пожаловать! Введите кодовое слово")
    bot.register_next_step_handler(message, callback=is_correct_secret_key)

def is_correct_secret_key(message):
    if message.text == os.environ.get("SECRET_WORD"):
        bot.send_message(message.chat.id, "Верно. Теперь предлагаю Вам зарегестрироваться."
                                          "\nНапишите слово - Зарегистрироваться")
    else:
        bot.send_message(message.chat.id, "Неверно")
        send_welcome(message)

@bot.message_handler(func=lambda message: message.text=="Зарегистрироваться")
def create_register_button(message):
        formatted_text = (

            "<b>Если вы регистрируетесь как родитель</b>, сначала создайте учетную запись для себя, "
            "а затем зарегистрируйте ваших детей.\n"
            "<b> Если вы регистрируетесь как спортсмен</b>, создайте учетную запись только для себя."
        )
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        register_parent = types.KeyboardButton("Зарегистрироваться как родитель")
        register_athlete = types.KeyboardButton("Зарегистрироваться как спортсмен")
        markup.add(register_parent, register_athlete)
        bot.send_message(message.chat.id, formatted_text, parse_mode='HTML', reply_markup=markup)
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


if __name__ =="__main__":
    bot.polling()
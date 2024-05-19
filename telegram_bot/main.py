import os
import telebot
from telebot import types
from telebot.types import Message
from dotenv import load_dotenv
from telegram_bot.registration import handler_registration

load_dotenv()

API_TOKEN = os.environ.get('API_TOKEN')


bot = telebot.TeleBot(API_TOKEN)
user = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    send_codeword_prompt(message.chat.id)


def send_codeword_prompt(chat_id):
    bot.send_message(chat_id, "Добро пожаловать! Введите кодовое слово")


@bot.message_handler(func=lambda message: True)
def handle_message(message: Message):
    if message.text == os.environ.get("SECRET_WORD"):
        bot.send_message(message.chat.id, "Верно. Теперь предлагаю Вам зарегестрироваться")
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
        bot.register_next_step_handler(message, registrate)
    else:
        bot.send_message(message.chat.id, "Неверное кодовое слово. Попробуйте еще раз.")
        send_codeword_prompt(message.chat.id)


@bot.message_handler(func=lambda message: True)
def registrate(message):
    if message.text == "Зарегистрироваться как родитель":
        user['is_parent'] = True
        user['is_child'] = False
    elif message.text == "Зарегистрироваться как спортсмен":
        user['is_parent'] = False
        user['is_child'] = True
    handler_registration(message, bot, user)








if __name__ =="__main__":
    bot.polling()
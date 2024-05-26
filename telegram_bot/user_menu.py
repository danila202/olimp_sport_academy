from telebot import types
def create_menu(message, bot, parent):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_personal_data = types.KeyboardButton("👤 Личные данные")
    button_schedule = types.KeyboardButton("📅 Расписание")
    button_visiting = types.KeyboardButton("✅ Посещения")
    button_logout = types.KeyboardButton("👋 Выйти")
    button_modify_personal_data = types.KeyboardButton("📝 Изменить личные данные")
    markup.add(
        button_personal_data,
        button_schedule,
        button_visiting,
        button_logout,
        button_modify_personal_data
    )
    if parent:
        register_athlete = types.KeyboardButton("Зарегистрироваться как спортсмен")
        markup.add(register_athlete)


    bot.send_message(message.chat.id, 'Вам доступно меню', reply_markup=markup)


def create_login_button(message, bot):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    login_button = types.KeyboardButton("Войти")
    markup.add(login_button)
    bot.send_message(message.chat.id,'', reply_markup=markup)


def create_registration_button(message, bot):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    register_parent = types.KeyboardButton("Зарегистрироваться как родитель")
    markup.add(register_parent)
    formatted_text = (
        "🟩🟩 <b><u>ПРАВИЛА РЕГИСТРАЦИИ </u></b>🟩🟩 \n"
        "1️⃣ <b>Сначала Вы регистрируетесь как родитель </b>.\n"
        "2️⃣ <b>После этого зарегистрируйтесь как спортсмен</b>\n"
        "❗❗❗<b><u>ВАЖНО</u></b>❗❗❗\n"
        "1️⃣ <b>Регистрация как родитель необходима для оформления абонемента."
        "Без регистрации родителя оформить абонемент будет невозможно</b>\n"
        "2️⃣ <b>С одного устройства можно зарегистрировать только одного родителя.</b>"
    )

    bot.send_message(message.chat.id, formatted_text, parse_mode='HTML', reply_markup=markup)
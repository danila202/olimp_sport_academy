from telegram_bot.auth import session
import requests


def display_shedule(response):
    messages = []
    for item in response:
        fio = item.get('ФИО')
        message = [f"<b>{fio}</b>"]
        for schedule in item.get('расписания'):
            view = (f'\nГруппа - <b>{schedule["Группа"]}</b>\n'
                    f'День недели - <b>{schedule["День недели"]}</b>\n'
                    f'Время начала - <b>{schedule["Время начала"]}</b>\n'
                    f'Время окончания - <b>{schedule["Время окончания"]}</b>')

            message.append(view)
        messages.append("\n".join(message))

    return "\n\n".join(messages)


def view_schedule(message, bot):
    if message.chat.id in session:
        if session[message.chat.id]["is_parent"]:
            response = requests.get(f'http://0.0.0.0:8000/tg/get-schedule-parent/'
                                    f'{session[message.chat.id]["id"]}')
        else:
            response = requests.get(f'http://0.0.0.0:8000/tg/get-schedule-child/'
                                    f'{session[message.chat.id]["id"]}')

        formatted_schedule = display_shedule(response.json())


        bot.send_message(
        message.chat.id,
        formatted_schedule,
        parse_mode="HTML"
    )







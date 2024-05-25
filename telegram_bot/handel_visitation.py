from telegram_bot.auth import session
import requests


def display_visit(response):
    visitation = []
    for visit in response:
        message = [f"<b>{visit.get('ФИО')}</b>"]
        for item in visit.get("посещения"):
            view = (f"\nДата - <b>{item['Дата']}</b>\n"
                    f"Время ррихода - <b>{item['Время прихода']}</b>"
                    )
            message.append(view)
        visitation.append("\n".join(message))
    return "\n\n".join(visitation)


def view_visitation(message, bot):
    if message.chat.id in session:
        if session[message.chat.id]["is_parent"]:
            response = requests.get(f'http://0.0.0.0:8000/tg/get-visiting-parent/'
                                    f'{session[message.chat.id]["id"]}')
        else:
            response = requests.get(f'http://0.0.0.0:8000/tg/get-visiting-child/'
                                    f'{session[message.chat.id]["id"]}')

        formatted_visitation = display_visit(response.json())

        bot.send_message(
        message.chat.id,
        formatted_visitation,
        parse_mode="HTML"
    )



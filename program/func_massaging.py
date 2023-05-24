import requests
from decouple import config


def send_massage(massage):
    """send message  with telegram bot """
    bot_token = config("TELEGRAM_TOKEN")
    chat_id = config("TELEGRAM_CHAT_ID")

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={massage}"
    res = requests.get(url)
    if res.status_code == 200:
        return "sent"
    else:
        return "failed"

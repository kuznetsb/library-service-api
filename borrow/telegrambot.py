import os

import requests
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv("BOT_TOKEN")
chat_id = os.getenv("CHAT_ID")


def send_notification(message):
    response = requests.get(f'https://api.telegram.org/bot{bot_token}/sendMessage', {
        'chat_id': chat_id,
        'text': message
    })

    if response.status_code == 200:
        print('ok')
    else:
        print(response.text)  # Do what you want with response


# import asyncio
# import telegram
# import os
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from dotenv import load_dotenv
#
# from borrow.models import Borrow

# load_dotenv()
#
# bot_token = os.getenv("BOT_TOKEN")
# chat_id = os.getenv("CHAT_ID")
#
#
# async def send_notification(message):
#     bot = telegram.Bot(token=bot_token)
#     await bot.send_message(chat_id=chat_id, text=message)

#
# def create_borrow_message(borrow):
#     return (f"New Borrow\nBook: {borrow.book.title}\nBorrower: {borrow.user.email}"
#             f"\nBorrow date: {borrow.borrow_date}\nExpected return date: {borrow.expected_return_date}")
#
#
# @receiver(post_save, sender=Borrow)
# def send_borrow_notification(sender, instance, created, **kwargs):
#     if created:
#         message = create_borrow_message(instance)
#         send_notification(message)

#
# message = "Hello, World!"
# asyncio.run(send_notification(message))

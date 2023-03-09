from aiogram import types
from aiogram.types import message
from . import messages
from .app import dp
from . data_fetcher import get_week_events

from aiogram import Bot

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply(messages.WELCOME_MESSAGE)


# @dp.message_handler()
# async def send_answer(message: types.Message):
#    your_variable = message.text
#    print(your_variable)
#    if your_variable == "/Test1":
#        await message.answer(messages.WELCOME_MESSAGE)

from datetime import datetime


@dp.message_handler()
async def date(message: types.Message):
    # date='07-03-2023'
    date = message.text.replace('/', '')
    date = datetime.strptime(date, "%d-%m-%Y").strftime("%d-%m-%Y")
    res = await get_week_events(date)

    response = ""
    for i in res:
        for item in res[f"{i}"]:
            if (len(item) == 0): break
            response += f"Мероприятие: {item['id']+1}"
            response += f"\nНазвание: {item['name']}"
            response += f"\nМесто: {item['place']}\n"
    
    await message.answer(response)
    






from aiogram import types
from . app import dp

@dp.message_handler(commands='week')
async def events_week(message: types.Message):
    await message.reply('events for week')
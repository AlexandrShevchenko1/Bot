from aiogram import types
from aiogram.types import message
from . import messages
from .app import dp, bot
from . data_fetcher import get_week_events, get_day_events, register_user_func, login_and_get_token, post_request_status, get_user_info, get_full_user_info
from . keyboards import inline_kb#, inline_kb_lr код без # не запускается
from aiogram import Bot
import datetime
import telegram
from telegram.constants import ParseMode
from . functions import *
from aiogram.dispatcher import FSMContext
from bot_app.states import GameStates

#слишком сложно, чтобы обьяснить словами
@dp.message_handler(commands=['help'], state="*")
async def send_welcome(message: types.Message):
    await message.reply(messages.HELP_MESSAGE)

@dp.message_handler(commands=['start'], state="*")
async def send_welcome(message: types.Message):
    await GameStates.neOK.set()
    await message.reply(messages.WELCOME_MESSAGE)


# events + username

@dp.message_handler(commands=['events'], state=GameStates.OK)
async def get_date(message: types.Message):
        try:
            res = message.text.split(' ')
            assert len(res) == 2
            get_date.date = datetime.datetime.strptime(f'{res[1]}', '%d-%m-%Y').strftime('%d-%m-%Y')
            await message.reply('Choose the appropriate option:', reply_markup=inline_kb)
        except Exception:
                    await message.reply('Invalid format, please try again.')

             

@dp.callback_query_handler(lambda c: c.data in ['Week events', 'Day events'], state="*")
async def buttom_click_call_back(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    answer = callback_query.data
#  если пользователь зарегался то он не залогинился и наоборот
    try: 
        buttom_click_call_back.token =  register_user_and_assign_token.userName_token[register_user_and_assign_token.curr_userName]
    except:
        buttom_click_call_back.token = login.token

    token = buttom_click_call_back.token

    if (answer == 'Week events'):    
        jsonString = await get_week_events(get_date.date, token)
        text = retrieveWeekEventsData(jsonString)
        if (text == ""):
            await bot.send_message(callback_query.from_user.id, "Nothing scheduled for this date.")
        else: 
            await bot.send_message(callback_query.from_user.id, text, parse_mode=telegram.constants.ParseMode.MARKDOWN)
    elif (answer == "Day events"):  
        jsonString = await get_day_events(get_date.date, token) 
        text= retrieveDayEventData(jsonString)
        if (text == ""):
            await bot.send_message(callback_query.from_user.id, "Nothing scheduled for this date.", parse_mode=telegram.constants.ParseMode.MARKDOWN)
        else: 
            await bot.send_message(callback_query.from_user.id, text, parse_mode=telegram.constants.ParseMode.MARKDOWN)



# пользовтель заходит и сразу авторизуется - уме возвращается token, который он может использовать, чтобы делать запросы
@dp.message_handler(commands=['register'], state=GameStates.neOK)
async def register_user_and_assign_token(message: types.Message):
                user_data = message.text.split()
                if (len(user_data) != 3):
                    await message.reply("wrong data provided", parse_mode=telegram.constants.ParseMode.MARKDOWN)
                else:
                    res = await register_user_func(user_data[1], user_data[2])
                    if (res.get('password') != None):
                        await message.reply('This password is too short. It must contain at least 8 characters.', parse_mode=telegram.constants.ParseMode.MARKDOWN)
                    elif (res.get('username') != None and res.get('id') == None):
                        await message.reply('A user with that username already exists.', parse_mode=telegram.constants.ParseMode.MARKDOWN)
                    elif (res.get('username') != None and res.get('id') != None):
                        await message.reply(f'*{user_data[1]} was registered*', parse_mode=telegram.constants.ParseMode.MARKDOWN)
                        await GameStates.OK.set()
                        # в поле я тожен сохранить is_staf - true либо false (реализовать отдельные запрос - вывод инфы о юзере)
                        register_user_and_assign_token.userName_token = { user_data[1]: (await login_and_get_token(user_data[1], user_data[2]))['auth_token']}
                        register_user_and_assign_token.curr_userName = user_data[1]          


    
# админ не регается он уже есть в базе он делает login
@dp.message_handler(commands=['login'], state=GameStates.neOK)
async def login(message: types.Message):
    data = message.text.split(' ')
    if (len(data) != 3):
        await message.reply("*Incorrect format*", parse_mode=telegram.constants.ParseMode.MARKDOWN)
    else:
        if ("auth_token" in (await post_request_status(data[1], data[2]))):

            login.token = (await login_and_get_token(data[1], data[2]))['auth_token']
            # нужен токен для получения информации о пользователе в которой я возьму id
            login.id = (await get_user_info(login.token))["id"]
            # нужно получить значение перменной is_staff
            login.is_staff = (await get_full_user_info(f"{login.id}"))["is_staff"]

            await message.reply(f"*Success! You logged in*", parse_mode=telegram.constants.ParseMode.MARKDOWN)
            await GameStates.OK.set()
        else:
            await message.reply("*Incorrect login password*", parse_mode=telegram.constants.ParseMode.MARKDOWN)
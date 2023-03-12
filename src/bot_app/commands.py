from aiogram import types
from aiogram.types import message
from . import messages
from .app import dp, bot
from . data_fetcher import get_week_events, get_day_events, register_user_func, login_and_get_token, post_request_status, get_user_info, get_full_user_info, get_user_info_by_username, edit_user, get_all_groups_info, create_group, show_event_info, change_event
from . keyboards import inline_kb#, inline_kb_lr код без # не запускается
from aiogram import Bot
import datetime
import telegram
# from telegram.constants import ParseMode
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
    send_welcome.token = ""
    send_welcome.is_staff = True
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
                    await message.reply("*Invalid format, please try again.*", parse_mode=telegram.constants.ParseMode.MARKDOWN)

             

@dp.callback_query_handler(lambda c: c.data in ['Week events', 'Day events'], state="*")
async def buttom_click_call_back(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    answer = callback_query.data
#  если пользователь зарегался то он не залогинился и наоборот
    # try: 
    #     buttom_click_call_back.token =  register_user_and_assign_token.userName_token[register_user_and_assign_token.curr_userName]
    # except:
    #     buttom_click_call_back.token = login.token

    token = send_welcome.token

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
                    await message.reply("*Wrong data provided*", parse_mode=telegram.constants.ParseMode.MARKDOWN)
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
                        send_welcome.token = (await login_and_get_token(user_data[1], user_data[2]))['auth_token']
                        register_user_and_assign_token.userName_token = { user_data[1]: send_welcome.token}
                        register_user_and_assign_token.curr_userName = user_data[1]
                        register_user_and_assign_token.id = (await get_user_info(register_user_and_assign_token.userName_token[user_data[1]]))["id"]
                        send_welcome.is_staff = (await get_full_user_info(f"{register_user_and_assign_token.id}"))["is_staff"]



    
# админ не регается он уже есть в базе он делает login
@dp.message_handler(commands=['login'], state=GameStates.neOK)
async def login(message: types.Message):
    data = message.text.split(' ')
    if (len(data) != 3):
        await message.reply("*Invalid format, please try again.*", parse_mode=telegram.constants.ParseMode.MARKDOWN)
    else:
        if ("auth_token" in (await post_request_status(data[1], data[2]))):

            send_welcome.token = (await login_and_get_token(data[1], data[2]))['auth_token']
            # нужен токен для получения информации о пользователе в которой я возьму id
            login.id = (await get_user_info(send_welcome.token))["id"]
            # нужно получить значение перменной is_staff
            send_welcome.is_staff = (await get_full_user_info(f"{login.id}"))["is_staff"]
            

            await message.reply(f"Success! You logged in.", parse_mode=telegram.constants.ParseMode.MARKDOWN)
            await GameStates.OK.set()
        else:
            await message.reply("*Incorrect login password.*", parse_mode=telegram.constants.ParseMode.MARKDOWN)

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup


# по дэфолту только админ может менять так что кайф /editEvents + date
@dp.message_handler(commands=['edit_events'], state=GameStates.OK)
async def edit_events(message: types.Message):

            token = send_welcome.token
            if (send_welcome.is_staff):
                    try:
                        res = message.text.split(' ')
                        assert len(res) == 2
                        date = datetime.datetime.strptime(f'{res[1]}', '%d-%m-%Y').strftime('%d-%m-%Y')
                            
                    except Exception:
                            await message.reply("*Invalid format, please try again.*", parse_mode=telegram.constants.ParseMode.MARKDOWN)
                    else:
                        events = await get_week_events(date, token)

                        cnt = 0
                        keys = ['0', '1', '2', '3', '4', '5', '6']
                        kb = InlineKeyboardMarkup()

                        edit_events.dic = {}
                        # await message.reply(events)

                        for key in keys:
                            if (len(events[key]) == 0):
                                cnt += 1
                            else:
                                for event in events[key]:
                                        event_name = event['name']
                                        kb.add(InlineKeyboardButton(f"{event_name}", callback_data=key))
                                        edit_events.dic.update({key: events[key]})
                        
                        if (cnt == 7):
                            await message.reply("Nothing scheduled for this date.")
                        else: 
                            await message.reply("What of the following events to edit: ", reply_markup=kb)
            else:
                await message.answer("You do not have permission to perform this action.")

#
# редактирование event уже зная индекс
# проверить что действительно при любом состоянии работатет нормально
@dp.callback_query_handler(lambda c: c.data in ['0', '1', '2', '3', '4', '5', '6'], state=GameStates.OK)
async def buttom_click_call_back(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    answer = callback_query.data
    
    await bot.send_message(callback_query.from_user.id, retrieveEventData(edit_events.dic[answer]), parse_mode=telegram.constants.ParseMode.MARKDOWN)


#editEventq
@dp.message_handler(commands=['edit'], state=GameStates.OK)
async def edit_event(message: types.Message):

            token = send_welcome.token

            new_info = message.text.split(' ')
            if (send_welcome.is_staff):

                if (len(new_info) == 4):
                    id = new_info[1]
                    
                    new_name = new_info[2]
                    # new_category = new_info[3]
                    new_group = new_info[3]

                    try:
                        type(int(id))
                        # type(int(new_category))
                    except Exception:
                        await message.reply("Id wasn't an integer.")
                    else:
                        event = await show_event_info(id, token)
                        
                        if (event.get('detail') != None):
                            await message.reply(f'There is no such event with id {id}.')
                        else:
                            
                            if (new_name == "-"):
                                new_name = event['name']
                            # if (new_category == "-"):
                            #     new_category = event['category']
                            if (new_group == "-"):
                                new_group = event['participant_groups'][0]['name']
                            

                            groups = await get_all_groups_info(token) 
                            exists = True

                            for group in groups:
                                        if (group.get('name') == new_group):
                                            new_group = group
                                            exists = False

                            if (exists):
                                await message.reply(f'There is no such group as {new_group}.')
                            else:

                                await change_event(id, new_name, event['start'], event['end'], event['category'], new_group, token)
                                # if (answer.get('detail') != None):
                                #     await message.answer("You do not have permission to perform this action.")
                                # if (type(answer['category']) == int):
                                #     await message.answer(f"Такой категории нет в базе данных")
                                await message.answer("Success! Event was changed!")
                else:
                    await message.reply("*Invalid format, please try again.*", parse_mode=telegram.constants.ParseMode.MARKDOWN)
            else:
                await message.answer("You do not have permission to perform this action.")
                 
     

# /userInfo + username
@dp.message_handler(commands=['user_info'], state="*")
async def find_user_info_by_username(message: types.Message):
        
            username = message.text.split(' ')
            if (len(username) == 2):
                user_info = await get_user_info_by_username(username[1])

                text = retrieveUserData(user_info)

                if (text == ""):
                    await message.reply("No user found.")
                else: 
                    await message.reply(text, parse_mode=telegram.constants.ParseMode.MARKDOWN)
            else:
                 await message.reply("*Invalid format, please try again.*", parse_mode=telegram.constants.ParseMode.MARKDOWN)


# проверяю существование группы, могу создать новую
# /addToGroup + username + group
@dp.message_handler(commands=['add_to_group'], state=GameStates.OK)
async def add_to_group(message: types.Message):
            

            token = send_welcome.token
            if (send_welcome.is_staff):
                    nameAndGroup = message.text.split(' ')
                    if (len(nameAndGroup) == 3):
                        user_info = await get_user_info_by_username(nameAndGroup[1])

                        if (len(user_info) == 0):
                                await message.reply("No user found.")
                        else:
                                id = user_info[0]['id']
                                name = user_info[0]['username']

                                groups = await get_all_groups_info(token)
                                groupID = 0 
                                exists = True

                                for group in groups:
                                        if (group.get('name') == nameAndGroup[2]):
                                            groupID = group.get('id')
                                            exists = False
                                
                                if (exists):
                                    await create_group(token, {"name" : f"{nameAndGroup[2]}"})
                                    groups = await get_all_groups_info(token)
                                    for group in groups:
                                        if (group.get('name') == nameAndGroup[2]):
                                            groupID = group.get('id')

                                await edit_user(str(id), name, groupID, nameAndGroup[2], token)
                                # if (answer.get('detail') != None):
                                #     await message.answer("You do not have permission to perform this action.")
                                # else:
                                await message.answer("Success! User was added to group!")
                    else:
                        await message.reply("*Invalid format, please try again.*", parse_mode=telegram.constants.ParseMode.MARKDOWN)
            else:
                 await message.answer("You do not have permission to perform this action.")



# /createGroup + croupName
# @dp.message_handler(commands=['createGroup'], state=GameStates.OK)
# async def creater_group(message: types.Message):
     
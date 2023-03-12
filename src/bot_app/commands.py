from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Tuple, Union, List, Dict, Any

import datetime

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message
from telegram.constants import ParseMode
import telegram

from bot_app.states import GameStates
from .app import dp, bot
from . import messages
from .keyboards import inline_kb #, inline_kb_lr код без # не запускается
from .functions import (
    retrieveWeekEventsData,
    retrieveDayEventData,
    retrieveEventData,
    retrieveUserData
)
from .data_fetcher import (
    get_week_events,
    get_day_events,
    register_user_func,
    login_and_get_token,
    post_request_status,
    get_user_info,
    get_full_user_info,
    get_user_info_by_username,
    edit_user,
    get_all_groups_info,
    create_group,
    show_event_info,
    change_event
)


#слишком сложно, чтобы обьяснить словами
@dp.message_handler(commands=['help'], state="*")
async def send_welcome(message: Message) -> None:
    await message.reply(messages.HELP_MESSAGE)

@dp.message_handler(commands=['start'], state="*")
async def send_welcome(message: Message) -> None:
    await GameStates.neOK.set()
    send_welcome.token = ""
    send_welcome.is_staff = True
    await message.reply(messages.WELCOME_MESSAGE)

# events + username
@dp.message_handler(commands=['events'], state=GameStates.OK)
async def get_date(message: Message) -> None:
    if not message.text or (len(res := message.text.split(' ')) != 2):
        await message.reply("*Invalid format, please try again.*", parse_mode=telegram.constants.ParseMode.MARKDOWN)

    try:
        get_date.date = datetime.datetime.strptime(f'{res[1]}', '%d-%m-%Y').strftime('%d-%m-%Y')
        await message.reply('Choose the appropriate option:', reply_markup=inline_kb)
    except Exception:
        await message.reply("*Invalid format, please try again.*", parse_mode=telegram.constants.ParseMode.MARKDOWN)

@dp.callback_query_handler(lambda c: c.data in ['Week events', 'Day events'], state="*")
async def buttom_click_call_back(callback_query: CallbackQuery) -> None:
    await bot.answer_callback_query(callback_query.id)
    answer = callback_query.data
    #  если пользователь зарегался то он не залогинился и наоборот
    # try: 
    #     buttom_click_call_back.token =  register_user_and_assign_token.userName_token[register_user_and_assign_token.curr_userName]
    # except:
    #     buttom_click_call_back.token = login.token

    token: Union[str, Any] = send_welcome.token
    if (answer == 'Week events'):    
        jsonString: Any = await get_week_events(get_date.date, token)
        text: str = retrieveWeekEventsData(jsonString)
    elif (answer == "Day events"):  
        jsonString: Any = await get_day_events(get_date.date, token) 
        text: str= retrieveDayEventData(jsonString)
    else:
        return

    if not text:
        await bot.send_message(callback_query.from_user.id, "Nothing scheduled for this date.", parse_mode=ParseMode.MARKDOWN)
    else: 
        await bot.send_message(callback_query.from_user.id, text, parse_mode=ParseMode.MARKDOWN)

# пользовтель заходит и сразу авторизуется - уме возвращается token, который он может использовать, чтобы делать запросы
@dp.message_handler(commands=['register'], state=GameStates.neOK)
async def register_user_and_assign_token(message: Message) -> None:
    user_data: List[str] = message.text.split()
    if (len(user_data) != 3):
        await message.reply("*Wrong data provided*", parse_mode=ParseMode.MARKDOWN)
        return
    
    res: Union[Dict, Any] = await register_user_func(user_data[1], user_data[2])
    if (res.get('username') is not None and res.get('email') is not None and res.get('id') is not None):
        await message.reply(f'*{user_data[1]} was registered*', parse_mode=ParseMode.MARKDOWN)
        await GameStates.OK.set()

        # в поле я тожен сохранить is_staf - true либо false (реализовать отдельные запрос - вывод инфы о юзере)
        send_welcome.token = (await login_and_get_token(user_data[1], user_data[2]))['auth_token']
        register_user_and_assign_token.userName_token = { user_data[1]: send_welcome.token }
        register_user_and_assign_token.curr_userName = user_data[1]
        register_user_and_assign_token.id = (await get_user_info(register_user_and_assign_token.userName_token[user_data[1]]))["id"]
        send_welcome.is_staff = (await get_full_user_info(f"{register_user_and_assign_token.id}"))["is_staff"]
    elif (res == {"username": ["A user with that username already exists."]}):
        await message.reply('A user with that username already exists.')
    elif (res == {"username": ["Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters."]}):
        await message.reply('Enter a valid username.')
    else:
        await message.reply('This password is too short. It must contain at least 8 characters.')

# админ не регается он уже есть в базе он делает login
@dp.message_handler(commands=['login'], state=GameStates.neOK)
async def login(message: Message) -> None:
    data: List[str] = message.text.split(' ')
    if (len(data) != 3):
        await message.reply("*Invalid format, please try again.*", parse_mode=ParseMode.MARKDOWN)
        return
    
    if ("auth_token" not in (await post_request_status(data[1], data[2]))):
        await message.reply("*Incorrect login password.*", parse_mode=ParseMode.MARKDOWN)
        return
    
    send_welcome.token = (await login_and_get_token(data[1], data[2]))['auth_token']
    # нужен токен для получения информации о пользователе в которой я возьму id
    login.id = (await get_user_info(send_welcome.token))["id"]
    # нужно получить значение перменной is_staff
    send_welcome.is_staff = (await get_full_user_info(f"{login.id}"))["is_staff"]

    await message.reply(f"Success! You logged in.", parse_mode=ParseMode.MARKDOWN)
    await GameStates.OK.set()    

# по дэфолту только админ может менять так что кайф /editEvents + date
@dp.message_handler(commands=['edit_events'], state=GameStates.OK)
async def edit_events(message: Message) -> None:
    token: Union[str, Any] = send_welcome.token
    if (not send_welcome.is_staff):
        await message.answer("You do not have permission to perform this action.")
        return
    
    if not message.text or (len(res := message.text.split(' ')) != 2):
        await message.reply("*Invalid format, please try again.*", parse_mode=telegram.constants.ParseMode.MARKDOWN)
        return

    try:
        date: str = datetime.datetime.strptime(f'{res[1]}', '%d-%m-%Y').strftime('%d-%m-%Y')
    except Exception:
        await message.reply("*Invalid format, please try again.*", parse_mode=telegram.constants.ParseMode.MARKDOWN)
    else:
        events: Union[Dict[str, Any], Any] = await get_week_events(date, token)

        days_with_no_events: int = 0
        keys: Tuple[str, ...] = ('0', '1', '2', '3', '4', '5', '6')
        kb: InlineKeyboardMarkup = InlineKeyboardMarkup()

        edit_events.dic = {}
        # await message.reply(events)

        for key in keys:
            if (len(events[key]) == 0):
                days_with_no_events += 1
            else:
                for event in events[key]:
                    event_name = event['name']
                    kb.add(InlineKeyboardButton(f"{event_name}", callback_data=key))
                    edit_events.dic.update({key: events[key]})
        
        if (days_with_no_events == 7):
            await message.reply("Nothing scheduled for this date.")
        else: 
            await message.reply("What of the following events to edit: ", reply_markup=kb)

# редактирование event уже зная индекс
# проверить что действительно при любом состоянии работатет нормально
@dp.callback_query_handler(lambda c: c.data in ['0', '1', '2', '3', '4', '5', '6'], state=GameStates.OK)
async def buttom_click_call_back(callback_query: CallbackQuery) -> None:
    await bot.answer_callback_query(callback_query.id)
    answer = callback_query.data
    
    await bot.send_message(callback_query.from_user.id, retrieveEventData(edit_events.dic[answer]), parse_mode=telegram.constants.ParseMode.MARKDOWN)

#editEventq
@dp.message_handler(commands=['edit'], state=GameStates.OK)
async def edit_event(message: Message) -> None:
    token: Union[str, Any] = send_welcome.token
    if not send_welcome.is_staff:
        await message.answer("You do not have permission to perform this action.")
        return
    
    new_info: List[str] = message.text.split(' ')
    
    if (len(new_info) != 4):
        await message.reply("*Invalid format, please try again.*", parse_mode=telegram.constants.ParseMode.MARKDOWN)
        return
    
    event_id: str = new_info[1]
    new_name: str = new_info[2]
    # new_category = new_info[3]
    new_group: str = new_info[3]

    if not event_id.isdecimal():
        try:
            type(int(event_id))
            # type(int(new_category))
        except Exception:
            await message.reply("Id wasn't an integer.")
            return
    
    event: Union[Dict, Any] = await show_event_info(event_id, token)
    if (event.get('detail') is not None):
        await message.reply(f'There is no such event with id {event_id}.')
        return
    
    if (new_name == "-"):
        new_name = event['name']
    # if (new_category == "-"):
    #     new_category = event['category']
    if (new_group == "-"):
        new_group = event['participant_groups'][0]['name']

    groups: Union[Dict, Any] = await get_all_groups_info(token) 
    exists: bool = True
    for group in groups:
        if (group.get('name') == new_group):
            new_group = group
            exists = False

    if (exists):
        await message.reply(f'There is no such group as {new_group}.')
    else:
        await change_event(event_id, new_name, event['start'], event['end'], event['category'], new_group, token)
        # if (answer.get('detail') != None):
        #     await message.answer("You do not have permission to perform this action.")
        # if (type(answer['category']) == int):
        #     await message.answer(f"Такой категории нет в базе данных")
        await message.answer("Success! Event was changed!") 

# /userInfo + username
@dp.message_handler(commands=['user_info'], state="*")
async def find_user_info_by_username(message: Message) -> None:
    username: List[str] = message.text.split(' ')
    if len(username) != 2:
        await message.reply("*Invalid format, please try again.*", parse_mode=telegram.constants.ParseMode.MARKDOWN)
        return

    user_info: Union[Dict, Any] = await get_user_info_by_username(username[1])
    text: str = retrieveUserData(user_info)
    if not text:
        await message.reply("No user found.")
    else: 
        await message.reply(text, parse_mode=telegram.constants.ParseMode.MARKDOWN)

# проверяю существование группы, могу создать новую
# /addToGroup + username + group
@dp.message_handler(commands=['add_to_group'], state=GameStates.OK)
async def add_to_group(message: Message) -> None:
    token: Union[str, Any] = send_welcome.token
    if not send_welcome.is_staff:
        await message.answer("You do not have permission to perform this action.")
        return
    
    nameAndGroup: List[str] = message.text.split(' ')
    if (len(nameAndGroup) !=  3):
        await message.reply("*Invalid format, please try again.*", parse_mode=telegram.constants.ParseMode.MARKDOWN)
        return

    user_info: Union[Dict, Any] = await get_user_info_by_username(nameAndGroup[1])
    if (len(user_info) == 0):
        await message.reply("No user found.")
        return
    
    user_id: Any = user_info[0]['id']
    name: Any = user_info[0]['username']

    groups: Union[Dict, Any] = await get_all_groups_info(token)
    groupID: int = 0 
    exists: bool = True

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

    await edit_user(str(user_id), name, groupID, nameAndGroup[2], token)
    # if (answer.get('detail') != None):
    #     await message.answer("You do not have permission to perform this action.")
    # else:
    await message.answer("Success! User was added to group!")

# /createGroup + croupName
# @dp.message_handler(commands=['createGroup'], state=GameStates.OK)
# async def creater_group(message: Message):

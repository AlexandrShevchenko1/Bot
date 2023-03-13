from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Union, Dict, Any

import aiohttp

from . local_settings import (
    WEEK_EVENTS_URL,
    DAY_EVENTS_URL,
    REGISTER_USER_URL,
    LOGIN_USER_URL,
    USER_INFO_URL_ID,
    USER_FULL_INFO_URL,
    FIND_USER_BY_USERNAME,
    GET_ALL_GROUPS_URL,
    SHOW_EVENT_INFO_URL
)


async def get_week_events(date: str, myToken) -> Union[Dict, Any]:
    async with aiohttp.ClientSession() as session:
        async with session.get(WEEK_EVENTS_URL + date, headers={'Authorization': f'token {myToken}'}) as response:
            return await response.json()

async def get_day_events(date: str, myToken) -> Union[Dict, Any]:
    async with aiohttp.ClientSession() as session:
        async with session.get(DAY_EVENTS_URL + date, headers={'Authorization': f'token {myToken}'}) as response:
            return await response.json()

# doesn't return token only register
async def register_user_func(username, password) -> Union[Dict, Any]:
    async with aiohttp.ClientSession() as session:
        async with session.post(REGISTER_USER_URL, json={'username': username, 'password': password}) as response: 
            return await response.json()

# передаю данные уже авторизованного пользователя
async def login_and_get_token(username, password) -> Union[Dict, Any]:
    async with aiohttp.ClientSession() as session:
        async with session.post(LOGIN_USER_URL, json={'username': username, 'password': password}) as response:
            print(LOGIN_USER_URL)
            print(response.json())
            return await response.json()

async def post_request_status(username, password) -> Union[Dict, Any]:
    async with aiohttp.ClientSession() as client:
        async with client.post(LOGIN_USER_URL, json={'username': username, 'password': password}) as resp:
            return await resp.json()

async def get_user_info(myToken) -> Union[Dict, Any]:
    async with aiohttp.ClientSession() as client:
        async with client.get(USER_INFO_URL_ID, headers={'Authorization': f'token {myToken}'}) as resp:
            return await resp.json()

async def get_full_user_info(user_id: str) -> Union[Dict, Any]:
    async with aiohttp.ClientSession() as client:
        async with client.get(USER_FULL_INFO_URL + user_id) as resp:
            return await resp.json()

async def get_user_info_by_username(username: str) -> Union[Dict, Any]:
    async with aiohttp.ClientSession() as client:
        async with client.get(FIND_USER_BY_USERNAME + username) as resp:
            return await resp.json()

async def edit_user(userID: str, name, groupID, groupNAME, myToken) -> Union[Dict, Any]:
    async with aiohttp.ClientSession() as client:
        jsong: Dict[str, Any] = {'username': name, 'participant_groups': [{"id": groupID, "name": groupNAME}]}
        async with client.put(USER_FULL_INFO_URL + userID + "/", json=jsong, headers={'Authorization': f'token {myToken}'}) as resp:
        # async with client.put(USER_FULL_INFO_URL + userID + "/", data==b'\x00Binary-data\x00', headers={'Authorization': 'token ' + myToken}) as resp:
            return await resp.json()

async def get_all_groups_info(myToken) -> Union[Dict, Any]:
    async with aiohttp.ClientSession() as client:
        async with client.get(GET_ALL_GROUPS_URL, headers={'Authorization': f'token {myToken}'}) as resp:
            return await resp.json()

async def create_group(myToken, jsongString) -> Union[Dict, Any]:
    async with aiohttp.ClientSession() as client:
        async with client.post(GET_ALL_GROUPS_URL, params=jsongString, headers={'Authorization': f'token {myToken}'}) as resp:
            return await resp.json()

async def show_event_info(event_id: str, myToken) -> Union[Dict, Any]:
    async with aiohttp.ClientSession() as client:
        async with client.get(SHOW_EVENT_INFO_URL + event_id, headers={'Authorization': f'token {myToken}'}) as resp:
            return await resp.json()

async def change_event(event_id: str, new_name, start, end, new_category, new_group, myToken) -> Union[Dict, Any]:
    async with aiohttp.ClientSession() as client:
        jsong: Dict[str, Any] = {"name": new_name,"start": start,"end": end,"category": int(new_category),"participant_groups": [new_group]}
        async with client.put(SHOW_EVENT_INFO_URL + event_id + "/", json=jsong, headers={'Authorization': f'token {myToken}'}) as resp:
            return await resp.json()

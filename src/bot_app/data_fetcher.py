import aiohttp
from . local_settings import WEEK_EVENTS_URL, DAY_EVENTS_URL, REGISTER_USER_URL, LOGIN_USER_URL, USER_INFO_URL_ID, USER_FULL_INFO_URL, FIND_USER_BY_USERNAME, GET_ALL_GROUPS_URL, SHOW_EVENT_INFO_URL

async def get_week_events(date, myToken):
    async with aiohttp.ClientSession() as session:
        async with session.get(WEEK_EVENTS_URL + date, headers={'Authorization': f'token {myToken}'}) as response:
            return await response.json()


async def get_day_events(date, myToken):
    async with aiohttp.ClientSession() as session:
        async with session.get(DAY_EVENTS_URL + date, headers={'Authorization': f'token {myToken}'}) as response:
            return await response.json()
        

# doesn't return token only register
async def register_user_func(username, password):
    async with aiohttp.ClientSession() as session:
        async with session.post(REGISTER_USER_URL, json={'username': username, 'password': password}) as response: 
            return await response.json()


# передаю данные уже авторизованного пользователя
async def login_and_get_token(username, password):
    async with aiohttp.ClientSession() as session:
        async with session.post(LOGIN_USER_URL, json={'username': username, 'password': password}) as response: 
            return await response.json()


async def post_request_status(username, password):
    async with aiohttp.ClientSession() as client:
        async with client.post(LOGIN_USER_URL, json={'username': username, 'password': password}) as resp:
            return await resp.json()


async def get_user_info(myToken):
    async with aiohttp.ClientSession() as client:
        async with client.get(USER_INFO_URL_ID, headers={'Authorization': f'token {myToken}'}) as resp:
            return await resp.json()
        
async def get_full_user_info(id):
    async with aiohttp.ClientSession() as client:
        async with client.get(USER_FULL_INFO_URL + id) as resp:
            return await resp.json()

async def get_user_info_by_username(username):
    async with aiohttp.ClientSession() as client:
        async with client.get(FIND_USER_BY_USERNAME + username) as resp:
            return await resp.json()

async def edit_user(userID, name, groupID, groupNAME, myToken):
    async with aiohttp.ClientSession() as client:
        jsong = {'username': name, 'participant_groups': [{"id": groupID, "name": groupNAME}]}
        async with client.put(USER_FULL_INFO_URL + userID + "/", json=jsong, headers={'Authorization': f'token {myToken}'}) as resp:
        # async with client.put(USER_FULL_INFO_URL + userID + "/", data==b'\x00Binary-data\x00', headers={'Authorization': 'token ' + myToken}) as resp:
            return await resp.json()

async def get_all_groups_info(myToken):
    async with aiohttp.ClientSession() as client:
        async with client.get(GET_ALL_GROUPS_URL, headers={'Authorization': f'token {myToken}'}) as resp:
            return await resp.json()

async def create_group(myToken, jsongString):
    async with aiohttp.ClientSession() as client:
        async with client.post(GET_ALL_GROUPS_URL, params=jsongString, headers={'Authorization': f'token {myToken}'}) as resp:
            return await resp.json()



async def show_event_info(id, myToken):
    async with aiohttp.ClientSession() as client:
        async with client.get(SHOW_EVENT_INFO_URL + id, headers={'Authorization': f'token {myToken}'}) as resp:
            return await resp.json()


async def change_event(id, new_name, start, end, new_category, new_group, myToken):
    async with aiohttp.ClientSession() as client:
        jsong = {"name": new_name,"start": start,"end": end,"category": int(new_category),"participant_groups": [new_group]}
        async with client.put(SHOW_EVENT_INFO_URL + id + "/", json=jsong, headers={'Authorization': f'token {myToken}'}) as resp:
            return await resp.json()
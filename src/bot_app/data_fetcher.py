import aiohttp
from . local_settings import WEEK_EVENTS_URL, DAY_EVENTS_URL, REGISTER_USER_URL, LOGIN_USER_URL, USER_INFO_URL_ID, USER_FULL_INFO_URL

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
            

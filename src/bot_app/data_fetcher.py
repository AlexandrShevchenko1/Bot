import aiohttp
from . local_settings import WEEK_EVENTS_URL

async def get_week_events(date):
    async with aiohttp.ClientSession() as session:
        async with session.get(WEEK_EVENTS_URL + date) as response:
            return await response.json()
            




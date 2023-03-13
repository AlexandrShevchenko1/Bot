import os
HOST_IP: str = os.environ.get("DJANGO_HOST", "127.0.0.1")
HOST_PORT: str = os.environ.get("DJANGO_PORT", ":8000/")
HOST_PROTOCOL: str = os.environ.get("DJANGO_PROTOCOL", "http://")

HOST_URL: str = f"{HOST_PROTOCOL}{HOST_IP}{HOST_PORT}"  
  
API_KEY = "6157472072:AAHFbAuPEgLvUAa82-PyqTwRX8GrhGBLZfA"
WEEK_EVENTS_URL: str = f"{HOST_URL}api/v1/week/"
DAY_EVENTS_URL: str = f"{HOST_URL}api/v1/day/"
REGISTER_USER_URL: str = f"{HOST_URL}api/v1/users/"
LOGIN_USER_URL: str = f"{HOST_URL}api/v1/token/login/"
USER_INFO_URL_ID: str = f"{HOST_URL}api/v1/users/me"
USER_FULL_INFO_URL: str = f"{HOST_URL}api/v1/user/"
FIND_USER_BY_USERNAME: str = f"{HOST_URL}api/v1/userbyname/"
GET_ALL_GROUPS_URL: str = f"{HOST_URL}api/v1/group/"
SHOW_EVENT_INFO_URL: str = f"{HOST_URL}api/v1/event/"

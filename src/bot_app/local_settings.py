import os
HOST_IP: str = os.environ.get("DJANGO_HOST", "127.0.0.1")

API_KEY = "6157472072:AAHFbAuPEgLvUAa82-PyqTwRX8GrhGBLZfA"
WEEK_EVENTS_URL: str = f"http://{HOST_IP}:8000/api/v1/week/"
DAY_EVENTS_URL: str = f"http://{HOST_IP}:8000/api/v1/day/"
REGISTER_USER_URL: str = f"http://{HOST_IP}:8000/api/v1/users/"
LOGIN_USER_URL: str = f"http://{HOST_IP}:8000/api/v1/token/login/"
USER_INFO_URL_ID: str = f"http://{HOST_IP}:8000/api/v1/users/me"
USER_FULL_INFO_URL: str = f"http://{HOST_IP}:8000/api/v1/user/"
FIND_USER_BY_USERNAME: str = f"http://{HOST_IP}:8000/api/v1/userbyname/"
GET_ALL_GROUPS_URL: str = f"http://{HOST_IP}:8000/api/v1/group/"
SHOW_EVENT_INFO_URL: str = f"http://{HOST_IP}:8000/api/v1/event/"
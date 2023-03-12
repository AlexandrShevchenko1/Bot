FROM python:3.11-slim-buster

COPY ./src ./bot

WORKDIR /bot

RUN python3 -m pip install pip --upgrade && \
    python3 -m pip install wheel --upgrade && \
    python3 -m pip install pip -r requirements.txt

CMD [ "python3", "/bot/main.py" ]
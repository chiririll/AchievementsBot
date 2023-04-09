FROM python:3.11.3-buster
WORKDIR /Bot
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY Bot .
CMD ["python", "telegram_bot.py"]

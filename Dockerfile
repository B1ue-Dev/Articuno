FROM python:3.10.10

COPY requirements.txt /
RUN python3 -m pip install -r requirements.txt

COPY . /app
WORKDIR /app
ENTRYPOINT ["python3", "bot.py"]

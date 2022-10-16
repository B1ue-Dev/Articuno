FROM debian:11-slim
RUN apt-get update
RUN apt-get install --no-install-suggests --no-install-recommends --yes python3.9 gcc python-pip
RUN apt-get clean

COPY requirements.txt /
RUN python3 -m pip install -r requirements.txt

COPY . /app
WORKDIR /app
ENTRYPOINT ["python3", "bot.py"]

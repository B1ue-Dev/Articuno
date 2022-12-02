FROM debian:11-slim
RUN apt-get update
RUN apt-get install --no-install-suggests --no-install-recommends --yes python3.10 gcc python3-pip
RUN apt-get clean

COPY pyproject.toml /
RUN python3 -m pip install poetry
RUN python3 -m poetry install

COPY . /app
WORKDIR /app
ENTRYPOINT ["python3 -m poetry run python", "bot.py"]

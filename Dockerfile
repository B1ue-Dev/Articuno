FROM python:3.9-slim

WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends libjemalloc2 git && rm -rf /var/lib/apt/lists/*
ENV LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libjemalloc.so.2

COPY requirements.txt /
RUN /venv/bin/pip install -r requirements.txt

COPY . .
CMD ["python", "bot.py"]

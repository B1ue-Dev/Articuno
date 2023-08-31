FROM python:3.10.11

# we want stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install uvloop for faster asyncio
RUN pip3.10 install uvloop

# install the requirements
COPY requirements.txt /tmp/
RUN pip3.10 install -r /tmp/requirements.txt

# copy over the source files
COPY . /app/

# add the path to pythonpath
ENV PYTHONPATH "${PYTHONPATH}:/app"

# start the bot
WORKDIR /app
CMD ["python3.10", "main.py"]

FROM python:3.10-slim-bullseye

# we want stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV VIRTUAL_ENV=/opt/venv

# create a virtualenv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

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
CMD ["python3.10", "-OO", "main.py"]

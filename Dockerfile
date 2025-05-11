FROM python:3.13.1-alpine

# Install git, linux-headers
RUN apk update
RUN apk add build-base linux-headers git

# we want stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV VIRTUAL_ENV=/opt/venv

# create a virtualenv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# install uvloop for faster asyncio
RUN pip3.13 install uvloop

# install the requirements
COPY requirements.txt /tmp/
RUN pip3.13 install --no-cache-dir -r /tmp/requirements.txt

# copy over the source files
COPY . /app/

# add the path to pythonpath
ENV PYTHONPATH "${PYTHONPATH}:/app"

# start the bot
WORKDIR /app
CMD ["python3.13", "-OO", "main.py"]

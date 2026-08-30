FROM python:3.13-slim

# we want stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV VIRTUAL_ENV=/opt/venv

# create a virtualenv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# install uvloop for faster asyncio
RUN pip install --no-cache-dir uvloop

# install the requirements
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# copy over the source files
COPY . /app/

# add the path to pythonpath
ENV PYTHONPATH="${PYTHONPATH}:/app"

# start the bot
WORKDIR /app
CMD ["python3", "-OO", "main.py"]

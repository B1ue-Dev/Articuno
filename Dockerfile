FROM debian:11-slim AS build
RUN apt-get update
RUN apt-get install --no-install-suggests --no-install-recommends --yes python3-venv gcc libpython3-dev
RUN apt-get clean
RUN python3 -m venv /venv

FROM build AS export-req
COPY requirements.txt /
RUN /venv/bin/pip install -r requirements.txt

FROM gcr.io/distroless/python3-debian11
COPY --from=export-req /venv /venv
COPY . /app
WORKDIR /app
ENTRYPOINT ["/venv/bin/python3", "bot.py"]

"""
Root file for exts/server.

(C) 2022-2023 - B1ue-Dev
"""

import logging
import datetime
import interactions
from const import EXT_SERVER


class Server(interactions.Extension):
    """exts/server Extension."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client
        [
            self.client.load_extension(f"exts.server.{ext}")
            for ext in EXT_SERVER
        ]


def setup(client) -> None:
    """Setup the extension"""
    log_time = (
        datetime.datetime.utcnow() + datetime.timedelta(hours=7)
    ).strftime("%d/%m/%Y %H:%M:%S")
    Server(client)
    logging.info("Loaded Server extension.")
    print(f"[{log_time}] Loaded Server extension.")

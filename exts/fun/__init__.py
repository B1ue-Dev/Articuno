"""
Root file for exts/core.

(C) 2022 - Jimmy-Blue
"""

import logging
import datetime
import interactions
from const import EXT_FUN


class Fun(interactions.Extension):
    """exts/fun Extension."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client
        [self.client.load(f"exts.fun.{ext}") for ext in EXT_FUN]


def setup(client) -> None:
    """Setup the extension"""
    log_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=7)).strftime(
        "%d/%m/%Y %H:%M:%S"
    )
    Fun(client)
    logging.debug("""[%s] Loaded Fun extension.""", log_time)
    print(f"[{log_time}] Loaded Fun extension.")

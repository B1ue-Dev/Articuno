"""
Root file for exts/core.

(C) 2022 - Jimmy-Blue
"""

import logging
import datetime
import interactions
from interactions.ext import molter
from const import MSG_EXT_FUN


class Fun(molter.MolterExtension):
    """exts/fun Extension."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client
        [self.client.load(f"exts.msg_exts.fun.{ext}") for ext in MSG_EXT_FUN]


def setup(client) -> None:
    """Setup the extension"""
    log_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=7)).strftime(
        "%d/%m/%Y %H:%M:%S"
    )
    Fun(client)
    logging.debug("""[%s] Loaded Msg-Fun extension.""", log_time)
    print(f"[{log_time}] Loaded Msg-Fun extension.")

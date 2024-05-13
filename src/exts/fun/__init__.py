"""
Root file for exts/fun.

(C) 2022-2023 - B1ue-Dev
"""

import logging
import interactions
from src.const import EXT_FUN


class BaseFun(interactions.Extension):
    """exts/fun Extension."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client
        [self.client.load_extension(f"src.exts.fun.{ext}") for ext in EXT_FUN]


def setup(client) -> None:
    """Setup the extension"""
    BaseFun(client)
    logging.info("Loaded Fun extension.")

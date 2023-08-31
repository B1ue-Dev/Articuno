"""
Root file for exts/utils.

(C) 2022-2023 - B1ue-Dev
"""

import logging
import interactions
from src.const import EXT_UTILS


class Utils(interactions.Extension):
    """exts/utils Extension."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client
        [
            self.client.load_extension(f"src.exts.utils.{ext}")
            for ext in EXT_UTILS
        ]


def setup(client) -> None:
    """Setup the extension"""
    Utils(client)
    logging.info("Loaded Utils extension.")

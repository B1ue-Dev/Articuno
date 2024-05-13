"""
Root file for exts/core.

(C) 2022-2023 - B1ue-Dev
"""

import logging
import interactions
from src.const import EXT_CORE


class BaseCore(interactions.Extension):
    """exts/core Extension."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client
        [
            self.client.load_extension(f"src.exts.core.{ext}")
            for ext in EXT_CORE
        ]


def setup(client) -> None:
    """Setup the extension"""
    BaseCore(client)
    logging.info("Loaded Core extension.")

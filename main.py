"""
Main runner file.

(C) 2023 - B1ue-Dev
"""

import asyncio
import logging
from src.bot import start


if __name__ == "__main__":
    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        logging.info("Shutting down.")

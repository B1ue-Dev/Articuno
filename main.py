"""
Main runner file.

(C) 2023 - B1ue-Dev
"""
# Disable writing of .pyc files
import sys
import asyncio
import argparse
import logging

sys.dont_write_bytecode = True


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Articuno bot, by B1ueDev (Blue)")
    parser.add_argument(
        "-d",
        "--debug",
        default=False,
        help="enable debug mode for Articuno",
        action="store_true",
    )
    args = parser.parse_args()

    try:
        from src.common.error_handler import enableDebug

        enableDebug(args.debug)
        from src.bot import start

        asyncio.run(start())
    except KeyboardInterrupt:
        logging.info("Shutting down.")

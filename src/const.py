"""
For value data.

(C) 2022 - B1ue-Dev
"""

import os
import tomllib

from dotenv import load_dotenv

with open("pyproject.toml", "rb") as f:
    config = tomllib.load(f)
load_dotenv()

TOKEN = os.getenv("TOKEN")
"""The token of the bot."""

VERSION = config["tool"]["poetry"]["version"]
"""Bot version."""

LOG_CHANNEL = os.getenv("LOG_CHANNEL")
"""ID of the log channel."""

EXT_CORE = [
    file.replace(".py", "")
    for file in os.listdir("src/exts/core")
    if not file.startswith("_")
]
"""List of core commands extension."""

EXT_FUN = [
    file.replace(".py", "")
    for file in os.listdir("src/exts/fun")
    if not file.startswith("_")
]
"""List of fun commands extension."""

EXT_UTILS = [
    file.replace(".py", "")
    for file in os.listdir("src/exts/utils")
    if not file.startswith("_")
]
"""List of utils commands extension."""

SOME_RANDOM_API = os.getenv("SOME_RANDOM_API")
"""API key for some-random-api."""

GOOGLE_CLOUD = os.getenv("GOOGLE_CLOUD")
"""Key for Google Cloud."""

GOOGLE_CSE = os.getenv("GOOGLE_CSE")
"""CSE Key for Google."""

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
"""MongoDB Cluster URL."""

TOPGGAPI = os.getenv("TOPGGAPI")
"""Top-gg API key."""

"""
For value data.

(C) 2022 - B1ue-Dev
"""

import os
import dotenv

dotenv.load_dotenv()

TOKEN = os.getenv("TOKEN")
"""The token of the bot."""

VERSION = "v5.0.3"
"""Bot version."""

LOG_CHANNEL = os.getenv("LOG_CHANNEL")

EXT_CORE = [
    file.replace(".py", "")
    for file in os.listdir("exts/core")
    if not file.startswith("_")
]
"""List of core commands extension."""

EXT_FUN = [
    file.replace(".py", "")
    for file in os.listdir("exts/fun")
    if not file.startswith("_")
]
"""List of fun commands extension."""

EXT_SERVER = [
    file.replace(".py", "")
    for file in os.listdir("exts/server")
    if not file.startswith("_")
]
"""List of server commands extension."""

EXT_UTILS = [
    file.replace(".py", "")
    for file in os.listdir("exts/utils")
    if not file.startswith("_")
]
"""List of utils commands extension."""

APIKEY = os.getenv("APIKEY")
"""API key for some-random-api."""

AUTHORIZATION = os.getenv("AUTHORIZATION")
"""API key for random-stuff-api."""

GOOGLE_CLOUD = os.getenv("GOOGLE_CLOUD")
"""Key for Google Cloud."""

GOOGLE_CSE = os.getenv("GOOGLE_CSE")
"""CSE Key for Google."""

U_KEY = os.getenv("UBERDUCK_KEY")
"""Uberduck Key."""

U_SECRET = os.getenv("UBERDUCK_SECRET")
"""Uberduck Secret."""

SERPAPI = os.getenv("SERPAPI")
"""SerpAPI Key."""

"""
For value data.

(C) 2022 - Jimmy-Blue
"""

import os
import dotenv

dotenv.load_dotenv()

global TOKEN
global VERSION
global EXT_CORE
global EXT_FUN
global EXT_SERVER
global EXT_UTILS
global APIKEY
global AUTHORIZATION
global GOOGLE_CLOUD
global GOOGLE_CSE
global U_KEY
global U_SECRET

TOKEN = os.getenv("TOKEN")
VERSION = "v4.2.1"
EXT_CORE = [
    file.replace(".py", "")
    for file in os.listdir("exts/core")
    if not file.startswith("_")
]
EXT_FUN = [
    file.replace(".py", "")
    for file in os.listdir("exts/fun")
    if not file.startswith("_")
]
EXT_SERVER = [
    file.replace(".py", "")
    for file in os.listdir("exts/server")
    if not file.startswith("_")
]
EXT_UTILS = [
    file.replace(".py", "")
    for file in os.listdir("exts/utils")
    if not file.startswith("_")
]
APIKEY = os.getenv("APIKEY")
AUTHORIZATION = os.getenv("AUTHORIZATION")
GOOGLE_CLOUD = os.getenv("GOOGLE_CLOUD")
GOOGLE_CSE = os.getenv("GOOGLE_CSE")
U_KEY = os.getenv("UBERDUCK_KEY")
U_SECRET = os.getenv("UBERDUCK_SECRET")

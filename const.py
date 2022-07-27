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
global APIKEY
global AUTHORIZATION
global GOOGLE_CLOUD
global GOOGLE_CSE
global U_KEY
global U_SECRET

TOKEN = os.getenv('TOKEN')
VERSION = "v4.2.0a"
EXT_CORE = [file.replace(".py", "") for file in os.listdir("exts/core") if not file.startswith("_")]
APIKEY = os.getenv("APIKEY")
AUTHORIZATION = os.getenv("AUTHORIZATION")
GOOGLE_CLOUD = os.getenv("GOOGLE_CLOUD")
GOOGLE_CSE = os.getenv("GOOGLE_CSE")
U_KEY = os.getenv('UBERDUCK_KEY')
U_SECRET = os.getenv('UBERDUCK_SECRET')

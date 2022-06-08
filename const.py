"""
For value data.

(C) 2022 - Jimmy-Blue
"""

import os
import dotenv
dotenv.load_dotenv()

global TOKEN
global VERSION
global APIKEY
global AUTHORIZATION
global GOOGLE_CLOUD
global GOOGLE_CSE

TOKEN = os.getenv('TOKEN')
VERSION = "v4.1.1"

APIKEY = os.getenv("APIKEY")
AUTHORIZATION = os.getenv("AUTHORIZATION")
GOOGLE_CLOUD = os.getenv("GOOGLE_CLOUD")
GOOGLE_CSE = os.getenv("GOOGLE_CSE")

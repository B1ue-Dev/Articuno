import os
from tokenize import Token
import dotenv
dotenv.load_dotenv()

global TOKEN
global VERSION
global OWNER_ID

TOKEN = os.getenv("TOKEN")
VERSION = "v4.1.3"
OWNER_ID = ""

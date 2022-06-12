import os
from tokenize import Token
import dotenv
dotenv.load_dotenv()

global TOKEN

TOKEN = os.getenv("TOKEN")
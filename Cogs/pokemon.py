import interactions
from interactions import extension_command as command
import aiohttp, json, os, io
from dotenv import load_dotenv
from interactions.ext.enhanced import (
	extension_command,
	EnhancedExtension,
	option
)

load_dotenv()
scope = int(os.getenv("SCOPE"))
apikey = os.getenv("APIKEY")


async def get_response(url: str = None, params: dict = None):
	async with aiohttp.ClientSession() as session:
		async with session.get(url, params=params) as resp:
			if resp.status == 200:
				if resp.content_type == "application/json":
					return await resp.json()
				elif resp.content_type in {"image/png", "image/jpeg", "image/gif"}:
					return io.BytesIO(await resp.read())
	await session.close()




class Pokemon(EnhancedExtension):
	def __init__(self, bot):
		self.bot = bot


	@extension_command(
		name="pokemon",
		description="Show the information about a Pokemon",
		scope=scope	
	)
	@option(str, "name", "Name of the Pokemon")
	async def pokemon(self, ctx: interactions.CommandContext,
		name: str
	):
		print("a")



def setup(bot):
	Pokemon(bot)


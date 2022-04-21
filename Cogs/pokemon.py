import interactions
import aiohttp, json, os, io
from dotenv import load_dotenv

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

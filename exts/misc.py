import interactions
from interactions import extension_command as command
import random, os, io, aiohttp
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





class Misc(interactions.Extension):
	def __init__(self, bot) -> None:
		super().__init__()
		self.bot = bot
	

	@command(
		name="hornycard",
		description="Send a hornycard",
		scope=scope,
		options=[
			interactions.Option(
				type=interactions.OptionType.USER,
				name="user",
				description="Targeted user",
				required=False
			)
		]
	)
	async def _hornycard(self, ctx: interactions.CommandContext,
		user: interactions.User = None
	):
		if not user:
			user = ctx.author.user
		else:
			user = user.user
		avatar_url = user.avatar_url
		url = "https://some-random-api.ml/canvas/horny"
		params = {
			"avatar": avatar_url,
		}
		resp = await get_response(url, params)
		img = interactions.File(filename="image.png", fp=resp, description="Image")
		await ctx.send(files=img)



	@command(
		name="simpcard",
		description="Send a simpcard",
		scope=scope,
		options=[
			interactions.Option(
				type=interactions.OptionType.USER,
				name="user",
				description="Targeted user",
				required=False
			)
		]
	)
	async def _simpcard(self, ctx: interactions.CommandContext,
		user: interactions.Member = None
	):
		if not user:
			user = ctx.author.user
		else:
			user = user.user
		avatar_url = user.avatar_url
		async with aiohttp.ClientSession() as session:
			url = "https://some-random-api.ml/canvas/simpcard"
			params = {
				"avatar": avatar_url
			}
			async with session.get(url, params=params) as resp:
				imageData = io.BytesIO(await resp.read())
				await session.close()
				img = interactions.File(filename="image.png", fp=imageData, description="Image")
				await ctx.send(files=img)



	@command(
		name="tweet",
		description="Send a Twitter tweet",
		scope=scope,
		options=[
			interactions.Option(
				type=interactions.OptionType.USER,
				name="user",
				description="Targeted user",
				required=True,
			),
			interactions.Option(
				type=interactions.OptionType.STRING,
				name="comment",
				description="Comment",
				required=True,
			)
		]
	)
	async def _tweet(self, ctx: interactions.CommandContext,
		user: interactions.Member,
		comment: str,
	):
		if len(user.user.username) >= 15:
			username = user.user.username[:12] + "..."
		else:
			username = user.user.username
		if user.nick is not None:
			if len(user.nick) >= 32:
				nick = user.nick[:29] + "..."
			else:
				nick = user.nick
		else:
			nick = username
		async with aiohttp.ClientSession() as session:
			url = "https://some-random-api.ml/canvas/tweet"
			params = {
				"avatar": user.user.avatar_url,
				"username": username,
				"displayname": nick,
				"comment": comment,
				"theme": "dark",
			}
			async with session.get(url, params=params) as resp:
				imageData = io.BytesIO(await resp.read())
				img = interactions.File(filename="image.png", fp=imageData, description="Image")
				await ctx.send(files=img)

	

	@command(
		name="youtube",
		description="Send a YouTube comment",
		scope=scope,
		options=[
			interactions.Option(
				type=interactions.OptionType.USER,
				name="user",
				description="Targeted user",
				required=True,
			),
			interactions.Option(
				type=interactions.OptionType.STRING,
				name="comment",
				description="Comment",
				required=True,
			)
		]
	)
	async def _youtube(self, ctx: interactions.CommandContext,
		user: interactions.Member,
		comment: str,
	):
		if len(user.user.username) >= 15:
			username = user.user.username[:12] + "..."
		else:
			username = user.user.username
		async with aiohttp.ClientSession() as session:
			url = "https://some-random-api.ml/canvas/youtube-comment"
			params = {
				"avatar": user.user.avatar_url,
				"username": username,
				"comment": comment,
			}
			async with session.get(url, params=params) as resp:
				imageData = io.BytesIO(await resp.read())
				await session.close()
				img = interactions.File(filename="image.png", fp=imageData, description="Image")
				await ctx.send(files=img)


	@command(
		name="amogus",
		description="Amogus",
		scope=scope,
		options=[
			interactions.Option(
				type=interactions.OptionType.USER,
				name="user",
				description="Targeted user",
				required=True,
			),
		]
	)
	async def _amogus(self, ctx: interactions.CommandContext,
		user: interactions.Member,
	):
		msg = await ctx.send("Executing...")
		url = "https://some-random-api.ml/premium/amongus"
		params = {
			"avatar": user.user.avatar_url,
			"username": user.user.username,
			"key": apikey,
			"imposter": str(random.choice(['true', 'false']))
		}
		resp = await get_response(url, params)
		img = interactions.File(filename="image.gif", fp=resp, description="Image")
		await msg.edit(content=None, files=img)
	

	"""
	@command(
		name="pet",
		description="Pet someone",
		scope=scope,
		options=[
			interactions.Option(
				type=interactions.OptionType.USER,
				name="user",
				description="Targeted user",
				required=True,
			),
		]
	)
	async def _pet(self, ctx: interactions.CommandContext,
		user: interactions.Member,
	):
		url = "https://cdn.discordapp.com/attachments/862636687226044436/965452327827935272/image.gif"
		#params = {
		#	"avatar": user.user.avatar_url,
		#	"key": apikey,
		#}
		resp = await get_response(url)
		#await ctx.defer()
		img = interactions.File(filename="image.gif", fp=resp, description="Image")
		await ctx.send(files=img)
	"""





def setup(bot):
	Misc(bot)
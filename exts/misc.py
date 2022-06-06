import interactions
from interactions import extension_command as command
import random, os, io, aiohttp
from utils import get_response
from dotenv import load_dotenv

load_dotenv()
apikey = os.getenv("APIKEY")






class Misc(interactions.Extension):
	def __init__(self, bot):
		self.bot = bot
	

	@command(
		name="hornycard",
		description="Send a hornycard",
		options=[
			interactions.Option(
				type=interactions.OptionType.USER,
				name="user",
				description="Targeted user",
				required=False
			)
		],
		dm_permission=False
	)
	async def _hornycard(self, ctx: interactions.CommandContext,
		user: interactions.Member = None
	):
		if user is None:
			user = ctx.member
		else:
			user = user
		avatar_url = user.user.avatar_url
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
		options=[
			interactions.Option(
				type=interactions.OptionType.USER,
				name="user",
				description="Targeted user",
				required=False
			)
		],
		dm_permission=False
	)
	async def _simpcard(self, ctx: interactions.CommandContext,
		user: interactions.Member = None
	):
		if user is None:
			user = ctx.member
		else:
			user = user
		avatar_url = user.user.avatar_url
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
		options=[
			interactions.Option(
				type=interactions.OptionType.USER,
				name="user",
				description="Targeted user",
				required=True
			),
			interactions.Option(
				type=interactions.OptionType.STRING,
				name="comment",
				description="Comment",
				required=True
			)
		],
		dm_permission=False
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
				required=True
			)
		],
		dm_permission=False
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
		options=[
			interactions.Option(
				type=interactions.OptionType.USER,
				name="user",
				description="Targeted user",
				required=True
			)
		],
		dm_permission=False
	)
	async def _amogus(self, ctx: interactions.CommandContext,
		user: interactions.Member,
	):
		url = "https://some-random-api.ml/premium/amongus"
		params = {
			"avatar": user.user.avatar_url,
			"username": user.user.username,
			"key": apikey,
			"imposter": str(random.choice(['true', 'false']))
		}
		resp = await get_response(url, params)
		img = interactions.File(filename="image.gif", fp=resp, description="Image")
		await ctx.send(files=img)
	


	@command(
		name="pet",
		description="Pet someone",
		options=[
			interactions.Option(
				type=interactions.OptionType.USER,
				name="user",
				description="Targeted user",
				required=True
			)
		],
		dm_permission=False
	)
	async def _pet(self, ctx: interactions.CommandContext,
		user: interactions.Member,
	):
		url = "https://some-random-api.ml/premium/petpet"
		params = {
			"avatar": user.user.avatar_url,
			"key": apikey,
		}
		resp = await get_response(url, params)
		img = interactions.File(filename="image.gif", fp=resp, description="Image")
		await ctx.send(files=img)






def setup(bot):
	Misc(bot)
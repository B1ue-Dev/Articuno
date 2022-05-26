import interactions
import os, logging, json, requests, utils.cache as cache, asyncio
from interactions.ext.tasks import IntervalTrigger, create_task
from dotenv import load_dotenv
load_dotenv()
bot_token = os.getenv("TOKEN")
google_cloud = os.getenv("GOOGLE_CLOUD")
google_cse = os.getenv("GOOGLE_CSE")

#logging.basicConfig(level=logging.DEBUG)
version = "v4.1.0"


bot = interactions.Client(
	token=bot_token,
	intents=interactions.Intents.ALL,
	presence=interactions.ClientPresence(
		activities=[
			interactions.PresenceActivity(
				type=interactions.PresenceActivityType.WATCHING,
				name=f"for {version}"
			),
		],
		status=interactions.StatusType.ONLINE,
	),
	#disable_sync=True
)
bot.load('utils.cache')
bot.load('interactions.ext.files')

bot.load('exts.automod')
bot.load('exts.basic')
bot.load('exts.emoji')
bot.load('exts.eval')
bot.load('exts.fun')
bot.load('exts.hacktool')
bot.load('exts.info')
bot.load('exts.logs')
bot.load('exts.menus')
bot.load('exts.misc')
bot.load('exts.mod')
bot.load('exts.pokemon')
bot.load('exts.snipe')
bot.load('exts.tag')



on_ready_trigger = 0;
@bot.event
async def on_ready():
	global on_ready_trigger
	await asyncio.sleep(2)
	_set_user_count: set = set()
	_set_guild_count: set = set()
	for guild in cache.__cached__:
		_set_guild_count.add(guild)
		for member in cache.__cached__[guild]:
			_set_user_count.add(member)
	user_count = len(_set_user_count)
	guild_count = len(_set_guild_count)
	websocket = f"{bot.latency * 1:.0f}"
	print(f'Logged in as {bot.me.name}')
	print(f'ID: {bot.me.id}')
	print(f'Latency: {websocket}ms')
	print(f'Connected to {guild_count} guilds with {user_count} users')
	if on_ready_trigger == 0:
		url = "https://json.psty.io/api_v1/stores/backup"
		headers = {
			"Api-Key": "2f44b242-76ca-4129-b55e-7910078d6930",
			"Content-Type": "application/json"
		}
		resp = requests.get(url, headers=headers)
		with open('./db/tag.json', 'w') as f:
			json.dump(resp.json()['data'], f, indent=4)
		on_ready_trigger = 1;
	else:
		pass
	await bot.change_presence(
		interactions.ClientPresence(
			activities=[
				interactions.PresenceActivity(
					type=interactions.PresenceActivityType.WATCHING,
					name=f"for {version}"
				)
			],
			status=interactions.StatusType.ONLINE,
		)
	)



@create_task(IntervalTrigger(1800)) # Trigger this task every 30 minutes
async def _back_up():
	url = "https://json.psty.io/api_v1/stores/backup"
	headers = {
		"Api-Key": "2f44b242-76ca-4129-b55e-7910078d6930",
		"Content-Type": "application/json"
	}
	with open('./db/tag.json', 'r') as f:
		tag = json.load(f)
		requests.put(url, headers=headers, data=json.dumps(tag))





_back_up.start()
bot.start()
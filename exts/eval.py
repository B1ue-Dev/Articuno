import interactions
import textwrap, inspect, contextlib, io, traceback





class Eval(interactions.Extension):
	def __init__(self, bot):
		self.bot = bot


	@interactions.extension_command(
		name='eval',
		description='Evaluates some code',
		options=[
			interactions.Option(
				type=interactions.OptionType.STRING,
				name="code",
				description="Code to evaluate",
				required=True
			)
		]
	)
	async def _eval(self, ctx: interactions.CommandContext, code: str):
		if int(ctx.user.id) != 892080548342820925:
			return await ctx.send("You must be the bot owner to use this command. Also, no.")
		else:

			blocked_words = ['.delete()', 'os', 'subprocess', 'history()', '("token")', "('token')",
							'aW1wb3J0IG9zCnJldHVybiBvcy5lbnZpcm9uLmdldCgndG9rZW4nKQ==', 'aW1wb3J0IG9zCnByaW50KG9zLmVudmlyb24uZ2V0KCd0b2tlbicpKQ==']
			for x in blocked_words:
				if x in code:
					return await ctx.send('Your code contains certain blocked words.', ephemeral=True)

			env = {
				'ctx': ctx,
				'channel': await ctx.get_channel(),
				'author': ctx.author,
				'user': ctx.user,
				'guild': await ctx.get_guild(),
				'message': ctx.message,
				'source': inspect.getsource,
				'interactions': interactions
			}

			env.update(globals())
			stdout = io.StringIO()

			to_compile = f'async def func():\n{textwrap.indent(code, "  ")}'
			try:
				exec(to_compile, env)
			except Exception:
				await ctx.send(f'```py\n{traceback.format_exc()}\n```')
				return

			func = env['func']
			try:
				with contextlib.redirect_stdout(stdout):
					await func()
			except Exception:
				value = stdout.getvalue()
				await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
				return
			else:
				value = stdout.getvalue()
				if value and len(value) < 1001:
					await ctx.send(f'```py\n>>> {code}\n{value}\n```')
				elif value:
					file = io.StringIO(value)
					with file as f:
						file = interactions.File(filename='output.txt', fp=f)
						await ctx.send(f'```py\n>>> {code}\n{value[:200]}...\n```', files=file)


	@interactions.extension_listener(name="on_message_create")
	async def _message_create(self, message: interactions.Message):
		channel = await message.get_channel()
		if message.content.startswith("$eval"):
			if int(message.author.id) != 892080548342820925:
				return await channel.send("You must be the bot owner to use this command. Also, no.")
			ends = int(len(message.content) - 6)
			code = str(message.content)[-ends:]
			blocked_words = ['.delete()', 'os', 'subprocess', 'history()', '("token")', "('token')",
							'aW1wb3J0IG9zCnJldHVybiBvcy5lbnZpcm9uLmdldCgndG9rZW4nKQ==', 'aW1wb3J0IG9zCnByaW50KG9zLmVudmlyb24uZ2V0KCd0b2tlbicpKQ==']
			for x in blocked_words:
				if x in code:
					return await channel.send('Your code contains certain blocked words.', ephemeral=True)

			env = {
				'ctx': channel,
				'channel': channel,
				'author': message.author,
				'user': interactions.User(**await self.bot._http.get_user(int(message.author.id)), _client=self.bot._http),
				'guild': await message.get_guild(),
				'message': message,
				'source': inspect.getsource,
				'interactions': interactions
			}

			env.update(globals())
			stdout = io.StringIO()

			to_compile = f'async def func():\n{textwrap.indent(code, "  ")}'
			try:
				exec(to_compile, env)
			except Exception:
				return await channel.send(f'```py\n{traceback.format_exc()}\n```')

			func = env['func']
			try:
				with contextlib.redirect_stdout(stdout):
					await func()
			except Exception:
				value = stdout.getvalue()
				return await channel.send(f'```py\n{value}{traceback.format_exc()}\n```')
			else:
				value = stdout.getvalue()
				if value and len(value) < 1001:
					await channel.send(f'```py\n{value}\n```')
				elif value:
					file = io.StringIO(value)
					with file as f:
						file = interactions.File(filename='output.txt', fp=f)
						await channel.send(f'```py\n{value[:200]}...\n```', files=file)







def setup(bot):
    Eval(bot)

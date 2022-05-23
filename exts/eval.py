import interactions
from interactions import extension_command as command
import io, traceback, inspect, textwrap, contextlib, typing


def cleanup_code(content):
	"""Automatically removes code blocks from the code."""
	if content.startswith('```') and content.endswith('```'):
		return '\n'.join(content.split('\n')[1:-1])
	return content.strip('` \n')





class Eval(interactions.Extension):
	def __init__(self, bot) -> None:
		super().__init__()
		self.bot = bot
	
	
	@command(
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
			return await ctx.send("You must be the bot owner to use eval.")
		else:

			"""Evaluates python code"""

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

			code = cleanup_code(code)
			stdout = io.StringIO()

			to_compile = f'async def func():\n{textwrap.indent(code, " ")}'

			def paginate(text: str):
				'''Simple generator that paginates text.'''
				last = 0
				pages = []
				for curr in range(0, len(text)):
					if curr % 1980 == 0:
						pages.append(text[last:curr])
						last = curr
						appd_index = curr
				if appd_index != len(text)-1:
					pages.append(text[last:curr])
				return list(filter(lambda a: a != '', pages))
			
			try:
				exec(to_compile, env)
			except Exception as e:
				await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

			func = env['func']
			print(env)
			try:
				with contextlib.redirect_stdout(stdout):
					ret = await func()
			except Exception as e:
				value = stdout.getvalue()
				await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')

			else:
				value = stdout.getvalue()
				if ret is None:
					if value:
						print(value)
						try:
							await ctx.send(f'```py\n{value}\n```')
						except:
							paginated_text = paginate(value)
							for page in paginated_text:
								if page == paginated_text[-1]:
									await ctx.send(f'```py\n{page}\n```')
									break
								await ctx.send(f'```py\n{page}\n```')



def setup(bot):
	Eval(bot)
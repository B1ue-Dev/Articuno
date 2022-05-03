import interactions
from interactions import extension_command as command
from interactions import extension_message_command as message_command
import os, base64 as b64, utils.brainfuck as brainfuck
from dotenv import load_dotenv

load_dotenv()
scope = int(os.getenv("SCOPE"))





class HackTool(interactions.Extension):
	def __init__(self, bot) -> None:
		super().__init__()
		self.bot = bot
	

	@command(name="base64",
			description="Base64 tools",
			scope=scope,
			options=[
				interactions.Option(
					type=interactions.OptionType.SUB_COMMAND,
					name="encode",
					description="Encode a string",
					options=[
						interactions.Option(
							type=interactions.OptionType.STRING,
							name="string",
							description="String to encode",
							required=True
						)
					]
				),
				interactions.Option(
					type=interactions.OptionType.SUB_COMMAND,
					name="decode",
					description="Decode a string",
					options=[
						interactions.Option(
							type=interactions.OptionType.STRING,
							name="string",
							description="String to decode",
							required=True
						)
					]
				)
			]
	)
	async def _base64(self,
		ctx: interactions.CommandContext,
		sub_command: str,
		string: str
	):
		if sub_command == "encode":
			string_message = string
			string_bytes = string_message.encode("utf-8")
			base64_bytes = b64.b64encode(string_bytes)
			base64_string = base64_bytes.decode("utf-8")
			await ctx.send(f"```{base64_string}```")
		elif sub_command == "decode":
			string_message = string
			string_bytes = string_message.encode("utf-8")
			try:
				base64_bytes = b64.b64decode(string_bytes)
				base64_string = base64_bytes.decode("utf-8")
				await ctx.send(f"```{base64_string}```")
			except:
				await ctx.send("```Invalid string. Please try again!```", ephemeral=True)
	

	@command(name="brainfuck",
			description="Brainfuck interpreter",
			scope=scope,
			options=[
				interactions.Option(
					type=interactions.OptionType.STRING,
					name="string",
					description="String to interpret",
					required=True
				)
			]
	)
	async def _brainfuck(self,
		ctx: interactions.CommandContext,
		string: str
	):
		string_bytes = brainfuck.evaluate(string)
		await ctx.send(f"```{string_bytes}```")






def setup(client):
	HackTool(client)

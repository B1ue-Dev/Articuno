import ast
import inspect
import re
import discord

def source(o):
	s = inspect.getsource(o).split("\n")
	indent = len(s[0]) - len(s[0].lstrip())
	return "\n".join(i[indent:] for i in s)


source_ = source(discord.gateway.DiscordWebSocket.identify)
patched = re.sub(
	r'([\'"]\$browser[\'"]:\s?[\'"]).+([\'"])',
	r"\1Discord iOS\2",
	source_
)

loc = {}
exec(compile(ast.parse(patched), "<string>", "exec"), discord.gateway.__dict__, loc)

discord.gateway.DiscordWebSocket.identify = loc["identify"]
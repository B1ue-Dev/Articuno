"""
Text-to-speech command.

(C) 2022 - Jimmy-Blue
"""

import datetime
import logging
import io
import asyncio
import interactions
import aiohttp
from const import U_KEY, U_SECRET


async def _get_audio(uuid: str) -> dict | bool:
    """
    Get the audio file from Uberduck AI.

    :param uuid: The UUID of the request.
    :type uuid: str
    :return: The json data, or False if None.
    :rtype: dict | bool
    """

    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.uberduck.ai/speak-status?uuid={uuid}") as _resp:
            json: dict = await _resp.json()
            await session.close()

            return json if json.get("path") else False


_voice_name_convert = {
    "sonic-jason-griffith": "Sonic the Hedgehog",
    "tails-colleen": "Tails",
    "amy-rose-cr": "Amy Rose",
    "knuckles": "Knuckles",
    "shadow-david-humphrey": "Shadow",
    "cosmo-the-seedrian": "Cosmo",
    "chris-thorndyke": "Chris Thorndyke",
    "donut-lord": "Tom Wachowski",
    "ash-ketchum": "Ash Ketchum",
    "professor-oak": "Professor Oak",
    "meowth": "Meowth",
}


class TTS(interactions.Extension):
    """Extension for /tts command."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @interactions.extension_command(
        name="tts",
        description="Send a TTS message with different voices (Powered by Uberduck)",
        options=[
            interactions.Option(
                type=interactions.OptionType.STRING,
                name="text",
                description="Text to convert to speech",
                required=True,
            ),
            interactions.Option(
                type=interactions.OptionType.STRING,
                name="voice",
                description="Voice to use",
                required=False,
                choices=[
                    interactions.Choice(name="Sonic", value="sonic-jason-griffith"),
                    interactions.Choice(name="Tails", value="tails-colleen"),
                    interactions.Choice(name="Amy", value="amy-rose-cr"),
                    interactions.Choice(name="Knuckles", value="knuckles"),
                    interactions.Choice(name="Shadow", value="shadow-david-humphrey"),
                    interactions.Choice(
                        name="Cosmo the Seedrian", value="cosmo-the-seedrian"
                    ),
                    interactions.Choice(
                        name="Chris Thorndyke", value="chris-thorndyke"
                    ),
                    interactions.Choice(name="Tom Wachowski", value="donut-lord"),
                    interactions.Choice(name="Ash Ketchum", value="ash-ketchum"),
                    interactions.Choice(name="Professor Oak", value="professor-oak"),
                    interactions.Choice(name="Meowth", value="meowth"),
                ],
            ),
        ],
    )
    async def _tts(
        self, ctx: interactions.CommandContext, text: str, voice: str = None
    ):
        """/tts command."""
        check_voice = [
            "sonic-jason-griffith",
            "tails-colleen",
            "amy-rose-cr",
            "knuckles",
            "shadow-david-humphrey",
            "cosmo-the-seedrian",
            "chris-thorndyke",
            "donut-lord",
            "ash-ketchum",
            "professor-oak",
            "meowth",
        ]
        if not voice:
            voice = "tails-colleen"
        elif voice and voice not in check_voice:
            return await ctx.send("Invalid voice. Please try again.", ephemeral=True)

        if len(text) > 1000:
            return await ctx.send("Text too large. Please try something shorter.", ephemeral=True)

        await ctx.defer()

        url = "https://api.uberduck.ai/speak"
        json = {"speech": text, "voice": voice.lower()}
        auth = aiohttp.BasicAuth(U_KEY, U_SECRET)

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=json, auth=auth) as response:
                    if response.status == 200:
                        uuid = (await response.json())["uuid"]
                        _json = None
                        while True:
                            failed_time = 0
                            audio = await _get_audio(uuid)
                            if failed_time < 10:
                                if audio is not False:
                                    _json = audio
                                    break
                                failed_time += 1
                                await asyncio.sleep(1)
                                continue

                            raise TimeoutError("Failed to get audio.")

                        async with session.get(_json["path"]) as resp:
                            audio = interactions.File(
                                filename="audio.wav",
                                fp=io.BytesIO(await resp.read()),
                            )
                            await ctx.send(
                                content=f"Message: {text}\nVoice: {_voice_name_convert[voice]}",
                                files=audio,
                            )

            await session.close()

        except TimeoutError:
            await ctx.send("Aww! Snap.", ephemeral=True)


def setup(client) -> None:
    """Setup the extension."""
    log_time = (
        datetime.datetime.utcnow() + datetime.timedelta(hours=7)
    ).strftime("%d/%m/%Y %H:%M:%S")
    TTS(client)
    logging.debug("""[%s] Loaded TTS extension.""", log_time)
    print(f"[{log_time}] Loaded TTS extension.")

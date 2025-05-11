import asyncio
import aiohttp

value_convert: dict = {
    "general": 9,
    "book": 10,
    "film": 11,
    "music": 12,
    "theatres": 13,
    "television": 14,
    "games": 15,
    "nature": 17,
    "computers": 18,
    "sports": 21,
    "geography": 22,
    "history": 23,
    "animal": 27,
    "vehicles": 28,
    "comics": 29,
    "anime": 31,
    "cartoons": 32,
}


async def get_response(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.json()


async def main():
    for i in value_convert.values():
        url = f"https://opentdb.com/api.php?amount=10&category={i}&type=boolean&encode=base64"
        print(f"Checking content with value {i}")
        resp = await get_response(url)
        if resp["response_code"] != 0:
            print(f"Failed for category {i}")
        await asyncio.sleep(5)  # Respect rate limit


# Run the event loop
asyncio.run(main())

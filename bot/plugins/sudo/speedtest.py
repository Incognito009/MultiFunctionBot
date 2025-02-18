from pyrogram import Client, filters
from pyrogram.types import Message
from speedtest import Speedtest

from bot import loop
from bot.config import *
from bot.helpers.decorators import sudo_commands
from bot.helpers.functions import get_readable_size
from bot.logging import LOGGER

commands = ["speedtest", f"speedtest@{BOT_USERNAME}"]


def speedtestcli():
    test = Speedtest()
    test.get_best_server()
    test.download()
    test.upload()
    test.results.share()
    result = test.results.dict()
    return result


@Client.on_message(filters.command(commands, **prefixes))
@sudo_commands
async def speedtest(_, message: Message):
    """
    Give speedtest of server where bot is running
    """
    speed = await message.reply("**Running Speedtest on your Server....**", quote=True)
    LOGGER(__name__).info("Starting Speedtest....")
    result = await loop.run_in_executor(None, speedtestcli)
    photo = result["share"]
    string_speed = f"""
    ╭─《 🚀 SPEEDTEST INFO 》
    ├ <b>Upload:</b> <code>{speed_convert(result['upload'], False)}</code>
    ├ <b>Download:</b>  <code>{speed_convert(result['download'], False)}</code>
    ├ <b>Ping:</b> <code>{result['ping']} ms</code>
    ├ <b>Time:</b> <code>{result['timestamp']}</code>
    ├ <b>Data Sent:</b> <code>{get_readable_size(int(result['bytes_sent']))}</code>
    ╰ <b>Data Received:</b> <code>{get_readable_size(int(result['bytes_received']))}</code>
    ╭─《 🌐 SPEEDTEST SERVER 》
    ├ <b>Name:</b> <code>{result['server']['name']}</code>
    ├ <b>Country:</b> <code>{result['server']['country']}, {result['server']['cc']}</code>
    ├ <b>Sponsor:</b> <code>{result['server']['sponsor']}</code>
    ├ <b>Latency:</b> <code>{result['server']['latency']}</code>
    ├ <b>Latitude:</b> <code>{result['server']['lat']}</code>
    ╰ <b>Longitude:</b> <code>{result['server']['lon']}</code>
    ╭─《 👤 CLIENT DETAILS 》
    ├ <b>IP Address:</b> <code>{result['client']['ip']}</code>
    ├ <b>Latitude:</b> <code>{result['client']['lat']}</code>
    ├ <b>Longitude:</b> <code>{result['client']['lon']}</code>
    ├ <b>Country:</b> <code>{result['client']['country']}</code>
    ├ <b>ISP:</b> <code>{result['client']['isp']}</code>
    ╰ <b>ISP Rating:</b> <code>{result['client']['isprating']}</code>
    """

    await speed.delete()
    await message.reply_photo(photo=photo, caption=string_speed, quote=True)


def speed_convert(size, byte=True):
    if not byte:
        size = size / 8
    power = 2**10
    zero = 0
    units = {0: "B/s", 1: "KB/s", 2: "MB/s", 3: "GB/s", 4: "TB/s"}
    while size > power:
        size /= power
        zero += 1
    return f"{round(size, 2)} {units[zero]}"

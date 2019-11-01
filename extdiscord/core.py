import asyncio
from typing import Optional
import threading

from discord import Client, Activity, ActivityType

from extutils.checker import param_type_ensure
from flags import Platform
from extdiscord import handle_discord_main
from extdiscord.logger import DISCORD
from JellyBot.components.utils import load_server
from msghandle.models import MessageEventObjectFactory

from .token_ import discord_token

__all__ = ["run_server", "_inst"]


class DiscordClient(Client):
    async def on_ready(self):
        DISCORD.logger.info(f"Logged on as {self.user}.")
        # Load server for possible reverse() call
        load_server()

        await self.change_presence(activity=Activity(name="8===D", type=ActivityType.playing))

    async def on_message(self, message):
        # Prevent self reading and bot resonate
        if message.author == self.user or message.author.bot:
            return

        await handle_discord_main(
            MessageEventObjectFactory.from_discord(message)).to_platform(Platform.DISCORD).send_discord(message.channel)


class DiscordClientWrapper:
    def __init__(self):
        self._core = DiscordClient(loop=asyncio.new_event_loop())

    def run(self, token):
        self._core.run(token)

    async def start(self, token):
        await self._core.start(token)

    @param_type_ensure
    def get_user_name_safe(self, uid: int) -> Optional[str]:
        udata = self._core.get_user(uid)

        if udata:
            return str(udata)
        else:
            return None


_inst = DiscordClientWrapper()


def run_server():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    _inst.run(discord_token)

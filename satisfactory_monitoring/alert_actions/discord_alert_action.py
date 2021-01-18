import discord
import logging
import threading
import asyncio
import time
import logging

class discord_alert_action:
    __LOGGER = logging.getLogger(__name__)

    def  __init__(self, token, guild_name, channel_name):
        self.client = discord.Client()
        self.ready = False
        self.token = token
        self.guild_name = guild_name
        self.channel_name = channel_name
    
    async def start(self):
        @self.client.event
        async def on_ready():
            self.__LOGGER.info('Discord connection ready.')
            self.ready = True
            self.guild_to_use = self.__get_matching_guild(self.guild_name)
            self.channel_to_use = self.__get_matching_channel(self.guild_to_use, self.channel_name)
        
        try:
            await self.client.start(self.token)
        except KeyboardInterrupt:
            pass
        finally:
            self.__LOGGER.info('Closing discord connection.')
            await self.client.close()

    async def close(self):
        self.client.close()

    async def execute(self, alert_message):

        while not self.ready:
            await asyncio.sleep(1)
        
        await self.channel_to_use.send(alert_message)

    def __get_matching_guild(self, guild_name):
        guild_to_use = next((guild for guild in self.client.guilds if guild.name == guild_name), None)
        if not guild_to_use:
            raise EnvironmentError(f'Discord client is not on a server with name {guild_name}')
        return guild_to_use

    def __get_matching_channel(self, guild, channel_name):
        channel_to_use = next((channel for channel in guild.channels if channel.name == channel_name), None)
        if not channel_to_use:
            raise EnvironmentError(f'No channel named {channel_name} present on server {guild.name}')
        return channel_to_use
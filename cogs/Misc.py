import discord
from discord.ext import commands
import random

random.seed(None, 2)


class Misc(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()  # Events for Cogs
    async def on_ready(self):  # When Bot loads Up
        await self.client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game("Best Bot Ever Made"))
        print('We have logged in as {0.user}'.format(self.client))

    @commands.command()  # Commands
    async def ping(self, ctx):  # Tells User Ping to Bot
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')

    @commands.command(aliases=['fischer'])
    async def fisher(self, ctx):
        await ctx.send("**:star2: Caught a legendary fish!! :star2: (" + str(random.randint(400, 1000)) + ") :dolphin:**")


def setup(client):  # Adds Cog
    client.add_cog(Misc(client))


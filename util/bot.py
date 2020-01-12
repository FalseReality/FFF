import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
import typing
from util.handlers import Handlers

class FFF(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = Handlers.JSON.read("config")

    async def load_extensions(self):
        extensions = ["general", "testing"]
        for extension in extensions:
            self.load_extension(f"extensions.{extension}")
            print(f"Loaded {extension}.")
        print("Starting...")

    async def update_activity(self):
        activity = discord.Activity(name=self.config["activity"]["name"],
                                    type=getattr(discord.ActivityType, self.config["activity"]["type"]))
        await self.change_presence(activity=activity)

    async def on_ready(self):
        self.remove_command('help')
        print("Starting...")
        await self.load_extensions()
        await self.update_activity()
        print(f"Logged in as {self.user} ({self.user.id})")

    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            embed = discord.Embed(title=":x: Invalid Command!", description="Please refer to the **help** command and try again.", color=ctx.author.color)
            embed.set_footer(text="FinalFloorFrags © 2020")
            return await ctx.send(embed=embed)

def get_pre(fff, message):
    id = fff.user.id
    l = [f"<@{id}> ", f"<@!{id}> ", fff.config["prefix"]]
    return l

fff = FFF(command_prefix=get_pre, owner_id=166630166825664512)

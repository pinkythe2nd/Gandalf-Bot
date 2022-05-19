import discord
from discord.ext import commands
from GandalfBotPaths import write_error

class ErrorHandler(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.CommandNotFound):
            return  

        elif isinstance(error, commands.CommandOnCooldown):
            embed_thing = discord.Embed(
                title=f"This command is on cooldown. Please try again after {round(error.retry_after, 1)} seconds.", description="", color=0xFF0000)

        elif isinstance(error, commands.MissingPermissions):
            embed_thing = discord.Embed(
                title=f"You are missing the required permissions to run this command!", description="", color=0xFF0000)

        elif isinstance(error, commands.UserInputError):
            embed_thing = discord.Embed(
                title=f"ur input is wrong u spoon", description="", color=0xFF0000)

        elif isinstance(error, discord.errors.Forbidden):
            embed_thing = discord.Embed(
                title=f"Gandalf is missing required Permissions", description="", color=0xFF0000)

        else:
            embed_thing = discord.Embed(
                title=f"{error}", description="🤷‍♂️", color=0xFF0000)
            write_error(error)

        await ctx.send(embed=embed_thing, delete_after=30)

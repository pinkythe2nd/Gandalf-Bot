import discord
from discord.ext import commands

class ErrorHandler(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.CommandNotFound):
            return  

        elif isinstance(error, commands.CommandOnCooldown):
            embed_thing = discord.Embed(
                title=f"This command is on cooldown. Please try again after {round(error.retry_after, 1)} seconds.", description="", color=0x1F5F9C)

        elif isinstance(error, commands.MissingPermissions):
            embed_thing = discord.Embed(
                title=f"You are missing the required permissions to run this command!", description="", color=0x1F5F9C)

        elif isinstance(error, commands.UserInputError):
            embed_thing = discord.Embed(
                title=f"ur input is wrong u spoon", description="", color=0x1F5F9C)

        elif isinstance(error, discord.errors.Forbidden):
            embed_thing = discord.Embed(
                title=f"Gandalf is missing required Permissions", description="", color=0x1F5F9C)

        else:
            embed_thing = discord.Embed(
                title=f"idk, ffs ghandi", description="", color=0x1F5F9C)
            print(error.with_traceback)

        await ctx.send(embed=embed_thing, delete_after=3)
        await ctx.message.delete(delay=3)

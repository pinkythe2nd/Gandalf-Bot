from discord.ext import commands
import random

class Utilities(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["Ping"], brief="Check to see if gandalf is online or his latency")
    async def ping(self, ctx):
        latency = self.client.latency * 1000
        await ctx.send(f"Fool of a took!\nMy latency is {round(latency)}!", delete_after=600)

    @commands.command(aliases=["Hello"], brief="says hello")
    async def hello(self, ctx):
        greetings = ["Hello!", "Hi!", "Gooday!",
                     "Whats up?", "Yo!", "How's it going?"]
        await ctx.send(random.choice(greetings), delete_after=600)

    @commands.command(brief="you've come from nothing, your going back to nothing, What have you lost? nothing!")
    async def die(self, ctx):
        await ctx.channel.send("Cheer Up You old bugger!", delete_after=600)
        await ctx.message.add_reaction("🙃")
import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx, *input):
        if not input:
            emb = discord.Embed(title='Commands and modules', color=discord.Color.blue(),
                                description=f'Use `.help <module>` to gain more information about that module ')

            cogs_desc = ''
            for cog in self.client.cogs:
                if cog == "ErrorHandler":
                    pass
                else:
                    cogs_desc += f'`{cog}`\n'
            
            emb.add_field(name='Modules', value=cogs_desc, inline=False)
            emb.set_footer(text=f"YOU SHALL NOT PASS!")

        elif len(input) == 1:
            for cog in self.client.cogs:
                if cog.lower() == input[0].lower():
                    emb = discord.Embed(title=f'{cog} - Commands', 
                                        color=discord.Color.green())

                    for command in self.client.get_cog(cog).get_commands():
                        if not command.hidden:
                            emb.add_field(name=f"`.{command.name}`", value=command.brief, inline=False)
                    break
            else:
                emb = discord.Embed(title="!!!",
                description=f"Learn how to type: there is no module called: `{input[0]}`",
                                    color=discord.Color.orange())

        # too many cogs requested - only one at a time allowed
        elif len(input) > 1:
            emb = discord.Embed(title="one module at a time",
                                description="😐🔫",
                                color=discord.Color.orange())

        else:
            emb = discord.Embed(title="ITS FUCKED",
                                description="OK SEND HELP",
                                color=discord.Color.orange())

        # sending reply embed using our own function defined above
        await ctx.send(embed=emb)

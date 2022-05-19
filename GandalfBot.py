# -----------------------Imports------------------------- "
from os import system
from random import choice

import discord
from GandalfBotUtil import Utilities
from GandalfBotMeme import Meme
from GandalfBotMusic import Music
from GandalfBotError import ErrorHandler
from GandalfBotHelp import Help
from GandalfBotPaths import loaded_json
#-------------------------------------------Preferences and oauth stuff------------------------------ "
client = discord.ext.commands.Bot(command_prefix=".", description="Gandalf Bot")
client.remove_command('help')
# ---------------------------------------Actual Commands---------------------------------------------- "
@client.event
async def on_ready():
    status = ["Visiting Hobbiton", "Turning Cave Trolls to Stone", "Telling Stories to Hobbits", "Smoking Pipe Weed", "Summoning Shadowfax",
              "Fighting a Balrog", "Lighting Fireworks", "Summoning Eagles", "Fool of a Took", "You Shall Not Pass", "Speak Friend and Enter", "Touching himself"]
    system("cls")
    print("                        ==(W{==========-      /===-                        ")
    print("                          ||  (.--.)         /===-_---~~~~~~~~~------____  ")
    print("                          | \_,|**|,__      |===-~___                _,-' `")
    print("             -==\\        `\ ' `--'   ),    `//~\\   ~~~~`---.___.-~~      ")
    print("         ______-==|        /`\_. .__/\ \    | |  \\           _-~`         ")
    print("   __--~~~  ,-/-==\\      (   | .  |~~~~|   | |   `\        ,'             ")
    print("_-~       /'    |  \\     )__/==0==-\<>/   / /      \      /               ")
    print(".'        /       |   \\      /~\___/~~\/  /' /        \   /'              ")
    print("/  ____  /         |    \`\.__/-~~   \  |_/'  /          \/'               ")
    print("/-'~    ~~~~~---__  |     ~-/~         ( )   /'        _--~`               ")
    print("              \_|      /        _) | ;  ),   __--~~                        ")
    print("                '~~--_/      _-~/- |/ \   '-~ \                            ")
    print("               {\__--_/}    / \\_>-|)<__\      \                           ")
    print("               /'   (_/  _-~  | |__>--<__|      |                          ")
    print("              |   _/) )-~     | |__>--<__|      |                          ")
    print("              / /~ ,_/       / /__>---<__/      |                          ")
    print("             o-o _//        /-~_>---<__-~      /                           ")
    print("             (^(~          /~_>---<__-      _-~                            ")
    print("            ,/|           /__>--<__/     _-~                               ")
    print("         ,//('(          |__>--<__|     /                  .----_          ")
    print("        ( ( '))          |__>--<__|    |                 /' _---_~\        ")
    print("     `-)) )) (           |__>--<__|    |               /'  /     ~\`\      ")
    print("    ,/,'//( (             \__>--<__\    \            /'  //        ||      ")
    print("  ,( ( ((, ))              ~-__>--<_~-_  ~--____---~' _/'/        /'       ")
    print("`~/  )` ) ,/|                 ~-_~>--<_/-__       __-~ _/                  ")
    print("._-~//( )/ )) `                    ~~-'_/_/ /~~~~~~~__--~                  ")
    print(" ;'( ')/ ,)(                              ~~~~~~~~~~                       ")
    print(" ' ') '( (/                                                                ")
    print("    '   '  `                                                               ")
    print("                         Gandalf 3.95 is up and running!                    ")
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name=choice(status)))
# ---------------------------------------Basic Bot---------------------------------------------------------------------"
client.add_cog(Music(client))
client.add_cog(Meme(client))
client.add_cog(ErrorHandler(client))
client.add_cog(Utilities(client))
client.add_cog(Help(client))
client.run(loaded_json["DISCORD_KEY"])

# -----------------------Imports------------------------- "
import asyncio
import functools
import itertools
import os
import random
import re
import subprocess
import sys
import threading
import time
import urllib.request

import discord
import ffmpeg
import ksoftapi
import lyricsgenius
import praw
import pyttsx3
import youtube_dlc
from async_timeout import timeout
from discord.ext import commands
from googlesearch import search

#-------------------------------------------Preferences and oauth stuff------------------------------ "
client = commands.Bot(command_prefix=".",
                    description="Gandalf Bot")
reddit = praw.Reddit(client_id="TQmrCly4KKGdRg",
                    client_secret="RvcgVefUZhvHfKGolvOa2Q2MwD0",
                    user_agent="yes this is my user agent")
genius = lyricsgenius.Genius("OB6heoxeNbMZH1fUtGWb9Skk6hN-fgSDRXxRimiaRKaQJMwLnogy4L43nAeHc5Fe")

kclient = ksoftapi.Client("eyJ0IjogImFwcCIsICJrIjogImtobWFjc2lnIiwgInBrIjogbnVsbCwgIm8iOiAiMjkzNDIxNTAwNjUwODgxMDQ1IiwgImMiOiA3NDg1MzAwfQ.45deeed06133628c7020248453996656eaa4d5067828175938d17453907b29f8")
# ---------------------------------------Actual Commands---------------------------------------------- "
@client.event
async def on_ready():
    status = ["Visiting Hobbiton", "Turning Cave Trolls to Stone", "Telling Stories to Hobbits", "Smoking Pipe Weed", "Summoning Shadowfax",
              "Fighting a Balrog", "Lighting Fireworks", "Summoning Eagles", "Fool of a Took", "You Shall Not Pass", "Speak Friend and Enter", "Touching himself"]
    os.system("clear")
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
    print("                         Gandalf 3.0 is up and running!                    ")
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name=random.choice(status)))



# ---------------------------------------Basic Bot---------------------------------------------------------------------"

class Meme(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=["Ping"])
    async def ping(self, ctx):
        latency = client.latency * 1000
        await ctx.send(f"Fool of a took!\nMy latency is {round(latency)}!", delete_after=600)

    @commands.command(pass_context=True, aliases=["Hello"])
    async def hello(self, ctx):
        greetings = ["Hello!", "Hi!", "Gooday!",
                    "Whats up?", "Yo!", "How's it going?"]
        await ctx.send(random.choice(greetings), delete_after=600)

    @commands.command()
    async def die(self, ctx):
        await ctx.channel.send("Cheer Up You Miserable Git!", delete_after=600)
        await ctx.message.add_reaction("🙃")

    @commands.command(aliases=["Meme", "Memes", "memes"])
    async def meme(self, ctx):
        result = None
        while result is None:
            memes_submissions = reddit.subreddit("memes").hot()
            randomint = random.randint(1, 100)
            secondrandomint = random.randint(1, 1000)
            if secondrandomint == 1000:
                result = await ctx.channel.send(file=discord.File("/home/pi/Discordbot/Imgs/humans.jpg"))
            else:
                for i in range(0, randomint):
                    result = next(
                        x for x in memes_submissions if not x.stickied)
                await ctx.channel.send(result.url)

    @commands.command(aliases=["Dank"])
    async def dank(self, ctx):
        result = None
        while result is None:
            memes_submissions = reddit.subreddit("dankmemes").hot()
            randomint = random.randint(1, 100)
            secondrandomint = random.randint(1, 500)
            if secondrandomint == 500:
                result = await ctx.channel.send(file=discord.File("/home/pi/Discordbot/Imgs/god.gif"))
            else:
                try:
                    for i in range(0, randomint):
                        result = next(
                            x for x in memes_submissions if not x.stickied)
                    await ctx.channel.send(result.url)
                except:
                    pass

    @commands.command(aliases=["Birb", "berb", "Berb"])
    async def birb(self, ctx):
        result = None
        while result is None:
            memes_submissions = reddit.subreddit("fatbirds").hot()
            randomint = random.randint(1, 100)
            try:
                for i in range(0, randomint):
                    result = next(x for x in memes_submissions if not x.stickied)
                await ctx.channel.send(result.url)
            except:
                pass

    @commands.command(aliases=["Chunk", "Chonk", "chonk"])
    async def chunk(self, ctx):
        result = None
        while result is None:
            memes_submissions = reddit.subreddit("Delightfullychubby").hot()
            randomint = random.randint(1, 100)
            secondrandomint = random.randint(1, 15)
            if secondrandomint == 1:
                await ctx.channel.send(file=discord.File("/home/pi/Discordbot/Imgs/wide.jpg"))
            else:
                try:
                    for i in range(0, randomint):
                        result = next(
                            x for x in memes_submissions if not x.stickied)
                    await ctx.channel.send(result.url)
                except:
                    pass

    @commands.command(aliases=["Cat", "Pussy", "pussy", "Kitten", "kitten", "Cats", "cats"])
    async def cat(self, ctx):
        result = None
        while result is None:
            memes_submissions = reddit.subreddit("cats").hot()
            randomint = random.randint(1, 100)
            try:
                for i in range(0, randomint):
                    result = next(
                        x for x in memes_submissions if not x.stickied)
                await ctx.channel.send(result.url)
            except:
                pass

    @commands.command(aliases=["Monkey", "Monkas", "monkas", "monka", "Monka"])
    async def monkey(self, ctx):
        result = None
        while result is None:
            memes_submissions = reddit.subreddit("monkeys").hot()
            randomint = random.randint(1, 100)
            try:
                for i in range(0, randomint):
                    result = next(
                        x for x in memes_submissions if not x.stickied)
                await ctx.channel.send(result.url)
            except:
                pass

    @commands.command(aliases=["Coon"])
    async def coon(self, ctx):
        rande_it = random.randint(0,50)
        if rande_it == 1:
            await ctx.channel.send(file=discord.File("/home/pi/Discordbot/Imgs/SPOILER_.mp4"))
        else:
            result = None
            while result is None:
                memes_submissions = reddit.subreddit("Raccoons").hot()
                randomint = random.randint(1, 100)
                try:
                    for i in range(0, randomint):
                        result = next( x for x in memes_submissions if not x.stickied)
                    await ctx.channel.send(result.url)
                except:
                    pass

    @commands.command(aliases=["Anos"])
    async def anos(self, ctx):
        gay_thanos_list = ["/home/pi/Discordbot/Imgs/thanos1.jpg",
                            "/home/pi/Discordbot/Imgs/thanos2.jpg"]
        random_gay_thanos = random.choice(gay_thanos_list)
        await ctx.channel.send(file=discord.File(random_gay_thanos), delete_after=1.5)

    @commands.command(aliases=["Thanos"])
    async def thanos(self, ctx):
        random_thanos_interger = random.randint(1, 100)
        if random_thanos_interger < 99:
            thanos_quotes = [
                "Fun isn't something one considers when balancing the universe. But this... does put a smile on my face.",
                "YOU'RE STRONG, BUT I COULD SNAP MY FINGERS AND YOU'D ALL CEASE TO EXIST.",
                "Perfectly balanced, as all things should be.",
                "You have my respect, Stark. When I'm done, half of humanity will still be alive. I hope they remember you.",
                "You're not the only one cursed with knowledge.",
                "I know what it's like to lose. To feel so desperately that you're right, yet to fail nonetheless. It's frightening, turns the legs to jelly. I ask you to what end? Dread it. Run from it. Destiny arrives all the same. And now it's here. Or should I say, I am.",
                "You were going to bed hungry, scrounging for scraps. Your planet was on the brink of collapse. I'm the one who stopped that. You know what's happened since then? The children born have known nothing but full bellies and clear skies. It's a paradise.",
                "What Did It Cost You?, Everything.",
                "THE HARDEST CHOICES REQUIRE THE STRONGEST WILLS.",
                "I'M A SURVIVOR",
                "I AM...INEVITABLE.",
                "I will shred this universe down to its last atom and then, with the stones you've collected for me, create a new one. It is not what is lost but only what it is been given... a grateful universe.",
                "YOU SHOULD HAVE GONE FOR THE HEAD",
                "YOU COULD NOT LIVE WITH YOUR OWN FAILURE, AND WHERE DID THAT BRING YOU? BACK TO ME."]
            random_thanos = random.choice(thanos_quotes)
            await ctx.channel.send(random_thanos)
        elif random_thanos_interger == 100:
            gay_thanos_list = ["/home/pi/Discordbot/Imgs/thanos1.jpg",
                               "/home/pi/Discordbot/Imgs/thanos2.jpg"]
            random_gay_thanos = random.choice(gay_thanos_list)
            await ctx.channel.send(file=discord.File(random_gay_thanos))


    @commands.command(aliases=["Pingu", "Pingus", "pingus"])
    async def pingu(self, ctx):
        pingu_list = ["/home/pi/Discordbot/Imgs/pingu1.gif",
                     "/home/pi/Discordbot/Imgs/pingu2.gif", 
                     "/home/pi/Discordbot/Imgs/pingu3.gif",
                     "/home/pi/Discordbot/Imgs/pingu4.gif",
                     "/home/pi/Discordbot/Imgs/pingu5.gif"]
        random_pingu = random.choice(pingu_list)
        await ctx.channel.send(file=discord.File(random_pingu))

    @commands.command(aliases = ["Bobin"])
    async def bobin(self, ctx):
        randomint = random.randint(1, 3)
        two_random_int = random.randint(1, 50)
        if two_random_int == 1:
            await ctx.channel.send(file=discord.File("/home/pi/Discordbot/Imgs/dont.jpg"))
        else:
            if randomint == 3:
                await ctx.channel.send(file=discord.File("/home/pi/Discordbot/Imgs/bobin.jpg"))
            else:
                embedthing = discord.Embed(title="Bobin is Robin:", description="", color=0x1F5F9C)
                embedthing.add_field(name=(r"https://www.twitch.tv/bobinhdv"), value=(f"😊"), inline=False)
                embedthing.add_field(name=(r"https://twitter.com/BobinHDv"), value=(f"😊"), inline=False)
                embedthing.add_field(name=(r"https://www.instagram.com/brewing_stand/"), value=(f"😊"), inline=False)
                await ctx.send(embed=embedthing, delete_after=600)

    @commands.command(aliases = ["Topgun"])
    async def topgun(self, ctx):
        random_topgun_interger = random.randint(1, 2)
        topguns_list = ["/home/pi/Discordbot/Imgs/Topgun4.jpg",
                        "/home/pi/Discordbot/Imgs/Topgun3.jpg",
                        "/home/pi/Discordbot/Imgs/Topgun2.png",
                        "/home/pi/Discordbot/Imgs/Topgun1.png"]
        random_topguns_list = random.choice(topguns_list)
        if random_topgun_interger == 1:
            await ctx.channel.send(file=discord.File(random_topguns_list))
        elif random_topgun_interger == 2:
            result = None
            while result is None:
                memes_submissions = reddit.subreddit("TankPorn").hot()
                randomint = random.randint(1, 100)
                try:
                    for i in range(0, randomint):
                        result = next(x for x in memes_submissions if not x.stickied)
                    await ctx.channel.send(result.url)
                except:
                    pass
    
    @commands.command(aliases = ["Harvey", "traps", "Traps", "Chickswithdicks", "chickswithdicks"])
    async def harvey(self, ctx):
        random_harvey_interger = random.randint(1, 5)
        descisions = random.randint(1,2)
        harveys_list = ["/home/pi/Discordbot/Imgs/harvey.png",
                        "/home/pi/Discordbot/Imgs/harvey2.png",
                        "/home/pi/Discordbot/Imgs/harvey3.png",
                        "/home/pi/Discordbot/Imgs/harvey4.jpg"
                                                            ]
        random_harveys_list = random.choice(harveys_list)
        if random_harvey_interger == 1:
            await ctx.channel.send(file=discord.File(random_harveys_list))
        else:
            if descisions == 1:
                result = None
                while result is None:
                    memes_submissions = reddit.subreddit("traps").hot()
                    randomint = random.randint(1, 100)
                    try:
                        for i in range(0, randomint):
                            result = next(x for x in memes_submissions if not x.stickied)
                        await ctx.channel.send(result.url, delete_after=10)
                    except:
                        pass
            else:
                result = None
                while result is None:
                    memes_submissions = reddit.subreddit("Animetrapss").hot()
                    randomint = random.randint(1, 100)
                    try:
                        for i in range(0, randomint):
                            result = next(x for x in memes_submissions if not x.stickied)
                        await ctx.channel.send(result.url, delete_after=10)
                    except:
                        pass

    @commands.command(aliases = ["Vygas"])
    async def vygas(self, ctx):
        chance = random.randint(1,3)
        if chance == 1:
            await ctx.channel.send(file=discord.File("/home/pi/Discordbot/Imgs/god.gif"))
        else:
            await ctx.channel.send(file=discord.File("/home/pi/Discordbot/Imgs/vygas1.png"))

    @commands.command(aliases = ["Josh", "JOSH"])
    async def josh(self, ctx):
        random_interger = random.randint(1, 2)
        if random_interger == 1:
            await ctx.channel.send("Likes Feet, like really likes feet🙄")
        else:
            josh_list = ["/home/pi/Discordbot/Imgs/feet1.jpg",
                        "/home/pi/Discordbot/Imgs/feet2.jpg",
                        "/home/pi/Discordbot/Imgs/feet3.jpg"]
            josh_pick = random.choice(josh_list)
            await ctx.channel.send(file=discord.File(josh_pick))
            await ctx.channel.send("Feeling hot under the collar josh?")

    @commands.command(aliases = ["Alex", "Alan", "alan", "Alek", "alek"])
    async def alex(self, ctx):
        random_number = random.randint(1,2)
        if random_number == 1:
            await ctx.channel.send(file=discord.File("/home/pi/Discordbot/Imgs/Alek.jpg"))
        elif random_number == 2:
            await ctx.channel.send(file=discord.File("/home/pi/Discordbot/Imgs/Josh.jpg"))
            await ctx.channel.send("Same person right?")
            await ctx.message.add_reaction("🤷‍♂️")

    @commands.command(aliases = ["Dom"])
    async def dom(self, ctx):
        await ctx.channel.send("csgo, tf2, valorant, he carries all")
        await ctx.channel.send(file=discord.File("/home/pi/Discordbot/Imgs/Dom.jpg"))
        await ctx.message.add_reaction("😳")
        await ctx.channel.send("I mean look at this man!")

    @commands.command(aliases = ["River"])
    async def river(self, ctx):
        random_int = random.randint(1, 3)
        if random_int == 1:
            await ctx.channel.send("SIEG HEIL")
        elif random_int == 2:
            await ctx.channel.send(file=discord.File("/home/pi/Discordbot/Imgs/Hitler.jpg"))
        elif random_int == 3:
            await ctx.channel.send(file=discord.File("/home/pi/Discordbot/Imgs/heil.gif"))

    @commands.command(aliases = ["Sam"])
    async def sam(self, ctx):
        await ctx.channel.send(file=discord.File("/home/pi/Discordbot/Imgs/goblin.jpg"))

    @commands.command(aliases = ["Scary"])
    async def scary(self, ctx):
        await ctx.channel.send(file=discord.File("/home/pi/Discordbot/Imgs/scary.gif"))

    @commands.command(aliases = ["Gay"])
    async def gay(self, ctx):
        random_gay_guy = ["/home/pi/Discordbot/Imgs/Alek.jpg",
                        "/home/pi/Discordbot/Imgs/bobin.jpg",
                        "/home/pi/Discordbot/Imgs/jake.jpg",
                        "/home/pi/Discordbot/Imgs/Josh.jpg",
                        "/home/pi/Discordbot/Imgs/sam2.jpeg"]
        choice = random.choice(random_gay_guy)
        await ctx.channel.send(file=discord.File(choice))
    
    @commands.command(aliases = ["Noman"])
    async def noman(self, ctx):
        result = None
        while result is None:
            memes_submissions = reddit.subreddit("cats").hot()
            randomint = random.randint(1, 100)
            second_random_int = random.randint(1, 10)
            if second_random_int <= 6:
                try:
                    for i in range(0, randomint):
                        result = next(
                            x for x in memes_submissions if not x.stickied)
                    await ctx.channel.send(result.url)
                except:
                    pass
            else:
                try:
                    memes_submissions = reddit.subreddit("Nekomimi").hot()
                    for i in range(0, randomint):
                        result = next(
                            x for x in memes_submissions if not x.stickied)
                    await ctx.channel.send(result.url)
                except:
                    pass
    
    @commands.command(aliases=["Baby17"])
    async def baby17(self, ctx):
        randomnum = random.randint(1,5)
        if randomnum < 3:
            embedthing = discord.Embed(title="He be homophobic", description="", color=0x1F5F9C)
            await ctx.send(embed=embedthing, delete_after=600)
        else:
            result = None
            while result is None:
                memes_submissions = reddit.subreddit("gay").hot()
                randomint = random.randint(1, 100)
                try:
                    for i in range(0, randomint):
                        result = next(x for x in memes_submissions if not x.stickied)
                    await ctx.channel.send(result.url, delete_after=10)
                except:
                    pass

    @commands.command(aliases=["Godisdead"])
    async def godisdead(self, ctx):
        embedthing = discord.Embed(title="God is dead. God remains dead. And we have killed him. How shall we comfort ourselves, the murderers of all murderers? What was holiest and mightiest of all that the world has yet owned has bled to death under our knives: who will wipe this blood off us?", description="", color=0x1F5F9C)
        await ctx.send(embed=embedthing, delete_after=600)


    @commands.command(aliases=["Search"])
    async def search(self, ctx, thingtosearch):
        embedthing = discord.Embed(title=f"Searched for {thingtosearch}", description="", color=0x1F5F9C)
        for j in search(thingtosearch, num_results=5):
            embedthing.add_field(name=(f"{j}"), value=("\u200b"), inline=False)
        await ctx.send(embed=embedthing, delete_after=600)
        
youtube_dlc.utils.bug_reports_message = lambda: ""

songs: list = []
queue: list = []
lyrics_queue: list = []

weeb_list = ["/home/pi/Discordbot/Songs/90s.mp3",
             "/home/pi/Discordbot/Songs/angelbeats.mp3",
             "/home/pi/Discordbot/Songs/bakamitai.mp3",
             "/home/pi/Discordbot/Songs/kisagari.mp3",
             "/home/pi/Discordbot/Songs/moveme.mp3",
             "/home/pi/Discordbot/Songs/p4opening.mp3",
             "/home/pi/Discordbot/Songs/smt4boss.mp3",
             "/home/pi/Discordbot/Songs/evangelion.mp3",
             "/home/pi/Discordbot/Songs/renai.mp3",
             "/home/pi/Discordbot/Songs/sao.mp3",
             "/home/pi/Discordbot/Songs/Unravel.mp3",
             "/home/pi/Discordbot/Songs/jojo.mp3",
             "/home/pi/Discordbot/Songs/attackontitan.mp3",
             "/home/pi/Discordbot/Songs/gasgasgas.mp3",
             "/home/pi/Discordbot/Songs/dejavu.mp3",
             "/home/pi/Discordbot/Songs/cowboy.mp3",
             "/home/pi/Discordbot/Songs/russiananime.mp3",
             "/home/pi/Discordbot/Songs/idk.mp3",
             "/home/pi/Discordbot/Songs/Evergarden.mp3",
             "/home/pi/Discordbot/Songs/One.mp3",
             "/home/pi/Discordbot/Songs/pulka.mp3",
             "/home/pi/Discordbot/Songs/scatman.mp3",
             "/home/pi/Discordbot/Songs/wings.mp3",
             "/home/pi/Discordbot/Songs/Cateargirls.mp3"]

ytdl_format_options = {
    "format": "bestaudio/best",
    "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": False,
    "nocheckcertificate": True,
    "ignoreerrors": True,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "0.0.0.0"
}

ffmpeg_options = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn"
}

ytdl = youtube_dlc.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=1):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get("title")
        self.url = data.get("webpage_url")
        self.duration = data.get("duration")
        self.thumbnail = data.get("thumbnail")
        self.artist = data.get("artist")

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        damn = url.replace(" ", "+")

        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + damn)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        if video_ids:
            url = ("https://www.youtube.com/watch?v=" + video_ids[0])
    
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        filename = data["url"] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["Leave", "L", "l", "fuckoff", "Fuckoff", "quit"])
    async def leave(self, ctx):
        try:
            voice_client = ctx.voice_client
            await voice_client.disconnect()
            songs.clear()
            queue.clear()
            await ctx.message.add_reaction("😭")
        except AttributeError:
            embedthing = discord.Embed(title="Nothing To Leave", description="", color=0x1F5F9C)
            await ctx.send(embed=embedthing, delete_after=600)

    @commands.command(aliases = ["Stop"])
    async def stop(self, ctx):
        try:
            voice_client = ctx.voice_client
            voice_client.stop()
            songs.clear()
            queue.clear()
            lyrics_queue.clear()
            await ctx.message.add_reaction("👌")
        except AttributeError:
            embedthing = discord.Embed(title="Cant Stop what aint playing bitch!", description="", color=0x1F5F9C)
            await ctx.send(embed=embedthing, delete_after=600)

    @commands.command(aliases=["P", "p", "Play"])
    async def play(self, ctx, *, url):
        try:
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            lyrics_queue.append(player)
            name_of_song = player.title
            queue.append(name_of_song)
            ctx.voice_client.play(player, after=lambda x: check_queue(ctx, player))
            urls = player.url
            embedthing = discord.Embed(title="Playing: ", description="", color=0x1F5F9C)
            embedthing.add_field(name=(f"{name_of_song}"), value=(f"😊"), inline=True)
            time_of_song = player.duration
            minutes, seconds = divmod(time_of_song, 60)
            embedthing.add_field(name=(f"Duration: "), value=(f"{minutes} minutes, {seconds} seconds"))
            embedthing.add_field(name="URL: ", value=(urls))
            embedthing.set_thumbnail(url=(player.thumbnail))
            await ctx.send(embed=embedthing, delete_after=time_of_song)
        except discord.ClientException:
            try:
                player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
                urls = player.url
                name_of_song = player.title
                embedthing = discord.Embed(title="Queued: ", description="", color=0x1F5F9C)
                embedthing.add_field(name=(f"{name_of_song}"), value=(f"😊"), inline=True)
                time_of_song = player.duration
                minutes, seconds = divmod(time_of_song, 60)
                embedthing.add_field(name=(f"Duration: "), value=(f"{minutes} minutes, {seconds} seconds"))
                embedthing.add_field(name="URL: ", value=(urls))
                embedthing.set_thumbnail(url=(player.thumbnail))
                await ctx.send(embed=embedthing, delete_after=600)
                songs.append(player)
            except AttributeError:
                embedthing = discord.Embed(title="Cant find a song, try being more specific. or gandalf might not have the permissions to join a chat.", description="", color=0x1F5F9C)
                await ctx.send(embed=embedthing, delete_after=600)

            except TypeError:
                embedthing = discord.Embed(title="Playing A Video", description="", color=0x1F5F9C)
                await ctx.send(embed=embedthing, delete_after=600)

            except:
                embedthing = discord.Embed(title="Cant find a song, try being more specific", description="", color=0x1F5F9C)
                await ctx.send(embed=embedthing, delete_after=600)

        except TypeError:
            embedthing = discord.Embed(title="Playing A Video", description="", color=0x1F5F9C)
            await ctx.send(embed=embedthing, delete_after=600)

        except:
            embedthing = discord.Embed(title="Cant find a song, try being more specific", description="", color=0x1F5F9C)
            await ctx.send(embed=embedthing, delete_after=600)

    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                try:
                    await ctx.author.voice.channel.connect(reconnect=False, timeout=5)
                except:
                    embedthing = discord.Embed(title="gandalf might not have the permissions to join a chat.", description="", color=0x1F5F9C)
                    await ctx.send(embed=embedthing, delete_after=600)
            else:
                embedthing = discord.Embed(title="You are not connected to a voice channel.", description="", color=0x1F5F9C)
                await ctx.send(embed=embedthing, delete_after=600)
        else:
            pass

    @commands.command(aliases=["S", "s", "Skip"])
    async def skip(self, ctx):
        vc = ctx.voice_client
        if not vc or not vc.is_connected():
            embedthing = discord.Embed(title="Cant skip nothing", description="", color=0x1F5F9C)
            await ctx.send(embed=embedthing, delete_after=600)
        else:
            vc.stop()
            embedthing = discord.Embed(title="Skipped a Song", description="", color=0x1F5F9C)
            await ctx.send(embed=embedthing, delete_after=600)
            await ctx.message.add_reaction("⏩")

    @commands.command(aliases=["Queue", "q", "Q"])
    async def queue(self, ctx):
        if not queue:
            embedthing = discord.Embed(title="Nothing In Queue: ", description="", color=0x1F5F9C)
            await ctx.send(embed=embedthing, delete_after=600)
        else:
            embedVar = discord.Embed(title="In Queue:", description="", color=0x1F5F9C)
            counter = -1
            for i in queue:
                counter = counter + 1
                embedVar.add_field(name=(f"{counter}: {i}"), value=("\u200b"), inline=False)
            await ctx.send(embed=embedVar, delete_after = 120)

    @commands.command(aliases= ["Remove"])
    async def remove(self, ctx: commands.Context, index: int):
        vc = ctx.voice_client
        if len(queue) == 0:
            return await ctx.send("Nothing in queue", delete_after=600)
        if index == 0:
            vc.stop()
            del lyrics_queue[0]
            await ctx.send("Skipped a song!", delete_after=600)
        if index > len(queue):
            await ctx.send(f"The queue is only {len(queue)} long", delete_after=600)
        if index < len(queue):
            await ctx.message.add_reaction("⏩")
        try:
            del songs[index - 1]
            del queue[index]
            del lyrics_queue[0]
        except:
            pass

    @commands.command(aliases = ["Weeb", "UwU", "uwu", "Uwu", "uwU", "OwO", "owo", "Owo", "owO"])
    async def weeb(self, ctx):
        try:
            query = random.choice(weeb_list)
            player = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
            ctx.voice_client.play(player, after=lambda x: weeb_check_queue(ctx, player))
            embedthing = discord.Embed(title="Playing: ", description="", color=0x1F5F9C)
            embedthing.add_field(name=("One UwU song"), value=(f"😊"), inline=True)
            embedthing.set_thumbnail(url=("https://yt3.ggpht.com/a/AATXAJwJGd4Z7Yb1bendBPsNxT4UipTY1eEuHiLd-w=s900-c-k-c0xffffffff-no-rj-mo"))
            await ctx.send(embed=embedthing, delete_after=600)
            queue.append("UwU OwO? ❤️")
            weeb_list.remove(query)
        except IndexError:
            try:
                weeb_list.extend(("/home/pi/Discordbot/Songs/90s.mp3",
                                  "/home/pi/Discordbot/Songs/angelbeats.mp3",
                                  "/home/pi/Discordbot/Songs/bakamitai.mp3",
                                  "/home/pi/Discordbot/Songs/kisagari.mp3",
                                  "/home/pi/Discordbot/Songs/moveme.mp3",
                                  "/home/pi/Discordbot/Songs/p4opening.mp3",
                                  "/home/pi/Discordbot/Songs/smt4boss.mp3",
                                  "/home/pi/Discordbot/Songs/evangelion.mp3",
                                  "/home/pi/Discordbot/Songs/renai.mp3",
                                  "/home/pi/Discordbot/Songs/sao.mp3",
                                  "/home/pi/Discordbot/Songs/Unravel.mp3",
                                  "/home/pi/Discordbot/Songs/jojo.mp3",
                                  "/home/pi/Discordbot/Songs/attackontitan.mp3",
                                  "/home/pi/Discordbot/Songs/gasgasgas.mp3",
                                  "/home/pi/Discordbot/Songs/dejavu.mp3",
                                  "/home/pi/Discordbot/Songs/cowboy.mp3",
                                  "/home/pi/Discordbot/Songs/russiananime.mp3",
                                  "/home/pi/Discordbot/Songs/idk.mp3",
                                  "/home/pi/Discordbot/Songs/Evergarden.mp3",
                                  "/home/pi/Discordbot/Songs/One.mp3",
                                  "/home/pi/Discordbot/Songs/pulka.mp3",
                                  "/home/pi/Discordbot/Songs/scatman.mp3",
                                  "/home/pi/Discordbot/Songs/wings.mp3",
                                  "/home/pi/Discordbot/Songs/Cateargirls.mp3"))
                query = random.choice(weeb_list)
                player = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
                ctx.voice_client.play(player, after=lambda x: weeb_check_queue(ctx, player))
                embedthing = discord.Embed(title="Playing: ", description="", color=0x1F5F9C)
                embedthing.add_field(name=("One UwU song"), value=(f"😊"), inline=True)
                embedthing.set_thumbnail(url=( "https://yt3.ggpht.com/a/AATXAJwJGd4Z7Yb1bendBPsNxT4UipTY1eEuHiLd-w=s900-c-k-c0xffffffff-no-rj-mo"))
                await ctx.send(embed=embedthing, delete_after=600)
                queue.append("UwU OwO? ❤️")
                weeb_list.remove(query)
            except discord.ClientException:
                player = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
                songs.append(player)
                queue.append("UwU OwO? ❤️")
                embedthing = discord.Embed(title="Queued: ", description="", color=0x1F5F9C)
                embedthing.add_field(name=("One UwU song"),value=(f"😊"), inline=True)
                embedthing.set_thumbnail(url=("https://yt3.ggpht.com/a/AATXAJwJGd4Z7Yb1bendBPsNxT4UipTY1eEuHiLd-w=s900-c-k-c0xffffffff-no-rj-mo"))
                await ctx.send(embed=embedthing, delete_after=600)
                weeb_list.remove(query)
        except discord.ClientException:
            player = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
            songs.append(player)
            queue.append("UwU OwO? ❤️")
            embedthing = discord.Embed(title="Queued: ", description="", color=0x1F5F9C)
            embedthing.add_field(name=("One UwU song"),value=(f"😊"), inline=True)
            embedthing.set_thumbnail(url=("https://yt3.ggpht.com/a/AATXAJwJGd4Z7Yb1bendBPsNxT4UipTY1eEuHiLd-w=s900-c-k-c0xffffffff-no-rj-mo"))
            await ctx.send(embed=embedthing, delete_after=600)
            try:
                weeb_list.remove(query)
            except:
                pass
    @weeb.before_invoke
    async def check_yes(self, ctx):
        if ctx.voice_client is None:
            try:
                if ctx.author.voice:
                    await ctx.author.voice.channel.connect(reconnect=False, timeout=5)
            except:
                await ctx.channel.send("Gandalf might not have the right permissions to join chat")
            else:
                embedthing = discord.Embed(title="You are not connected to a voice channel.", description="", color=0x1F5F9C)
                await ctx.send(embed=embedthing, delete_after=600)


    @commands.command()
    async def lyrics(self, ctx):
        query = lyrics_queue[0]
        try:
            results = await kclient.music.lyrics(query)
        except ksoftapi.NoResults:
            print('No lyrics found for ' + query)
        else:
            first = results[0]
            print(first.lyrics)

            
def check_queue(ctx, player):
    if songs != []:
        player = songs.pop(0)
        try:
            del queue[0]
        except:
            pass
        try:
            ctx.voice_client.play(player, after=lambda x: check_queue(ctx, player))
            lyrics_queue.clear()
        except:
            try:
                query = "/home/pi/Discordbot/Songs/noise.mp3"
                player = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
                ctx.voice_client.play(player, after=lambda x: check_queue(ctx, player))
            except:
                print("Error on lines 685 to 687")
                pass
    else:
        try:
            del queue[0]
        except:
            pass

def weeb_check_queue(ctx, player):
    if songs != []:
        player = songs.pop(0)
        try:
            del queue[0]
        except:
            pass
        try:
            ctx.voice_client.play(player, after=lambda x: weeb_check_queue(ctx, player))
            lyrics_queue.clear()
        except:
            try:
                query = "/home/pi/Discordbot/Songs/noise.mp3"
                player = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
                ctx.voice_client.play(player, after=lambda x: weeb_check_queue(ctx, player))
                try:
                    lyrics_queue.clear()
                except:
                    pass
            except:
                print("Error on lines 685 to 687")
                pass
    else:
        try:
            del queue[0]
        except:
            pass


client.add_cog(Music(client))
client.add_cog(Meme(client))
client.run("")

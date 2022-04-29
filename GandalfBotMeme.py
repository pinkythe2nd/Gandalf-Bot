import discord, asyncpraw, random
from discord.ext import commands
from GandalfBotPaths import IMGPATH, loaded_json

reddit = asyncpraw.Reddit(client_id=loaded_json["CLIENT_ID"],
                          client_secret=loaded_json["CLIENT_SECRET"],
                          user_agent="yes this is my user agent")

class Meme(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.louis_list = []
        for i in range(1, 24):
            self.louis_list.append(f"{IMGPATH}louis{i}.jpg")
            i += 1

    @commands.command(aliases=["Meme", "Memes", "memes"], brief="r/memes")
    async def meme(self, ctx):
        second_rnd_int = random.randint(1, 1000)
        if second_rnd_int == 1000:
            await ctx.channel.send(file=discord.File(f"{IMGPATH}humans.jpg"))
        else:
            subreddit = await reddit.subreddit("memes")
            all_subs = []
            async for submission in subreddit.hot(limit=100):
                all_subs.append(submission)
            random_sub = random.choice(all_subs)
            await ctx.channel.send(random_sub.url)

    @commands.command(aliases=["profile"], brief="gets a profile pic of who ever is @'d or yourself if no one is @'d")
    async def getpfp(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author
        await ctx.send(member.avatar_url)

    @commands.command(aliases=["Cock", "CockSize", "Cocksize", "COCKSIZE", "cock"], brief="are you above average?")
    async def cocksize(self, ctx):
        l_cock_list = ["MY GOD IS THAT A EXTRA FOREARM?!", "HOlY SHIT NO WONDER UR GIRLFRIED WAS LIMPING", "Do they even do condoms that large?", "😳", "You've got a giant Penis, congrats!"]
        s_cock_list = ["r u even a man?!?!",
                        "Sorry we havent developed technology to see that small yet come back in a few thousand years:(", "Tiny winy iny winy short dick man", "Oh cute an extra belly button", "Yikes, just yikes", "your pubes are longer than ur shaft -_-"]
        user = ctx.author.id
        if user == 293421500650881045 or user == 600815646389043289 or user == 227858703603204096 or user == 557837474861416450:
            await ctx.channel.send(random.choice(l_cock_list))
        else:
            await ctx.channel.send(random.choice(s_cock_list))

    @commands.command(aliases=["CHRISTMAS"])
    async def christmas(self, ctx):
        await ctx.channel.send(file=discord.File(f"{IMGPATH}christmas.png"))
        await ctx.send("Merry Christmas, u beatiful bastards! x", delete_after=600)

    @commands.command(aliases=["Dank"], brief="r/dankmemes")
    async def dank(self, ctx):
        second_rnd_int = random.randint(1, 500)
        if second_rnd_int == 500:
            await ctx.channel.send(file=discord.File(f"{IMGPATH}god.gif"))
        else:
            subreddit = await reddit.subreddit("dankmemes")
            all_subs = []
            async for submission in subreddit.hot(limit=100):
                all_subs.append(submission)
        random_sub = random.choice(all_subs)
        await ctx.channel.send(random_sub.url)

    @commands.command(aliases=["Birb", "berb", "Berb"], brief="r/fatbirds")
    async def birb(self, ctx):
        subreddit = await reddit.subreddit("fatbirds")
        all_subs = []
        async for submission in subreddit.hot(limit=100):
            all_subs.append(submission)
        random_sub = random.choice(all_subs)
        await ctx.channel.send(random_sub.url)

    @commands.command(aliases=["Chunk", "Chonk", "chonk"], brief="r/delightfullychubby")
    async def chunk(self, ctx):
        second_rnd_int = random.randint(1, 15)
        if second_rnd_int == 1:
            await ctx.channel.send(file=discord.File(f"{IMGPATH}wide.jpg"))
        else:
            subreddit = await reddit.subreddit("Delightfullychubby")
            all_subs = []
            async for submission in subreddit.hot(limit=100):
                all_subs.append(submission)
        random_sub = random.choice(all_subs)
        await ctx.channel.send(random_sub.url)

    @commands.command(aliases=["geckos", "GECKOS", "Lizard", "lizard", "lizards", "Lizards", "Gecko", "GECKO"], brief="r/geckos")
    async def gecko(self, ctx):
        second_rnd_int = random.randint(1, 15)
        if second_rnd_int <= 7:
            subreddit = await reddit.subreddit("geckos")
            all_subs = []
            async for submission in subreddit.hot(limit=100):
                all_subs.append(submission)
        else:
            subreddit = await reddit.subreddit("leopardgeckos")
            all_subs = []
            async for submission in subreddit.hot(limit=100):
                all_subs.append(submission)

        random_sub = random.choice(all_subs)
        await ctx.channel.send(random_sub.url)

    @commands.command(aliases=["Monkey", "Monkas", "monkas", "monka", "Monka"], brief="r/monkeys")
    async def monkey(self, ctx):
        subreddit = await reddit.subreddit("monkeys")
        all_subs = []
        async for submission in subreddit.hot(limit=100):
            all_subs.append(submission)
        random_sub = random.choice(all_subs)
        await ctx.channel.send(random_sub.url)

    @commands.command(aliases=["Coon"], brief="r/trashpandas")
    async def coon(self, ctx):
        if random.randint(0, 50) == 1:
            await ctx.channel.send(file=discord.File(f"{IMGPATH}SPOILER_.mp4"))
        else:
            subreddit = await reddit.subreddit("trashpandas")
            all_subs = []
            async for submission in subreddit.hot(limit=100):
                all_subs.append(submission)
            random_sub = random.choice(all_subs)
            await ctx.channel.send(random_sub.url)

    @commands.command(aliases=["Anos"], brief="Perfectly Balanced")
    async def anos(self, ctx):
        gay_thanos_list = [f"{IMGPATH}thanos1.jpg",
                           f"{IMGPATH}thanos2.jpg"]
        await ctx.channel.send(file=discord.File(random.choice(gay_thanos_list)), delete_after=1.5)

    @commands.command(aliases=["Thanos"], brief="Purple man")
    async def thanos(self, ctx):
        random_thanos_interger = random.randint(1, 100)
        if random.randint(1, 100) < 99:
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
            gay_thanos_list = [f"{IMGPATH}thanos1.jpg",
                               f"{IMGPATH}thanos2.jpg"]
            await ctx.channel.send(file=discord.File(random.choice(gay_thanos_list)))

    @commands.command(aliases=["Pingu", "Pingus", "pingus"], brief="Noot Noot")
    async def pingu(self, ctx):
        pingu_list = [f"{IMGPATH}pingu1.gif",
                      f"{IMGPATH}pingu2.gif",
                      f"{IMGPATH}pingu3.gif",
                      f"{IMGPATH}pingu4.gif",
                      f"{IMGPATH}pingu5.gif"]
        await ctx.channel.send(file=discord.File(random.choice(pingu_list)))

    @commands.command(aliases=["Bobin"], brief="handsome man")
    async def bobin(self, ctx):
        random_int = random.randint(1, 3)
        second_rnd_int = random.randint(1, 50)
        if second_rnd_int == 1:
            await ctx.channel.send(file=discord.File(f"{IMGPATH}dont.jpg"))
        else:
            if random_int == 3:
                await ctx.channel.send(file=discord.File(f"{IMGPATH}bobin.jpg"))
            else:
                embedthing = discord.Embed(
                    title="Bobin is Robin:", description="", color=0x1F5F9C)
                embedthing.add_field(
                    name=(r"https://www.twitch.tv/bobinhdv"), value=(f"😊"), inline=False)
                embedthing.add_field(
                    name=(r"https://twitter.com/BobinHDv"), value=(f"😊"), inline=False)
                embedthing.add_field(
                    name=(r"https://www.instagram.com/brewing_stand/"), value=(f"😊"), inline=False)
                await ctx.send(embed=embedthing, delete_after=600)

    @commands.command(aliases=["Topgun"], brief="more handsome man")
    async def topgun(self, ctx):
        topguns_list = [f"{IMGPATH}Topgun4.jpg",
                        f"{IMGPATH}Topgun3.jpg",
                        f"{IMGPATH}Topgun2.png",
                        f"{IMGPATH}Topgun1.png"]
        if random.randint(1, 20) == 1:
            await ctx.channel.send(file=discord.File(random.choice(topguns_list)))
        else:
            subreddit = await reddit.subreddit("tankporn")
            all_subs = []
            async for submission in subreddit.hot(limit=100):
                all_subs.append(submission)
            random_sub = random.choice(all_subs)
            await ctx.channel.send(random_sub.url)

    @commands.command(aliases=["Traps", "Chickswithdicks", "chickswithdicks", "harvey", "Harvey"], brief="😳")
    async def traps(self, ctx):
        if random.randint(1, 2) == 1:
            subreddit = await reddit.subreddit("traps")
            all_subs = []
            async for submission in subreddit.hot(limit=100):
                all_subs.append(submission)
            random_sub = random.choice(all_subs)
            await ctx.channel.send(random_sub.url, delete_after=5)
            await ctx.message.delete(delay=3)
        else:
            subreddit = await reddit.subreddit("Animetrapss")
            all_subs = []
            async for submission in subreddit.hot(limit=100):
                all_subs.append(submission)
            random_sub = random.choice(all_subs)
            await ctx.channel.send(random_sub.url, delete_after=5)
            await ctx.message.delete(delay=3)

    @commands.command(aliases=["Vygas"], brief="r/kanye west")
    async def vygas(self, ctx):
        chance = random.randint(1, 3)
        if chance == 1:
            await ctx.channel.send(file=discord.File(f"{IMGPATH}god.gif"))
        else:
            await ctx.channel.send(file=discord.File(f"{IMGPATH}vygas1.png"))

    @commands.command(aliases=["Josh", "JOSH"], brief="Alex?")
    async def josh(self, ctx):
        if random.randint(1, 5) == 1:
            await ctx.channel.send("Likes Feet, like really likes feet🙄")
        else:
            josh_list = [f"{IMGPATH}feet1.jpg",
                         f"{IMGPATH}feet2.jpg",
                         f"{IMGPATH}feet3.jpg"]
            josh_pick = random.choice(josh_list)
            await ctx.channel.send(file=discord.File(josh_pick))
            await ctx.channel.send("Feeling hot under the collar josh?")

    @commands.command(aliases=["Alex", "Alan", "alan", "Alek", "alek"], brief="Josh?")
    async def alex(self, ctx):
        if random.randint(1, 2) == 1:
            await ctx.channel.send(file=discord.File(f"{IMGPATH}Alek.jpg"))
        else:
            await ctx.channel.send(file=discord.File(f"{IMGPATH}Josh.jpg"))
            await ctx.channel.send("Same person right?")
            await ctx.message.add_reaction("🤷‍♂️")

    @commands.command(aliases=["Dom"], brief="hes attractive")
    async def dom(self, ctx):
        await ctx.channel.send(file=discord.File(f"{IMGPATH}Dom.jpg"))
        await ctx.message.add_reaction("😳")

    @commands.command(aliases=["River"], brief="the best german I know second to only the funny one with a moustache")
    async def river(self, ctx):
        random_int = random.randint(1, 3)
        if random_int == 1:
            await ctx.channel.send("SIEG HEIL")
        elif random_int == 2:
            await ctx.channel.send(file=discord.File(f"{IMGPATH}Hitler.jpg"))
        elif random_int == 3:
            await ctx.channel.send(file=discord.File(f"{IMGPATH}heil.gif"))

    @commands.command(aliases=["Sam"], brief="has killed a man")
    async def sam(self, ctx):
        await ctx.channel.send(file=discord.File(f"{IMGPATH}goblin.jpg"))

    @commands.command(aliases=["Scary"], brief="*jumpscare*")
    async def scary(self, ctx):
        await ctx.channel.send(file=discord.File(f"{IMGPATH}scary.gif"))

    @commands.command(aliases=["Gay"], brief="😳")
    async def gay(self, ctx):
        random_gay_guy = [f"{IMGPATH}Alek.jpg",
                          f"{IMGPATH}bobin.jpg",
                          f"{IMGPATH}jake.jpg",
                          f"{IMGPATH}Josh.jpg",
                          f"{IMGPATH}sam2.jpeg"]
        choice = random.choice(random_gay_guy)
        await ctx.channel.send(file=discord.File(choice))

    @commands.command(aliases=["Noman", "noman", "cats", "Cat", "Cats", "CATS", "CAT"], brief="sexy anime cats or just cats")
    async def cat(self, ctx):
        second_random_int = random.randint(1, 10)
        if second_random_int <= 6:
            subreddit = await reddit.subreddit("cats")
            all_subs = []
            async for submission in subreddit.hot(limit=100):
                all_subs.append(submission)
            random_sub = random.choice(all_subs)
            await ctx.channel.send(random_sub.url)
        else:
            subreddit = await reddit.subreddit("nekomimi")
            all_subs = []
            async for submission in subreddit.hot(limit=100):
                all_subs.append(submission)
            random_sub = random.choice(all_subs)
            await ctx.channel.send(random_sub.url, delete_after=10)

    @commands.command(aliases=["Godisdead"], brief="idk")
    async def godisdead(self, ctx):
        embedthing = discord.Embed(title="God is dead. God remains dead. And we have killed him. How shall we comfort ourselves, the murderers of all murderers? What was holiest and mightiest of all that the world has yet owned has bled to death under our knives: who will wipe this blood off us?", description="", color=0x1F5F9C)
        await ctx.send(embed=embedthing, delete_after=600)

    @commands.command(aliases=["Louis"], brief="The best command")
    async def louis(self, ctx):
        img = random.choice(self.louis_list)
        await ctx.send(file=discord.File(img))

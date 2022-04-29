import spotipy, discord, youtube_dl, json
import youtubesearchpython as yts

from discord.ext import commands
from random import choice
from asyncio import sleep
from GandalfBotPaths import *

SPOTIPY_CLIENT_ID = loaded_json["SPOTIPY_CLIENT_ID"]
SPOTIPY_CLIENT_SECRET = loaded_json["SPOTIPY_CLIENT_SECRET"]
sp = spotipy.Spotify(client_credentials_manager=spotipy.oauth2.SpotifyClientCredentials(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET))

ytdl_format_options = {
    "format": "bestaudio/best",
    "extractaudio": True,
    "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
    "restrictfilenames": True,
    "yesplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": True,
    "logtostderr": False,
    "quiet": True,
    "default_search": "auto",
    "source_address": "0.0.0.0",
    "cookiefile": COOKIE_PATH,
}

ffmpeg_options = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -nostdin",
    'options': '-vn -threads 1'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class Video():
    def __init__(self, url):
        video_search = yts.VideosSearch(url, limit=1)
        video = video_search.result()
        result = video["result"]
        
        for i in result:
            self.title = i["title"]
            self.url = i["link"]
            
            self.duration = i["duration"]
            for t in i["thumbnails"]:
                self.thumbnail = t["url"]


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
    async def from_url(cls, url, *, stream=False):
        data = ytdl.extract_info(url, download=not stream)
        data = ytdl.extract_info(url, download=not stream)

        if 'entries' in data:
            data = data['entries'][0]

        try:
            filename = data['url'] if stream else ytdl.prepare_filename(data)
            return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
        except Exception as E:
            write_error(E)
            print(E)
            return -1


class Music(commands.Cog):
    def __init__(self, client):
        self.disconnect_timer_check = False
        self.loop = False
        self.loop_url: str
        self.queue: list = []
        self.visual_queue: list = []
        self.counter = 0
        self.client = client
        self.playing: str
        self.weeb_list = ["Caramella Girls - Caramelldansen",
                          "Baka Mitai",
                          "Angel Beats! - Opening 1",
                          "Attack on Titan Opening theme 1",
                          "Running in the 90's",
                          "Cowboy Bebop – Opening Theme – Tank",
                          "Initial D - Deja Vu",
                          "Neon Genesis Evangelion(A Cruel Angel's Thesis)",
                          "Manuel - Gas Gas Gas",
                          "JoJo's Bizarre Adventure Opening 1 Full SONO CHI NO SADAME",
                          "https://www.youtube.com/watch?v=UxM5UgpXYM4",
                          "One Punch Man - Opening 1: The Hero!!",
                          "Ievan Polkka x Fubuki",
                          "Im. Scatman fubuki",
                          "https://www.youtube.com/watch?v=uKxyLmbOc0Q",
                          "Hikaru Nara - Your Lie In April",
                          "LiSA - Crossing Field",
                          "Tokyo Ghoul - Unravel",
                          "https://www.youtube.com/watch?v=S1W93_J3MH8",
                          "Kill Me Baby ED(Full)",
                          "KANA-BOON - Silhouette",
                          "真夜中のドア/Stay With Me", 
                          "https://www.youtube.com/watch?v=DjUtmbZt8zc",
                          "https://www.youtube.com/watch?v=EtjQVqXUPHo",
                          "https://www.youtube.com/watch?v=LKP-vZvjbh8",
                          "https://www.youtube.com/watch?v=PbWFpzi8C94",
                          "https://www.youtube.com/watch?v=XIr8ZnpQEXM"]

    async def stuck_step_bro(self, safety):
        video = Video(safety)
        embed = discord.Embed(title="Cannot play. Sorry.", description="", color=0x1F5F9C)
        embed.add_field(name=(f"{video.title}"), value=(f"🐧"), inline=True)
        player = -1
        if self.queue != []:
            while player == -1:
                a = self.queue.pop(0)
                self.visual_queue.pop(0)
                player = await YTDLSource.from_url(a, stream=True)
                if player == -1:
                    video = Video(a)
                    embed.add_field(name=(f"{video.title}"), value=(f"🐧"), inline=True)
                    self.visual_queue.pop(0)
            #self.visual_queue.append(video.title)
            self.playing = video.title
        return player, embed

    async def check_queue(self, ctx):
        if ctx.voice_client:
            print("Checking queue")
            if self.loop == True:
                player = await YTDLSource.from_url(self.loop_url, stream=True)
                ctx.voice_client.play(
                    player, after=lambda e: self.client.loop.create_task(self.check_queue(ctx)))
                embed, minutes, seconds = await self.send_play_msg(player)
                time = minutes * 60 + seconds
                await ctx.send(embed=embed, delete_after=time)
            else:
                if self.queue != []:
                    safety = self.queue.pop(0)
                    player = await YTDLSource.from_url(safety, stream=True)
                    if player == -1:
                        player, embed = await self.stuck_step_bro(safety)
                        await ctx.send(embed=embed, delete_after=20)

                    self.playing = self.visual_queue.pop(0)
                    try:
                        ctx.voice_client.play(player, after=lambda e: self.client.loop.create_task(self.check_queue(ctx)))
                        embed, minutes, seconds = await self.send_play_msg(player)
                        time = minutes * 60 + seconds
                        await ctx.send(embed=embed, delete_after=time)
                        self.loop_url = player.url
                    except Exception as e:
                        print(e)
                        write_error(e)
                        try:
                            query = f"{SONG_PATH}noise.mp3"
                            player = discord.PCMVolumeTransformer(
                                discord.FFmpegPCMAudio(query))
                            ctx.voice_client.play(
                                player, after=lambda e: self.client.loop.create_task(self.check_queue(ctx)))
                        except Exception as e:
                            print(e)
                            write_error(e)
                            pass
                else:
                    self.playing = ""
                    self.queue.clear()
                    self.visual_queue.clear()
                    if self.disconnect_timer_check == False:
                        counter = 0
                        self.disconnect_timer_check = True
                        while True:
                            await sleep(1)
                            counter += 1
                            if ctx.voice_client.is_playing() == False:
                                if counter == 1800:
                                    await ctx.voice_client.disconnect()
                                    self.disconnect_timer_check = False
                                    break
                            else:
                                self.disconnect_timer_check = False
                                return


    @commands.command(aliases=["Leave", "L", "l", "fuckoff", "Fuckoff", "quit"], brief="leave vc and cleares the queue")
    async def leave(self, ctx):
        try:
            await ctx.voice_client.disconnect()
            self.queue.clear()
            self.visual_queue.clear()
            await ctx.message.add_reaction("😭")
        except AttributeError:
            embed = discord.Embed(
                title="Nothing To Leave", description="", color=0x1F5F9C)
            await ctx.send(embed=embed, delete_after=600)

    @commands.command(aliases=["Pause"], brief="pause the song")
    async def pause(self, ctx):
        vc = ctx.voice_client
        if not vc or not vc.is_connected():
            embed = discord.Embed(
                title="Cant Pause Nuttin", description="", color=0x1F5F9C)
            await ctx.send(embed)
        else:
            ctx.voice_client.pause()
            await ctx.message.add_reaction('⏯')

    @commands.command(aliases=["Resume"], brief="resume the song")
    async def resume(self, ctx):
        vc = ctx.voice_client
        if not vc or not vc.is_connected():
            embed = discord.Embed(
                title="Cant Remove Nuttin", description="", color=0x1F5F9C)
            await ctx.send(embed)
        else:
            ctx.voice_client.resume()
            await ctx.message.add_reaction('⏯')

    @commands.command(aliases=["Stop"], brief="Clear the queue and stop whats playing")
    async def stop(self, ctx):
        try:
            voice_client = ctx.voice_client
            voice_client.stop()
            self.queue.clear()
            self.visual_queue.clear()
            self.loop = False
            self.loop_url = ""
            await ctx.message.add_reaction("👌")
        except AttributeError:
            embed = discord.Embed(
                title="Cant Stop what aint playing bitch!", description="", color=0x1F5F9C)
            await ctx.send(embed=embed, delete_after=600)

    async def send_play_msg(self, player):
        embed = discord.Embed(title="Playing: ", description="", color=0x1F5F9C)
        embed.add_field(name=(f"{player.title}"), value=(f"🐧"), inline=True)
        if player.duration != None:
            time_of_song = player.duration
            try:
                minutes, seconds = divmod(time_of_song, 60)
                embed.add_field(name=(f"Duration: "), value=(f"{minutes} minutes, {seconds} seconds"))
            except TypeError as E:
                minutes, seconds = player.duration.split(":")
                embed.add_field(name=(f"Duration: "), value=(f"{minutes} minutes, {seconds} seconds"))
            embed.add_field(name="URL: ", value=(player.url))
            embed.set_thumbnail(url=(player.thumbnail))
        if self.loop == True:
            embed.set_footer(text="LOOPED:♾️")
        return embed, minutes, seconds

    async def send_queued_msg(self, url):
        g = Video(url)
        embed = discord.Embed(
            title="Queued: ", description="", color=0x1F5F9C)
        embed.add_field(name=(f"{g.title}"), value=(f"🐧"), inline=True)
        minutes, seconds = g.duration.split(":", 1)
        embed.add_field(name=(f"Duration: "), value=(
            f"{minutes} minutes, {seconds} seconds"))
        embed.add_field(name="URL: ", value=(g.url))
        embed.set_thumbnail(url=(g.thumbnail))
        return embed, g.url, g.title

    async def playlist(self, url):
        error = False
        results = sp.user_playlist(user="", playlist_id=url)

        track_list = []
        # For each track in the playlist.
        for i in results["tracks"]["items"]:
            # In case there's only one artist.
            try:
                if (i["track"]["artists"].__len__() == 1):
                    # We add trackName - artist.
                    track_list.append(i["track"]["name"] + " - " +
                                    i["track"]["artists"][0]["name"])
                else:
                    nameString = ""
                    # For each artist in the track.
                    for index, b in enumerate(i["track"]["artists"]):
                        nameString += (b["name"])
                        # If it isn't the last artist.
                        if (i["track"]["artists"].__len__() - 1 != index):
                            nameString += ", "
                    # Adding the track to the list.
                    track_list.append(i["track"]["name"] + " - " + nameString)
            except TypeError as E:
                write_error(E)
                error = True
    
        first_song = track_list.pop(0)
        self.queue.extend(track_list)
        self.visual_queue.extend(track_list)
        if error:
            embed = discord.Embed(title=f"Queued:{len(track_list)}\n The was an error playing 1 or more songs :(", description="", color=0x1F5F9C)
        else:
            embed = discord.Embed(title=f"Queued:{len(track_list)}", description="", color=0x1F5F9C)
        return(first_song, embed)

    async def spot(self, url):
        result = sp.track(url)
        artists = result["artists"]
        for i in artists:
            artist = i["name"]
        title_artist = result["name"] + " " + artist
        return title_artist

    async def yt_playlist(self, url):
        before, after = url.split("watch?")
        dog, list = after.split("&", 1)
        url = f"{before}playlist?{list}"
        playlist_videos = yts.Playlist.getVideos(url)
        for i in playlist_videos["videos"]:
            self.queue.append("https://www.youtube.com/watch?v=" + i["id"])
            self.visual_queue.append(i["title"])
        return self.queue.pop(0)

    @commands.command(aliases=["P", "p", "Play", "PLAY"], brief="play a song!")
    async def play(self, ctx, *, url):
        play_list_bool = False
        if ctx.author.voice:
            if "playlist" in url and "spotify" in url:
                play_list_bool = True
                url, embed = await self.playlist(url)
            elif "spotify" in url:
                url = await self.spot(url)

            if "list" in url and "youtube" in url:
                url = await self.yt_playlist(url)

            if ctx.voice_client.is_playing() == False:
                player = await YTDLSource.from_url(url, stream=True)
                if player == -1:
                    embed = discord.Embed(title="Cannot play. Sorry.", description = "", color=0x1F5F9C)
                    embed.add_field(
                        name=(f"{Video(url).title}"), value=("🐧"), inline=True)
                    await ctx.send(embed=embed, delete_after=20)
                    self.playing = ""
                else:
                    ctx.voice_client.play(player, after=lambda e: self.client.loop.create_task(self.check_queue(ctx)))
                    self.playing = player.title
                    self.loop_url = player.url
                    print(player.url)
                    embed, minutes, seconds = await self.send_play_msg(player)
                    await ctx.send(embed=embed, delete_after=player.duration)
            else:
                if play_list_bool == True:
                    await ctx.send(embed=embed, delete_after=10)
                else:
                    embed, url, title = await self.send_queued_msg(url)
                    await ctx.send(embed=embed, delete_after=10)
                    print(url)
                    self.queue.append(url)
                    self.visual_queue.append(title)

    @play.before_invoke
    async def check(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect(reconnect=False, timeout=5)
            else:
                embed = discord.Embed(
                    title="You are not connected to a voice channel.", description="", color=0x1F5F9C)
                await ctx.send(embed=embed, delete_after=120)

    @commands.command(aliases=["Loop", "unloop"], brief="loop the song, stopped with .loop again")
    async def loop(self, ctx):
        self.loop = not(self.loop)
        await ctx.message.add_reaction("♾️")

    @commands.command(aliases=["S", "s", "Skip"], brief="skip the current song")
    async def skip(self, ctx):
        vc = ctx.voice_client
        if not vc or not vc.is_connected():
            embed = discord.Embed(
                title="Cant skip nothing", description="", color=0x1F5F9C)
            await ctx.send(embed=embed, delete_after=20)
        else:
            embed = discord.Embed(
                title=f"skipped: {self.playing} ", description="", color=0x1F5F9C)
            await ctx.send(embed=embed, delete_after=20)
            await ctx.message.add_reaction("⏩")
            vc.stop()

    @commands.command(aliases=["e", "Eel", "EEL"], brief="🐟")
    async def eel(self, ctx):
        if ctx.author.voice:
            await ctx.message.add_reaction("🐟")
            voice_client = ctx.voice_client
            voice_client.stop()
            self.queue.clear()
            query = f"{SONG_PATH}eel.mp3"
            player = discord.PCMVolumeTransformer(
                discord.FFmpegPCMAudio(query))
            ctx.voice_client.play(
                player, after=lambda e: self.client.loop.create_task(self.check_queue(ctx)))

    @eel.before_invoke
    async def eel_check(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect(reconnect=False, timeout=5)
            else:
                embed = discord.Embed(
                    title="You are not connected to a voice channel.", description="", color=0x1F5F9C)
                await ctx.send(embed=embed, delete_after=120)

    @commands.command(aliases=["chez", "CHEESE", "cheez"], brief="🐟")
    async def cheese(self, ctx):
        if ctx.author.voice:
            await ctx.message.add_reaction("🧀")
            voice_client = ctx.voice_client
            voice_client.stop()
            self.queue.clear()
            query = f"{SONG_PATH}cheese.mp4"
            player = discord.PCMVolumeTransformer(
                discord.FFmpegPCMAudio(query))
            ctx.voice_client.play(
                player, after=lambda e: self.client.loop.create_task(self.check_queue(ctx)))

    @cheese.before_invoke
    async def cheese_check(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect(reconnect=False, timeout=5)
            else:
                embed = discord.Embed(
                    title="You are not connected to a voice channel.", description="", color=0x1F5F9C)
                await ctx.send(embed=embed, delete_after=120)

    @commands.command(aliases=["Q", "q"], brief="list what items are in the queue and what position there are at")
    async def queue(self, ctx):
        self.counter = 0
        if not(self.queue):
            embed = discord.Embed(
                title="Nothing In Queue: ", description="", color=0x1F5F9C)
            if self.playing:
                embed = discord.Embed(
                    title="In Queue:", description=f"PLAYING: {self.counter}: {self.playing}", color=0x1F5F9C)
            await ctx.send(embed=embed, delete_after=300)
        else:
            embedVar = discord.Embed(
                title="In Queue:", description=f"PLAYING: {self.counter}: {self.playing}", color=0x1F5F9C)
            for i in self.visual_queue:
                self.counter = self.counter + 1
                embedVar.add_field(name=(f"{self.counter}:"), value=(i), inline=False)
                if self.counter == 10:
                    break

            msg = await ctx.send(embed=embedVar, delete_after=600)
            await msg.add_reaction('⏪')
            await msg.add_reaction('⏩')

        @self.client.event
        async def on_reaction_add(reaction, user):
            print(self.counter)
            if user.bot:
                return
            if str(reaction) == '⏪':
                if self.counter >= 20:
                    self.counter -= 20
                    embedVar1 = discord.Embed(
                        title="In Queue:", description=f"PLAYING: {0}: {self.playing}", color=0x1F5F9C)
                    for i in self.visual_queue[self.counter:]:
                        self.counter += 1
                        embedVar1.add_field(
                            name=(f"{self.counter}:"), value=(i), inline=False)
                        if self.counter % 10 == 0:
                            break
                    await msg.edit(embed=embedVar1, delete_after=300)
            elif str(reaction) == '⏩':
                if self.counter < len(self.queue) - 1:
                    embedVar2 = discord.Embed(
                        title="In Queue:", description=f"PLAYING: {0}: {self.playing}", color=0x1F5F9C)
                    for i in self.visual_queue[self.counter:]:
                        self.counter += 1
                        embedVar2.add_field(
                            name=(f"{self.counter}:"), value=(i), inline=False)
                        if self.counter % 10 == 0:
                            break
                        if self.counter == len(self.queue):
                            if self.counter % 10 != 0:
                                count = abs(self.counter % 10 -10)
                                self.counter += count
                                while count != 0:
                                    embedVar2.add_field(
                                        name=(f"{self.counter}"), value=(" 🐧 "), inline=False)
                                    count -= 1
                                    
                    await msg.edit(embed=embedVar2, delete_after=300)

    @commands.command(aliases=["Remove"], brief="remove a song at a certain position in the queue")
    async def remove(self, ctx, index: int):
        if len(self.queue) == 0:
            await ctx.send("Nothing in queue", delete_after=3)
            await ctx.message.delete(delay=3)
        elif index == 0:
            await self.skip(ctx)
        elif index > len(self.queue):
            await ctx.send(f"The queue is only {len(self.queue)} long", delete_after=5)
            await ctx.message.delete(delay=3)
        elif index <= len(self.queue):
            index -= 1
            print(len(self.queue))
            embed = discord.Embed(title=f"Removed: {self.visual_queue[index]} at position {index + 1}", description="", color=0x1F5F9C)
            await ctx.send(embed=embed, delete_after=20)
            del self.queue[index]
            del self.visual_queue[index]

    async def list_run_out(self):
        second_list = ["Caramella Girls - Caramelldansen",
                        "Baka Mitai",
                        "Angel Beats! - Opening 1",
                        "Attack on Titan Opening theme 1",
                        "Running in the 90's",
                        "Cowboy Bebop – Opening Theme – Tank",
                        "Initial D - Deja Vu",
                        "Neon Genesis Evangelion(A Cruel Angel's Thesis)",
                        "Manuel - Gas Gas Gas",
                        "https://www.youtube.com/watch?v=XIr8ZnpQEXM",
                        "https://www.youtube.com/watch?v=EP62gl-sj2I",
                        "https://www.youtube.com/watch?v=UxM5UgpXYM4",
                        "Im. Scatman fubuki",
                        "https://www.youtube.com/watch?v=uKxyLmbOc0Q",
                        "Hikaru Nara - Your Lie In April",
                        "LiSA - Crossing Field",
                        "Tokyo Ghoul - Unravel",
                        "https://www.youtube.com/watch?v=S1W93_J3MH8",
                        "Kill Me Baby ED(Full)",
                        "Duvet Boa"]
        self.weeb_list.extend(second_list)
        query = choice(self.weeb_list)
        self.weeb_list.remove(query)
        return query

    @commands.command(aliases=["Weeb", "UwU", "uwu", "Uwu", "uwU", "OwO", "owo", "Owo", "owO"])
    async def weeb(self, ctx):
        if ctx.voice_client.is_playing() == False:
            if self.weeb_list != []:
                query = choice(self.weeb_list)
                self.weeb_list.remove(query)

                player = await YTDLSource.from_url(query, stream=True)
                ctx.voice_client.play(player, after=lambda e: self.client.loop.create_task(self.check_queue(ctx)))
                self.playing = player.title
                self.loop_url = player.url

                embed, minutes, seconds = await self.send_play_msg(player)
                await ctx.send(embed=embed, delete_after=player.duration)
            else:
                query = await self.list_run_out()

                player = await YTDLSource.from_url(query, stream=True)
                ctx.voice_client.play(player, after=lambda e: self.client.loop.create_task(self.check_queue(ctx)))
                self.playing = player.title
                self.loop_url = player.url

                embed, minutes, seconds = await self.send_play_msg(player)
                await ctx.send(embed=embed, delete_after=player.duration)
        else:
            if self.weeb_list != []:
                query = choice(self.weeb_list)
                self.weeb_list.remove(query)

                embed, url, title = await self.send_queued_msg(query)
                await ctx.send(embed=embed, delete_after=10)

                self.queue.append(url)
                self.visual_queue.append(title)

            else:
                query = await self.list_run_out()

                embed, url = await self.send_queued_msg(query)
                await ctx.send(embed=embed, delete_after=10)

                self.queue.append(url)
                self.visual_queue.append(title)

    @weeb.before_invoke
    async def checkz(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect(reconnect=False, timeout=5)
            else:
                embed = discord.Embed(
                    title="You are not connected to a voice channel.", description="", color=0x1F5F9C)
                await ctx.send(embed=embed, delete_after=30) 

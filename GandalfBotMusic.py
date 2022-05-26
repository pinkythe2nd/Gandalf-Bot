import spotipy, discord, youtube_dl
import youtubesearchpython as yts
from discord.ext import commands
from asyncio import sleep
from GandalfBotPaths import *
from random import shuffle, choice

SPOTIPY_CLIENT_ID = loaded_json["SPOTIPY_CLIENT_ID"]
SPOTIPY_CLIENT_SECRET = loaded_json["SPOTIPY_CLIENT_SECRET"]
sp = spotipy.Spotify(client_credentials_manager=spotipy.oauth2.SpotifyClientCredentials(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET))

ytdl_format_options = {
    "format": "bestaudio",
    "extractaudio": True,
    "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    #"ignoreerrors": True,
    #"logtostderr": False,
    #"quiet": True,
    "default_search": "auto",
    "source_address": "0.0.0.0",
    "cookiefile": COOKIE_PATH,
    "no-cache-dir": True,
    "abort-on-error": False,
}

ffmpeg_options = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -nostdin",
    'options': '-vn -threads 1'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class Video():
    """A Class to get details of a youtube video without using youtube-dl"""
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
    """extracts info from a url via youtube-dl"""
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
        """takes in a url, returns a ffmpeg streamable audio source known in the code as a player"""
        data = ytdl.extract_info(url, download=not stream)

        if 'entries' in data:
            data = data['entries'][0]

        try:
            filename = data['url'] if stream else ytdl.prepare_filename(data)
            return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
        except youtube_dl.utils.ExtractorError as E:
            count = 0
            while count < 3:
                try:
                    filename = data['url'] if stream else ytdl.prepare_filename(data)
                    break
                except youtube_dl.utils.ExtractorError as E:
                    pass
            return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
        except Exception as E:
            write_error(E)
            return -1


class Music(commands.Cog):
    """A class containg all the music related commands and helper functions for those commands"""
    def __init__(self, client):
        self.disconnect_timer_check = False
        self._loop = False
        self._loop_url: str = ""
        self._queue: list = [] #list of tuples [0] is the url [1] is the title
        self.counter = 0
        self.client = client
        self.playing: str = ""
        self.player = None

    async def stuck(self, safety):
        """takes in a string, returns a player and a embed"""
        print("WHEN DOES THIS HAPPEN! IF EVER?!")
        embed = discord.Embed(title="Cannot play. Sorry.", description="", color=0x1F5F9C) 
        embed.add_field(name=(f"{safety[1]}"), value=(f"🐧"), inline=True)
        self.player = -1
        if self._queue != []:
            while self.player == -1:
                next_song = self._queue.pop(0)[0]
                self.player = await YTDLSource.from_url(next_song, stream=True)
                if self.player == -1:
                    embed.add_field(name=(f"{next_song[1]}"), value=(f"🐧"), inline=True)
        return self.player, embed

    async def check_queue(self, ctx):
        """Plays the next song in the queue and sets 'playable' to the new song playing"""
        if ctx.voice_client:
            if self._loop == True:
                self.player = await YTDLSource.from_url(self._loop_url, stream=True)
                ctx.voice_client.play(
                    self.player, after=lambda e: self.client.loop.create_task(self.check_queue(ctx)))
                embed, minutes, seconds = await self.send_play_msg()
                time = minutes * 60 + seconds
                await ctx.send(embed=embed, delete_after=time)
            else:
                if self._queue != []:
                    safety = self._queue.pop(0)
                    self.player = await YTDLSource.from_url(safety[0], stream=True)
                    if self.player == -1:
                        self.player, embed = await self.stuck(safety)
                        await ctx.send(embed=embed, delete_after=20)

                    self.playing = safety[1]
                    ctx.voice_client.play(self.player, after=lambda e: self.client.loop.create_task(self.check_queue(ctx)))
                    embed, minutes, seconds = await self.send_play_msg()
                    time = minutes * 60 + seconds
                    await ctx.send(embed=embed, delete_after=time)
                    self._loop_url = self.player.url
                else:
                    self.playing = ""
                    self._queue.clear()
                    if self.disconnect_timer_check == False:
                        timer = 0
                        self.disconnect_timer_check = True
                        while True:
                            await sleep(1)
                            timer += 1
                            if ctx.voice_client.is_playing() == False:
                                if timer == 1800:
                                    await ctx.voice_client.disconnect()
                                    self.disconnect_timer_check = False
                                    break
                            else:
                                self.disconnect_timer_check = False
                                return

    @commands.command(aliases=["Leave", "L", "l"], brief="leave vc and clears the queue")
    async def leave(self, ctx):
        """leaves a voice chat"""
        try:
            await ctx.voice_client.disconnect()
            self._queue.clear()
            await ctx.message.add_reaction("😭")
        except AttributeError:
            embed = discord.Embed(
                title="Not connected to a voice chat", description="", color=0x1F5F9C)
            await ctx.send(embed=embed, delete_after=600)

    @commands.command(aliases=["Join", "J", "j"], brief="Joins a vc, if already in a vc moves to the users vc")
    async def join(self, ctx):
        """Joins a voice chat or moves to a voice chat"""
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect(reconnect=False, timeout=5)
                await ctx.message.add_reaction('👍')
            else:
                embed = discord.Embed(
                    title="You are not connected to a voice channel.", description="", color=0x1F5F9C)
                await ctx.send(embed=embed, delete_after=120)
        else:
            await ctx.voice_client.move_to(ctx.author.voice.channel)
            await ctx.message.add_reaction('👍')

    @commands.command(aliases=["Pause"], brief="pause the song")
    async def pause(self, ctx):
        """pauses the currently playing song"""
        vc = ctx.voice_client
        if not vc or not vc.is_connected():
            embed = discord.Embed(
                title="Nothings playing", description="", color=0x1F5F9C)
            await ctx.send(embed)
        else:
            ctx.voice_client.pause()
            await ctx.message.add_reaction('⏯')

    @commands.command(aliases=["Resume"], brief="resume the song")
    async def resume(self, ctx):
        """resumes the current playing song"""
        vc = ctx.voice_client
        if not vc or not vc.is_connected():
            embed = discord.Embed(
                title="Nothings playing", description="", color=0x1F5F9C)
            await ctx.send(embed)
        else:
            ctx.voice_client.resume()
            await ctx.message.add_reaction('⏯')

    @commands.command(aliases=["Stop"], brief="Clear the queue and stop whats playing")
    async def stop(self, ctx):
        """stops whatevers playing and clears the entire queue"""
        try:
            voice_client = ctx.voice_client
            voice_client.stop()
            self._queue.clear()
            self._loop = False
            self._loop_url = ""
            await ctx.message.add_reaction("👌")
        except AttributeError:
            embed = discord.Embed(
                title="Nothings playing", description="", color=0x1F5F9C)
            await ctx.send(embed=embed, delete_after=600)

    @commands.command(aliases=["Volume", "VOLUME", "v", "V"], brief="sets the volume. Values between 0 and 100.")
    async def volume(self, ctx, vol: int):
        """adjusts the volume of the player"""
        if vol <= 0:
            await ctx.message.add_reaction("🔇")
        elif vol < 30 and vol >= 1:
            await ctx.message.add_reaction("🔈")
        elif vol < 75 and vol >= 30:
            await ctx.message.add_reaction("🔉")
        elif vol >= 75 and vol <= 100:
            await ctx.message.add_reaction("🔊")
        elif vol > 100:
            await ctx.message.add_reaction("📢")
        vol = vol / 100
        self.player.volume = vol

    async def send_play_msg(self):
        """takes in a player, returns a embed and two numbers, minutes and seconds"""
        embed = discord.Embed(title="Playing: ", description="", color=0x1F5F9C)
        embed.add_field(name=(f"{self.player.title}"), value=(f"🐧"), inline=True)
        if self.player.duration != None:
            time_of_song = self.player.duration
            try:
                minutes, seconds = divmod(time_of_song, 60)
                embed.add_field(name=(f"Duration: "), value=(f"{minutes} minutes, {seconds} seconds"))
            except TypeError as E:
                minutes, seconds = self.player.duration.split(":")
                embed.add_field(name=(f"Duration: "), value=(f"{minutes} minutes, {seconds} seconds"))
            embed.add_field(name="URL: ", value=(self.player.url))
            embed.set_thumbnail(url=(self.player.thumbnail))
        if self._loop == True:
            embed.set_footer(text="_looped:🔁")
        return embed, minutes, seconds

    async def send_queued_msg(self, url):
        """takes in a string, returns a embed and two strings, url and title"""
        g = Video(url)
        embed = discord.Embed(
            title="queued: ", description="", color=0x1F5F9C)
        embed.add_field(name=(f"{g.title}"), value=(f"🐧"), inline=True)
        minutes, seconds = g.duration.split(":", 1)
        embed.add_field(name=(f"Duration: "), value=(
            f"{minutes} minutes, {seconds} seconds"))
        embed.add_field(name="URL: ", value=(g.url))
        embed.set_thumbnail(url=(g.thumbnail))
        return embed, g.url, g.title

    async def album(self, url):
        """takes in a url, returns the first song in the album and a embed"""
        error = False
        results = sp.album_tracks(url)
        count = 0
        try: 
            for track in results['items']:
                count += 1
                artists = track["artists"]
                for i in artists:
                    artist = i["name"]
                title_artist = track["name"] + " " + artist
                self._queue.append((title_artist, track["name"]))
        except TypeError as E:
            count -= 1
            error = True

        if error:
            embed = discord.Embed(
                title=f"queued:{count}\n The was an error playing 1 or more songs :(", description="", color=0xFF0000)
        else:
            embed = discord.Embed(
                title=f"queued:{count}", description="", color=0x00FF00)

        return self._queue.pop(0)[0], embed

    def playlist_helper(self, tracks, count):
        """takes in a array, a number and two more arrays, track_list, track_list2. returns count, tracklist, tracklist2 and a boolean flag"""
        error = False
        for i in tracks["items"]:
            count += 1
            try:
                if (i["track"]["artists"].__len__() == 1):
                    self._queue.append(
                        (i["track"]["name"] + " - " + i["track"]["artists"][0]["name"], 
                        i["track"]["name"]))
                else:
                    nameString = ""
                    for index, b in enumerate(i["track"]["artists"]):
                        nameString += (b["name"])
                        if (i["track"]["artists"].__len__() - 1 != index):
                            nameString += ", "
                    self._queue.append(
                        (i["track"]["name"] + " - " + nameString, 
                        i["track"]["name"]))
            except TypeError as E:
                count -= 1
                write_error(E)
                error = True
        return count, error

    async def playlist(self, url):
        """takes in a url, returns a string and a embed"""
        error = False
        results = sp.user_playlist(user="", playlist_id=url)
        count = 0
        tracks = results["tracks"]
        while tracks["next"]:
            count, error = self.playlist_helper(tracks, count)
            tracks = sp.next(tracks)

        count, error = self.playlist_helper(tracks, count)

        if error:
            embed = discord.Embed(
                title=f"queued:{count}\n The was an error loading 1 or more songs :(", description="", color=0xFF0000)
        else:
            embed = discord.Embed(
                title=f"queued:{count}", description="", color=0x00FF00)

        print(self._queue[0][0])

        return self._queue.pop(0)[0], embed

    async def spot(self, url):
        """takes a string in, returns a string"""
        result = sp.track(url)
        artists = result["artists"]
        for i in artists:
            artist = i["name"]
        title_artist = result["name"] + " " + artist
        return title_artist

    async def yt_playlist(self, url):
        """takes in a url, returns the first song and a embed"""
        playlist = yts.Playlist(url)
        track_list = []
        track_list2 = []
        while playlist.hasMoreVideos:
            playlist.getNextVideos()
        for i in playlist.videos:
            self._queue.append(("https://www.youtube.com/watch?v=" + i["id"], i["title"]))
        embed = discord.Embed(title=f"queued:{len(playlist.videos)}", description="", color=0x00FF00)

        return self._queue.pop(0)[0], embed

    @commands.command(aliases=["P", "p", "Play", "PLAY"], brief="play a song!")
    async def play(self, ctx, *, url):
        """takes in a user input, creates a player, and plays it"""
        play_list_bool = False
        if ctx.author.voice:
            if "playlist" in url and "spotify" in url:
                play_list_bool = True
                embed1 = discord.Embed(
                    title="-- Spotify Playlist Loading! --", description="", color=0xFFA500)
                msg = await ctx.send(embed=embed1, delete_after=20)
                await msg.add_reaction("⌛")
                url, embed = await self.playlist(url)
                await msg.clear_reaction("⌛")
                await msg.edit(embed=embed, delete_after=20)
                await msg.add_reaction("✅")

            if "album" in url and "spotify" in url:
                play_list_bool = True
                embed1 = discord.Embed(
                    title="-- Spotify Album Loading! --", description="", color=0xFFA500)
                msg = await ctx.send(embed=embed1, delete_after=20)
                await msg.add_reaction("⌛")
                url, embed = await self.album(url)
                await msg.clear_reaction("⌛")
                await msg.edit(embed=embed, delete_after=20)
                await msg.add_reaction("✅")

            if "list" in url and "youtube" in url:
                play_list_bool = True
                embed1 = discord.Embed(
                    title="-- Youtube Playlist Readying! --", description="", color=0xFFA500)
                msg = await ctx.send(embed=embed1, delete_after=20)
                await msg.add_reaction("⌛")
                url, embed = await self.yt_playlist(url)
                await msg.clear_reaction("⌛")
                await msg.edit(embed=embed, delete_after=20)
                await msg.add_reaction("✅")

            if "spotify" in url:
                url = await self.spot(url)

            if ctx.voice_client.is_playing() == False:
                embed1 = discord.Embed(title="...Loading...", description="", color=0xFFA500)
                msg = await ctx.send(embed=embed1)
                await msg.add_reaction("⌛")
                self.player = await YTDLSource.from_url(url, stream=True)
                if self.player == -1:
                    await msg.clear_reaction("⌛")
                    embed = discord.Embed(title="Cannot play. Sorry.", description = "", color=0xFF0000)
                    embed.add_field(name=(f"{Video(url).title}"), value=("🐧"), inline=True)
                    await msg.edit(embed=embed, delete_after=20)
                    self.playing = ""
                else:
                    await msg.clear_reaction("⌛")
                    try:
                        """this try catch loop allows gandalf to leave while queueing a song and not break"""
                        ctx.voice_client.play(self.player, after=lambda e: self.client.loop.create_task(self.check_queue(ctx)))
                        self.playing = self.player.title
                        self._loop_url = self.player.url
                        embed, minutes, seconds = await self.send_play_msg()
                        await msg.edit(embed=embed, delete_after=self.player.duration)
                    except AttributeError:
                        await self.vc_check(ctx)
                        ctx.voice_client.play(self.player, after=lambda e: self.client.loop.create_task(self.check_queue(ctx)))
                        self.playing = self.player.title
                        self._loop_url = self.player.url
                        embed, minutes, seconds = await self.send_play_msg()
                        await msg.edit(embed=embed, delete_after=self.player.duration)
            else:
                if play_list_bool == True:
                    await ctx.send(embed=embed, delete_after=10)
                else:
                    embed, url, title = await self.send_queued_msg(url)
                    await ctx.send(embed=embed, delete_after=10)
                    self._queue.append((url, title))

    @play.before_invoke
    async def vc_check(self, ctx):
        """checks if the bot is connected before running the play command"""
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect(reconnect=False, timeout=5)
            else:
                embed = discord.Embed(
                    title="You are not connected to a voice channel.", description="", color=0x1F5F9C)
                await ctx.send(embed=embed, delete_after=120)

    @commands.command(aliases=["Shuffle", "SHUFFLE"], brief="Shuffles the queue")
    async def shuffle(self, ctx):
        """shuffles the queue"""
        await ctx.message.add_reaction("🔀")
        shuffle(self._queue)

    @commands.command(aliases=["Loop", "un_loop"], brief="loop the song, stopped with .loop again")
    async def loop(self, ctx):
        """loops the currently playing song"""
        self._loop = not(self._loop)
        await ctx.message.add_reaction("🔁")

    @commands.command(aliases=["S", "s", "Skip"], brief="skip the current song")
    async def skip(self, ctx):
        """stops the currently playing song and plays the next in the queue"""
        vc = ctx.voice_client
        if not vc or not vc.is_connected():
            embed = discord.Embed(
                title="Nothing to skip", description="", color=0x1F5F9C)
            await ctx.send(embed=embed, delete_after=20)
        else:
            embed = discord.Embed(
                title=f"skipped: {self.playing} ", description="", color=0x1F5F9C)
            await ctx.send(embed=embed, delete_after=20)
            await ctx.message.add_reaction("⏩")
            vc.stop()

    @commands.command(aliases=["Jump"], brief="Stops whatever is playing and jumps to a song in the queue")
    async def jump(self, ctx, index: int):
        """takes in a user input, skips the current playing song and plays the users input"""
        if len(self._queue) == 0:
            embed = discord.Embed(
                title="nothing in queue", description="", color=0x1F5F9C)
            await ctx.send(embed=embed, delete_after=5)
        elif index == 0:
            embed = discord.Embed(
                title="that song is already playing", description="", color=0x1F5F9C)
            await ctx.send(embed=embed, delete_after=5)
        elif index > len(self._queue):
            embed = discord.Embed(
                title=f"The queue is only {len(self._queue)} long", description="", color=0x1F5F9C)
            await ctx.send(embed=embed, delete_after=5)
        elif index <= len(self._queue):
            self._queue.insert(0, self._queue.pop(index-1))
            await self.skip(ctx)
            await ctx.message.add_reaction("🦘")


    @commands.command(aliases=["Remove"], brief="remove a song at a certain position in the queue")
    async def remove(self, ctx, index: int):
        """takes in a int, and removes the song at the index location"""
        if len(self._queue) == 0:
            await ctx.send("Nothing in queue", delete_after=3)
            await ctx.message.delete(delay=3)
        elif index == 0:
            await self.skip(ctx)
        elif index > len(self._queue):
            await ctx.send(f"The queue is only {len(self._queue)} long", delete_after=5)
            await ctx.message.delete(delay=3)
        elif index <= len(self._queue):
            index -= 1
            embed = discord.Embed(
                title=f"Removed: {self._queue[index][1]} at position {index + 1}", description="", color=0x1F5F9C)
            await ctx.send(embed=embed, delete_after=20)
            del self._queue[index]

    @commands.command(aliases=["Q", "q", "Queue", "QUEUE"], brief="list what items are in the queue and what position there are at")
    async def queue(self, ctx):
        """sends a embed of items in the queue"""
        self.counter = 0
        if not(self._queue):
            embed = discord.Embed(
                title="Nothing In queue: ", description="", color=0x1F5F9C)
            if self.playing:
                embed = discord.Embed(
                    title="In queue:", description=f"PLAYING: {self.counter}: {self.playing}", color=0x1F5F9C)
            await ctx.send(embed=embed, delete_after=300)
        else:
            embedVar = discord.Embed(
                title="In queue:", description=f"PLAYING: {self.counter}: {self.playing}", color=0x1F5F9C)
            for i in self._queue:
                self.counter = self.counter + 1
                embedVar.add_field(name=(f"{self.counter}:"), value=(i[1]), inline=False)
                if self.counter == 10:
                    break

            msg = await ctx.send(embed=embedVar, delete_after=600)
            await msg.add_reaction('⏪')
            await msg.add_reaction('⏩')

        @self.client.event
        async def on_reaction_add(reaction, user):
            """lets users manuver through the queue"""
            if user.bot:
                return
            if str(reaction) == '⏪':
                if self.counter >= 20:
                    self.counter -= 20
                    embedVar1 = discord.Embed(
                        title="In queue:", description=f"PLAYING: {0}: {self.playing}", color=0x1F5F9C)
                    for i in self._queue[self.counter:]:
                        self.counter += 1
                        embedVar1.add_field(
                            name=(f"{self.counter}:"), value=(i[1]), inline=False)
                        if self.counter % 10 == 0:
                            break
                    await msg.edit(embed=embedVar1, delete_after=300)
            elif str(reaction) == '⏩':
                if self.counter < len(self._queue) - 1:
                    embedVar2 = discord.Embed(
                        title="In queue:", description=f"PLAYING: {0}: {self.playing}", color=0x1F5F9C)
                    for i in self._queue[self.counter:]:
                        self.counter += 1
                        embedVar2.add_field(
                            name=(f"{self.counter}:"), value=(i[1]), inline=False)
                        if self.counter % 10 == 0:
                            break
                        if self.counter == len(self._queue):
                            if self.counter % 10 != 0:
                                count = abs(self.counter % 10 -10)
                                self.counter += count
                                while count != 0:
                                    embedVar2.add_field(
                                        name=(f"{self.counter}"), value=(" 🐧 "), inline=False)
                                    count -= 1
                                    
                    await msg.edit(embed=embedVar2, delete_after=300)

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

    @commands.command(aliases=["Weeb", "UwU", "uwu", "Uwu", "uwU", "OwO", "owo", "Owo", "owO"], brief="WEEEEBBB MUSSICCC")
    async def weeb(self, ctx):
        if ctx.voice_client.is_playing() == False:
            if self.weeb_list != []:
                query = choice(self.weeb_list)
                self.weeb_list.remove(query)

                self.player = await YTDLSource.from_url(query, stream=True)
                ctx.voice_client.play(self.player, after=lambda e: self.client.loop.create_task(self.check_queue(ctx)))
                self.playing = self.player.title
                self.loop_url = self.player.url

                embed, minutes, seconds = await self.send_play_msg()
                await ctx.send(embed=embed, delete_after=self.player.duration)
            else:
                query = await self.list_run_out()

                self.player = await YTDLSource.from_url(query, stream=True)
                ctx.voice_client.play(self.player, after=lambda e: self.client.loop.create_task(self.check_queue(ctx)))
                self.playing = self.player.title
                self.loop_url = self.player.url

                embed, minutes, seconds = await self.send_play_msg()
                await ctx.send(embed=embed, delete_after=self.player.duration)
        else:
            if self.weeb_list != []:
                query = choice(self.weeb_list)
                self.weeb_list.remove(query)

                embed, url, title = await self.send_queued_msg(query)
                await ctx.send(embed=embed, delete_after=10)

                self._queue.append((url, title))
            else:
                query = await self.list_run_out()

                embed, url = await self.send_queued_msg(query)
                await ctx.send(embed=embed, delete_after=10)

                self._queue.append((url, title))

    @weeb.before_invoke
    async def checkz(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect(reconnect=False, timeout=5)
            else:
                embed = discord.Embed(
                    title="You are not connected to a voice channel.", description="", color=0x1F5F9C)
                await ctx.send(embed=embed, delete_after=30) 

    @commands.command(aliases=["e", "Eel", "EEL"], brief="🐟")
    async def eel(self, ctx):
        if ctx.author.voice:
            await ctx.message.add_reaction("🐟")
            voice_client = ctx.voice_client
            voice_client.stop()
            self._queue.clear()
            query = f"{SONG_PATH}eel.mp3"
            self.player = discord.PCMVolumeTransformer(
                discord.FFmpegPCMAudio(query))
            ctx.voice_client.play(
                self.player, after=lambda e: self.client.loop.create_task(self.check_queue(ctx)))

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
            ctx.voice_client.stop()
            self._queue.clear()
            query = f"{SONG_PATH}cheese.mp4"
            self.player = discord.PCMVolumeTransformer(
                discord.FFmpegPCMAudio(query))
            ctx.voice_client.play(
                self.player, after=lambda e: self.client.loop.create_task(self.check_queue(ctx)))

    @cheese.before_invoke
    async def cheese_check(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect(reconnect=False, timeout=5)
            else:
                embed = discord.Embed(
                    title="You are not connected to a voice channel.", description="", color=0x1F5F9C)
                await ctx.send(embed=embed, delete_after=120)

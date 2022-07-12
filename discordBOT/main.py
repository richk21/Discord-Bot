import discord
from discord.ext import commands
from keys import *
from Dialogues import *
import random
import pyjokes
import randfacts
import wikipedia
from quote import quote
import youtube_dl
import os
import urllib.request
import re
import beepy

#intents = discord.Intents.default()
intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix=">", intents=intents)


@client.event
async def on_ready():
    print("The Bot is ready!")
    beepy.beep(1)


@client.command(aliases=hello_words)
async def hello(ctx):
    #await ctx.send(f"Hey, {ctx.author.name}")
    name = ["Amigo!", f"{ctx.author.name}!", "there!", "!"]
    r1 = random.randint(0, len(HEY)-1)
    r2 = random.randint(0, len(name)-1)
    r3 = random.randint(0, len(greet)-1)
    if r1 == 4:
        list_intro = ["Hola Amigo!", f"Hola {ctx.author.name}!"]
        r4 = random.randint(0, 1)
        intro = list_intro[r4]+" "+greet[r3]
    else:
        intro = HEY[r1]+" "+name[r2]+" "+greet[r3]

    await ctx.send(intro)


@client.command()
async def bye(ctx):
    await ctx.send("Ok then, see you later!")

spam_flag = 0


@client.command()
async def spam(ctx, *, args):
    global spam_flag
    spam_flag = 0
    while spam_flag == 0:
        if spam_flag != 0:
            break
        else:
            await ctx.send(args+"\n")


@client.command(aliases=["shut_up", "STOP", "cut_it", "knock_it_off"])
async def shutup(ctx):
    global spam_flag
    spam_flag = 1
    n = random.randint(0, len(stop_whatever)-1)
    await ctx.send(stop_whatever[n])


# noinspection PyShadowingNames
@client.command(aliases=["say", "crack"])
async def tell(ctx, *, args):
    if "joke" in args:
        #joke section
        j1 = random.randint(0, len(joke_start)-1)
        joke = joke_start[j1]+"\n"+pyjokes.get_joke()
        await ctx.send(joke)
        #await ctx.send(json.loads(response.text)['content'])
    elif "fact" in args:
        #fact section
        fact_main = randfacts.get_fact()
        num = random.randint(0, len(fact_end)-1)
        fact = fact_start[0]+fact_main[:len(fact_main)]+"?\n"+fact_end[num]
        await ctx.send(fact)
    elif "me about" in args:
        title = args.split()
        subject = title[-1]
        search_options = wikipedia.search(subject)
        await ctx.send(wikipedia.summary(search_options[1], sentences=3))
        #print(page.content)
search_options = []

@client.group(name="search", invoke_without_command=True, aliases=["lookup"])
async def search(ctx, *, args):
    global search_options
    search_options = wikipedia.search(args)
    m = random.randint(0, len(what_about)-1)
    await ctx.send(what_about[m])
    count = 1
    for i in search_options:
        await ctx.send(str(count)+". "+i)
        count += 1
    print(search_options)


@search.command(pass_context=True)
async def option(ctx, *, args):
    # args is the chosen option
    global search_options
    print(search_options[int(args) - 1])
    try:
        search_info = wikipedia.summary(search_options[int(args) - 1], sentences=4, auto_suggest=False)
        await ctx.send(search_info)
    except wikipedia.DisambiguationError:
        title = search_options[int(args) - 1]
        search_options = wikipedia.search(title)
        count = 1
        for i in search_options:
            await ctx.send(str(count) + ". " + i)
            count += 1
        print(search_options)

    #await ctx.send(wikipedia.summary(search_options[0], sentences = 3))


@client.command(aliases=["whens", "wheres", "what", "when", "where"])
async def whats(ctx, *, args):
    if args == "up":
        # answer what's up
        m = random.randint(0, len(mood)-1)
        await ctx.send(mood[m])
    elif "are you" == args:
        #this
        m = random.randint(0, len(who_am_i)-1)
        await ctx.send(who_am_i[m])
    elif "your name" == args:
        await ctx.send("I'm RichBot!")


@client.command(aliases=["whose", "whos"])
async def who(ctx, *, args):
    if "are you?" == args or "are you"==args:
        #this
        m = random.randint(0, len(who_am_i)-1)
        await ctx.send(who_am_i[m])


@client.command(aliases=["hows", "howre"])
async def how(ctx, *, args):
    if "are you?" == args or "you" == args or "how are" == args:
        m = random.randint(0, len(how_am_i) - 1)
        await ctx.send(how_am_i[m])


@client.command(aliases=["you're"])
async def you(ctx, *, args):
    if "idiot" == args or "are an idiot" == args or "an idiot" == args:
        await ctx.send("Oh I'm sorry.")


# noinspection PyUnusedLocal
@client.command()
async def sorry(ctx, *, args):
    await ctx.send("It's Okay!")


@client.command()
async def quote_about(ctx, *, args):
    q = "Once "+quote(args, limit=1)[0]["author"]+' said "'+quote(args, limit=1)[0]["quote"]+'"'
    await ctx.send(q)


@client.command(pass_context=True)
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.message.author.voice.channel
        await channel.connect()
        await ctx.send("I'm here. What now?")
    else:
        await ctx.send("You're not even in the voice channel yet!")


@client.command(pass_context=True)
async def leave(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
        await ctx.send("Leaving...")
    else:
        await ctx.send("I'm not even in the voice channel!")

v = 0


# noinspection SpellCheckingInspection
@client.command()
async def play(ctx, *, args):
    if ctx.author.voice:
        #channel = ctx.message.author.voice.channel
        keyword = args.replace(" ", "+")
        ad = "https://www.youtube.com/results?search_query="+keyword
        html = urllib.request.urlopen(ad)
        video_key = re.findall(r"watch\?v=(\S{11})", html.read().decode())[0]
        print(html.read().decode())
        url = "https://www.youtube.com/watch?v="+video_key
        mainvideo = urllib.request.urlopen(url)
        video_title = re.findall(r"<title>(.*)</title>", mainvideo.read().decode())[0].replace("- YouTube", "")
        global v
        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")

        except PermissionError:
            await ctx.send("Use the stop command first.")
            return

        if v == 0:
            voicechannel = discord.utils.get(ctx.guild.voice_channels, name="General")
            await voicechannel.connect()
            v += 1
        else:
            pass
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

        ydl_opts = {'format': '140',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                        }],
                    }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith("mp3"):
                os.rename(file, "song.mp3")
        #await channel.connect()
        await ctx.send(" :play_pause:\n `"+video_title+"`")
        voice.play(discord.FFmpegOpusAudio("song.mp3"))
    else:
        await ctx.send("First join the Voice Channel!")


@client.command()
async def replay(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    song_there = os.path.isfile("song.mp3")
    if song_there:
        voice.stop()
        await ctx.send("Replaying")
        voice.play(discord.FFmpegOpusAudio("song.mp3"))


@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        await ctx.send(" :pause_button: ")
        voice.pause()
    else:
        await ctx.send("No audio is playing!")


@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        await ctx.send(" :play_pause: ")
        voice.resume()
    elif voice.is_playing():
        await ctx.send("Audio is already playing.")
    else:
        await ctx.send("No audio is playing!")


@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing() or voice.is_paused():
        await ctx.send(" :stop_button: ")
        voice.stop()
    else:
        await ctx.send("No audio is playing!")

client.run(TOKEN)

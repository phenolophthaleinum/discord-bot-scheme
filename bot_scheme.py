import discord
from discord.ext import commands
import random
import time
from datetime import datetime
from datetime import timedelta

__version_ = "test_bot_001"
__author__ = "hyperscroll"

bot = commands.Bot(command_prefix='.')
bot.run('put your token here')

# VARIABLES
last_update = datetime(2020, 6, 9, 21, 20, 00)

# PATHS
IMG = 'media/image/'
AUDIO = 'media/audio/'
ffmpeg_exec = "C:/ffmpeg/bin/ffmpeg.exe"

# pictures argument table "key": [f"{IMG}value", f"{IMG}value2"...]
pictures = {
    "avatar": [f"{IMG}hl_anim.gif"],
    "lambda": [f"{IMG}hl_lambda.png"]
}

# sounds argument table "key": [f"{AUDIO}value", f"{AUDIO}value2"...]
sounds = {
    "about": [f"{AUDIO}about.mp3", f"{AUDIO}about_pl.mp3"],
}

# emoji argument table "key": "emoji"]
emojis = {
    "text": "🇹",
    "audio": "🎵",
    "image": "🖼️",
    "check": "✅",
    "B": "🅱️",
    "love": "♥️",
}

#"CHANGELOG"
update_motd = f"""I have new features. Check .help sound"""


# STANDARD BOT EVENTS
@bot.event
async def on_ready():
    print('I have come and steady am I.')
    print(f"Running version {__version_}")


@bot.event
async def on_member_join(ctx, member):
    print(f"Welcome {member}")


@bot.event
async def on_member_remove(member):
    print(f'{member} has gone.')


# ERROR HANDLING EVENTS
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        vc = ctx.guild.voice_client
        vc.play(discord.FFmpegPCMAudio(executable=ffmpeg_exec, source=f"{AUDIO}error.mp3"))
        await ctx.send("Missed an argument")
    if isinstance(error, commands.CommandError):
        vc = ctx.guild.voice_client
        vc.play(discord.FFmpegPCMAudio(executable=ffmpeg_exec, source=f"{AUDIO}error.mp3"))
        await ctx.send("Missing command")

# STANDARD METHOD TO PRINT BOT STATUS ON CHANNEL JOIN
def bot_status_on_summon(update):
    since_update = datetime.now() - update
    bot_status = ""
    use_motd = True
    if since_update < timedelta(days=3):
        bot_status = f"""I was updated again!{emojis["love"]}"""
    else:
        bot_status = f"""I was left again."""
        use_motd = False
    return bot_status, use_motd, since_update

# ----------------Commands----------------

# SUMMON
# note that '**' in text makes it bold
@bot.command(
    name="summon",
    usage=None,
    description="Join me!",
    pass_context=True, aliases=["SUMMON"])
async def summon(ctx):
    status, use_motd, since_update = bot_status_on_summon(last_update)
    channel = ctx.message.author.voice.channel
    await channel.connect()
    vc = ctx.guild.voice_client
    vc.play(discord.FFmpegPCMAudio(executable=ffmpeg_exec, source=f"{AUDIO}startup.mp3"))
    if use_motd is True:
        await ctx.send(f"""**Your personal bot**
I was updated {str(since_update).split('.')[0]} ago.
{update_motd}
    {status}""")
    else:
        await ctx.send(f"""**Your personal bot**
I was updated {str(since_update).split('.')[0]} ago.
    {status}""")

# LEAVE
@bot.command(
    name="leave",
    usage=None,
    description="Gotta go then",
    pass_context=True, aliases=["LEAVE"])
async def leave(ctx):
    server = ctx.message.guild.voice_client
    server.play(discord.FFmpegPCMAudio(executable=ffmpeg_exec, source=f"{AUDIO}shutdown.mp3"))
    time.sleep(3)
    await server.disconnect()

# PIC
@bot.command(
    name="pic",
    usage=list(pictures.keys()),
    description="Post a picture",
    aliases=["p", "P", "PIC"])
async def pic(ctx, arg):
    await ctx.send(file=discord.File(random.choice(pictures[arg.lower()])))

# SOUND
@bot.command(
    name="sound",
    usage=list(sounds.keys()),
    description="Play some sounds",
    aliases=["s", "S", "SOUND"])
async def sound(ctx, arg):
    vc = ctx.guild.voice_client
    vc.play(discord.FFmpegPCMAudio(executable=ffmpeg_exec, source=random.choice(sounds[arg.lower()])))
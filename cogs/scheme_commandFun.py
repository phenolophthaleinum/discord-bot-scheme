import discord
from discord.ext import commands
import random
import bot as scheme_bot


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    '''
    Fun commands.
    - sound command: plays given sound
    - pic command: sends given sound in text channel
    '''

    @commands.command(
        name="sound",
        usage=list(scheme_bot.sounds.keys()),
        description="Play some sounds",
        brief="Play some sounds",
        aliases=["s", "S", "SOUND"])
    async def sound(self, ctx, arg):
        vc = ctx.guild.voice_client
        vc.play(discord.FFmpegPCMAudio(executable=scheme_bot.ffmpeg_exec,
                                       source=random.choice(scheme_bot.sounds[arg.lower()])))

    @commands.command(
        name="pic",
        usage=list(scheme_bot.pictures.keys()),
        description="Post a picture",
        brief="Post a picture",
        aliases=["p", "P", "PIC"])
    async def pic(self, ctx, arg):
        await ctx.send(file=discord.File(random.choice(scheme_bot.pictures[arg.lower()])))


def setup(bot):
    bot.add_cog(Fun(bot))

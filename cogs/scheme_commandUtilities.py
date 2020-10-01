import discord
from discord.ext import commands
import bot as scheme_bot


class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    '''
    Utility commands.
    - changelog command: shows last update's changes. The command uses embeds to display contents.
    More on embeds at https://pythondiscord.com/pages/guides/discordpy/learning-discordpy/#embeds
    '''
    @commands.command(
        name="changelog",
        usage=None,
        description="See what's new",
        brief="See what's new",
        pass_context=True,
        aliases=["CHANGELOG", "ch", "CH"])
    async def changelog(self, ctx):
        vc = ctx.guild.voice_client
        thumbnail_file = discord.File(f"{scheme_bot.IMG}windows_update.png", filename="windows_update.png")
        embed = discord.Embed(
            title="Changelog",
            description=f"{scheme_bot.changelog_content['update_name']} version: {scheme_bot.changelog_content['version']}",
            colour=discord.Color.blue()
        )
        embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        embed.set_thumbnail(url="attachment://windows_update.png")
        embed.add_field(name=f"{scheme_bot.changelog_content['update_date']} full report:",
                        value=scheme_bot.changelog_content['update_content'])
        await ctx.send(file=thumbnail_file, embed=embed)


def setup(bot):
    bot.add_cog(Utilities(bot))

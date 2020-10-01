# Discord bot scheme
This is an example of Discord bot written in python that has basic functionality along with commands implemented using **cogs**. Simple comments are present in the code itself, but I provide some additional description of some parts of code below.
## Setting up workspace
In order to write your own Discord bot you will need to **install python3 package.**
```
pip install discord
```
Then, in your code, you need to **import the whole package and its commands**.
```python3
import discord
from discord.ext import commands
```
## Code
We will go through the code and explain the **basics** without your bot won't run. Then I will explain some very **handful constructions** that I used in my bot scheme and lastly, I will cover **cogs construction**.
### Basic functions
#### Bot object and command prefix
The very first thing you need to do is to **create a bot object** which will be called by a command in Discord. To run command correctly, you must **specify a command prefix.**
```python3
bot = commands.Bot(command_prefix='.')
```
**This code defined period character as command prefix.** If you would like to run bot's commands by mentioning it, you can do it.
```python3
bot = commands.Bot(command_prefix=commands.when_mentioned_or('.'))
```
**This is preferable way, because it makes possible to run commands by mentioning the bot or by typing defined prefix.**\
Your bot still waits for your action to actually **run it**. To do this, you write this line:
```python3
bot.run('<put your token here>')
```
**In quotes you need to put your token, so that your bot will be recognised by the Discord.**
### Bot events and joining bot to voice channel
To have the confirmation that bot is running, we can **call an event** to confirm that.
```python3
@bot.event
async def on_ready():
    print('I am actually running.')
```
**This is an asynchronous function that bot will automatically call if succesfully joins the server. This information appears only in your command line - there will be no message sent on Discord. Also, note, that every Discord related functions ought to have decorators.**

So, **how to make something appear on Discord!?** It's not complicated and to show this, I will use **command that joins bot to voice channel.**
```python3
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
```
There is going on a lot but **everything is easy to understand.**\
Firstly, this is an **actual Discord command, so we use command decorator. These decorators have several variables, which are very useful:**
```python3
@bot.command(
    name="summon", # This is a name of command which you type in text channel to perform it
    usage=None,    # This is used to show the example usage in help command (in our scheme - .help). There is no additional usage of this command (e.g. arguments to use), so we leave this empty.
    description="Join me!", # This is full description of command that appears in help command.
    pass_context=True,  # This is used to pass the context between commands, so that they can share information between them. 
    aliases=["SUMMON"]) # Aliases makes the life easier - you can define different names for command so that you can type less or avoid errors (because of some typos).
```
Then, there are **some information about bot - when was last updated, or showing motd. Actual data for these variables is defined in the code (you only need to understand dictionaries).**

Now, there is the critical part of function where we **define which channel bot joins and calling that function.**
```python3
channel = ctx.message.author.voice.channel # This declares bot's target channel - it is channel from which the command was sent
await channel.connect()  # This connects bot to channel
vc = ctx.guild.voice_client # This defines bot's voice client - bot will be able to send audio as if it was a normal person
vc.play(discord.FFmpegPCMAudio(executable=ffmpeg_exec, source=f"{AUDIO}startup.mp3"))  # This plays the specific audio file
```
To be able to play audio files, **you need to have FFmpeg libraries installed** on the machine that hosts the bot (e.g your computer).

Similiar situation appears if we want to **write command that makes bot to leave the server. The difference is the function that needs to be used.** We make changes in two lines:
```python3
channel = ctx.message.author.voice.channel
await channel.connect()
```
```python3
server = ctx.message.guild.voice_client
await server.disconnect()
```
### Using dictionaries to define command arguments
Although they have appeared earlier, I haven't covered them. This is a **very convenient way to define arguments that certain commands will understand**.\
**Using dictionaries we can assing certain action or object to a word.** In this bot scheme it is done as follows:
```python3
AUDIO = 'media/audio/' # This saves time in case of bigger dictionary
sounds = {
    "about": [f"{AUDIO}about.mp3", f"{AUDIO}about_pl.mp3"],
}
```
This is an example of dictionary that has assinged paths to a word 'about'. Then it is utilised in the code:
```python3
@commands.command(...)
async def sound(self, ctx, arg):

... # The rest of function is not important right now

vc.play(discord.FFmpegPCMAudio(executable=scheme_bot.ffmpeg_exec,
                                       source=random.choice(scheme_bot.sounds[arg.lower()])))
}
```
**So, whenever user tries to call a command by typing the command name and passing an argument, this code will be executed.**
### Making a cog
Cogs enable us to organise our commands better, put them into classes and make our code flexible. We can imagine cogs as extension blocks that can be attached and detached in the process of making our bot without reconstruction of the whole code.

**To make a cog, you have to make a folder, where all the cogs (.py files) will be stored. The name does matter because you will need to refer it in the code.**\
Then, in the new script **import these packages:**
```python3
import discord
from discord.ext import commands
import bot as scheme_bot  # Name doesn't matter but you will refer to a bot object through that name in the cog code.
```

**Next step is to make a class. Name of the class is automatically the name of your cog. Create a constructor as follows:**
```python3
class Utilities(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
```
**Now, you need to define a function outside the class that is need to be recognised as cog by the bot.**
```python3
class Utilities(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    
    
def setup(bot):
    bot.add_cog(Fun(bot))
```
**Lastly, you need to load cog in your main bot file.**
```python3
bot.load_extension("cogs.scheme_commandUtilities") # **Important!** scheme_commandUtilities is the name of .py file and cogs is the name of folder
```

Cog should be loaded and now, the only thing to do is to make commands or whatever that your cog needs to play its role.

## More about making a Discord bot in python
There is quite a lot handful sources of information and Youtube tutorials but you need to make sure that you're looking for information about ***discord.py rewrite*** which is the currently developed version.\
Some links:
* [Python Discord Site](https://pythondiscord.com/pages/guides/discordpy/learning-discordpy/)
* [Discord.py Rewrite Documentation](https://discordpy.readthedocs.io/en/latest/)
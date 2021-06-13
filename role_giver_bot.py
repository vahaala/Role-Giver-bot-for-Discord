import discord #imports Discord module
import os #imports OS module
from discord.ext import commands #imports commands submodule from discord.ext
from dotenv import load_dotenv #imports load_dotenv submodule from dotenv

load_dotenv() #loads .env file, which stores our Discord bot token

bot = commands.Bot(command_prefix = '!') #defines that this is a bot, and it's commands prefix

@bot.event #on bot event:
async def on_ready(): #when bot is fully ready:
    print("Successfully initiated {0.user}".format(bot)) #prints specified message in the console

@bot.command() #sets up a bot command
async def roles(ctx): #defines the command name, and it's arguments. Usage is !roles (prefix, then actual command without space inbetween. It's using the def name for it)
    await ctx.channel.send("Here are available roles: \n" + ", ".join([str(r.name) for r in ctx.guild.roles if r.name not in ["@everyone", "Role Giver"]]) + "\nYou can give yourself desired role (and access to linked channels) by typing \"!addrole role_name\". One at a time please!") #sends a message to channel the bot command was activated in

@bot.command() #sets up another bot command, it is required for each command - if you do multiple defs in one @bot decorator, the bot will only properly recognize the first command.
async def addrole(ctx, arg): #defines command name, context (as in, message) and it's arguments (what comes after the !addrole):
    role_name = discord.utils.get(ctx.guild.roles, name = f"{arg}") #extracts role name from given message
    await ctx.author.add_roles(role_name) #adds specified role to the user who invoked the command
    await ctx.channel.send("Role added!") #prints a confirmation message in the channel

@bot.command() #another command
async def delrole(ctx, arg): #basically same as above command, just for removing roles instead of adding them
    role_name = discord.utils.get(ctx.guild.roles, name = f"{arg}")
    await ctx.author.remove_roles(role_name)
    await ctx.channel.send("Role removed!")

bot.run(os.getenv("DISCORD_TOKEN"))
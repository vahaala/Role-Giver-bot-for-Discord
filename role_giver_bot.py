import discord #imports Discord module
import os #imports OS module
from discord.ext import commands #imports commands submodule from discord.ext
from dotenv import load_dotenv #imports load_dotenv submodule from dotenv
intents = discord.Intents.all()


load_dotenv() #loads .env file, which stores our Discord bot token. You probably will need to make one yourself, in the same spot as the script.

bot = commands.Bot(command_prefix = '!', intents = intents) #defines that this is a bot, and it's commands prefix

@bot.event #on bot event:
async def on_ready(): #when bot is fully ready:
    print("Successfully initiated {0.user}".format(bot)) #prints specified message in the console

@bot.command() #sets up a bot command
async def roles(ctx): #defines the command name, and it's arguments. Usage is !roles (prefix, then actual command without space inbetween. It's using the def name for it)
    embed = discord.Embed(title = "Roles list", description = "Here are available roles: ", color = discord.Color.gold()) #formats the bot message in embed style, looks nicely
    global rls #defines a global list of roles
    rls = [r.name for r in ctx.guild.roles if r.name not in ["@everyone", "Role Giver"]] #makes actual content for it
    global emojis #defines a global list of emojis (reactions) available
    emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"] #and also contents
    for index, r in enumerate(rls): #iterates over the roles list
        embed.add_field(name = f"{r}", value = f"React with {emojis[index]} emoji to give yourself a **{r}** role.", inline = False) #for each role, adds a new embed field, with emoji and role name inserted inside
    global msg #defines a global variable of message
    msg = await ctx.send(embed = embed) #sends a message as embed
    for i in range(len(rls)): #adds appropriate number of reactions, equal to number of roles
        await msg.add_reaction(emojis[i])

@bot.event
async def on_reaction_add(reaction, usr): #on added reaction:
    message_id = msg.id #extracts id of bot message
    if reaction.message.id != message_id: #compares if they're not the same - if the bot isn't responding to it's own
        return
    global roles_dict
    roles_dict = {}  #dictionary of roles, with keys being emojis and roles being values
    for i in range(len(rls)): #populates dictionary, effectively binding a role to emoji
        roles_dict[emojis[i]] = rls[i] #takes first item from emoji list as a key, and then first item from roles list as a value
    for i in roles_dict: #iterates over populated roles dictionary
        role_name = discord.utils.get(usr.guild.roles, name = roles_dict.get(i)) #calculates correct role name
        if reaction.emoji == i: #if someone clicked on a reaction:
            if usr.bot: #don't let bot get the roles itself
                pass
            else:
                await usr.add_roles(role_name, atomic = True) #adds role that is bound to clicked emoji

@bot.event
async def on_reaction_remove(reaction, usr): #on revoked reaction (lots of code same as for adding reaction):
    message_id = msg.id
    for i in roles_dict:
        role_name = discord.utils.get(usr.roles, name = roles_dict.get(i))
        if reaction.emoji == i:
            if reaction.message.id != message_id: #checks if you're reacting to the latest message, instead of any of the previous. if yes, then add role, if message was older - do nothing.
                return
            await usr.remove_roles(role_name, atomic = True)

bot.run(os.getenv("DISCORD_TOKEN"))
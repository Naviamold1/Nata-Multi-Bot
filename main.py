import os

import nextcord
from dotenv import load_dotenv
from nextcord import Interaction, Member
from nextcord.ext import application_checks, commands

#Sets up the variable intents, and the variable client, and loads the dotenv file with the bot token
intents = nextcord.Intents.default()
intents.members = True
client = commands.Bot(intents=intents)
load_dotenv()


#let's us know when the program has started the bot, and the bot is ready to be used
@client.event
async def on_ready():
    print("The bot is now ready!")

#creates a command that let's you say hi
@client.slash_command(name = "hello", description = "Get a friendly hello message")
async def hello(interaction: Interaction):
    await interaction.response.send_message("Hello")

#creates a command with a embed file over all our commands
@client.slash_command(name = "commands", description = "The bot's commands")
async def command(interaction: Interaction):
    embed = nextcord.Embed(title="Commands", url="", description="Our commands, but sadly they are under construction...", color=0x6a57ba)
    embed.add_field(name="/hello", value="A command to to finally feel noticed", inline=False)
    embed.add_field(name="/credits", value="A command to find out who contributed to this bot", inline=False)
    embed.add_field(name="/commands", value="A command for the dumb people, so they can know the bot's commands", inline=False)
    embed.add_field(name="/kick", value="Kick someone from the server", inline=False)
    embed.add_field(name="/ban", value="Ban someone from the server", inline=False)
    embed.add_field(name="/unban", value="Unban a banned member (This command is created by Naviamold#1592)", inline=False)
    embed.add_field(name="/id_ban", value="Ban someone thru their user id", inline=False)
    embed.add_field(name="/user_info", value="Get info about a spesific user", inline=False)
    embed.add_field(name="/wip_commands", value="Commands we are working on", inline=False)
    embed.add_field(name="/invite", value="Ask the bot for a link to invite it to your servers", inline=False)
    embed.add_field(name="/update_logs", value="what we have added in this update of the bot", inline=False)
    await interaction.send(embed=embed)

#creates a embed with the list over all people who have helped create the bot
@client.slash_command(name="credits", description="To find out who helped make this bot")
async def credits(interaction: Interaction):
    embed = nextcord.Embed(title="Developers:", url="", description="The people who helped create the bot", color=0x32a852)
    embed.add_field(name="Owner/creator", value="<@640189156013899816>,", inline=False)
    embed.add_field(name="unban command:", value="Naviamold#1592", inline=True)
    await interaction.send(embed=embed)

#creates a slashcommand that let's you kick members from the guild
@client.slash_command(name="kick", description="Kick a member")
@commands.bot_has_permissions(kick_members=True)
@application_checks.has_permissions(kick_members=True)
async def kick(interaction: Interaction, member: Member, *, reason=None):
    if reason == None:
        reason = "No reason provided"

    await member.kick(reason = reason)
    await interaction.send(f'User {member} has been kicked')
#tells the script what it is gonna do if the kick doesn't work
@kick.error
async def kick_err(interaction: Interaction, error:commands.MissingPermissions):
    if isinstance(error, commands.MissingPermissions):
        await interaction.response.send_message(f"you don't have perms to kick")
    elif isinstance(error, commands.BotMissingPermissions):
        await interaction.response.send_message(f"The bot doesn't have perms to kick")

#a slashcommand to ban someone from the server
@client.slash_command(name="ban", description="ban a member")
@commands.bot_has_permissions(ban_members=True)
@application_checks.has_permissions(ban_members=True)
async def ban(interaction: Interaction, member: Member, *, reason=None):
    if reason == None:
        reason = "No reason provided"
    await member.ban(delete_message_days=0, reason = reason)
    await interaction.send(f'**{member}** is banned!')
#tells the script what to do with the ban doesn't work
@ban.error
async def ban_err(interaction: Interaction, error:commands.MissingPermissions):
    if isinstance(error, commands.MissingPermissions):
        await interaction.response.send_message(f"you don't have perms to ban this user")
    elif isinstance(error, commands.BotMissingPermissions):
        await interaction.response.send_message(f"The bot doesn't have perms to ban this user")

#code written by Naviamold
#let's a banned user get unbanned
@client.slash_command(name='unban', description="unban someone")
@commands.has_permissions(ban_members=True)
@application_checks.has_permissions(ban_members=True)
async def unban(interaction:Interaction, *, member: nextcord.User = nextcord.SlashOption(name='user', description='Enter User Id of who you want to unban')):
    await interaction.guild.unban(user=member)
    await interaction.send(f'unbanned {member}')

#a command that let's you ban someone thru their accounts id, instead of their name and discriminator
@client.slash_command(name="id_ban", description="ban a member thru their used id")
@commands.bot_has_permissions(ban_members=True)
@application_checks.has_permissions(ban_members=True)
async def ban(interaction:Interaction, *, member: nextcord.User = nextcord.SlashOption(name='user', description='Enter User Id of who you want to ban'), reason = None):
    if reason == None:
        reason = "No reason provided"

    await interaction.guild.ban(user=member)
    await interaction.send(f'banned {member}')

#a command that shows you some info about a spesific user
@client.slash_command(name="user_info", description="info about a user")
async def user_info(interaction:Interaction, *, member: nextcord.User = nextcord.SlashOption(name='user', description='Enter User Id of who you want to know more about')):
    userid = member.id
    creaton_date = member.created_at
    user_pfp = member.default_avatar
    embed = nextcord.Embed(title=f"{userid}'s stats", url="", description="This user's info & stats", color=0x42f5a1)
    embed.add_field(name="This is the discord user", value=f"<@{userid}>", inline=False)
    embed.add_field(name="This is the users id", value=f"{userid}", inline=False)
    embed.add_field(name="This user was created at", value=f"{creaton_date}, in UTC time", inline=False)
    await interaction.send(embed=embed)

#a command that creates a embed with a list over all the command we plan to add to the bot
@client.slash_command(name = "wip_commands", description = "commands we are working on")
async def wip_commands(interaction:Interaction):
    embed = nextcord.Embed(title="commands we are working on", url="", description="The commands we plan to add", color=0x2763c4)
    embed.add_field(name="/user_info", value="a command to get userinfo", inline=False)
    embed.add_field(name="/purge", value="a command to purge messages", inline=False)
    embed.add_field(name="logs", value="a place to see deleted or edited messages", inline=False)
    embed.add_field(name="warn system", value="a system to warn members, and give punishments from the ammount of warns", inline=False)
    embed.add_field(name="/about", value="info about the bot (idea is stolen from carlbot....)", inline=False)
    embed.add_field(name="/bans", value="Shows all the banned members in the server", inline=False)
    embed.add_field(name="/mute", value="a command to mute a member", inline=False)
    embed.add_field(name="voting system", value="we might add a voting system", inline=False)
    embed.add_field(name="/reporting", value="as a normal member, report someone in the server to the server staff", inline=False)
    embed.add_field(name="/PM_rules", value="Pre made rules, for the lazy people out there", inline=False)
    embed.add_field(name="ideas", value="a system to give me update ideas for the bot", inline=False)
    embed.add_field(name="/bot_stats", value="a command see the bot's stats", inline=False)
    embed.add_field(name="/poll", value="a command to do a poll", inline=False)
    await interaction.send(embed=embed)


#a command that sends out a link if you want to invite the bot to your guild
@client.slash_command(name="invite", description="Invite me to other servers")
async def invite(interaction: Interaction):
    await interaction.response.send_message("https://discord.com/api/oauth2/authorize?client_id=1033997178349301760&permissions=8&scope=bot")

#a embed that shows all the updates that we have done to the bot for this version
@client.slash_command(name="update_logs", description="A overview of the lates update of the bot")
async def udate_logs(interaction:Interaction):
    embed = nextcord.Embed(title="update log 0.0.1", description="The changes we did in this version of the bot")
    embed.add_field(name="Basic commands", value="we created the bot and added some basic commands", inline=True)
    await interaction.send(embed=embed)

@client.slash_command(name="banned_members", description="get a list over all the banned members")
async def banned_members(interaction:Interaction,):
    embed = nextcord.Embed(title="banned members", description="Get a list over all the banned members, and the reason they are banned")


#connects the script to the discord api, and starts the bot
client.run(os.getenv("BOT_TOKEN"))
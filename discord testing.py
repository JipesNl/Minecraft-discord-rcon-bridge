import discord
from discord.ext import commands

client = commands.Bot(command_prefix = '$')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    game = discord.Game("with the API")
    await client.change_presence(status=discord.Status.idle, activity=game)

@client.command()
async def ping(ctx):
    await ctx.send('Pong!')
@client.command()
async def whitelist(ctx, arg):
    

client.run("Njk5OTA3MTkxOTg0ODgxNjc2.XpbNgQ.Xs3gHPs4hMnj18aT13QfpB3oujo")

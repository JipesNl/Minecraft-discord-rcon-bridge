from __future__ import print_function
import argparse
import socket
import mcrcon
import discord
from discord.ext import commands

def main(command):
    # Parse arguments

    # Connect
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("HOSTNAME", RCON PORT))

    try:
        # Log in
        result = mcrcon.login(sock, "RCON PASSWORD")
        if not result:
            print("Incorrect rcon password")
            return

        # Start looping
        request = command
        response = mcrcon.command(sock, request)
        return response
    finally:
        sock.close()

client = commands.Bot(command_prefix = '$')
client.remove_command('help')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    game = discord.Game("Kermitcraft")
    await client.change_presence(status=discord.Status.idle, activity=game)

#ping command
@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

#whitelist command
@client.command()
@commands.has_any_role('VIP', 'MVP', 'MVP+', 'Admin', 'Owner')
async def whitelist(ctx, arg):
    r = main("whitelist add " + arg)
    await ctx.send(r)

#hidden console command
@client.command(hidden=True)
async def hidden_cmdl0l(ctx, arg):
    r = main(arg)
    await ctx.channel.purge(limit=1)
    print(r)
    author = ctx.message.author
    await author.send(r)

#clear command
@client.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

#New help command
@client.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author
    embed = discord.Embed(
        colour = discord.Colour.orange()
    )

    embed.set_author(name='Help')
    embed.add_field(name='$whitelist [user]', value='Whitelists a user on the server!', inline=False)

    await ctx.channel.send(embed=embed)

client.run("DISCORD BOT TOKEN")






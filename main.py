#!/usr/bin/env python3
from __future__ import print_function
import argparse
import socket
import mcrcon
import discord
from discord.ext import commands
from multicraftapi import MulticraftAPI

mc = MulticraftAPI("http://panel.pebblehost.com/api.php",  "user_name",  "api_key")

def response():
    response = mc("getServerStatus", "server_id")
    print(response)
    if response['success'] == True:
        print("Connected!")
        return True
    else:
        print("Error!")
        return False

def main(command):
    # Parse arguments

    # Connect
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("server_ip", 8051))

    try:
        # Log in
        result = mcrcon.login(sock, "rcon_password")
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

#start command
@client.command()
async def start_server(ctx):
    r = response()
    if r == True:
        start = mc("startServer", "server_id")
        if start['success'] == True:
            await ctx.send("The server has been started")
        else:
            print("Error code 2")
    else:
        print("Error code 1")
        await ctx.send(r)

#stop command
@client.command()
@commands.has_any_role('VIP', 'MVP', 'MVP+', 'Admin', 'Owner')
async def stop_server(ctx):
    r = response()
    if r == True:
        start = mc("stopServer", "server_id")
        if start['success'] == True:
            await ctx.send("The server has been stopped")
        else:
            print("Error code 2")
    else:
        print("Error code 1")
        await ctx.send(r)

#kill command
@client.command()
@commands.has_any_role('VIP', 'MVP', 'MVP+', 'Admin', 'Owner')
async def kill_server(ctx):
    r = response()
    if r == True:
        start = client("killServer", "server_id")
        if start['success'] == True:
            await ctx.send("The server has been stopped")
        else:
            print("Error code 2")
    else:
        print("Error code 1")
        await ctx.send(r)

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
@commands.has_any_role('Admin', 'Owner')
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
    embed.add_field(name='$whitelist [user]', value='Whitelists a user on the server!')
    embed.add_field(name='$ping', value='Pings the bot!')
    embed.add_field(name='$start_server', value='Starts the server')
    embed.add_field(name='$stop_server', value='Stops the server, only usable by Admins')
    embed.add_field(name='$kill_server', value='Kills the server, only usable by Admins')
    embed.add_field(name='$help', value='Displays this list')
    await ctx.channel.send(embed=embed)

client.run("discord_key")






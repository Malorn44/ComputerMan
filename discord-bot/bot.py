import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
import json
import random
import datetime
from locallib import directorysearch

# scoredict = {}
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = commands.Bot(command_prefix = '!')
currentguild = 'rpi'


@client.event
async def on_ready():
    global scoredict
    print("Bot is ready.")
    print("Logged in as", client.user.display_name)
    try:
        x = datetime.datetime
        os.system('cp data/scores.json data/scores.json.' + str(x.now()).replace(' ','-') + '.bak')
        with open("data/scores.json", 'r') as f:
            scoredict = json.load(f)
    except Exception as e:
        print(e)
    print("Scores:")
    print(scoredict)
             

@client.event
async def on_message(message):
    global scoredict
    # Triggers whenever a message is sent in a channel the bot has access to view, in all guilds.
    if currentguild == str(message.guild):
        if message.author.bot:
            return
        if str(int(message.author.id)) in scoredict:
            scoredict[str(int(message.author.id))] += 1
        else:
            scoredict[str(int(message.author.id))] = 1
    # print(message.author.id)
    # user = client.get_user(message.author.id)
    # print(client.is_closed)
    # print(message.guild)
    # print(str(user))
    # print(scoredict)
    await client.process_commands(message)

async def update_stats():
    await client.wait_until_ready()
    await asyncio.sleep(15)
    print('stats updater running')
    global scoredict
    while True:
        print('log set')
        try:
            with open("data/scores.json", 'w') as f:
                # print(scoredict)
                json.dump(scoredict,f)
        except Exception as e:
            print(e)
        await asyncio.sleep(120)

@client.command(name='clear')
async def clear(ctx,number = 0):
    if str(ctx.channel) != 'bots':
        pass#return -1
    print('clearing ' + str(ctx.author) + ' in channel (' + str(ctx.channel) + ', ' + str(ctx.guild) + ') times ' + str(number))
    def is_requester(msg):
        if msg.author == ctx.author:
            return True
        else:
            return False
    
    async with ctx.typing():
        deleted = await ctx.channel.purge(limit=(number+1),check=is_requester,bulk=True)
    
    print('done clearing ' + str(ctx.author) + ' in channel (' + str(ctx.channel) + ', ' + str(ctx.guild) + ') times ' + str(number))
    await ctx.send(r':white_check_mark: deleted ' + str(len(deleted)) + ' messages')

@client.command(name='isstudent')
async def isstudent(ctx,rcs):

    # print()
    studenthood = await directorysearch.check_is_student(rcs)
    print(studenthood,rcs)
    if studenthood[0]:
        s1 = 'Student'
    else:
        s1 = studenthood[1].replace('&amp;','&')
    message = await ctx.send(rcs + '\'s role is ' + s1 + '.')
    await asyncio.sleep(10)
    await message.delete()
    await ctx.message.delete()

@client.command(name='botclear')
async def botclear(ctx,number):
    if ctx.message.author.guild_permissions.administrator:
        ms1 = await ctx.send('Clearing ' + str(number) + ' of my own messages...')
        print('clearing ' + str(ms1.author) + ' in channel (' + str(ctx.channel) + ', ' + str(ctx.guild) + ') times ' + str(number))
        def is_requester(msg):
            if msg.author == ms1.author:
                return True
            else:
                return False
        
        async with ctx.typing():
            deleted = await ctx.channel.purge(limit=(number+1),check=is_requester,bulk=True)
        
        print('done clearing ' + str(ms1.author) + ' in channel (' + str(ctx.channel) + ', ' + str(ctx.guild) + ') times ' + str(number))
        await ctx.send(r':white_check_mark: deleted ' + str(len(deleted)) + ' messages')
    else:
        pass    

@client.command(name='echo')
async def echo(ctx):
    await ctx.send(str(ctx.message.content)[6:])
    await ctx.message.delete()

client.loop.create_task(update_stats())
client.run(TOKEN)
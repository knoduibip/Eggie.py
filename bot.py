
import os
import math
import datetime
import random

import discord
from discord import colour
from discord.ext import commands, tasks
from discord import Status
import pytube
from dotenv import load_dotenv
from pytube.__main__ import YouTube
import yaml

HostID = os.getenv('HOST_ID')

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

def make_uchr(code: str):
    return chr(int(code.lstrip("U+").zfill(8), 16))

def distortTXT(text):
    text = text.lower()
    output = ''
    for letter in text:
        gen = random.randint(1, 2)
        if gen == 2:
            letter = letter.upper()
        output = output + letter
    return output

def saveECO(mean):
    for name, val in mean.items():
        with open('Economies/economy_' + str(name) + '.yml', 'r') as fi:
            inDict = yaml.safe_load(fi)
        for subname, subvalue in val.items():
            inDict[str(subname)] += val[subname]
            if val[subname] != 0:
                val[subname] = 0
        with open('Economies/economy_' + str(name) + '.yml', 'w') as fi2:
            fi2.write(yaml.dump(inDict))

    for guild in bot.guilds:

        if 'feed_' + str(guild.id) + '.txt' not in os.listdir('Feeds'):

            open('Feeds/feed_' + str(guild.id) + '.txt', 'w')

        if 'economy_' + str(guild.id) + '.yml' not in os.listdir('Economies'):

            LaecoDict = dict()
            for member in guild.members:
                if not member.bot:
                    LaecoDict[str(member.id)] = 0

            with open('Economies/economy_' + str(guild.id) + '.yml', 'w') as ecf:
                yaml.dump(LaecoDict, ecf)

        meastatt[guild.id] = {mem.id : 0 for mem in guild.members if not mem.bot}

meastatt = dict()

intents = discord.Intents.default()
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix='^', intents=intents, help_command=None, case_insensitive=True)

@bot.event
async def on_ready():

    print('$ Starting the bot... | ' + str(os.getpid()) + '\n')

    print('$ Creating the necessary files... \n')
    for guild in bot.guilds:
        if 'feed_' + str(guild.id) + '.txt' not in os.listdir('Feeds'):

            open('Feeds/feed_' + str(guild.id) + '.txt', 'w')
            print('\tFeeds/feed_' + str(guild.id) + '.txt was created')

        if 'economy_' + str(guild.id) + '.yml' not in os.listdir('Economies'):

            LaecoDict = dict()
            for member in guild.members:
                if not member.bot:
                    LaecoDict[str(member.id)] = 0

            with open('Economies/economy_' + str(guild.id) + '.yml', 'w') as ecf:
                yaml.dump(LaecoDict, ecf)

            print('\tEconomies/economy_' + str(guild.id) + '.yml was created\n')

        meastatt[guild.id] = {mem.id : 0 for mem in guild.members if not mem.bot}

    print('$ Servers that the bot is currently in:\n')
    for guild in bot.guilds:
        print(f'\t- {guild.name}\n')

    print(f'{bot.user.name} is ready for action!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="^help"))
    updateEggs.start()

@bot.event
async def on_member_join(member):
    meastatt[member.guild.id][str(member.id)] = 0
    with open('Economies\economy_' + str(member.guild.id) + '.yml', 'r') as loaddata1:
        yamlDATA = yaml.safe_load(loaddata1)
        yamlDATA[str(member.id)] = 0
    with open('Economies\economy_' + str(member.guild.id) + '.yml', 'w') as savedata1:
        savedata1.write(yaml.dump(yamlDATA))

@bot.event
async def on_member_remove(member):
    meastatt[member.guild.id].pop(str(member.id))
    with open('Economies\economy_' + str(member.guild.id) + '.yml', 'r') as loaddata2:
        yamlDATA = yaml.safe_load(loaddata2)
        yamlDATA.pop(str(member.id))
    with open('Economies\economy_' + str(member.guild.id) + '.yml', 'w') as savedata2:
        savedata2.write(yaml.dump(yamlDATA))

@bot.command(name='info')
async def hello(ctx, link):

    try:
        video = pytube.YouTube(link)
    except:
        pass

    thumbnail = video.thumbnail_url
    title = video.title
    channel = video.author
    uploadDate = video.publish_date
    views = video.views
    length = video.length
    thumbnail = video.thumbnail_url

    if views >= 1000000:
        views = str(math.floor(views/1000000)) + 'm'
    elif views >= 1000:
        views = str(math.floor(views/1000)) + 'k'

    length = str(datetime.timedelta(seconds=length))

    infoEmbed = discord.Embed(title=title, url=link, description=f'Information about {title}:\n\n**Author:** *{channel}*\n**Upload date:** *{uploadDate}*\n**Views:** *{views}*\n**Length:** *{length}*\n**Thumbnail:** *{thumbnail}*', color=0xFF0000)
    infoEmbed.set_image(url=thumbnail)

    await ctx.send(embed=infoEmbed)

@bot.command(name='showmembers')
async def showMembers(ctx):
    statDict = {'online': 0, 'offline': 0, 'bots': 0}
    for member in ctx.author.guild.members:
        if member.bot:
            statDict['bots'] += 1 
        elif member.status == discord.Status.online or member.status == discord.Status.idle or member.status == discord.Status.dnd:
            statDict['online'] += 1
        else:
            statDict['offline'] += 1

    activityEmbed = discord.Embed(title='Member activity of ' + ctx.author.guild.name, description='\n' + make_uchr('U+1F7E2') + ' **ONLINE: **' + str(statDict['online']) + '\n\n' + make_uchr('U+1F534') + ' **OFFLINE: **' + str(statDict['offline']) + '\n\n' + make_uchr('U+1F916') + ' **BOTS: **' + str(statDict['bots']), color=0x00FF7C)
    await ctx.send(embed=activityEmbed)

@bot.command(name='distort')
async def distort(ctx, *, arg):
    txt = str(arg)
    await ctx.send(distortTXT(txt))

annoyList = {}

@bot.command(name='annoy')
async def annoy(ctx, user: discord.User):
    global annoyList
    if ctx.author.id == ctx.guild.owner.id:
        if user.id == bot.user.id:
            await ctx.send('Sorry, I can\'t annoy myself') 
        elif user.id not in annoyList:
            annoyList[user.id] = True
    else:
        await ctx.send('Sorry, you don\'t have the permission to use this command')

@bot.command(name='unannoy')
async def unannoy(ctx, user: discord.User):
    global annoyList
    if ctx.author.id == ctx.guild.owner.id:
        annoyList.pop(user.id)
    else:
        await ctx.send('Sorry, you don\'t have the permission to use this command')
        
@bot.event
async def on_message(message):  
    for victim in annoyList:
        if message.author.id == victim:
            await message.channel.send(distortTXT(message.content))
    await bot.process_commands(message)

@bot.command(name='feed')
async def feed(ctx, *args):
    with open('Feeds/feed_' + str(ctx.author.guild.id) + '.txt','rt') as fw:
        flist = list()
        for line in fw.readlines():
            strline = line.strip()
            flist.append(strline)
    if not args:
        feedEmbed = discord.Embed(title='Feed:', color=0xFF0000)
        for ytc in flist:
            ytChannel = pytube.Channel(ytc)
            newestVid = YouTube(ytChannel.video_urls[0])
            length = newestVid.length
            length = str(datetime.timedelta(seconds=length))
            views = newestVid.views
            if views >= 1000000:
                views = str(math.floor(views/1000000)) + 'm'
            elif views >= 1000:
                views = str(math.floor(views/1000)) + 'k'
            thumbnail = newestVid.thumbnail_url
            feedEmbed.add_field(name=ytChannel.channel_name, value=f'**Title:** *{newestVid.title}*\n**Length:** *{length}*\n**Views:** *{views}*\n**Thumbnail:** *{thumbnail}*\n**Link:** *{ytChannel.video_urls[0]}*', inline=False)
        await ctx.send(embed=feedEmbed)
    elif args[0] == '+':
        with open('Feeds/feed_' + str(ctx.author.guild.id) + '.txt', 'a') as fa:
            if len(flist) > 0:
                try:
                    channel = pytube.Channel(args[1])
                    fa.seek(0)
                    fa.write('\n')
                    fa.write(args[1])
                except:
                    pass
            else:
                try:
                    channel = pytube.Channel(args[1])
                    fa.write(args[1])
                except:
                    pass
    elif args[0] == '-':
        if args[1] in flist:
            flist.remove(args[1])
        open('Feeds/feed_' + str(ctx.author.guild.id) + '.txt', 'w').close()
        with open('Feeds/feed_' + str(ctx.author.guild.id) + '.txt', 'a') as fr:
            for line in flist:
                if flist.index(line) > 0:
                    fr.write('\n')
                    fr.write(line)
                else:
                    fr.write(line)

@bot.command(name='economy', aliases=['leaderboard'])
async def eco(ctx):
    leaderboard = dict()
    ecoEmbed = discord.Embed(title='Economy of ' + ctx.author.guild.name, color=0xF4FF00)
    with open('Economies/' + 'economy_' + str(ctx.author.guild.id) + '.yml', 'r') as ecoFile:
        ecol = yaml.safe_load(ecoFile)
        INPleaderboard = sorted(ecol.items(), key=lambda x:x[1], reverse=True)
        for n in INPleaderboard:
            leaderboard[str(n[0])] = n[1]
    place = 1
    for key, value in leaderboard.items():
        user = await bot.fetch_user(key)
        username = user.name
        ecoEmbed.add_field(name=f'**{place}.** **{username}**', value=f'*{value}* Eggs', inline=False)
        place += 1
    ecoEmbed.add_field(name='**WARNING**', value='**THE ECONOMY UPDATES ITSELF EVERY 5 MINUTES**')
    await ctx.send(embed=ecoEmbed)

@commands.cooldown(1, 60, commands.BucketType.user)
@bot.command(name='egg', aliases=['work'])
async def cash(ctx):
    guildID = ctx.author.guild.id
    memberID = ctx.author.id
    PlusCash = random.randint(1, 10)
    meastatt[guildID][memberID] += PlusCash
    await ctx.send(f'You\'ve won {PlusCash} egg/s!')

@cash.error
async def cashERR(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f'This command is on cooldown, please try again in {int(error.retry_after)} seconds')
    else:
        raise error

@commands.cooldown(1, 120, commands.BucketType.user)
@bot.command(name='spin', aliases=['roulette', 'casino'])
async def roulette(ctx):
    with open('Economies/economy_' + str(ctx.author.guild.id) + '.yml', 'r') as myFile:

        bal = yaml.safe_load(myFile)

        if bal[str(ctx.author.id)] + meastatt[ctx.author.guild.id][ctx.author.id] >= 20:
            meastatt[ctx.author.guild.id][ctx.author.id] -= 20

            await ctx.send(file=discord.File('Images/Chances.jpg'))
            plusmoney = 0
            spin = random.randint(1, 100)

            if spin <= 50:
                plusmoney = 0
            elif spin > 50 and spin <= 75:
                plusmoney = 40
            elif spin > 75 and spin <= 87:
                plusmoney = 100
            elif spin > 87 and spin <= 93:
                plusmoney = 250
            elif spin > 93 and spin <= 97:
                plusmoney = 500
            elif spin > 97 and spin <= 99:
                plusmoney = 1000
            elif spin == 100:
                plusmoney = 10000

            meastatt[ctx.author.guild.id][ctx.author.id] += plusmoney

            spinEmbed = discord.Embed(title='The Result', description=f'You\'ve won {plusmoney} Eggs! (Profit: {plusmoney - 20})', color=0xF4FF00)
            await ctx.send(embed=spinEmbed)

        else:
            await ctx.send('Sorry, you don\'t have enough money, the spin costs 20 Eggs')

@roulette.error
async def rouletteERR(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f'This command is on cooldown, please try again in {int(error.retry_after)} seconds')
    else:
        raise error

@commands.cooldown(1, 120, commands.BucketType.user)
@bot.command(name='bal', aliases=['balance', 'wallet'])
async def balance(ctx, user: discord.User = None):
    if user:
        with open('Economies/economy_' + str(ctx.author.guild.id) + '.yml', 'r') as muns:
            bal = yaml.safe_load(muns)
            Balance = bal[str(user.id)] + meastatt[ctx.author.guild.id][user.id]
            balanceEmbed = discord.Embed(title=f'{user.name}\'s#{user.discriminator} balance', description=f'{Balance} Eggs', color=0xF4FF00)
            await ctx.send(embed=balanceEmbed)
    else:
        with open('Economies/economy_' + str(ctx.author.guild.id) + '.yml', 'r') as muns:
            bal = yaml.safe_load(muns)
            Balance = bal[str(ctx.author.id)] + meastatt[ctx.author.guild.id][ctx.author.id]
            balanceEmbed = discord.Embed(title=f'{ctx.author.name}\'s#{ctx.author.discriminator} balance', description=f'{Balance} Eggs', color=0xF4FF00)
            await ctx.send(embed=balanceEmbed)

@balance.error
async def balanceERR(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f'This command is on cooldown, please try again in {int(error.retry_after)} seconds')
    else:
        raise error

@tasks.loop(seconds=300)
async def updateEggs():
    saveECO(meastatt)

@bot.command(name='logout')
async def logout(ctx):
    if ctx.author.id == 509002743256580107:
        saveECO(meastatt)
        print('logging out...')
        await bot.close()
    else:
        await ctx.send('Sorry, you don\'t have the permission to use this command')

@bot.command(name='help')
async def helpMe(ctx):

    helpEmbed = discord.Embed(title='Eggie\'s commands', description='Prefix: ^', color=0x0033FF)
    helpEmbed.add_field(name='help', value='**Arguments:** *Takes 0 arguments*\n**Description:** *Shows all of the available commands*', inline=False)
    helpEmbed.add_field(name='showmembers', value='**Arguments:** *Takes 0 arguments*\n**Description:** *Shows the amount of: online members, offline members, bots*', inline=False)
    helpEmbed.set_thumbnail(url='https://c.tenor.com/AcrJynkiNzcAAAAM/cmd-command.gif')

    helpYoutubeEmbed = discord.Embed(title='YouTube related commands:', description='Prefix: ^', color=0xFF0000)
    helpYoutubeEmbed.add_field(name='info {link}', value='**Arguments:** *Takes 1 crucial argument: youtube video link*\n**Description:** *Shows basic info about a youtube video*', inline=False)
    helpYoutubeEmbed.add_field(name='downloadaudio {link}', value='**Arguments:** *Takes 1 crucial argument: youtube video link*\n**Description:** *Downloads the audio of a youtube video as a mp3 file*', inline=False)
    helpYoutubeEmbed.add_field(name='feed {operator} {link}', value='**Arguments:** *Takes 2 optional arguments: operator [+, -], youtube channel link*\n**Description:** *\"+\" operator adds the youtube channel represented by the link to the feed, while \"-\" operator deletes a channel from the feed. If no arguments are given, the feed is displayed*', inline=False)
    helpYoutubeEmbed.set_thumbnail(url='https://thumbs.gfycat.com/BruisedOrnateBullfrog-small.gif')

    helpEconomyEmbed = discord.Embed(title='Economy related commands:', description='Prefix: ^', color=0xF4FF00)
    helpEconomyEmbed.add_field(name='economy', value='**Arguments:** *Takes 0 arguments*\n**Description:** *Shows the economy leaderboard*', inline=False)
    helpEconomyEmbed.add_field(name='egg', value='**Arguments:** *Takes 0 arguments*\n**Description:** *Gives you a random amount of eggs from range 1 to 10*', inline=False)
    helpEconomyEmbed.add_field(name='bal {user mention}', value='**Arguments:** *Takes 1 optional argument: user mention*\n**Description:** *Shows the balance of the mentioned user, if no arguments are given, it shows the balance of the command author*', inline=False)
    helpEconomyEmbed.add_field(name='spin', value='**Arguments:** *Takes 0 arguments*\n**Description:** *For 20 eggs you can roll the dice! You can lose your Eggs, or earn a great fortune*', inline=False)
    helpEconomyEmbed.set_thumbnail(url='https://acegif.com/wp-content/gifs/coin-flip-49.gif')

    helpFunnyEmbed = discord.Embed(title='Utterly useless commands:', description='Prefix: ^', color=0x11BD00)
    helpFunnyEmbed.add_field(name='distort', value='**Arguments:** *Takes 1 crucial argument: text*\n**Description:** *Distorts a text ex. Eggs are cool ==> eGGs ArE cOoL*', inline=False)
    helpFunnyEmbed.add_field(name='annoy {user mention}', value='**Arguments:** *Takes 1 crucial argument: user mention*\n**Description:** *Annoys the chosen user*\n**SERVER OWNER COMMAND**', inline=False)
    helpFunnyEmbed.add_field(name='unannoy {user mention}', value='**Arguments:** *Takes 1 crucial argument: user mention*\n**Description:** *Unannoys the chosen user*\n**SERVER OWNER COMMAND**', inline=False)
    helpFunnyEmbed.set_thumbnail(url='https://media3.giphy.com/media/UtcBRO8cxulRzkrVLc/200.gif')

    await ctx.send(embed=helpEmbed)
    await ctx.send(embed=helpYoutubeEmbed)
    await ctx.send(embed=helpEconomyEmbed)
    await ctx.send(embed=helpFunnyEmbed)
bot.run(TOKEN)
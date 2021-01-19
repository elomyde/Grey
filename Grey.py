#3537984 : perm int
#Basics
import os #to get token
import json #json file parse
import random #used in many games and features
from features import minesweeper, emojitext, embeds
import time
import math
import re
import asyncio

#Word tokenizers
import nltk
from nltk.tokenize import TreebankWordTokenizer
from nltk.tokenize import sent_tokenize

#Discord APIs
import discord
from discord.ext import commands
from discord.ext import tasks

#Word tokenizers
nltk.download('punkt')
tokenizer = TreebankWordTokenizer()
avatarFlag = True

CONFIG = {}
with open("./config.json", "r") as f:
    CONFIG = json.load(f)

RAND_HELLO = list()
with open("./random_hello.txt", "r", encoding = "utf-8") as f2 :
    while True :
        line = f2.readline().rstrip("\n")
        if not line :
            break
        RAND_HELLO.append(line)

CONFIG_PROHIBITED_CHANNEL = list(CONFIG.pop('prohibitlists').values())
GREYMOJI = CONFIG.pop('emojis')
GREYMOJI_LIST = list(GREYMOJI.values())
AVATAR_TIME_PRIOR = 0

#Constants
NoU = ["No U", "I am alive", "Grey is alive", "I didn't die", "You are a liar"]
SOLDIER_CATMAID = ["But Soldier, you are a cat maid!", "I think soldier is a cat maid", "Soldier is a cat maid", "Soldier catmaid confirmed"]
REPLY_NIRA = ["<a:E_greydontworryme:789817643297013770>", "<:greysmile:742805250469265409>", "<:E_greysmile:796762990794899467>", "<:E_greyUwU:790553515663163413>"]
CALL_NIRA = "<@740606402330099752>"

#Discord APIs
bot = commands.Bot(command_prefix='=')
client = discord.Client()
bot.remove_command('help')

# Channel

# Internal functions
def grey_love_checker(content) :
    sentences = sent_tokenize(content)
    sentenceFlag = False
    for sentence in sentences :
        token_words = tokenizer.tokenize(sentence)
        greyFlag = False
        loveFlag = False
        notFlag = False
        for word in token_words :
            if (('grey' == word) or ('gray' == word)) :
                greyFlag = True
                continue
            if (('love' == word) or ('cute' == word) or ('luv' == word)) :
                loveFlag = True
                continue
            if word == 'no' or word == 'not' or word =='n\'t' :
                notFlag = not notFlag
                continue
        sentenceFlag = sentenceFlag or (greyFlag and loveFlag and not notFlag)
    return sentenceFlag

def grey_death_checker(content) :
    sentences = sent_tokenize(content)
    sentenceFlag = False
    #for every sentence, check if the sentece has the meaning 'grey is dead'
    for sentence in sentences:
        token_words = tokenizer.tokenize(sentence)
        greyFlag = False
        deathFlag = False
        notFlag = False
        for word in token_words :
            if (('grey' == word) or ('gray' == word)) :
                greyFlag = True
                continue

            if (('dead' == word) or ('die' == word) or ('gone' == word)) :
                deathFlag = True
                continue
            
            if ('alive' == word or 'sentien' == word) :
                deathFlag = True
                notFlag = not notFlag
                continue

            if word == 'no' or word == 'not' or word =='n\'t' :
                notFlag = not notFlag
                continue
        sentenceFlag = sentenceFlag or (greyFlag and deathFlag and not notFlag)
    return sentenceFlag

def embed_text(text) :
    embed = discord.Embed(color = discord.Color.greyple())
    embed.set_author(name = bot.user, icon_url = bot.user.avatar_url)
    embed.add_field(name = 'message from grey', value = text)
    return embed

@bot.command()
async def initiate_help() :
    BOT_COMMANDS_CHANNEL = 742548177462231120
    channel = bot.get_channel(BOT_COMMANDS_CHANNEL)
    HELP_REGULAR_ID = 800923698214731782
    HELP_FUN_ID = 800923698743345192
    regular_msg = await channel.fetch_message(HELP_REGULAR_ID)
    await regular_msg.edit(embed = embeds.help_regular)
    fun_msg = await channel.fetch_message(HELP_FUN_ID)
    await fun_msg.edit(embed = embeds.help_fun)

# loops

@tasks.loop(hours = 8)
async def hellonira() :
    global bot
    channel = bot.get_channel(603246092402032673) #603246092402032673 #798217844784758894
    async with channel.typing() :
        await asyncio.sleep(3)
    await channel.send(RAND_HELLO[random.randint(0,len(RAND_HELLO)-1)].format(nira = CALL_NIRA))

# Test commands
@bot.command(pass_context = True, aliases = ['hn'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def hitonira(ctx) :
    async with ctx.channel.typing() :
        await asyncio.sleep(3)
    await ctx.send("<@740606402330099752> " + "Hello, Nira-chan!")

@bot.command()
async def ping(ctx):
    await ctx.send("pong! {0}ms".format(round(bot.latency, 1)))

# Fun commands

@bot.command(pass_context = True , aliases = ['mine', 'm'])
async def mines(ctx, mapsizeX, mapsizeY, bombnum) :
    NUMBERS = [":zero:", ":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:"]
    try:
        mapsizeX = int(mapsizeX)
        mapsizeY = int(mapsizeY)
        bombnum = int (bombnum)
    except :
        await ctx.send("Please input proper numbers please!")
        return
    
    if ((mapsizeX < 3 or mapsizeY < 3) or (mapsizeX > 12 or mapsizeY > 12) or (bombnum > (mapsizeX*mapsizeY - 2)) or mapsizeX*mapsizeY > 120) :
        await ctx.send("Please input proper numbers please!")
        return

    mine = minesweeper.assembleMap(mapsizeX, mapsizeY, bombnum)

    context = ""
    for lines in mine :
        for j in lines :
            if j == 'bomb' :
                context += "||:bomb:||"
            else :
                context += "||" + NUMBERS[j] + "||"
        context += "\n"
    context += " "
    await ctx.send(context)

@commands.cooldown(1, 20, commands.BucketType.user)
@bot.command(pass_context = True, aliases = ['etext', 'et'])
async def emojitotext(ctx, emo, text) :
    mask_normal = re.compile(r'^<[:]\w+[:]\w+>$')
    mask_moving = re.compile(r'^<a[:]\w+[:]\w+>$')
    if not(re.fullmatch(mask_normal, emo) or re.fullmatch(mask_moving, emo)) :
        await ctx.send(embed = embed_text("Please input proper emoji!"))
        return
    
    emo_id = emo.split(':')[-1][:-1]

    try :
        x = bot.get_emoji(int(emo_id))
    except :
        await ctx.send(embed = embed_text("Please input proper emoji!"))
        return
    
    if x == None :
        await ctx.send(embed = embed_text("Please input proper emoji!"))
        return

    if len(text) > 10 :
        await ctx.send(embed = embed_text("This text is too long to convert"))
        return
    conv_text = emojitext.emojiconverter(text, emo, "<:blank:788433633655783434>")

    for x in conv_text :
        await ctx.send(x)

@emojitotext.error
async def info_error(ctx, error) :
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is ratelimited, please try again in {:.1f}s'.format(error.retry_after)
        await ctx.send(embed = embed_text(msg))

@bot.command(pass_context = True, aliases = ['sa'])
async def saturnage(ctx, age):
    try:
        age = int(age)
        await ctx.send (embed = embed_text("Your age in Saturnian is %.2f" % (float(age)/29.4577)))
    except :
        await ctx.send(embed = embed_text("Please input proper age!"))

@bot.command(pass_context = True, aliases = ['ea'])
async def earthage(ctx, age):
    try:
        age = int(age)
        await ctx.send (embed = embed_text("Your age in Earth is %d" % math.floor(int(float(age)*29.4577))))
    except :
        await ctx.send(embed = embed_text("Please input proper age!"))

@bot.command(pass_context = True, aliases = ['ChangeAvatar', 'ca'])
async def changeavatar(ctx):
    global AVATAR_TIME_PRIOR
    if (time.time() - AVATAR_TIME_PRIOR) < 300 :
        await ctx.send (embed = embed_text("I can't change my avatar that quick!"))
        return

    global avatarFlag
    AVATAR_TIME_PRIOR = time.time()
    with open('./images/grey1.png', 'rb') as f :
        image1 = f.read()
    with open('./images/grey2.png', 'rb') as f :
        image2 = f.read()
    
    if avatarFlag :
        avatarFlag = not avatarFlag
        await bot.user.edit(avatar = image2)
        await ctx.send (embed = embed_text("Changed avatar to Hunch gray's Grey-kun."))
        return
    else :
        avatarFlag = not avatarFlag
        await bot.user.edit(avatar = image1)
        await ctx.send (embed = embed_text("Changed avatar to Ham's Grey-chan."))
        return

@bot.command(pass_context = True , aliases=['UwU'])
async def uwu(ctx):
    await ctx.send("<:E_greyUwU:790553515663163413>")
    await ctx.message.delete()
    
@bot.command(pass_context = True , aliases=['greypat', 'gpp', 'gp', 'GPP', 'GP'])
async def greypatpat(ctx):
    await ctx.send(GREYMOJI['GreyPat'])
    await ctx.message.delete()
    
# Regular commands

@bot.command(pass_context = True , aliases = ['Help', 'h'])
async def help(ctx): 
    await ctx.send(embed = embeds.help_regular)
    await ctx.send(embed = embeds.help_fun)

@bot.command(pass_context = True , aliases = ['Invite'])
async def invite(ctx):
    embed = discord.Embed(color = discord.Color.greyple())
    embed.add_field(name = 'Invitation', value = "Click [Here](https://discord.com/oauth2/authorize?client_id=790571552345030686&scope=bot&permissions=3537984) to make Grey join your server!")
    await ctx.send(embed = embed)

@bot.command(pass_context = True , aliases = ['Vote', 'v'])
async def vote(ctx, *args):
    texts = []
    sentence = ""
    for arg in args :
        if arg == 'or' or arg == 'Or':
            if sentence != "" :
                texts.append(sentence)
                sentence = ""
        else :
            sentence += arg + ' '
    texts.append(sentence)

    embed = discord.Embed(color = discord.Color.greyple())
    embed.set_author(name = ctx.message.author, icon_url = ctx.message.author.avatar_url)
    INDICATORS = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭']

    if sentence == "" :
        embed.add_field(name = 'Vote', value = "Please create a proper vote!\nYou must input at least one item.")
        await ctx.send(embed = embed)
        return

    if len(texts) == 1 :
        embed.add_field(name = 'Vote', value = sentence)
        vote = await ctx.send(embed = embed)
        await vote.add_reaction('✅')
        await vote.add_reaction('❎')
    
    elif len(texts) > 1 and len(texts) <= 8 :
        text = ""
        i = 0
        for item in texts :
            text += INDICATORS[i] + " " + item + "\n"
            i += 1
            if i < len(texts) : 
                text += "Or\n"
        embed.add_field(name = 'Vote', value = text)
        vote = await ctx.send(embed = embed)
        for i in range(len(texts)) :
            await vote.add_reaction(INDICATORS[i])

    else :
        embed.add_field(name = 'Vote', value = "Please create a proper vote!\nThere can be up to 8 items.")
        await ctx.send(embed = embed)

# On-message events

@bot.event
async def on_message(message):
    #pretreatment
    content = message.content.lower()
    toknized_content = tokenizer.tokenize(content)
    channel = str(message.channel.id)
    author = message.author.id
    guild_id = message.guild.id

    #Check the server
    if channel in CONFIG_PROHIBITED_CHANNEL :
        return

    #Check the message is not from itself
    if author == bot.user.id : # itself
        return
    
    #Reply to @Grey
    if bot.user.mentioned_in(message) :
        await message.add_reaction(GREYMOJI['GreyNod'])
        if author == 740606402330099752 : #only for Nira-chan
            async with message.channel.typing() :
                await asyncio.sleep(1.5)
            await message.channel.send(REPLY_NIRA[random.randint(0,len(REPLY_NIRA))-1])
        return
    else :
        pass

    #Hai
    if (content == "hai") :
        await message.channel.send("Hai!")
        return
    elif ("hai" in toknized_content) and random.randint(0,1) == 0 :
        await message.channel.send("Hai!")
        return
    else :
        pass
    
    #Reply to "Grey is dead" or "I love grey"
    if grey_death_checker(content) :
        i = random.randint(0, len(NoU)-1)
        await message.channel.send(NoU[i])
        return
    elif grey_love_checker(content) :
        await message.add_reaction(GREYMOJI_LIST[random.randint(0,len(GREYMOJI_LIST))-1])
        return
    else :
        pass

    await bot.process_commands(message)

    #soldier catmaid meme
    if author == 314358105205112834 :
        if (("no" in content or "not" in content) and ("maid" in content or "cat" in content)) :
            await message.channel.send(SOLDIER_CATMAID[random.randint(0,len(SOLDIER_CATMAID))-1]+ GREYMOJI['GreyNod'])

    #Grey patpat feature
    if "patpat" in content or "greypat" in content :
        #Check if the message is from ZZ server
        if guild_id == 603246092402032670 :
            for role in message.author.roles :
                #Patpat role check
                if role.id == 765347466169024512 :
                    try:
                        await message.add_reaction(GREYMOJI['GreyPat'])
                    except:
                        pass
                    break
                else :
                    pass
        else :
            await message.add_reaction(GREYMOJI['GreyPat'])

# On-ready events
@bot.event
async def on_ready():
    print('logging in')
    print('connection was succesful')
    await bot.change_presence(status=discord.Status.online, activity=None)
    await initiate_help()
    hellonira.start()
    bot.remove_command('initiate_help')

bot.run(os.environ['token'])
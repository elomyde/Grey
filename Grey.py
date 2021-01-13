#3537984 : perm int

#Basics
import os #to get token
import json #json file parse
import random #used in many games and features
from features import minesweeper
from features import emojitext
import time
import math
import re

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

CONFIG_PROHIBITED_CHANNEL = list(CONFIG.pop('prohibitlists').values())
GREYMOJI = CONFIG.pop('emojis')
GREYMOJI_LIST = list(GREYMOJI.values())
AVATAR_TIME_PRIOR = 0

#Answers
NoU = ["No U", "I am alive", "Grey is alive", "I didn't die", "You are a liar"]
SOLDIER_CATMAID = ["But Soldier, you are a cat maid!", "I think soldier is a cat maid", "Soldier is a cat maid", "Soldier catmaid confirmed"]
REPLY_NIRA = ["hi!", "poyo!", "Good day, Nira-chan!", "<a:E_greydontworryme:789817643297013770>"]

#Discord APIs
bot = commands.Bot(command_prefix='=')
client = discord.Client()
bot.remove_command('help')

#Internal Functions
def grey_love_checker(content) :
    sentences = sent_tokenize(content)
    sentenceFlag = False
    for sentence in sentences :
        token_words = tokenizer.tokenize(sentence)
        greyFlag = False
        loveFlag = False
        notFlag = False
        for word in token_words :
            if (('grey' in word) or ('gray' in word)) :
                greyFlag = True
                continue
            if (('love' in word) or ('cute' in word) or ('luv' in word)) :
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
            if (('grey' in word) or ('gray' in word)) :
                greyFlag = True
                continue

            if (('dead' in word) or ('die' in word) or ('gone' in word)) :
                deathFlag = True
                continue
            
            if ('alive' in word or 'sentien' in word) :
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

#Commands
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

@bot.command(pass_context = True , aliases=['UwU'])
async def uwu(ctx):
    await ctx.send("<:E_greyUwU:790553515663163413>")
    await ctx.message.delete()
    
@bot.command(pass_context = True , aliases=['greypat', 'gpp', 'gp', 'GPP', 'GP'])
async def greypatpat(ctx):
    await ctx.send(GREYMOJI['GreyPat'])
    await ctx.message.delete()
    
@bot.command()
async def ping(ctx):
    await ctx.send("pong! {0}ms".format(round(bot.latency, 1)))

@bot.command(pass_context = True , aliases = ['Help', 'h'])
async def help(ctx):
    embed = discord.Embed(color = discord.Color.greyple())
    embed.set_author(name='Help')
    embed.add_field(name = '=mines [x] [y] [z], =mine, =m', value = "Make minesweeper, size of x * y with z mines.", inline = False)
    embed.add_field(name = '=uwu, =UwU', value = "UwU", inline = False)
    embed.add_field(name = '=greypatpat, =gpp, =gp, =GPP, GP', value = "Grey will patpat you!", inline = False)
    embed.add_field(name = '=ping', value = "Pong!", inline = False)
    embed.add_field(name = '=invite, =Invite', value = "Make a invitation for your server.", inline = False)
    embed.add_field(name = '=vote item / =vote a or b or ...(up to 8), =Vote, =v', value = "Create a vote!\nYou can create a single Yes-or-no vote\nor a vote with up to eight items.", inline = False)
    embed.add_field(name = '=changeavatar, =ChangeAvatar, =ca', value = "Change an avatar of Grey, can only be used once per hour!", inline=False)
    embed.add_field(name = '=saturnage, =sa', value = "Convert your Earth-age into gorgeous Saturn-age", inline=False)
    embed.add_field(name = '=earthage, =ea', value = "Convert your Saturn-age into Earth-age", inline=False)
    embed.add_field(name = '=emojitotext [emoji] [text], =etext, =et', value = "Convert your text to emoji!", inline=False)
    await ctx.send(embed = embed)

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

@bot.command(pass_context = True, aliases = ['sa'])
async def saturnage(ctx, age):
    await ctx.send (embed = embed_text("Your age in Saturnian is %d" % math.floor(int(age) * 10.8433)))

@bot.command(pass_context = True, aliases = ['ea'])
async def earthage(ctx, age):
    await ctx.send (embed = embed_text("Your age in Earth is %d" % math.floor(int(age) / 10.8433)))

@bot.command()
@commands.has_permissions(administrator=True)
async def initiate_avatar(ctx) :
    with open('./images/grey1.png', 'rb') as f :
        image = f.read()
    print("changed to grey1")
    await bot.user.edit(avatar = image)

@bot.command(pass_context = True, aliases = ['ChangeAvatar', 'ca'])
async def changeavatar(ctx):
    global AVATAR_TIME_PRIOR
    if (time.time() - AVATAR_TIME_PRIOR) < 3600 :
        await ctx.send (embed = embed_text("I can't change my avatar that quick!"))
        return

    global avatarFlag
    AVATAR_TIME_PRIOR = time.time()
    with open('./images/grey1.png', 'rb') as f :
        image1 = f.read()
    with open('./images/grey2.png', 'rb') as f :
        image2 = f.read()
    
    if avatarFlag :
        print("changed to grey2")
        avatarFlag = not avatarFlag
        await bot.user.edit(avatar = image2)
    else :
        print("changed to grey1")
        avatarFlag = not avatarFlag
        await bot.user.edit(avatar = image1)

#On-message events
@bot.event
async def on_message(message):
    #pretreatment
    content = message.content.lower()
    channel = str(message.channel.id)
    author = str(message.author.id)
    guild_id = str(message.guild.id)
    #Check the server
    if channel in CONFIG_PROHIBITED_CHANNEL :
        return

    #Check the message is not from itself
    if author == bot.user:
        print("bot")
        return
    
    #Reply to @Grey
    if bot.user.mentioned_in(message) :
        print(author)
        await message.add_reaction(GREYMOJI['GreyNod'])
        if author == "740606402330099752" : #only for Nira-chan
            print("Nira")
            await message.channel.send(REPLY_NIRA[random.randint(0,len(REPLY_NIRA))-1])

    #Reply to "Grey is dead" or "I love grey"
    if grey_death_checker(content) :
        i = random.randint(0, len(NoU)-1)
        await message.channel.send(NoU[i])
    elif grey_love_checker(content) :
        await message.add_reaction(GREYMOJI_LIST[random.randint(0,len(GREYMOJI_LIST))-1])
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
        if guild_id == "603246092402032670" :
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

@bot.event
async def on_ready():
    print('logging in')
    print('connection was succesful')
    await bot.change_presence(status=discord.Status.online, activity=None)

bot.run(os.environ['token'])

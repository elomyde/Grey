#await ctx.send(text) : 텍스트 보내기
#await ctx.message.delete : 방금 보낸 텍스트 삭제
#bot.command 뒤에 (pass_context = True, aliases =[]) 으로 여러개의 명령어가 같은 역할 수행하게 할 수 있음

#Basics
import random
from features import minesweeper

#Word tokenizers
import nltk
from nltk.tokenize import TreebankWordTokenizer
from nltk.tokenize import sent_tokenize

#Discord APIs
import discord
from discord.ext import commands
from discord.ext import tasks

#To get token from Heroku
import os

#Word tokenizers
nltk.download('punkt')
tokenizer = TreebankWordTokenizer()

#Discord APIs
bot = commands.Bot(command_prefix='=')
client = discord.Client()

#Answers
NoU = ["No U", "I am alive", "Grey is alive", "I didn't die", "You are a liar"]
avilable_greymoji = ["<:E_Grey1:789817319760330794>", "<:greyUwU:790553515663163413>", "<:E_Grey3:789817320204664862>"]

def grey_love_checker(message) :
    raw_words = message.content.lower()
    if "i love grey" in raw_words or "i love gray" in raw_words :
        return True
    else :
        return False

def grey_death_checker(message) :
    #tokenize sentences
    raw_words = message.content.lower()
    sentences = sent_tokenize(raw_words)
    sentenceFlag = False

    #for every sentence, check if the sentece has the meaning 'grey is dead'
    for sentence in sentences:
        sentence = sentence.lower()
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

@bot.command()
async def mines(ctx, mapsizeX, mapsizeY, bombnum, aliases = ['mine', 'ms']) :
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

@bot.command()
async def echo(ctx):
    mention = ctx.message.mentions
    role_mention = ctx.message.role_mentions
    print(mention, role_mention)
    text = ctx.message.content[5:]
    if (not ("id" in mention or "id" in role_mention or "@here" in text)) :
        await ctx.send(text)

@bot.command(pass_context = True , aliases=['UwU'])
async def uwu(ctx):
    await ctx.message.delete()
    await ctx.send("<:greyUwU:790553515663163413>")

@bot.command(pass_context = True , aliases=['greypat', 'gpp', 'gp', 'GPP', 'GP'])
async def greypatpat(ctx):
    await ctx.message.delete()
    await ctx.send("<a:greypat:793768136859713546>")

@bot.command()
async def ping(ctx):
    await ctx.send("pong! {0}ms".format(round(bot.latency, 1)))

@bot.event
async def on_message(message):
    #check the message is not from itself
    if message.author == bot.user:
        return
    
    if grey_death_checker(message) :
        i = random.randint(0, len(NoU)-1)
        await message.channel.send(NoU[i])
    await bot.process_commands(message)

    if grey_love_checker(message) :
        await message.add_reaction(avilable_greymoji[random.randint(0,len(avilable_greymoji))])
    
    if "patpat" in message.content.lower() or "greypat" in message.content.lower() :
        await message.add_reaction('<a:greypat:793768136859713546>')

@bot.event
async def on_ready():
    print('logging in')
    print('connection was succesful')
    await bot.change_presence(status=discord.Status.online, activity=None)

bot.run(os.environ['token'])

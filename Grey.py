#3537984 : perm int

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
bot.remove_command('help')

#Answers
NoU = ["No U", "I am alive", "Grey is alive", "I didn't die", "You are a liar"]
avilable_greymoji = ["<:E_greyUwU:790553515663163413>", "<:E_greystare:789817320779546645>", "<:E_greynod:789817319760330794>", "<:E_greygiveme:789817320204664862>", "<a:E_greydontworryme:789817643297013770>"]
SOLDIER_CATMAID = ["But Soldier, you are a cat maid!", "I think soldier is a cat maid", "Soldier is a cat maid", "Soldier catmaid confirmed"]

#Server Emojis

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

@bot.command(pass_context = True , aliases=['UwU'])
async def uwu(ctx):
    await ctx.send("<:E_greyUwU:790553515663163413>")
    await ctx.message.delete()
    
@bot.command(pass_context = True , aliases=['greypat', 'gpp', 'gp', 'GPP', 'GP'])
async def greypatpat(ctx):
    await ctx.send("<a:E_greypat:793768136859713546>")
    await ctx.message.delete()
    
@bot.command()
async def ping(ctx):
    await ctx.send("pong! {0}ms".format(round(bot.latency, 1)))

@bot.command()
async def help(ctx):
    embed = discord.Embed(color = discord.Color.red())
    embed.set_author(name='Help')
    embed.add_field(name = '=mines x y z', value = "Make minesweeper, by size of x * y, with z mines.", inline = False)
    embed.add_field(name = '=uwu', value = "UwU", inline = False)
    embed.add_field(name = '=greypatpat, =gpp, =gp', value = "Grey will patpat to you!", inline = False)
    embed.add_field(name = '=ping', value = "Pong!", inline = False)
    embed.add_field(name = '=invite', value = "Make a invitation for your server.", inline = False)
    await ctx.send(embed = embed)

@bot.command()
async def invite(ctx):
    embed = discord.Embed(color = discord.Color.orange())
    embed.add_field(name = 'Invitation', value = "Click [Here](https://discord.com/oauth2/authorize?client_id=790571552345030686&scope=bot&permissions=3537984) to make Grey join your server!")

    await ctx.send(embed = embed)

@bot.event
async def on_message(message):
    #Check the message is not from itself
    if message.author == bot.user:
        return
    
    #Reply to "Grey is dead"
    if grey_death_checker(message) :
        i = random.randint(0, len(NoU)-1)
        await message.channel.send(NoU[i])
    await bot.process_commands(message)

    #Reply to "I love grey"
    if grey_love_checker(message) :
        await message.add_reaction(avilable_greymoji[random.randint(0,len(avilable_greymoji))])
    
    #soldier catmaid meme
    if message.author.id == 314358105205112834 :
        raw_words = message.content.lower()
        if (("no" in raw_words or "not" in raw_words) and ("maid" in raw_words or "cat" in raw_words)) :
            await message.channel.send(SOLDIER_CATMAID[random.randint(0,len(SOLDIER_CATMAID))]+ " <:greysmile:742805250469265409>")

    #Grey patpat feature
    if "patpat" in message.content.lower() or "greypat" in message.content.lower() :
        #Check if the message is from ZZ server
        if message.guild.id == 603246092402032670 :
            for role in message.author.roles :
                #Patpat role check
                if role.id == 765347466169024512 :
                    try:
                        await message.add_reaction('<a:E_greypat:793768136859713546>')
                    except :
                        pass
                    break
                else :
                    pass
        else :
            print("not in zz")
            await message.add_reaction('<a:E_greypat:793768136859713546>')

@bot.event
async def on_ready():
    print('logging in')
    print('connection was succesful')
    await bot.change_presence(status=discord.Status.online, activity=None)

bot.run(os.environ['token'])

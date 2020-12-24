#await ctx.send(text) : 텍스트 보내기
#await ctx.message.delete : 방금 보낸 텍스트 삭제
#bot.command 뒤에 (pass_context = True, aliases =[]) 으로 여러개의 명령어가 같은 역할 수행하게 할 수 있음

#Basics
import random

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
async def test(ctx, text):
    if (not text.startswith("@")) or (not text.startswith("\\")):
        await ctx.send(text)

@bot.command(pass_context = True , aliases=['UwU'])
async def uwu(ctx):
    await ctx.message.delete()
    await ctx.send("<:greyUwU:790553515663163413>")

@bot.command(pass_context = True , aliases=['greypat', 'gpp', 'gp', 'GPP', 'GP'])
async def greypatpat(ctx):
    await ctx.message.delete()
    await ctx.send("<a:patpat:790589898724868097>")

@bot.command()
async def ping(ctx):
    await ctx.send("pong! {0}ms".format(round(bot.latency, 1)))

@bot.event
async def on_message(message):
    print("activated onmessage")
    #check the message is not from itself
    if message.author == bot.user:
        return
    
    if grey_death_checker(message) :
        print("activated process")
        i = random.randint(0, len(NoU)-1)
        await message.channel.send(NoU[i])
    await bot.process_commands(message)

@bot.event
async def on_ready():
    print('logging in')
    print('connection was succesful')
    await bot.change_presence(status=discord.Status.online, activity=None)


bot.run(os.environ['token'])

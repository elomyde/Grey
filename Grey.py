<<<<<<< HEAD
#await ctx.send(text) : 텍스트 보내기
#await ctx.message.delete : 방금 보낸 텍스트 삭제
#bot.command 뒤에 (pass_context = True, aliases =[]) 으로 여러개의 명령어가 같은 역할 수행하게 할 수 있음

import random
import discord
from discord.ext import commands
from discord.ext import tasks
import os

bot = commands.Bot(command_prefix='=')
client = discord.Client()

NoU = ["No U", "I am alive", "Grey is alive", "I didn't die", "You are a liar"]

def grey_death_checker(message) :
    content = message.content.lower()
    contents = content.split()
    isGreyIn = False
    isDeathIn = False
    isNotIn = False

    for words in contents :
        if ('grey' in words or 'gray' in words) :
            isGreyIn = True
        
        if ('dead' in words or 'die' in words) :
            isDeathIn = True
        
        if ('alive' in words) :
            isDeathIn = True
            isNotIn = not isNotIn
        
        if ('not' in words or "n\'t" in words):
            if words == "notn\'t" :
                continue
            isNotIn = not isNotIn
    
    return isGreyIn and isDeathIn and not isNotIn

@bot.command()
async def test(ctx, text):
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


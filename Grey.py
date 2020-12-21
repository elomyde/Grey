#await ctx.send(text) : 텍스트 보내기
#await ctx.message.delete : 방금 보낸 텍스트 삭제
#bot.command 뒤에 (pass_context = True, aliases =[]) 으로 여러개의 명령어가 같은 역할 수행하게 할 수 있음

import discord
from discord.ext import commands
import os

bot = commands.Bot(command_prefix='=')
client = discord.Client()

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

@bot.event
async def on_ready():
    print('logging in')
    print('connection was succesful')
    await bot.change_presence(status=discord.Status.online, activity=None)

bot.run(os.environ['token'])


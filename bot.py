from discord.ext import commands
import os
import random
import discord
import requests

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
bot.videos = [
  'https://www.youtube.com/watch?v=XmoKM4RunZQ',
  'https://www.youtube.com/watch?v=qTmjKpl2Jk0',
  'https://www.youtube.com/watch?v=hY7m5jjJ9mM'
]
bot.happyList = []


@bot.command()
async def hello(ctx):
  await ctx.send("hello " + ctx.author.display_name)


@bot.command()
async def cat(ctx):
  await ctx.send(random.choice(bot.videos))


# * used to allow user to input
# item variable is what stores user input
@bot.command()
async def happy(ctx, *, item):
  await ctx.send("Aight got it!")
  bot.happyList.append(item)
  print(bot.happyList)


@bot.command()
async def sad(ctx):
  print("Hope you feel better!")
  await ctx.send(random.choice(bot.happyList))


@bot.command()
async def calc(ctx, x, fn, y):
  x = float(x)
  y = float(y)
  if fn == '+':
    await ctx.send(x + y)
  elif fn == '-':
    await ctx.send(x - y)
  elif fn == '*':
    await ctx.send(x * y)
  elif fn == '/':
    await ctx.send(x / y)
  else:
    await ctx.send("Operation not supported")


@bot.command()
async def weather(ctx, *, item):
  url = "https://weatherapi-com.p.rapidapi.com/current.json"
  querystring = {"q": item}
  headers = {
    "X-RapidAPI-Key": "e68f6c4d38msh54f97756455af10p154872jsn68a36fe73521",
    "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
  }
  response = requests.get(url, headers=headers, params=querystring)
  output = response.json()
  await ctx.send(output['current']['condition']['text'])

with open("BOT_TOKEN.txt", "r") as token_file:
    TOKEN = token_file.read()
    print("Token file read")
    bot.run(TOKEN)
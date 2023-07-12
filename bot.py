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
api_key = ""

with open("RAPIDAPI_KEY.txt", "r") as api_file:
    api_key = api_file.read()
    print("API key read")

@bot.command()
async def hello(ctx):
  await ctx.send("hello " + ctx.author.display_name)


@bot.command()
async def cat(ctx):
  await ctx.send(random.choice(bot.videos))


# * used to allow user to input multiple unknown inputs
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
async def current_weather(ctx, *, item):
  url = "https://weatherapi-com.p.rapidapi.com/current.json"
  querystring = {"q": item}
  headers = {
    "X-RapidAPI-Key": api_key,
    "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
  }
  response = requests.get(url, headers=headers, params=querystring)
  output = response.json()
  await ctx.send(output['current']['condition']['text'])

@bot.command()
async def wind_speed(ctx, *, item):
  url = "https://weatherapi-com.p.rapidapi.com/current.json"
  querystring = {"q": item}
  headers = {
    "X-RapidAPI-Key": api_key,
    "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
  }
  response = requests.get(url, headers=headers, params=querystring)
  output = response.json()
  sp_kph = output['current']['wind_kph']
  sp_mph = output['current']['wind_mph']
  kph = str(sp_kph) + " kph"
  mph = str(sp_mph) + " mph"
  await ctx.send(kph + ", " + mph)

@bot.command()
async def weather_forecast_tomorrow(ctx, *, item):
  url = "https://weatherapi-com.p.rapidapi.com/forecast.json"
  querystring = {"q":item,"dt":1}
  headers = {
    "X-RapidAPI-Key": api_key,
    "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
  }
  response = requests.get(url, headers=headers, params=querystring)
  # print(response.json())
  output = response.json()
  conditions = output['forecast']['forecastday'][0]['day']['condition']['text']
  mt = output['forecast']['forecastday'][0]['day']['maxtemp_c']
  max_temp = str(mt) + " degrees celsius"
  mt2 = output['forecast']['forecastday'][0]['day']['mintemp_c']
  min_temp = str(mt2) + " degrees celsius"
  cor = output['forecast']['forecastday'][0]['day']['daily_chance_of_rain']
  cos = output['forecast']['forecastday'][0]['day']['daily_chance_of_snow']
  await ctx.send(conditions)
  await ctx.send("Maximum temperature: " + max_temp)
  await ctx.send("Minimum temperature: " + min_temp)
  await ctx.send("Chance of rain: " + str(cor) + "%")
  await ctx.send("Chance of snow: " + str(cos) + "%")

@bot.command()
async def translate(ctx, *, input):
  url = "https://nlp-translation.p.rapidapi.com/v1/translate"
  input = input.strip()
  words = input.split()
  target_lang = words[-1]
  original_lang = words[-2]
  tex = input[:-5]
  querystring = {"text":tex,"to":target_lang,"from":original_lang}
  headers = {
    "X-RapidAPI-Key": api_key,
    "X-RapidAPI-Host": "nlp-translation.p.rapidapi.com"
  }
  response = requests.get(url, headers=headers, params=querystring)
  print(response.json())
  output = response.json()
  await ctx.send(output['translated_text'][target_lang])

with open("BOT_TOKEN.txt", "r") as token_file:
    TOKEN = token_file.read()
    print("Token file read")
    bot.run(TOKEN)
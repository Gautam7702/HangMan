import discord
import os
import random
from replit import db
import requests
from discord.ext import commands
from keep_alive import keep_alive

bot = commands.Bot(command_prefix='#')
token = os.environ['token']


def func7(guess,ctx):
  already_guessed = db[f'{ctx.guild.id}']["already_guessed"]
  if guess.lower() in already_guessed:
    return False
  return True

def change(ctx):
  if db[f'{ctx.guild.id}']["game_play"] == True:
    finaldic  =dict(db[f'{ctx.guild.id}']["tl"])
    sortdic = sorted(finaldic.items(), key=lambda x: x[1], reverse=True)
    db[f'{ctx.guild.id}']["tl"] = dict(sortdic)
    pdic = db[f'{ctx.guild.id}']["pl"]
    for i in finaldic.keys():
      if i in pdic.keys():
        pdic[i]+=finaldic[i]
      else:
        pdic[i] = finaldic[i]
    db[f'{ctx.guild.id}']["pl"] = pdic 
  db[f'{ctx.guild.id}']["game_play"] =  not db[f'{ctx.guild.id}']["game_play"]


def check_guess(guess,ctx):
  movie = db[f'{ctx.guild.id}']["movie"]
  movie_name = db[f'{ctx.guild.id}']["movie_name"]
  already_guessed =  db[f'{ctx.guild.id}']["already_guessed"]
  s = ""
  already_guessed.append(guess.lower())
  db[f'{ctx.guild.id}']["already_guessed"] = already_guessed

  if guess.upper()==movie_name.upper():
    movie = movie_name
    db[f'{ctx.guild.id}']["movie"] = movie
    return True

  
  if guess.upper() not in movie_name.upper():
    return False
   
  for i in range(len(movie_name)):
    if movie_name[i].upper()==guess.upper():
      s += guess
    else:
      s +=movie[i]
  movie = s
  db[f'{ctx.guild.id}']["movie"] = movie
  return True

  
def get_movie(ctx):
  x = random.randint(1,6)
  response =  requests.get(f'https://api.themoviedb.org/3/discover/movie?api_key=9b9f4fee49df8e527a202a5d46be2703&language=en-US&sort_by=popularity.desc&include_adult=true&include_video=false&page={x}&with_watch_monetization_types=flatrate')
  d = response.json()
  x =  random.randint(1,20)
  movie_name = d["results"][x-1]["title"]
  db[f'{ctx.guild.id}']["movie_name"] = movie_name
  movie = ""
  for i in movie_name:
    if i in [".","-"," ",":","+"]:
      movie += i
    else:
      movie += "\u2605"  
  return movie


@bot.event
async def on_ready():
  print(f"{bot.user.name} is connected")


@bot.command(name='game',help=': This starts the game')
async def func1(ctx):
  emptydic = {

    }
  if f'{ctx.guild.id}' not in db.keys():
    
    dic = {
      'game_play': False,
      'movie': "",
      'movie_name':"",
      'already_guessed':[],
      'tl':emptydic,
      'pl':emptydic
    }
    db[f'{ctx.guild.id}'] = dic

  if not db[f'{ctx.guild.id}']["game_play"]:
    dic = db[f'{ctx.guild.id}']
    if 'pl' not in dic.keys():
      dic['pl'] = emptydic
      db[f'{ctx.guild.id}'] = dic
    tempdic = db[f'{ctx.guild.id}']['pl']
    dic = {
      'game_play': False,
      'movie': "",
      'movie_name':"",
      'already_guessed':[],
      'tl': emptydic,
      'pl':tempdic
    }
    db[f'{ctx.guild.id}'] = dic
    change(ctx)
    movie = get_movie(ctx)
    db[f'{ctx.guild.id}']["movie"] = movie
    print(movie)
    await ctx.send(movie)
  else: 
    await ctx.send("A game is already going on. Quit the game or guess!")
  

@bot.command(name='g',help=': this command is used to guess letter of the movie')
async def func2(ctx,*,guess):
  name  = ctx.message.author.name
  point =0
  if db[f'{ctx.guild.id}']["game_play"]:
    if func7(guess,ctx): 
      if check_guess(guess,ctx):
        if  db[f'{ctx.guild.id}']["movie"]==db[f'{ctx.guild.id}']["movie_name"]:
          point = 15
        else:
          point = 5
        await ctx.send(f'Correct Guess!! {name} gets {point} points')
      else:
        point  = -5
        await ctx.send(f'Incorrect Guess!! {name} gets {point} points')
      movie = db[f'{ctx.guild.id}']["movie"]
      movie_name = db[f'{ctx.guild.id}']["movie_name"]
      print(movie)
      await ctx.send(movie)
      tempdic = db[f'{ctx.guild.id}']["tl"]
      if name in tempdic.keys():
        tempdic[name] +=point
      else:
        tempdic[name] = point
      db[f'{ctx.guild.id}']["tl"] =tempdic
      if db[f'{ctx.guild.id}']["movie"].lower()==db[f'{ctx.guild.id}']["movie_name"].lower():
        change(ctx)
        finaldic = db[f'{ctx.guild.id}']["tl"]
        j=1
        for i in finaldic:
          await ctx.send(f'{j}: {i} -> {finaldic[i]}')
          j+=1
    else:
      await ctx.send("Already Guessed")
  else:
    await ctx.send("First create a game - u boomer")


@bot.command(name='quit',help=': this will quit the game')
async def func5(ctx):
  if db[f'{ctx.guild.id}']["game_play"]:
    movie_name = db[f'{ctx.guild.id}']["movie_name"]
    change(ctx)
    await ctx.send(movie_name)
    finaldic = db[f'{ctx.guild.id}']["tl"]
    j=1
    for i in finaldic:
      await ctx.send(f'{j}: {i} -> {finaldic[i]}')
      j+=1
  else:
    await ctx.send("First create a game")

@bot.command(name='lb',help=': this command will give u the leader board')
async def func3(ctx):
    finaldic  =dict(db[f'{ctx.guild.id}']["pl"])
    finaldic = sorted(finaldic.items(), key=lambda x: x[1], reverse=True)
    finaldic =  dict(finaldic)
    j=1
    for i in finaldic:
      await ctx.send(f'{j}: {i} -> {finaldic[i]}')
      j+=1
  
keep_alive()
bot.run(token)
import discord
import os
import random
from replit import db
import requests
from discord.ext import commands
from keep_alive import keep_alive

bot = commands.Bot(command_prefix='#')
token = os.environ['token']


def func7(guess,ctx):
  already_guessed = db[f'{ctx.guild.id}']["already_guessed"]
  if guess.lower() in already_guessed:
    return False
  return True

def change(ctx):
  if db[f'{ctx.guild.id}']["game_play"] == True:
    finaldic  =dict(db[f'{ctx.guild.id}']["tl"])
    sortdic = sorted(finaldic.items(), key=lambda x: x[1], reverse=True)
    db[f'{ctx.guild.id}']["tl"] = dict(sortdic)
    pdic = db[f'{ctx.guild.id}']["pl"]
    for i in finaldic.keys():
      if i in pdic.keys():
        pdic[i]+=finaldic[i]
      else:
        pdic[i] = finaldic[i]
    db[f'{ctx.guild.id}']["pl"] = pdic 
  db[f'{ctx.guild.id}']["game_play"] =  not db[f'{ctx.guild.id}']["game_play"]


def check_guess(guess,ctx):
  movie = db[f'{ctx.guild.id}']["movie"]
  movie_name = db[f'{ctx.guild.id}']["movie_name"]
  already_guessed =  db[f'{ctx.guild.id}']["already_guessed"]
  s = ""
  already_guessed.append(guess.lower())
  db[f'{ctx.guild.id}']["already_guessed"] = already_guessed

  if guess.upper()==movie_name.upper():
    movie = movie_name
    db[f'{ctx.guild.id}']["movie"] = movie
    return True

  
  if guess.upper() not in movie_name.upper():
    return False
   
  for i in range(len(movie_name)):
    if movie_name[i].upper()==guess.upper():
      s += guess
    else:
      s +=movie[i]
  movie = s
  db[f'{ctx.guild.id}']["movie"] = movie
  return True

  
def get_movie(ctx):
  x = random.randint(1,6)
  response =  requests.get(f'https://api.themoviedb.org/3/discover/movie?api_key=9b9f4fee49df8e527a202a5d46be2703&language=en-US&sort_by=popularity.desc&include_adult=true&include_video=false&page={x}&with_watch_monetization_types=flatrate')
  d = response.json()
  x =  random.randint(1,20)
  movie_name = d["results"][x-1]["title"]
  db[f'{ctx.guild.id}']["movie_name"] = movie_name
  movie = ""
  for i in movie_name:
    if i in [".","-"," ",":","+"]:
      movie += i
    else:
      movie += "\u2605"  
  return movie


@bot.event
async def on_ready():
  print(f"{bot.user.name} is connected")


@bot.command(name='game',help=': This starts the game')
async def func1(ctx):
  emptydic = {

    }
  if f'{ctx.guild.id}' not in db.keys():
    
    dic = {
      'game_play': False,
      'movie': "",
      'movie_name':"",
      'already_guessed':[],
      'tl':emptydic,
      'pl':emptydic
    }
    db[f'{ctx.guild.id}'] = dic

  if not db[f'{ctx.guild.id}']["game_play"]:
    dic = db[f'{ctx.guild.id}']
    if 'pl' not in dic.keys():
      dic['pl'] = emptydic
      db[f'{ctx.guild.id}'] = dic
    tempdic = db[f'{ctx.guild.id}']['pl']
    dic = {
      'game_play': False,
      'movie': "",
      'movie_name':"",
      'already_guessed':[],
      'tl': emptydic,
      'pl':tempdic
    }
    db[f'{ctx.guild.id}'] = dic
    change(ctx)
    movie = get_movie(ctx)
    db[f'{ctx.guild.id}']["movie"] = movie
    print(movie)
    await ctx.send(movie)
  else: 
    await ctx.send("A game is already going on. Quit the game or guess!")
  

@bot.command(name='g',help=': this command is used to guess letter of the movie')
async def func2(ctx,*,guess):
  name  = ctx.message.author.name
  point =0
  if db[f'{ctx.guild.id}']["game_play"]:
    if func7(guess,ctx): 
      if check_guess(guess,ctx):
        if  db[f'{ctx.guild.id}']["movie"]==db[f'{ctx.guild.id}']["movie_name"]:
          point = 15
        else:
          point = 5
        await ctx.send(f'Correct Guess!! {name} gets {point} points')
      else:
        point  = -5
        await ctx.send(f'Incorrect Guess!! {name} gets {point} points')
      movie = db[f'{ctx.guild.id}']["movie"]
      movie_name = db[f'{ctx.guild.id}']["movie_name"]
      print(movie)
      await ctx.send(movie)
      tempdic = db[f'{ctx.guild.id}']["tl"]
      if name in tempdic.keys():
        tempdic[name] +=point
      else:
        tempdic[name] = point
      db[f'{ctx.guild.id}']["tl"] =tempdic
      if db[f'{ctx.guild.id}']["movie"].lower()==db[f'{ctx.guild.id}']["movie_name"].lower():
        change(ctx)
        finaldic = db[f'{ctx.guild.id}']["tl"]
        j=1
        for i in finaldic:
          await ctx.send(f'{j}: {i} -> {finaldic[i]}')
          j+=1
    else:
      await ctx.send("Already Guessed")
  else:
    await ctx.send("First create a game - u boomer")


@bot.command(name='quit',help=': this will quit the game')
async def func5(ctx):
  if db[f'{ctx.guild.id}']["game_play"]:
    movie_name = db[f'{ctx.guild.id}']["movie_name"]
    change(ctx)
    await ctx.send(movie_name)
    finaldic = db[f'{ctx.guild.id}']["tl"]
    j=1
    for i in finaldic:
      await ctx.send(f'{j}: {i} -> {finaldic[i]}')
      j+=1
  else:
    await ctx.send("First create a game")

@bot.command(name='lb',help=': this command will give u the leader board')
async def func3(ctx):
    finaldic  =dict(db[f'{ctx.guild.id}']["pl"])
    finaldic = sorted(finaldic.items(), key=lambda x: x[1], reverse=True)
    finaldic =  dict(finaldic)
    j=1
    for i in finaldic:
      await ctx.send(f'{j}: {i} -> {finaldic[i]}')
      j+=1
  
keep_alive()
bot.run(token)

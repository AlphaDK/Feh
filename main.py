#Feh v1.4.2, a Discord bot by AlphaDK#2649
#v0.1 created 9/10/17 (the 9th of October, not the 10th of September you silly Americans)
#v1.0 released 19/10/17
#Does Fire Emblem: Heroes stuff
#Made originally for Mike's Discord, just to link tweets
#Special thanks: Struct, D'Amour, Boggy, 3AM, Mike, StackOverflow, Intelligent Systems, Nintendo

import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import random
import time
import tweepy
import fileinput
import pytz
from datetime import datetime
from secret import *

from commands import CommandHandler

loop = asyncio.get_event_loop()

auth = tweepy.OAuthHandler(TWITTER_AUTH1, TWITTER_AUTH2)
auth.set_access_token(TWITTER_ACCESS1, TWITTER_ACCESS2)

api = tweepy.API(auth)
client = discord.Client()

mainhasbeenrunoncealready = False #So if the bot loses connection to Discord due to server outages on their end or something, it'll rerun on_ready() again. This is undesired behaviour, as it causes things like double posting of the daily reset, and this is the lowest effort solution to this problem, it'll set this to True once main() has been run once.

#Tells the user they messed up
async def error(message):
    if message.author.id == "188123523691053060": #Yellow
        await client.send_message(message.channel, "<@188123523691053060> I don't think you typed that correctly! Classic yellow.")
    elif message.author.id == "126197907392167937": #Me
        await client.send_message(message.channel, "lol alpha doesn't know how to use his own bot")
    else: #@everyone else
        await client.send_message(message.channel, "<@" + message.author.id + "> I don't know what you mean! If you think I should, use !report to tell Alpha to fix it")

def post_daily():
    loop.call_later(86400, post_daily) #86400 seconds is 24 hours, ie just call it again in a day.
    asyncio.ensure_future(client.send_message(client.get_channel("333859340253396992"), "<:feh:344700243910197259> It's time for the daily reset!"))
    days = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
    shards = {0: "random", 1: "Scarlet", 2: "Azure", 3: "Verdant", 4: "Transparent", 5: "random", 6: "random"}
    sp = {0: "", 1: "", 2: "", 3: "", 4: "\nDouble SP weekend starts now!", 5: "\nDouble SP weekend is in effect!", 6: "\nDouble SP weekend is over!"}
    asyncio.ensure_future(client.send_message(client.get_channel("333859340253396992"), "It's " + days[datetime.today().weekday()] + ", so the Training Tower has " + shards[datetime.today().weekday()] + " badges!\nRemember to log in and do your dailies!" + sp[datetime.today().weekday()]))

async def check_tweets(lastnews, lastgauntlet):
    while True:
        tweetsnews = api.user_timeline("FEHeroes_News", since_id=lastnews)
        tweetsgauntlet = api.user_timeline("FEHGauntletBot", since_id=lastgauntlet)
        for tweet in tweetsnews[::-1]: #Reads tweets from timeline in chronological order, since api.user_timeline gives them in reverse chronological
            await client.send_message(client.get_channel("333859340253396992"), "@FEHeroes_News: <http://twitter.com/FEHeroes_News/status/" + str(tweet.id) + ">\n" + str(tweet.text))
            lastnews = tweet.id
        for tweet in tweetsgauntlet[::-1]:
            if "is losing with" in tweet.text: #So, I don't think we need the exact link to run-of-the-mill updates. I'll leave the link for the rest though
                await client.send_message(client.get_channel("333859340253396992"), str(tweet.text).split("(")[0][:-1]) #In fact, get rid of that (Round X Hour Y) stuff too I think it's pretty obvious within Discord's context
            else:
                await client.send_message(client.get_channel("333859340253396992"), "@FEHGauntletBot: <http://www.twitter.com/FEHGauntletBot/status/" + str(tweet.id) + ">\n" + str(tweet.text))
            lastgauntlet = tweet.id
        await asyncio.sleep(60) #Checks both accounts once a minute, could be more often but I'll respect the Twitter API gods and their 100 requests/15 minutes rate limit

@asyncio.coroutine
def main(lastnews, lastgauntlet):
    now = datetime.now(pytz.utc) #Checks UTC's current time, since that's you know, where the game is based off and doesn't have daylight savings
    seconds_delta = (now.replace(hour=7, minute=0, second=0, microsecond=5) - now).total_seconds() % 86400 #Figures out how long until 7AM the next day, microseconds are just so it doesn't post at 6:59AM instead
    loop.call_later(seconds_delta, post_daily)
    yield from asyncio.ensure_future(check_tweets(lastnews, lastgauntlet))

@client.event
async def on_ready():
    print("Feh v1.4.2 online")
    global mainhasbeenrunoncealready
    if not mainhasbeenrunoncealready:
        mainhasbeenrunoncealready = True
        await client.change_presence(game=discord.Game(name="Fire Emblem: Heroes"))
        lastnews = api.user_timeline("FEHeroes_News", count=1)
        lastnews = lastnews[0].id #These check the most recent tweet from each account, since we only care about tweets yet to happen
        lastgauntlet = api.user_timeline("FEHGauntletBot", count=1)
        lastgauntlet = lastgauntlet[0].id
        asyncio.ensure_future(main(lastnews, lastgauntlet))
    
@client.event
async def on_message(message):
    if message.author.bot:
        return

    cmd_handler = CommandHandler(client, message)
    await cmd_handler.handle_commands()

    if "\N{NERD FACE}" in message.content: #nerd into feh is a true combo
        await client.add_reaction(message, "feh:344700243910197259")
    
    if message.content.lower().startswith("!draug") or message.content.lower().startswith("!knowyourdraug"): #Source: reddit, it's important to be familiar with Draug and his variants
        await client.send_file(message.channel, "draug.jpg")
    elif message.content.lower().startswith("!fehhelp"):
        await client.send_message(message.channel, "Hi! I'm Feh (v1.4.2), a bot created to help out with Fire Emblem: Heroes content! <:feh:344700243910197259>\nI can provide information to you about various weapons, skills or units! Try {{Quickened Pulse}}!\nIf you have any suggestions for improvements or if I'm broken, tell AlphaDK!\n(Use `!report [issue]` and I'll let him know)")
    elif message.content.lower().startswith("!report "):
        await client.send_message(client.get_channel("368631261071147009"), str(message.author) + " (" + message.author.id + ") in " + str(message.channel) + " (" + message.channel.id  + ") from " + message.server.name + ": " + str(message.content[8:]))
        await client.send_message(message.channel, "I've reported the issue! We hope you continue to enjoy Fire Emblem! Heroes.")
    elif message.content.lower().startswith("<@366885945846267906> what "): #Legit just picks random skills it's not useful lmao
        skill = message.content[27:]
        if skill.lower().startswith("sacred seal") or skill.lower().startswith("seal"):
            doc = "seals.txt"
        elif skill.lower().startswith("a slot") or skill.lower().startswith("a skill"):
            doc = "a.txt"
        elif skill.lower().startswith("b slot") or skill.lower().startswith("b skill"):
            doc = "b.txt"
        elif skill.lower().startswith("c slot") or skill.lower().startswith("c skill"):
            doc = "c.txt"
        try:
            with open(doc) as skills:
                options = skills.readlines()
                option = options[random.randint(0, len(options)-2)][:-1]
                await client.send_message(message.channel, "<@" + message.author.id + "> " + option)
        except UnboundLocalError: #This will proc if they don't say a skill/seal/c slot etc
            asyncio.ensure_future(error(message))
    elif message.content.startswith("!playing ") and message.author.id == "126197907392167937": #Here starts the commands only I can use, this one is just to change the game Feh is playing
        playtype = message.content[9]
        gaem = message.content[11:]
        await client.change_presence(game=discord.Game(name=gaem, url="http://twitch.tv/Nintendude92", type=int(playtype)))
    elif message.content.startswith("!say ") and message.author.id == "126197907392167937": #Lets me talk to #feheroes, that's it
        messag = message.content[5:]
        await client.send_message(client.get_channel("333859340253396992"), messag)
    elif message.content.startswith("!typing") and message.author.id == "126197907392167937": #This one just sucks I barely use it
        await client.send_typing(client.get_channel("333859340253396992"))

client.run(DISCORD_CLIENT_ID)         

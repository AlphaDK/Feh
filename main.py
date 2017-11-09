#Feh v1.4.1, a Discord bot by AlphaDK#2649
#v0.1 created 9/10/17 (the 9th of October, not the 10th of September you silly Americans)
#v1.0 released 19/10/17
#v1.5 released publically ??/??/??
#Does Fire Emblem: Heroes stuff
#Made originally for Mike's Discord, just to link tweets
#Special thanks: Struct, Boggy, D'Amour, Mike, StackOverflow, Intelligent Systems, Nintendo

import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import random
import time
import tweepy
import re #only
import fileinput
import pytz
from datetime import datetime
from secret import *

import commands

loop = asyncio.get_event_loop()

auth = tweepy.OAuthHandler(TWITTER_AUTH1, TWITTER_AUTH2)
auth.set_access_token(TWITTER_ACCESS1, TWITTER_ACCESS2)

api = tweepy.API(auth)
client = discord.Client()

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
    print("Feh v1.4.1 online")
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

    if "\N{NERD FACE}" in message.content: #nerd into feh is a true combo
        await client.add_reaction(message, "feh:344700243910197259")
    if "{{" in message.content and "}}" in message.content:
        colourtypes = {"red": 0xD92242, "green": 0x0CA428, "blue": 0x2763D6, "grey": 0x63737B, "cyan": 0x28EFEF, "purple": 0xA012ED, "yellow": 0xDEC027, "orange": 0xEA803F}
        start = "{{"
        end = "}}"
        query = re.search("%s(.*)%s" % (start, end), message.content).group(1).lower() #This just gets the part between {{ and }} to be used for checking
        skills = {}
        colourdict = {}
        printas = {}
        skilltype = {}
        with open("skills.txt") as f:
            for line in f:
                (key, val, colourtype, aka, skill) = line.split("|") #These get the arguments for each line in the document, and arrange them into dictionaries
                skills[key] = val
                colourdict[key] = colourtype
                printas[key] = aka
                skilltype[key] = skill
        try:
            skill = skills[query].split("$")
            sk = ""
            for arg in skill: #Newline can't be read from the document directly, so $ is used instead and is replaced into newline here. Don't ask me why this has to work like this
                sk = sk + arg + "\n"
            sk = sk[:-1]
            emb = discord.Embed(title=printas[query], description=sk, colour=int(colourtypes[colourdict[query]]))
            emb.set_author(name=skilltype[query][:-1], icon_url="https://i.imgur.com/CyaOfZE.png")
            await client.send_message(message.channel, embed=emb)
        except KeyError:
            asyncio.ensure_future(error(message)) #This will post if the queried phrase isn't found in the text document, most of the time it's just joke but better to let them know than to not respond
    if message.content.lower().startswith("!sit"): #Copypasta source: Nintendude92, informing people how to spend orbs wisely
        await client.send_message(message.channel, "Sit for a few days\nThe play for f2p is high key pull lastish day of the banner with a big stack when you know you don't want to play the next one\nYou'd all probably hit way more and save orbs\nThere has been a single banner that we didn\'t get prelaunch info for")
    elif message.content.lower().startswith("!selena"): #Copypasta source: 3AM, informing people of why he uses Selena
        await client.send_message(message.channel, "So for me I think I would use Selena just because I freaking like her. I mean sure she's overlooked but that does not stop me. Her flaws do not freaking stop me from using her. I use her and that's that. I think I'm good with knowing how to roll with her. I'm just a guy who wants to play this game for fun with any hero regardless if they're good or bad.")
    elif message.content.lower().startswith("!6k"): #Copypasta source: Some people say Boggy but I think it was just someone in Twitch chat excited about their tobin
        await client.send_message(message.channel, "i got to 6k today! I just got my first tobin, I really hope I don't miss out on this seal, it looks very good and I'm new to this game VoHiYo")
    elif message.content.lower().startswith("!30k"): #Copypasta source: This one's Boggy, after yellow was curious why there was no 30k command. Boggy was disappointed that I told him we couldn't force one
        await client.send_message(message.channel, "What do you mean you can't force 30k, are you trying to say something to me, to my face?! To my pride?! TO MY LEGACY?!? I will have you know 6k isn't the only thing I can smash but I can also get the 5* Arden and I will reach tier 20. No, I won't reach tier 20, I will ascend with Arden to tiers people cannot comprehend. Together, Arden and his guidance 1 seal will carry me into the heavens of tier 21, where Arden can run down Brave Lyn like the Brave Syn she is. Welcome to the new age, eat your hardt out.")
    elif message.content.lower().startswith("!didntgetquickenedpulse") or message.content.lower().startswith("!didntgetqp"): #Copypasta source: Also Boggy, letting Mike know how not-disappointed he was when he missed Quickened Pulse by less than 100 points
        await client.send_message(message.channel, "Hello Mike, it is I, Mr. I-Didn't-Get-Quickened-Pulse, here to tell you what a wonderful life it is for me. The sun is always shining over here in Tier 17, and all my -atk/-spd units are smiling, and the fact I don't have Quickened Pulse only adds onto the boons of existence. You see, unlike you, I only need to choose 4 out of __**5**__ of my seals rather than 6, by god, I can only imagine your pain. Especially with only 4 units per team, what's even the point of having a 6th seal like Quickened Pulse, I see no real point, it only adds to the pain of choice. So you may laugh at the fact I may have missed QP by 13 points at the last minute, but I, my good sir, am delighted that whatever god was looking down on me that day, knew exactly how to make my Fire Emblem: Heroes gacha life better. Good day and hats off to you chap!")
    elif message.content.lower().startswith("!draug") or message.content.lower().startswith("!knowyourdraug"): #Source: reddit, it's important to be familiar with Draug and his variants
        await client.send_file(message.channel, "draug.jpg")
    elif message.content.lower().startswith("!pat") or message.content.lower().startswith("!headpat") or message.content.lower().startswith("!pet") or message.content.lower().startswith("!halfp"): #Source: Trashy asked if Feh accepted headpats.
        if message.content.lower().startswith("!halfp"):
            await client.send_message(message.channel, "Thanks!")
        else:
            await client.send_message(message.channel, "Thanks! ^_^")
        with open("pats.txt") as pats: #Then I track stats for how many times everyone's pat Feh for no good reason. Mostly just a thing I wanted to try doing
            patcount = {}
            for line in pats:
                (user, count) = line.split("|")
                patcount[user] = count
            pats.close()
            if message.author.id in patcount:
                with open("pats.txt", "r+") as pats:
                    data = pats.readlines()
                bata = data
                i = 0
                for line in data:
                    bata[i] = data[i]
                    if line.startswith(str(message.author.id)):
                        numbb = line.split("|")
                        if message.content.lower().startswith("!halfp"): #A head pat is a head pat, you can't just call it a half. Works surprisingly well
                            half = 0.5
                        else:
                            half = 1
                        line = str(message.author.id) + "|" + str(float(numbb[1])+half)
                        if line.endswith(".0"): #I only want the decimal to be there if it's a half, and float makes everything a decimal
                            line = line[:-2] + "\n"
                        else:
                            line += "\n"
                        bata[i] = line
                    i += 1
                with open("pats.txt", "w") as pats:
                    pats.writelines(bata)
            else: #If the user hasn't pet Feh, there's nothing to add to, so they get chucked on at the end of the document
                with open("pats.txt", "a") as pats:
                    if message.content.lower().startswith("!halfp"):
                        pats.write(str(message.author.id) + "|0.5\n")
                    else:
                        pats.write(str(message.author.id) + "|1\n")
    elif message.content.lower().startswith("!checkpets") or message.content.lower().startswith("!checkpats"): #Just tells them how many pats they have. I'm currently winning with 2^21 pats, my favourite number
        patcounts = {}
        with open("pats.txt") as pats:
            for line in pats:
                (user, count) = line.split("|")
                patcounts[user] = str(count)[:-1]
        if message.author.id not in patcounts: #Believe it or not, it didn't occur to me at first that people might try to check before petting, thankfully nobody tried it
            await client.send_message(message.channel, "<@" + message.author.id + "> You haven't pet Feh yet :(")
        else:
            if patcounts[message.author.id] == "1": #Grammar is IMPORTANT!
                tim = " time!"
            else:
                tim = " times!"
            await client.send_message(message.channel, "<@" + message.author.id + "> You've pet Feh " + str(patcounts[message.author.id]) + tim)
    elif message.content.lower().startswith("!fehhelp"):
        await client.send_message(message.channel, "Hi! I'm Feh (v1.4.1), a bot created to help out with Fire Emblem: Heroes content! <:feh:344700243910197259>\nI can provide information to you about various weapons, skills or units! Try {{Quickened Pulse}}!\nIf you have any suggestions for improvements or if I'm broken, tell AlphaDK!\n(Use `!report [issue]` and I'll let him know)")
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
        gaem = message.content[9:]
        await client.change_presence(game=discord.Game(name=gaem))
    elif message.content.startswith("!say ") and message.author.id == "126197907392167937": #Lets me talk to #feheroes, that's it
        messag = message.content[5:]
        await client.send_message(client.get_channel("333859340253396992"), messag)
    elif message.content.startswith("!typing") and message.author.id == "126197907392167937": #This one just sucks I barely use it
        await client.send_typing(client.get_channel("333859340253396992"))

client.run(DISCORD_CLIENT_ID)           

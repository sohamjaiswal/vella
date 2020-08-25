import requests
import random
import os
import configparser
import discord
import time
import json
import lavalink
import urbandictionary as ud
from discord import utils
from PyDictionary import PyDictionary
from pathlib import Path
from discord.ext import commands
from discord.errors import *
from discord import Embed
from discord.ext.commands import *

dictionary = PyDictionary()

client = discord.Client()

if os.path.isfile('register.json') :
    saves = open("register.json", "r")
    register = json.loads(saves.readlines().pop())
    saves.close()
else:
    register = {}
    saves = open("register.json", "w+")

config = configparser.ConfigParser()
config.read('config.ini')

owmAPI = config['OWM']['api_key']

prefix = config['DISCORD']['prefix']
client = commands.Bot(command_prefix=config['DISCORD']['prefix'])

def debit(message, amt):
    register[str(message.author)] -= amt

def credit(message, amt):
    register[str(message.author)] += amt

def saveup():
    saves = open("register.json", "a+")
    saves.write('\n')
    save = json.dumps(register)
    saves.write(save)

def lava():
    global client
    client.music = lavalink.Client(client.user.id)
    client.music.add_node('localhost', 6942, 'testing', 'na', 'music-node')
    client.add_listener(client.music.voice_update_handler, 'on_socket_response')
    client.music.add_event_hook(track_hook)

def mcheck(m):
    return m.author.id == m.author.id

def wordsearch(word):
    meaning = str(dictionary.meaning(word))
    if meaning != 'None':
        return meaning
    else:
        return "Could not find the meaning :cry:"

async def track_hook(event):
    if isinstance(event, lavalink.events.QueueEndEvent):
      guild_id = int(event.player.guild_id)
      await connect_to(guild_id, None)
      
async def connect_to(guild_id: int, channel_id: str):
    ws = client._connection._get_websocket(guild_id)
    await ws.voice_state(str(guild_id), channel_id)

def stringformer(listlol):
    string = ''
    for element in listlol:
        string = string + str(element) + ' '
    return(string)

@client.event
async def on_ready():
    lava()
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(name="Fall Guys"))

@client.event
async def on_message(message):

    def checker(message):
        yield (message.author in message.mentions)



    if str(message.author) not in register.keys():
        register[str(message.author)] = 1
    else:
        register[str(message.author)] += 1

    if message.author == client.user:
        return

    if message.content[0] == prefix:
        rmessage = message.content[1::].lower()
        roughcommand = rmessage.split(' ')
        command = roughcommand[0]
        args = roughcommand[1::]

        if command == 'hello':
            await message.channel.send('Hello!')
        
        elif command == 'help':
            await message.channel.send('''
Hi! I am an economy bot made by Soham! I was made cuz' 
he was feeling socially distanced and nobody was talking :cry:
But yours truly knew everybody loved bots, so he made me!

So every message sent (I DONT LOG THEM BECAUSE MY CREATOR
HAS NO INTEREST IN ANYONE'S LIVES, Although I certainly could :joy:) 
by a person gives him/her a point!these points can be redeemed
for things like random meme templates and waifus 
(more functionality being added, the project is completely 
open source so u can contribute too, search vella on github).

I am constantly under heavy development so I may be a little buggy.

My prefix is ^

To see ur points do: 
^points

To redeem em do: 
^redeem [Item Name]

I can also do Word definitions Just type:
^def [word]

Invite me:
https://discord.com/api/oauth2/authorize?client_id=744774971380989993&permissions=8&scope=bot
            ''')

        elif command == 'ping':
            await message.channel.send('pong!')  

        elif command == 'points':
            await message.channel.send(message.author.mention + ' You have ' + str(register[str(message.author)])+ ' points!')
        
        elif command == 'velle':
            vella = ("Tu vella bc :face_with_symbols_over_mouth:")
            embed = Embed()
            embed.description = vella
            await message.channel.send(embed=embed)


        elif command == 'join':
            member = utils.find(lambda m: m.id == message.author.id, message.guild.members)
            if member is not None and member.voice is not None:
                vc = member.voice.channel
                player = client.music.player_manager.create(message.guild.id, endpoint=str(message.guild.region))
                if not player.is_connected:
                    player.store('channel', message.channel.id)
                    await connect_to(message.guild.id, str(vc.id))

        elif command == 'play':
            try:
                player = client.music.player_manager.get(message.guild.id)
                query = stringformer(args[0::])
                query = f'ytsearch:{query}'
                results = await player.node.get_tracks(query)
                tracks = results['tracks'][0:10]
                i = 0
                query_result = ''
                for track in tracks:
                    i = i + 1
                    query_result = query_result + f'{i}) {track["info"]["title"]} - {track["info"]["uri"]}\n'
                embed = Embed()
                embed.description = query_result

                await message.channel.send(embed=embed)
            
                response = await client.wait_for('message', check=mcheck)
                track = tracks[int(response.content)-1]

                player.add(requester=message.author.id, track=track)
                if not player.is_playing:
                    await player.play()

            except Exception as e:
                print(e)

        elif command == 'purge':
            if args[0] and len(message.mentions) > 0:
                try:
                    num = int(args[0])
                    deleted = await message.channel.purge(limit = num, check=checker, bulk=False)
                    await message.channel.send("Deleted {} message(s)".format(len(deleted))+f"from {str(message.mentions[0])}")
                except ValueError:
                    await message.channel.send("Please enter the number of messages to delete")
        

            elif args[0]:
                try:
                    num = int(args[0])
                    deleted = await message.channel.purge(limit = num)
                    await message.channel.send("Deleted {} message(s)".format(len(deleted)))
                except ValueError:
                    await message.channel.send("Please enter the number of messages to delete")
                except Forbidden:
                    await message.channel.send("I don't have the permissions to do that!")
                except HTTPException:
                    await message.channel.send("Purging all the messages failed")
                finally:
                    await message.channel.send("Successfully deleted the messages, no hiccups")
            else:
                await message.channel.send("How many to delete again???")

        elif command == 'weather':
            if len(args)>=1:
                city = stringformer(args)
                base_url = "http://api.openweathermap.org/data/2.5/weather?"
                complete_url = base_url + "appid=" + owmAPI + "&q=" + city
                response = requests.get(complete_url) 
                x = response.json() 
                if x["cod"] != "404": 
                    y = x["main"] 
                    current_temperature = y["temp"] 
                    current_pressure = y["pressure"]
                    current_humidiy = y["humidity"] 
                    z = x["weather"]
                    weather_description = z[0]["description"] 
                    info = (" Temperature (in kelvin unit) = " +str(current_temperature) + "\n atmospheric pressure (in hPa unit) = " +str(current_pressure) + "\n humidity (in percentage) = " +str(current_humidiy) +"\n description = " +str(weather_description)) 
                    embed = Embed()
                    embed.description = info

                    await message.channel.send(embed=embed)
                else:
                    await message.channel.send("City not found :cry:")
            else:
                await message.channel.send("Which place's weather? Command usage: <command> <city>")

        elif command == 'clear':
            await message.channel.send('''
clear
clear     
clear
clear
clear
clear       
clear
clear     
clear
clear
clear
clear                  
clear
clear     
clear
clear
clear
clear       
clear
clear     
clear
clear
clear
clear                 
clear
clear     
clear
clear
clear
clear       
clear
clear     
clear
clear
clear
clear                  
clear
clear     
clear
clear
clear
clear       
clear
clear     
clear
clear
clear
clear              
clear
clear     
clear
clear
clear
clear       
clear
clear     
clear
clear
clear
clear                  
clear
clear     
clear
clear
clear
clear       
clear
clear     
clear
clear
clear
clear            
            ''')

            if command == 'start':
                if str(message.author) not in register.keys():
                    register[str(message.author)] = 1
                else:
                    register[str(message.author)] += 1

        elif command == 'avatar':
            if message.mentions:
                for lol in message.mentions:
                    await message.channel.send("Here you go! "+ str(lol.avatar_url))
            else:
                await message.channel.send("Mention the user of whose avatar you want!")

        elif command == 'def':
            if args[0]:
                try:
                    definition = (message.author.mention + ' meaning of requested word is:- ' + str(ud.define(str(stringformer(args[0::])))[0].definition))
                    embed = Embed()
                    embed.description = definition
                    await message.channel.send(embed=embed)
                except IndexError:
                    await message.channel.send("Could not find the meaning :worried:")
            else:
                await message.channel.send(message.author.mention + ' meaning of what?')

        elif command == 'choose':
            if len(args) > 2:
                await message.channel.send(random.choice(args))
            else:
                await message.channel.send("Choose b/w what?? Command usage: <command> <choice 1> <choice 2> <choice 3> ... (Choices should not have space)")

        elif command == 'transfer':
            print(args)
            if message.mentions and int(args[1]):
                if int(register.get(str(message.author))) > int(args[1]):
                    register[str(message.author)] -= int(args[1])
                    if str(message.mentions[0]) not in register.keys():
                        register[str(message.mentions[0])] = 0
                        register[str(message.mentions[0])] += int(args[1])
                    else:
                        register[str(message.mentions[0])] += int(args[1])
                    await message.channel.send(f"Debited {args[1]} point(s) from {message.author}'s account and credited {args[1]} point(s) to {message.mentions[0]}'s account")
                else:
                    await message.channel.send("You don't have enough points to do that!")
            else:
                message.channel.send("Invalid transfer! The format is <Command> <Mention> <Amount>")

        elif command == 'redeem':
            if args[0] == 'template':
                amt = 50
                if amt <= register.get(str(message.author)):
                    await message.channel.send("Here's your template "+message.author.mention+"!", file = discord.File(os.path.join(os.getcwd()+"\\assets\\images\\templates",random.choice(os.listdir("assets\\images\\templates")))))
                    debit(message, amt)
                else:
                    await message.channel.send(message.author.mention + f'You require {amt} points fot this redeem')
            

            elif args[0] == 'waifu':
                try: 
                    if args[0] == 'waifu' and args[1]:
                        amt = 50
                        if amt <= register.get(str(message.author)):
                            if args[1]+'.png' in os.listdir("assets\\images\\waifus\\images") or args[1]+'.jpeg' in os.listdir("assets\\images\\waifus\\images"):
                                amt = 100
                                if amt <= register.get(str(message.author)):
                                    if args[1]+'.png' in os.listdir("assets\\images\\waifus\\images"):
                                        waifu = args[1]+'.png'
                                        await message.channel.send("Requested waifu is: {}".format(waifu[:-4:]), file = discord.File(os.path.join(os.getcwd()+"\\assets\\images\\waifus\\images",waifu)))
                                        debit(message, amt)
                                    elif args[1]+'.jpeg' in os.listdir("assets\\images\\waifus\\images"):
                                        waifu = args[1]+'.jpeg'
                                        await message.channel.send("Requested waifu is: {}".format(waifu[:-5:]), file = discord.File(os.path.join(os.getcwd()+"\\assets\\images\\waifus\\images",waifu)))
                                        debit(message, amt)
                                    else:
                                        await message.channel.send("An error occured, no points have been debited")
                                else:
                                    message.channel.send(message.author.mention + f' No Points No Waifu :joy: You require {amt} points for this redeem')
                            else:
                                await message.channel.send("A waifu with that id does not exist. Stay 4ever Alone ☮️, however I need 50 points for my date so m gonna take em from u!")
                                debit(message, 50)
                except IndexError:
                    amt = 200
                    if amt <= register.get(str(message.author)):
                        waifu = random.choice(os.listdir("assets\\images\\waifus\\images"))
                        if '.png' in waifu:
                            await message.channel.send("And u r gonna be shipped with ... waifu: {}".format(waifu[:-4:]), file = discord.File(os.path.join(os.getcwd()+"\\assets\\images\\waifus\\images",waifu)))
                            debit(message, amt)
                        if '.jpeg' in waifu:
                            await message.channel.send("And u r gonna be shipped with ... waifu: {}".format(waifu[:-5:]), file = discord.File(os.path.join(os.getcwd()+"\\assets\\images\\waifus\\images",waifu)))
                            debit(message, amt)
                    else:
                        await message.channel.send(message.author.mention + f' No Points No Waifu :joy: You require {amt} points fot this redeem')

            elif args[0] == 'poll':
                amt = 20
                if amt <= register.get(str(message.author)):
                    poll = await message.channel.send(stringformer(args[1::]))
                    await poll.add_reaction("👍")
                    await poll.add_reaction("👎")
                    debit(message, amt)
                else:
                    message.channel.send("Insufficient points for initiating poll! It requires 20! :cry:")

            elif args[0] == 'stranger':
                amt = 100
                if amt <= register.get(str(message.author)):
                    person = random.choice(list(register.keys()))
                    peopleknown = len(register.keys())
                    await message.channel.send(f"And u get... {person} out of the {peopleknown} people I know!")
                    debit(message, amt)
                else:
                    await message.channel.send(random.choice(["Information is a commdity my friend and it costs 100 points for this one", "Introductions are expensive 100 points for this one"]))

            elif args[0] == 'roll':
                amt = 6
                if amt <= register.get(str(message.author)):
                    await message.channel.send(message.author.mention+" rolled the die & its a "+random.choice(["1","2","3","4","5","6"])+"!")

            elif args[0] == '8ball':
                amt = 8
                if amt <= register.get(str(message.author)) and args[1]:
                    if '?' in args or args[-1][-1]:
                        await message.channel.send(random.choice(["Yes.", "Yes definitely", "As I see it, yes", "You may rely on it", "Without a doubt", "Signs point to yes", "Outlook good", "Most likely", "It is decidedly so", "It is certain", "Think first, then ask", "Not interested in answering that", "Boring question, ask something else", "U r not supposed to ask me something like that", "Don't bother me kid", "You can do better than that", "C'mon BRO!", "I would ask Yuri", "I don't know ask Joe", "SIMP", "Shut up.", "STFU", "GTFO", "As true as a flat earth", "As false as someone loving you", "Better not tell", "I don't snitch", "Not answering", "I am not answerable to boring people", "Duck off", "Buzz off punk", "Buzz off", "Concentrate, and ask again", "Don't count on it", "I wouldn't count on it", "You should not count on it", "Give it up", "I would give up on that", "You should give up", "My reply is no", "Outlook is not good", "My sources say NO", "I am doubtful", "Very doubtful", "Not that sure", "Nada", "Not happening"]))
                        debit(message, amt)
                    else:
                        message.channel.send("Questions end with a '?' dummy.")
                else:
                    message.channel.send("Either you don't have the 8 points to ask me that or that aint a question usage: <redeem> <8ball> <Ur Question>")
            elif args[0] == 'flip':
                amt = 2
                if amt <= register.get(str(message.author)):
                    await message.channel.send("And it's a... " + random.choice(["Heads", "Tails"])+"!")
                    debit(message, amt)
                else:
                    await message.channel.send("You require 2 points to flip the coin!")

            elif args[0] == 'ducku' or 'duck u' or 'fuck u' or 'fucku' :
                amt = 100
                if amt <= register.get(str(message.author)):
                    await message.channel.send("Fuck You Too! :smile: I have debited 100 points from your account!")
                    debit(message, amt)

                else:
                    await message.channel.send("If u have less than 100 points, u cant fuck me sry, fucks cost points! :smile:")
            else:
                await message.channel.send("Redeem does not exist :sad:")
        
        elif command == 'cheatcode':
            if args[0] == 'hesoyam' and int(args[1]):
                register[str(message.author)] += int(args[1])
                await message.channel.send(f"Credited {args[1]} to {message.author}'s account")

            elif args[0] == 'helloladies' and int(args[1]):
                if int(args[1]) <= 10:
                    for i in range(0,int(args[1])):
                        await message.channel.send("And u r gonna be shipped with ...", file = discord.File(os.path.join(os.getcwd()+"\\assets\\images\\waifus\\images",random.choice(os.listdir("assets\\images\\waifus\\images")))))
                else:
                    message.channel.send("Merul or Tejas, whoever u are... u r bargaining for way too much booty")
            else:
                await message.channel.send("Invalid cheat :joy:")
        else:
            await message.channel.send('I know of no such command :thinking:')

    saveup()


client.run(config['DISCORD']['token'])

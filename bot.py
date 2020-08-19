import requests
import random
import os
import configparser
import discord
import time
import json
from PyDictionary import PyDictionary
from pathlib import Path
from discord.ext.commands import *

dictionary = PyDictionary()

client = discord.Client()

prefix = '^'

if os.path.isfile('register.json') :
    saves = open("register.json", "r")
    register = json.loads(saves.readlines().pop())
    saves.close()
else:
    register = {}
    saves = open("register.json", "w+")

config = configparser.ConfigParser()
config.read('config.ini')

def debit(message, amt):
    register[str(message.author)] -= amt

def credit(message, amt):
    register[str(message.author)] += amt

def saveup():
    saves = open("register.json", "a+")
    saves.write('\n')
    save = json.dumps(register)
    saves.write(save)

def wordsearch(word):
    meaning = str(dictionary.meaning(word))
    if meaning != 'None':
        return meaning
    else:
        return "Could not find the meaning :cry:"

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(name="Fall Guys"))

@client.event
async def on_message(message):

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
        
        elif command == 'purge':
            if args[0]:
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
                await message.channel.send(message.author.mention + ' meaning of requested word is:- ' + str(wordsearch(args[0])))

            else:
                await message.channel.send(message.author.mention + ' meaning of what?')

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
                amt = 5
                if amt <= register.get(str(message.author)):
                    await message.channel.send("Here's your template "+message.author.mention+"!", file = discord.File(os.path.join(os.getcwd()+"\\assets\\templates",random.choice(os.listdir("assets\\templates")))))
                    debit(message, amt)
                else:
                    await message.channel.send(message.author.mention + f'You require {amt} points fot this redeem')

            elif args[0] == 'waifu':
                amt = 10
                if amt <= register.get(str(message.author)):
                    await message.channel.send("And u r gonna be shipped with ...", file = discord.File(os.path.join(os.getcwd()+"\\assets\\waifus\\images",random.choice(os.listdir("assets\\waifus\\images")))))
                    debit(message, amt)
                else:
                    await message.channel.send(message.author.mention + f' No Points No Waifu :joy: You require {amt} points fot this redeem')
            
            elif args[0] == 'roll':
                amt = 6
                if amt <= register.get(str(message.author)):
                    await message.channel.send(message.author.mention+" rolled the die & its a "+random.choice("1","2","3","4","5","6")+"!")

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
                for i in range(0,int(args[1])):
                    await message.channel.send("And u r gonna be shipped with ...", file = discord.File(os.path.join(os.getcwd()+"\\assets\\waifus\\images",random.choice(os.listdir("assets\\waifus\\images")))))
            
            else:
                await message.channel.send("Invalid cheat :joy:")
        else:
            await message.channel.send('I know of no such command :worried:')

    saveup()


client.run(config['DISCORD']['token'])
import requests
import random
import os
import configparser
import praw
import discord
import time

client = discord.Client()

prefix = '^'

register = {}

config = configparser.ConfigParser()
config.read('config.ini')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content[0] == prefix:
        rmessage = message.content[1::].lower()
        roughcommand = rmessage.split(' ')
        command = roughcommand[0]
        args = roughcommand[1::]

        if command == 'hello':
            await message.channel.send('Hello!')
        
        if command == 'ping':
            await message.channel.send('pong!')  

        if command == 'points':
            await message.channel.send(message.author.mention + ' You have ' + str(register[message.author])+ ' points!')
        
        if command == 'redeem':
            if args[0] == 'template':
                await message.channel.send("Here's your template "+message.author.mention+"!", file = discord.File(os.path.join(os.getcwd()+"\\assets\\templates",random.choice(os.listdir("assets\\templates")))))
        
        else:
            await message.channel.send('I know of no such command :worried:')

    if message.author not in register.keys():
        register[message.author] = 1
    else:
        register[message.author] += 1

client.run(config['DISCORD']['token'])
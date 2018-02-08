#! /usr/bin/env python

# Patrick Haugh 2018
# MIT License

import discord
import asyncio
import sys
from discord.ext import commands

description = '''A bot for managing games of Kings.

Type `!help` for a list of commands.
'''

bot = commands.Bot(command_prefix='!', description=description)

games = {}


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-----')


@bot.command(pass_context=True)
async def start(ctx):
    '''
    Starts a game of kings in this channel.
    '''


@bot.command(pass_context=True)
async def end(ctx):
    '''
    Ends the game of kings in the current channel.
    '''


@bot.command(pass_context=True)
async def shuffle(ctx):
    '''
    Shuffles all cards back into the deck, emptying hands.
    '''


@bot.command(pass_context=True)
async def deal(ctx):
    '''
    Deals a card to the player.
    '''


if len(sys.argv) == 2:
    bot.run(sys.argv[1])
else:
    bot.run(input())

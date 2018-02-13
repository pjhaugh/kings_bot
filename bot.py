#! /usr/bin/env python

# Patrick Haugh 2018
# MIT License

import sys
import discord
from discord.ext import commands
from Game import Game
from Player import Player

description = '''A bot for managing games of Kings.'''

bot = commands.Bot(command_prefix='!', description=description)

games = {}


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-----')
    await bot.change_presence(game=discord.Game(name='Kings'))


@bot.command(pass_context=True)
async def playing(ctx):
    '''
    Checks if there is a game in the current channel.
    '''
    if ctx.message.channel in games:
        await bot.say('There is a game in this channel!  Say !join to join.')
    else:
        await bot.say('There is no game in this channel. Say !start to start one!')


@bot.command(pass_context=True)
async def players(ctx):
    '''
    Display the players in this game.
    '''
    if ctx.message.channel in games:
        message = '\n'.join(player.user.display_name for player in games[ctx.message.channel].players)
        await bot.say(message)


@bot.command(pass_context=True)
async def start(ctx):
    '''
    Starts a game of kings in this channel.
    '''
    if ctx.message.channel in games:
        await bot.say('There is already a game of Kings in this channel.')
    else:
        game = await Game.create(await Player.create(ctx.message.author))
        games[ctx.message.channel] = game
        await bot.say('#havefungetdrunk Tell those scrubs to !join')


@bot.command(pass_context=True)
async def end(ctx):
    '''
    Ends the game of kings in the current channel.
    '''
    if ctx.message.channel in games:
        del games[ctx.message.channel]
        await bot.say('Game Over. You could always !start another one.')
    else:
        await bot.say('No game in this channel.')


@bot.command(pass_context=True)
async def shuffle(ctx):
    '''
    Shuffles all cards back into the deck, emptying hands.
    '''
    if ctx.message.channel in games:
        game = games[ctx.message.channel]
        await game.deck.reset()
        for player in game.players:
            player.hand = set()
        await bot.say('Everything is back in the pile.')


@bot.command(pass_context=True)
async def hand(ctx):
    '''
    DMs your hand to you
    '''
    if ctx.message.channel in games:
        game = games[ctx.message.channel]
        if ctx.message.author in game.players:
            player = await game.get_player(ctx.message.author)
            message = '\n'.join(player.hand) if player.hand else 'You have an empty hand'
            await bot.send_message(ctx.message.author, message)


@bot.command(pass_context=True)
async def deal(ctx):
    '''
    Deals a card to the player.
    '''
    if ctx.message.channel not in games:
        return
    game = games[ctx.message.channel]
    tup = await game.draw()
    if not tup:
        bot.say('That was the last card!  Feel free to !start over...')
    else:
        player, card = tup
        mention = player.user.mention
        await bot.say('{} you drew the {}'.format(mention, card))


@bot.command(pass_context=True)
async def join(ctx):
    '''
    Join the game in this channel.
    '''
    if ctx.message.channel in games:
        game = games[ctx.message.channel]
        if ctx.message.author not in game.players:
            await game.add(await Player.create(ctx.message.author))
            await bot.say('{} added.'.format(ctx.message.author.mention))
        else:
            await bot.say("You're already playing {}".format(ctx.message.author.mention))


@bot.command(pass_context=True)
async def quit(ctx):
    '''
    Leave the game in this channel.
    '''
    if ctx.message.channel in games:
        game = games[ctx.message.channel]
        if ctx.message.author in game.players:
            game.players.remove(ctx.message.author)
            if not game.players:
                del games[ctx.message.channel]
        await bot.say('Bye!')


@bot.command(pass_context=True)
async def rules(ctx):
    '''
    Display the basic rules of Kings.
    '''
    if ctx.message.channel in games:
        message = '\n'.join('{}: {}'.format(*item) for item in
                            games[ctx.message.channel].rules.items())
        await bot.say(message)


@bot.command(pass_context=True)
async def addrule(ctx, name, rule):
    '''
    Add a rule to the game.
    '''
    if ctx.message.channel in games:
        games[ctx.message.channel].rules[name] = rule
        await bot.say('Added')


@bot.command(pass_context=True)
async def removerule(ctx, name):
    '''
    Remove a rule by name
    '''
    if ctx.message.channel in games:
        rules = games[ctx.message.channel].rules
        if name in rules:
            del rules[name]
            await bot.say('{} removed'.format(name))

if len(sys.argv) == 2:
    bot.run(sys.argv[1])
else:
    bot.run(input())

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
    await bot.change_presence(activity=discord.Game(name='Kings'))


@bot.command()
async def playing(ctx):
    '''
    Checks if there is a game in the current channel.
    '''
    if ctx.channel in games:
        await ctx.send('There is a game in this channel!  Say !join to join.')
    else:
        await ctx.send('There is no game in this channel. Say !start to start one!')


@bot.command()
async def players(ctx):
    '''
    Display the players in this game.
    '''
    if ctx.channel in games:
        message = '\n'.join(
            player.user.display_name for player in games[ctx.channel].players)
        await ctx.send(message)


@bot.command()
async def next():
    '''
    Display the next person to draw.
    '''
    await ctx.send(games[ctx.channel].players[-1])


@bot.command()
async def start(ctx):
    '''
    Starts a game of kings in this channel.
    '''
    if ctx.channel in games:
        await ctx.send('There is already a game of Kings in this channel.')
    else:
        game = await Game.create(await Player.create(ctx.author))
        games[ctx.channel] = game
        await ctx.send('#havefungetdrunk Tell those scrubs to !join')


@bot.command()
async def end(ctx):
    '''
    Ends the game of kings in the current channel.
    '''
    if ctx.channel in games:
        del games[ctx.channel]
        await ctx.send('Game Over. You could always !start another one.')
    else:
        await ctx.send('No game in this channel.')


@bot.command()
async def shuffle(ctx):
    '''
    Shuffles all cards back into the deck, emptying hands.
    '''
    if ctx.channel in games:
        game = games[ctx.channel]
        await game.deck.reset()
        await game.deck.shuffle()
        for player in game.players:
            player.hand = set()
        await ctx.send('Everything is back in the pile.')


@bot.command()
async def hand(ctx):
    '''
    DMs your hand to you
    '''
    if ctx.channel in games:
        game = games[ctx.channel]
        if ctx.author in game.players:
            player = await game.get_player(ctx.author)
            message = '\n'.join(
                player.hand) if player.hand else 'You have an empty hand'
            await ctx.author.send(message)


@bot.command()
async def deal(ctx):
    '''
    Deals a card to the player.
    '''
    if ctx.channel not in games:
        return
    game = games[ctx.channel]
    tup = await game.draw()
    if not tup:
        ctx.send('That was the last card!  Feel free to !start over...')
    else:
        player, card = tup
        await ctx.send('{} you drew the {}'.format(player.mention, card))
        if card.value in game.rules:
            await ctx.send('{}: {}'.format(card.value, game.rules[card.value]))


@bot.command()
async def join(ctx):
    '''
    Join the game in this channel.
    '''
    if ctx.channel in games:
        game = games[ctx.channel]
        if ctx.author not in game.players:
            await game.add(await Player.create(ctx.author))
            await ctx.send('{} added.'.format(ctx.author.mention))
        else:
            await ctx.send("You're already playing {}".format(ctx.author.mention))


@bot.command()
async def quit(ctx):
    '''
    Leave the game in this channel.
    '''
    if ctx.channel in games:
        game = games[ctx.channel]
        if ctx.author in game.players:
            game.players.remove(ctx.author)
            if not game.players:
                del games[ctx.channel]
        await ctx.send('Bye!')


@bot.command()
async def rules(ctx):
    '''
    Display the basic rules of Kings.
    '''
    if ctx.channel in games:
        message = '\n'.join('{}: {}'.format(*item)
                            for item in games[ctx.channel].rules.items())
        await ctx.send(message)


@bot.command()
async def addrule(ctx, name, *, rule):
    '''
    Add a rule to the game.
    '''
    if ctx.channel in games:
        games[ctx.channel].rules[name] = rule
        await ctx.send('Added')


@bot.command()
async def removerule(ctx, name):
    '''
    Remove a rule by name
    '''
    if ctx.channel in games:
        rules = games[ctx.channel].rules
        if name in rules:
            del rules[name]
            await ctx.send('{} removed'.format(name))


@bot.command()
async def kick(ctx, player: discord.Member):
    '''
    Remove a player from the game
    '''
    if ctx.channel in games and player in games[ctx.channel].players:
        games[ctx.channel].players.remove(player)
        await ctx.send("{} removed.".format(player.mention))


@bot.command()
async def count(ctx):
    '''
    Display the number of remaining cards
    '''
    await ctx.send("Thare are {} cards remaining.".format(len(games[ctx.channel].deck)))


@bot.command()
async def addplayer(ctx, player: discord.User):
    '''
    Add a person to the game.
    '''
    if ctx.channel in games:
        game = games[ctx.channel]
        if player not in game.players:
            await game.add(await Player.create(player))
            await ctx.send('{} added.'.format(player.mention))
        else:
            await ctx.send("You're already playing {}".format(player.mention))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.author.send("Invalid command")
        return
    print("OK")


if len(sys.argv) == 2:
    bot.run(sys.argv[1])
else:
    bot.run(input())

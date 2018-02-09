# Patrick Haugh
# MIT license

from Deck import Deck
from collections import deque


class Game:
    @classmethod
    async def create(cls, first):
        self = Game()
        self.deck = await Deck.create()
        self.players = deque()
        await self.add(first)
        return self

    async def add(self, player):
        self.players.append(player)

    async def draw(self):
        if not len(self.deck):
            return ()
        player = self.players.pop()
        self.players.appendleft(player)
        card = await self.deck.deal()
        player.hand.add(card)
        return (player, card)

    async def get_player(self, user):
        for player in self.players:
            if user == player.user:
                return player
        raise ValueError('User not playing game.')

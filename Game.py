# Patrick Haugh
# MIT license

from Deck import Deck
from collections import deque, OrderedDict

game_rules = [
    ('2', 'Make someone drink'),
    ('3', 'You drink'),
    ('4', 'Women drink'),
    ('5', 'Never Have I Ever'),
    ('6', 'Men drink'),
    ('7', 'Waterfall. Everyone drinks until the person preceding them stops.'),
    ('8', 'Predict the color of the next card. If you guess wrong, drink.'
          ' Otherwise give a drink.'),
    ('9', 'Say a word.  Everyone rhymes until someone messes up. They then'
          ' drink.'),
    ('10', 'Name a category. Everyone names things in that category until '
           'someone repeats a thing, or cannot name one quickly. '
           'They then drink'),
    ('Jack', 'Everybody tells you a joke.  Everyone but the best joker has'
             ' to drink'),
    ('Queen', 'Ask everyone the same question. Those who refuse to answer'
              ' must drink'),
    ('King', 'Hotseat.  Everyone asks you a question. You must drink if'
             ' you refuse to answer.'),
    ('Ace', 'Make a rule. Use !addrule "name" "description" to add it here.')
]


class Game:
    @classmethod
    async def create(cls, first):
        self = Game()
        self.deck = await Deck.create()
        self.players = deque()
        self.rules = OrderedDict(game_rules)
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

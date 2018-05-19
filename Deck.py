# Patrick Haugh
# MIT License

from Card import Card
import random

values = [*map(str, range(2, 11)), 'Jack', 'Queen', 'King', 'Ace']
suits = '♠♥♦♣'


class Deck:
    @classmethod
    async def create(cls):
        self = Deck()
        await self.reset()
        await self.shuffle()
        return self

    async def shuffle(self):
        random.shuffle(self._deck)

    async def reset(self):
        self._deck = [Card(value, suit) for value in values for suit in suits]
        self._discard = []

    async def deal(self):
        return self._deck.pop()

    def __len__(self):
        return len(self._deck)

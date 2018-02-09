# Patrick Haugh
# MIT License

import random

values = [*range(2, 11), 'Jack', 'King', 'Queen', 'Ace']
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
        self._deck = ['{} of {}'.format(value, suit) for value in values for suit in suits]
        self._discard = []

    async def deal(self):
        return self._deck.pop()

    def __len__(self):
        return len(self._deck)

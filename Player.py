# Patrick Haugh
# MIT license


class Player:
    @classmethod
    async def create(cls, user):
        self = Player()
        self.user = user
        self.hand = set()
        self.mention = user.mention
        return self

    def __eq__(self, other):
        return self.user == other

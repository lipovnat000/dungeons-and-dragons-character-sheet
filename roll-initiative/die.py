import random

class Die:
    def __init__(self, sides):
        self.sides = sides

    def roll(self):
        return random.randint(1, self.sides)

    def roll_advantage(self):
        r1 = self.roll()
        r2 = self.roll()
        return max(r1, r2), (r1, r2)

    def roll_disadvantage(self):
        r1 = self.roll()
        r2 = self.roll()
        return min(r1, r2), (r1, r2)

    def max_roll(self):
        return self.sides

import random

class RandMemory:

    def __init__(self, lowest=1, heighest=100):
        self.lowest = lowest
        self.heighest = heighest
        self.data = []

    @property
    def get(self):
        number = random.randint(self.lowest, self.heighest)
        self.data.append(number)
        return number

    def history(self):
        return self.data


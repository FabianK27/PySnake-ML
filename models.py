# NN test simulation, returns random inputs

import random

class randomNN:
    def __init__(self, numPos):
        self.numPos = numPos
    def returnAction(self):
        return random.randrange(0, self.numPos)
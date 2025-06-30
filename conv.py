from config import *
from building import Building

class Conv(Building):
    def __init__(self, pos, spritesheet, orientation):
        super().__init__(pos, spritesheet, orientation)
        self.animationSpeed = 6 # 10 times per second
        self.add(tilesConvGroup)
        self.id = "conveyor"

        


from config import *
from building import Building

class Conv(Building):
    def __init__(self, pos, spritesheet, orientation):
        super().__init__(pos, spritesheet, orientation)
        self.animationSpeed = 6 # 10 times per second
        self.add(tilesConvGroup)

        if tilesConvGroup.empty:
            self.animationTimer = 0
            self.animationFrame = 0
        else:
            self.animationTimer = tilesConvGroup.sprites()[0].animationTimer
            self.animationFrame = tilesConvGroup.sprites()[0].animationFrame


from config import *
from building import Building

class Conv(Building):
    def __init__(self, pos, spritesheet, orientation):
        super().__init__(pos, spritesheet, orientation)
        
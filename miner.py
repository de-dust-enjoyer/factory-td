from config import *
from building import Building

class Miner(Building):
    def __init__(self, pos:tuple, spritesheet:pygame.Surface, orientation:str, tilesize:tuple):
        super().__init__(pos, spritesheet, orientation, tilesize)
        self.id = "miner"
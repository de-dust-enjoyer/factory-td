from config import *
from tile import Tile

class WorldTile(Tile):
    def __init__(self, pos:tuple, img:pygame.Surface, tilesize:tuple = (16, 16)):
        super().__init__(pos, img, tilesize)
        self.add(tilesWorldGroup)
        


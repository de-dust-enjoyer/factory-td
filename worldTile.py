from config import *
from tile import Tile
class WorldTile(Tile):
    def __init__(self, pos, img):
        super().__init__(pos, img)
        
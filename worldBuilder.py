from config import *
from worldTile import WorldTile
from spritesheet import Spritesheet
from pytmx.util_pygame import load_pygame


class Worldbuilder:
    def __init__(self):
        self.tilemap = None
        self.spritesheet = None
        self.tilesize = None
        self.worldImg = None
    
    def buildWorld(self, tilemap:dict, spritesheet:Spritesheet, tilesize:int):
        self.tilemap = tilemap
        self.spritesheet = spritesheet
        self.tilesize = tilesize
        worldSurf = pygame.Surface((len(tilemap[0]) * tilesize, len(tilemap) * tilesize), pygame.SRCALPHA)

        for row in tilemap:
            for tile in row:
                worldTile = WorldTile((tile.key, row.key), self.spritesheet.get_img_world(tile))
                worldTile.draw(worldSurf)

        return worldSurf
    
    def buildLevel(self, pathToTilemap:str):
        tmxData = load_pygame(pathToTilemap)


        


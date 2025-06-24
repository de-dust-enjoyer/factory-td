from config import *
from worldTile import WorldTile
from spritesheet import Spritesheet
from building import Building
from pytmx.util_pygame import load_pygame


class WorldBuilder:
    def __init__(self):
        self.tmxData = None
        self.tilesize = None
        self.worldSurf = None
        self.levelName = None
        self.buildingLayer = {}

    def buildWorld(self, pathToTilemap:str):
        self.tmxData = load_pygame(pathToTilemap)
        self.tilesize = (self.tmxData.tilewidth, self.tmxData.tileheight)
        worldSurf = pygame.Surface((self.tmxData.width * self.tilesize[0], self.tmxData.height * self.tilesize[1]), pygame.SRCALPHA)
        for layer in self.tmxData.visible_layers:
            for x, y, surf in layer.tiles():
                WorldTile((x * self.tilesize[0], y * self.tilesize[1]), surf)
        self.worldSurf = worldSurf
        self.levelName = os.path.splitext(os.path.basename(pathToTilemap))[0]


    


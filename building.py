from config import *
from tile import Tile
from tools import cutSpritesheet

class Building(Tile):
    def __init__(self, pos, spritesheet, orientation, tilesize:tuple= (16, 16)):
        super().__init__(pos, cutSpritesheet(spritesheet, tilesize[0])[0], tilesize)
        self.animationSpeed = 15
        if tilesBuildingGroup.empty:
            self.animationTimer = 0
            self.animationFrame = 0
        else:
            self.animationTimer = tilesBuildingGroup.sprites()[0].animationTimer
            self.animationFrame = tilesBuildingGroup.sprites()[0].animationFrame

        self.frames = cutSpritesheet(spritesheet, tilesize[0])
        self.image = self.frames[self.animationFrame]
        self.rect = self.frames[0].get_rect(topleft= pos)

        self.add(tilesBuildingGroup)

        

    def updateAnimation(self):
        self.animationTimer += 1
        if self.animationTimer >= self.animationSpeed:
            self.animationFrame += 1
            self.animationTimer = 0
            if self.animationFrame == len(self.frames):
                self.animationFrame = 0
        self.image = self.frames[self.animationFrame]


    def update(self):
        self.updateAnimation()
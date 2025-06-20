from config import *
from tile import Tile
from tools import cutSpritesheet

class Building(Tile):
    def __init__(self, pos, spritesheet, orientation):
        super().__init__(pos, spritesheet)
        self.animationSpeed = 15
        self.animationTimer = 0
        self.animationFrame = 0

        self.frames = cutSpritesheet(spritesheet, TILESIZE, int(spritesheet.get_width() / TILESIZE))
        self.rect = self.frames[0].get_rect(topleft= self.pos)

        

    def updateAnimation(self):
        self.animationTimer += 1
        if self.animationTimer >= self.animationSpeed:
            self.animationFrame += 1
            self.animationTimer = 0
            if self.animationFrame > len(self.frames):
                self.animationFrame = 0

    def draw(self, display):
        display.blit(self.frames[self.animationFrame], self.rect)

    def update(self):
        self.updateAnimation()
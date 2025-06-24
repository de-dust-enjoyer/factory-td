from config import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos:tuple, img:pygame.Surface, tilesize:tuple = (16, 16)):
        super().__init__()
        self.image = img
        self.tilesize = tilesize
        self.rect = pygame.Rect(pos[0], pos[1], tilesize[0], tilesize[1])
        self.originalImage = img
        self.rect = self.image.get_rect(topleft=pos)
        self.zoomCache = {}


    def getScaledImg(self, zoom):
        if zoom not in self.zoomCache:
            self.zoomCache[zoom] = pygame.transform.scale(self.originalImage, (self.tilesize[0]*zoom, self.tilesize[1]*zoom))
        return self.zoomCache[zoom]
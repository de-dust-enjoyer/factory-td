from config import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos:tuple, img:pygame.Surface, tilesize:tuple = (16, 16)):
        super().__init__()
        self.image = img
        self.rect = pygame.Rect(pos[0], pos[1], tilesize[0], tilesize[1])
        self.add(cameraGroup)



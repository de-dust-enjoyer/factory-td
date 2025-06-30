from config import *

class Item(pygame.sprite.Sprite):
    def __init__(self, pos:tuple, id:str, img:pygame.Surface, tilesize:tuple= (8, 8)):
        super().__init__()
        self.id = id
        self.add(itemGroup)
        self.add(cameraGroup)
        self.image = img
        self.rect = pygame.Rect(pos[0], pos[1], img.get_width(), img.get_height())
        
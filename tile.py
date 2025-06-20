from config import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, spritesheet):
        super().__init__()
        # pos on spritesheet gets converted to pixel position
        self.pos = (pos[0] * TILESIZE, pos[1] * TILESIZE)
        self.spritesheet = spritesheet
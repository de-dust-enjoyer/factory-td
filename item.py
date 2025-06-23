from config import *

class Item(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.add(itemGroup)
        
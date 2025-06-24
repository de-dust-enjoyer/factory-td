from config import *

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def customDraw(self, screen):
        for sprite in self.sprites():
            screen.blit(sprite.image, sprite.rect)
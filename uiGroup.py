import pygame

class UiGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def draw(self, surface:pygame.Surface):
        for sprite in self.sprites():  # type:ignore
            if sprite.visible:
                surface.blit(sprite.image, sprite.rect)
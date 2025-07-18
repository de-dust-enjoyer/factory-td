import pygame, colors
from camera import CameraGroup
from uiGroup import UiGroup
# constants
FPS = 60
SCREENSIZE = (1920, 1080)
TILESIZE = 16





# Sprite Groups:
tilesWorldGroup = pygame.sprite.Group()
tilesBuildingGroup = pygame.sprite.Group()
tilesConvGroup = pygame.sprite.Group()
itemGroup = pygame.sprite.Group()
cameraGroup = CameraGroup([tilesBuildingGroup, itemGroup])
uiGroup = UiGroup()

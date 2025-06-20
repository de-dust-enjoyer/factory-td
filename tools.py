from config import *

def cutSpritesheet(spritesheet:pygame.surface.Surface, tilesize:int, numSprites:int):
    frames = []
    for i in range(numSprites):
        tile = pygame.Surface((tilesize, tilesize), pygame.SRCALPHA)
        rect = pygame.Rect(i * tilesize, 0, tilesize, tilesize)
        tile.blit(spritesheet, (0, 0), rect)
        frames.append(tile)
    return frames

def rotate(img, rotationValue):
    rotation = 0
    match rotationValue:
        case "up":
            rotation = 0
        case "right":
            rotation = 270
        case "left":
            rotation = 90
        case "down":
            rotation = 180
        case _:
            rotation = rotationValue
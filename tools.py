from config import *

def cutSpritesheet(spritesheet:pygame.surface.Surface, tilesize:int):
    frames = []
    for i in range(int(spritesheet.get_width() / tilesize)):
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

def gridAllign(pos:tuple, tilesize:int):
    return (round(pos[0] / tilesize) * tilesize, round(pos[1] / tilesize) * tilesize)


class TextRenderer:
    def __init__(self, pathToFont:str):
        self.fonts = {}
        self.textObjects = {}
        self.pathToFont = pathToFont


    def addText(self, text:str, id:str, size:int, color, pos:tuple, center:bool= False, rotation= None):
        if size not in self.fonts:
            self.fonts[size] = pygame.font.Font(self.pathToFont, size)
        # create the text object
        textSurfRaw = self.fonts[size].render(text, False, color)
        # only call the rotate method if rotation is wanted
        if rotation:
            textSurf = pygame.transform.rotate(textSurfRaw, rotation)
        else:
            textSurf = textSurfRaw
        # create a rect object for positioning
        rect = textSurf.get_rect()
        if center:
            rect.center = pos
        else:
            rect.topleft = pos

        textObject = CustomTextObject(textSurf, rect)
        # add the text object to the dict
        self.textObjects[id] = textObject

    def render(self, surface:pygame.Surface):
        for textObject in self.textObjects:
            print(textObject)
            surface.blit(self.textObjects[textObject].image, self.textObjects[textObject].rect)


class CustomTextObject:
    def __init__(self, textSurf:pygame.Surface, rect:pygame.Rect):
        self.image = textSurf
        self.rect = rect
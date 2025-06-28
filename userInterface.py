from config import *
from tools import cutSpritesheet, TextRenderer
from conv import Conv
from furnace import Furnace
from miner import Miner
from buildingInfo import buildingIDS, buildingGroups


class MiniMap(pygame.sprite.Sprite):
    def __init__(self, worldSurf:pygame.Surface, sizeX:int, pos:tuple):
        super().__init__()
        self.visible = True

        self.borders = {"left": 10, "top": 10, "right": 10, "bottom": 10}

        # computing the new size of the minimap
        self.mapWidth = sizeX - self.borders["left"] - self.borders["right"]
        self.mapScale = self.mapWidth / worldSurf.get_width()
        self.mapHeight = worldSurf.get_height() * self.mapScale
        
        # creating the surface rect with absosote positions (for blitting)
        self.image = pygame.Surface((sizeX, self.mapHeight + self.borders["top"] + self.borders["bottom"]), pygame.SRCALPHA) # type:ignore
        self.rect = self.image.get_rect(topleft= pos)

        # creating a map rect object with relative positions
        self.mapSurf = pygame.transform.scale(worldSurf, (self.mapWidth, self.mapHeight))
        self.mapRect = self.mapSurf.get_rect(center= (self.rect.width / 2, self.rect.height / 2))       
        
        # creating the viewRect
        self.viewRect = pygame.Rect()
        self.viewRectThickness = 2
        self.borderThickness = 4
        
        # colors
        self.bgColor = colors.BLACK
        self.viewRectColor = colors.RED
        self.borderColor = colors.DARKGREY

        # add to ui Group
        self.add(uiGroup)

    def update(self, cameraRect:pygame.Rect):
        if self.visible:
        # updating the viewRect
            width = cameraRect.width * self.mapScale
            height = cameraRect.height * self.mapScale
            self.viewRect.size = (width, height)
            left = cameraRect.left * self.mapScale + self.borders["left"]
            top = cameraRect.top * self.mapScale + self.borders["top"]
            self.viewRect.topleft = (left, top)

            # drawing the map on the self.image surface
            self.image.fill(self.bgColor) # type:ignore
            self.image.blit(self.mapSurf, self.mapRect) # type:ignore
            pygame.draw.rect(self.image, self.viewRectColor, self.viewRect, self.viewRectThickness) # type:ignore
            pygame.draw.rect(self.image, self.borderColor, (0,0,self.rect.width,self.rect.height), self.borderThickness) # type:ignore
        


class BuildingMenu(pygame.sprite.Sprite):
    def __init__(self, buildings:list, tilesize:int, sizeX:int, pos:tuple):
        super().__init__()
        self.textRenderer = TextRenderer("assets/font/pixel_font.otf")
        self.textRenderer.addText("logistics", "0", 10, colors.GREEN, (10,10), rotation=90)
        self.visible = True
        self.buildingGroups = buildingGroups
        # formating
        self.borders = {"left": 10, "top": 10, "right": 10, "bottom": 10}
        self.gridPadding = 5
        self.scale = 2
        # getting the imgs for the menu
        


        # colors
        self.bgColor = colors.BLACK
        self.borderColor = colors.DARKGREY
        self.borderThickness = 4

        self.image = pygame.Surface((sizeX, sizeX * 2), pygame.SRCALPHA)
        self.image.fill(self.bgColor)
        self.rect = self.image.get_rect(topleft= pos)
        pygame.draw.rect(self.image, self.borderColor, (0,0,self.rect.width,self.rect.height), self.borderThickness)
        self.textRenderer.render(self.image)
        self.add(uiGroup)

    def update(self, cameraRect:pygame.Rect):
        pass
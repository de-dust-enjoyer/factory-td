from config import *
from tools import cutSpritesheet, TextRenderer
from conv import Conv
from furnace import Furnace
from miner import Miner
from buildingInfo import buildingIDS, buildingGroups


class MiniMap(pygame.sprite.Sprite):
    def __init__(self, worldSurf:pygame.Surface, sizeX:int, pos:tuple):
        super().__init__()
        self.id = "MiniMap"
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
        self.id = "BuildingMenu"
        self.visible = True
        self.buildingGroups = buildingGroups
        self.selected = "organization"
        self.clicking = False
        # formating
        self.borders = {"left": 10, "top": 10, "right": 10, "bottom": 10}
        self.gridPadding = 5
        self.scale = 2
        # getting the imgs for the menu
        

        


        # colors
        self.bgColor = colors.BLACK
        self.borderColor = colors.DARKGREY
        self.borderThickness = 4
        self.textColor = colors.LIGHTGREY
        self.buttonColor = colors.GREY

        self.image = pygame.Surface((sizeX, sizeX * 2), pygame.SRCALPHA)
        self.image.fill(self.bgColor)
        self.rect = self.image.get_rect(topleft= pos)
        
        self.add(uiGroup)
        
        self.textRenderer = TextRenderer("assets/font/pixel_font.otf")
        first = True
        for group in self.buildingGroups:
            if first:
                groupPos = (10,12)
            else:
                groupPos = (10, self.textRenderer.textObjects[previousGroup].rect.bottom)
            self.textRenderer.addText(f" {group} ", group, 11, self.textColor, groupPos, rotation=90)
            first = False
            previousGroup = group
            
        

    def update(self, cameraRect:pygame.Rect): # camera Rect not used in this class
        self.image.fill(self.bgColor)
        pygame.draw.rect(self.image, self.borderColor, (0,0,self.rect.width,self.rect.height), self.borderThickness)
        for group in self.buildingGroups:
            if self.selected != group:
                pygame.draw.rect(self.image, self.buttonColor, self.textRenderer.textObjects[group].rect) # type:ignore
            if pygame.mouse.get_pressed()[0]:
                if not self.clicking:
                    if self.textRenderer.textObjects[group].rect.collidepoint(self.getRelPos(pygame.mouse.get_pos())):
                        self.selected = group
                        self.clicking = True

            else:
                self.clicking = False

        self.textRenderer.render(self.image) # type:ignore







    def getRelPos(self, absPos:tuple):
        relX = absPos[0] - self.rect.left # type:ignore
        relY = absPos[1] - self.rect.top # type:ignore
        return (relX, relY)


        
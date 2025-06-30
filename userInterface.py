from config import *
from tools import cutSpritesheet, TextRenderer
from conv import Conv
from furnace import Furnace
from miner import Miner
from buildingInfo import buildingGroups


class MiniMap(pygame.sprite.Sprite):
    def __init__(self, worldSurf:pygame.Surface, sizeX:int, pos:tuple):
        super().__init__()
        self.id = "MiniMap"
        self.visible = True
        # 250 px is the intended size
        self.scale = sizeX / 250
        self.borders = {"left": 10 * self.scale, "top": 10 * self.scale, "right": 10 * self.scale, "bottom": 10 * self.scale}

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
        self.viewRectThickness = max(1, int(2 * self.scale))
        self.borderThickness = max(1, int(4 * self.scale))
        
        # colors
        self.bgColor = (0,0,0,200)
        self.viewRectColor = colors.BLUE
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
        self.buildingButtons = {}
        self.selected = "organization"
        self.clicking = False
        # formating
        self.scale = sizeX / 250
        self.gridPadding = max(1, int(10 * self.scale))
        self.gridTileSize = max(1, int(50 * self.scale)), max(1, int(50 * self.scale))


        # colors
        self.bgColor = (0,0,0,200)
        self.borderColor = colors.DARKGREY
        self.borderThickness = max(1, int(4 * self.scale))
        self.textColor = colors.LIGHTGREY
        self.buttonColor = colors.GREY

        self.image = pygame.Surface((sizeX, sizeX * 2), pygame.SRCALPHA)

        self.rect = self.image.get_rect(topleft= pos)

        
        self.add(uiGroup)
        
        self.textRenderer = TextRenderer("assets/font/pixel_font.otf")
        first = True
        for group in self.buildingGroups:
            if first:
                groupPos = (10 * self.scale, self.gridPadding)
            else:
                groupPos = (10 * self.scale, self.textRenderer.textObjects[previousGroup].rect.bottom)
            self.textRenderer.addText(f" {group} ", group, 11, self.textColor, groupPos, rotation=90)
            # scaling
            oldsize = self.textRenderer.textObjects[group].rect.size
            newsize = (oldsize[0] * self.scale, oldsize[1] * self.scale)
            self.textRenderer.scale(group, newsize[0] * 1.6, newsize[1])
            first = False
            previousGroup = group

        # creating a surf wich will display all the buildings in a grid and scales dynamicly
        gridSurfX = self.rect.width - 2*self.gridPadding - self.textRenderer.textObjects[list(self.buildingGroups)[0]].rect.right - self.borderThickness
        gridSurfY = self.rect.height - 2*self.gridPadding
        self.gridSurf = pygame.Surface((gridSurfX, gridSurfY), pygame.SRCALPHA)
        self.gridSurfRect = self.gridSurf.get_rect(center = (self.getRelPos(self.rect.center)[0] + self.textRenderer.textObjects[list(self.buildingGroups)[0]].rect.right / 2, self.getRelPos(self.rect.center)[1]))
        


        
        collums = 3
        for group in self.buildingGroups:
            posX = 0
            posY = 0
            counter = 0
            self.buildingButtons[group] = []
            for element in self.buildingGroups[group]:
                row = counter // collums
                collum = counter % collums
                posX = self.gridTileSize[1] * collum + self.gridPadding * collum + self.gridPadding
                posY = self.gridTileSize[0] * row + self.gridPadding * row + self.gridPadding
                self.buildingButtons[group].append(BuildingButton(self.gridTileSize, element, (posX, posY)))
                counter += 1
            
                


        

    def update(self, cameraRect:pygame.Rect): # camera Rect not used in this class
        self.image.fill(self.bgColor) # type:ignore
        pygame.draw.rect(self.image, self.borderColor, (0,0,self.rect.width,self.rect.height), self.borderThickness) # type:ignore
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

        for group in self.buildingButtons:
            if group == self.selected:
                for button in self.buildingButtons[group]:
                    button.update()
                    button.draw(self.gridSurf)
                    print(button.rect)
        self.image.blit(self.gridSurf, self.gridSurfRect) # type:ignore
            

        self.textRenderer.render(self.image) # type:ignore


    def getRelPos(self, absPos:tuple):
        relX = absPos[0] - self.rect.left # type:ignore
        relY = absPos[1] - self.rect.top # type:ignore
        return (relX, relY)


class BuildingButton:
    def __init__(self, size:tuple, id:str, pos:tuple):
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft= pos)
        self.id = id
        match(self.id):
            case "conveyor": self.image.fill(colors.BLUEBRIGHT)
            case "miner": self.image.fill(colors.REDBRIGHT)
            case "furnace": self.image.fill(colors.GREENBRIGHT)
            case "placeholder": self.image.fill(colors.LIGHTGREY)
            case _: self.image.fill(colors.MINTBRIGHT)
        
        self.visible = True

    def draw(self, surface:pygame.Surface):
        if self.visible:
            
            surface.blit(self.image, self.rect)

    def update(self):
        pass

        
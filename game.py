from config import *
from tile import Tile
from item import Item
from conv import Conv
from worldTile import WorldTile

class Game:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode(SCREENSIZE)
        pygame.display.set_caption("FACTORY GAME")
        self.running = True
        self.mousePos = (0, 0)

        # creating sprite groups
        self.tilesWorldGroup = pygame.sprite.Group()
        self.tilesBuildingGroup = pygame.sprite.Group()
        self.itemGroup = pygame.sprite.Group()
        
        # importing imgs
        self.imgConvStraight = pygame.image.load("assets/sprites/conv/conv-up.png").convert_alpha()
        self.imgConvTurnLeft = pygame.image.load("assets/sprites/conv/conv-turn-left.png").convert_alpha()
        self.imgConvTurnRight = pygame.image.load("assets/sprites/conv/conv-turn-right.png").convert_alpha()

        # debug--------------------------
        print(type(self.imgConvStraight))
        self.conveyor = Conv((10,10), self.imgConvStraight, "left")
        self.conveyor.add(self.tilesBuildingGroup)
        print(self.tilesBuildingGroup)
        # debug--------------------------
        

        

        


    # just a basic input collection method (it reads the player input)
    def getInput(self):
        self.mousePos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
                

    # the gameLogic method updates the game state (all the exiting stuff happens here)
    def gameLogic(self):
        self.tilesBuildingGroup.update()

    # the drawing method (it draws everything. shocking right?)
    def renderFrame(self):
        self.display.fill("black")

        self.tilesWorldGroup.draw(self.display)
        self.tilesBuildingGroup.draw(self.display)
        self.itemGroup.draw(self.display)

        pygame.display.flip()

    # The main game loop (using methods for visual appeal lol)
    def run(self):
        while self.running:
            self.getInput()

            self.gameLogic()

            self.renderFrame()
            
        
        pygame.quit()
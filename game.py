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
        self.clock = pygame.time.Clock()
        
        # importing imgs
        self.imgConvStraight = pygame.image.load("assets/sprites/conv/conv-up.png").convert_alpha()
        self.imgConvTurnLeft = pygame.image.load("assets/sprites/conv/conv-turn-left.png").convert_alpha()
        self.imgConvTurnRight = pygame.image.load("assets/sprites/conv/conv-turn-right.png").convert_alpha()

        # debug--------------------------
        
        

        # debug--------------------------
        

        

        


    # just a basic input collection method (it reads the player input)
    def getInput(self):
        self.mousePos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
                

    # the gameLogic method updates the game state (all the exiting stuff happens here)
    def gameLogic(self):
        tilesBuildingGroup.update()

        if pygame.mouse.get_pressed()[0]:
            conveyor = Conv((self.mousePos[0] / TILESIZE, self.mousePos[1] / TILESIZE), self.imgConvTurnLeft, "left")
        elif pygame.mouse.get_pressed()[1]:
            conveyor = Conv((self.mousePos[0] / TILESIZE, self.mousePos[1] / TILESIZE), self.imgConvStraight, "left")
        elif pygame.mouse.get_pressed()[2]:
            conveyor = Conv((self.mousePos[0] / TILESIZE, self.mousePos[1] / TILESIZE), self.imgConvTurnRight, "left")
    # the drawing method (it draws everything. shocking right?)
    def renderFrame(self):
        self.display.fill("black")

        for sprite in tilesWorldGroup:
            sprite.draw(self.display)
        for sprite in tilesBuildingGroup:
            sprite.draw(self.display)
        for sprite in itemGroup:
            sprite.draw(self.display)

        pygame.display.flip()

    # The main game loop (using methods for visual appeal lol)
    def run(self):
        while self.running:
            self.getInput()

            self.gameLogic()

            self.renderFrame()

            self.clock.tick(FPS)
            
        
        pygame.quit()
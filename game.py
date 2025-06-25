from config import *
from tile import Tile
from item import Item
from conv import Conv
from worldBuilder import WorldBuilder
from debugInfo import DebugInfo
from userInterface import MiniMap




class Game:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode(SCREENSIZE)
        pygame.display.set_caption("FACTORY GAME")
        self.running = True
        self.mousePos = (0, 0)
        self.keys = pygame.key.get_pressed()
        self.clock = pygame.time.Clock()
        self.clicked = False

        self.uiScale = 1

        
        
        # setting the sisplay surface for the camera
        cameraGroup.setDisplaySurf(self.display)
        # importing imgs
        self.imgConvStraight = pygame.image.load("assets/sprites/conv/conv-up.png").convert_alpha()
        self.imgConvTurnLeft = pygame.image.load("assets/sprites/conv/conv-turn-left.png").convert_alpha()
        self.imgConvTurnRight = pygame.image.load("assets/sprites/conv/conv-turn-right.png").convert_alpha()

        # debug--------------------------
        
        debugFont = pygame.font.SysFont("consolas", 16)
        self.debugInfo = DebugInfo(debugFont)
        self.renderedSprites = 0
        
        # debug--------------------------

        # initializing objects
        self.worldBuilder = WorldBuilder("assets/maps/desert-01.tmx")
        cameraGroup.setWorldSurf(self.worldBuilder.worldSurf) # type:ignore
        miniMapSize = (200 * self.uiScale)
        miniMapPos = (self.display.get_width() - miniMapSize, 0)

        self.miniMap = MiniMap(self.worldBuilder.worldSurf, miniMapSize, miniMapPos) # type:ignore
        
    

    # just a basic input collection method (it reads the player input)
    def getInput(self):
        self.mousePos = pygame.mouse.get_pos()
        self.keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            # zooming only here possible
            if event.type == pygame.MOUSEWHEEL:
                mouseScreen = pygame.Vector2(self.mousePos)
                mouseWorldBefore = cameraGroup.offset + mouseScreen / cameraGroup.zoomScale
                
                cameraGroup.zoomScale += event.y * cameraGroup.zoomForce
                cameraGroup.zoomScale = max(cameraGroup.minZoom, min(cameraGroup.maxZoom, cameraGroup.zoomScale))
                
                mouseWorldAfter = cameraGroup.offset + mouseScreen / cameraGroup.zoomScale
                cameraGroup.offset += (mouseWorldBefore - mouseWorldAfter
                                )
                #cameraGroup.zoomScale = round(cameraGroup.zoomScale * 2) / 2
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DELETE:
                    self.debugInfo.visible = not self.debugInfo.visible   
        
                
                

    # the gameLogic method updates the game state (all the exiting stuff happens here)
    def gameLogic(self):
        
        tilesBuildingGroup.update()
        cameraGroup.update(self.keys, self.mousePos)
        uiGroup.update(cameraGroup.cameraRect)

        # debug---------------
        self.debugInfo.add("FPS", round(self.clock.get_fps()))
        self.debugInfo.add("Camera Offset", cameraGroup.offset)
        self.debugInfo.add("Zoom", round(cameraGroup.zoomScale, 2))
        self.debugInfo.add("Mouse Pos", pygame.mouse.get_pos())
        self.debugInfo.add("Sprites Rendered", self.renderedSprites)
        self.debugInfo.add("Camera Rect", cameraGroup.cameraRect)
        #self.debug_info.add("Tile Under Cursor", world_pos)


        # debug---------------
        

        

    # the drawing method (it draws everything. shocking right?)
    def renderFrame(self):
        self.display.fill(colors.BLACK)
        # renderering sprites affected by the camera in the order specified in config
        self.renderedSprites = cameraGroup.customDraw()
        # renders the ui
        uiGroup.draw(self.display)

        # renders debug info disable with delete key
        self.debugInfo.render(self.display)

        pygame.display.flip()

    # The main game loop (using methods for visual appeal lol)
    def run(self):
        while self.running:
            self.getInput()

            self.gameLogic()

            self.renderFrame()
            #print(self.clock.get_fps())
            self.clock.tick(120)
            
        
        pygame.quit()
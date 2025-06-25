from config import *
from tile import Tile
from item import Item
from conv import Conv
from worldBuilder import WorldBuilder
from debugInfo import DebugInfo
from userInterface import MiniMap
import time




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

        self.fps = 120

        
        
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
        conv = Conv((16*10,16*10), self.imgConvStraight, "up")
        
        # debug--------------------------

        # initializing objects
        self.worldBuilder = WorldBuilder("assets/maps/desert-01.tmx")
        cameraGroup.setWorldSurf(self.worldBuilder.worldSurf) # type:ignore
        miniMapSize = (200 * self.uiScale)
        miniMapPos = (self.display.get_width() - miniMapSize - 5, 5)

        self.miniMap = MiniMap(self.worldBuilder.worldSurf, miniMapSize, miniMapPos) # type:ignore
        
    

    # just a basic input collection method (it reads the player input)
    def getInput(self, dt):
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
                if event.key == pygame.K_F2:
                    self.debugInfo.visible = not self.debugInfo.visible
                if event.key == pygame.K_F1:
                    for uiElement in uiGroup:
                        uiElement.visible = not uiElement.visible
        
                
                

    # the gameLogic method updates the game state (all the exiting stuff happens here)
    def gameLogic(self, dt):
        
        tilesBuildingGroup.update()
        cameraGroup.update(self.keys, self.mousePos, dt)
        uiGroup.update(cameraGroup.cameraRect)

        # debug---------------
        self.debugInfo.add("FPS", round(1.0 / dt, 1))
        self.debugInfo.add("Delta Time", round(dt, 6))
        self.debugInfo.add("Camera Offset", cameraGroup.offset)
        self.debugInfo.add("Zoom", round(cameraGroup.zoomScale, 2))
        self.debugInfo.add("Mouse Pos", self.mousePos)
        relMousePosX = self.mousePos[0] / cameraGroup.zoomScale + cameraGroup.offset.x
        relMousePosY = self.mousePos[1] / cameraGroup.zoomScale + cameraGroup.offset.y
        self.debugInfo.add("Rel. Mouse Pos", (round(relMousePosX), round(relMousePosY)))
        self.debugInfo.add("Sprites Rendered", self.renderedSprites)
        self.debugInfo.add("Camera Rect", cameraGroup.cameraRect)
        #self.debug_info.add("Tile Under Cursor", world_pos)


        # debug---------------
        

        

    # the drawing method (it draws everything. shocking right?)
    def renderFrame(self, dt):
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
        # for dt
        previousTime = time.time()
        frameDuration = 1.0 / self.fps

        while self.running:
            # calculating dt
            dt = time.time() - previousTime
            if dt < frameDuration:
                time.sleep(frameDuration - dt)
            currentTime = time.time()
            dt = min(currentTime - previousTime, frameDuration)    
            previousTime = currentTime
            

            self.getInput(dt)

            self.gameLogic(dt)

            self.renderFrame(dt)
           
            
        
        pygame.quit()
import pygame


class CameraGroup(pygame.sprite.Group):
    def __init__(self, groups:list): # sprite groups in render order
        super().__init__()
        self.hasDisplaySurf = False # camera needs display surf to work
        self.displaySurf = None
        self.groups = groups
        self.speed = 5
        self.speedModifier = 3
        self.cameraRect = None

        # need to render tiles as one surface when zooming out:
        self.worldSurf1x = None # same as Display ´Surf
        self.worldSurf05x = None
        self.hasWorldSurf = False
        self.worldWidth = None
        self.worldHeight = None


        self.offset = pygame.math.Vector2()
        self.cameraBorders = {"left": 200, "right": 200, "top": 100, "bottom": 100}
        self.cameraRect = None
        self.direction = pygame.math.Vector2()

        # draging controll
        self.dragStartMouse = pygame.math.Vector2()
        self.dragStartOffset = self.offset.copy()
        self.dragging = False

        # zoom
        self.zoomScale = 1.0
        self.zoomForce = 0.5
        self.maxZoom = 4
        self.minZoom = 0.5

    
    def setDisplaySurf(self, displaySurf:pygame.Surface):
        self.displaySurf = displaySurf
        self.offset = pygame.math.Vector2(displaySurf.get_size()) / 2
        self.w = self.displaySurf.get_width()
        self.h = self.displaySurf.get_height()
        self.cameraSurf = pygame.Surface((self.w, self.h))
        self.hasDisplaySurf = True

    def setWorldSurf(self, worldsurf:pygame.Surface):
        self.worldSurf1x = worldsurf
        self.worldSurf05x = pygame.transform.scale(worldsurf, (worldsurf.get_width() * 0.5, worldsurf.get_height() * 0.5))
        self.hasWorldSurf = True
        self.worldWidth = worldsurf.get_width()
        self.worldHeight = worldsurf.get_height()
    
    def customDraw(self, keys:pygame.key.ScancodeWrapper, mousePos:tuple):
        if not self.hasDisplaySurf:
            raise RuntimeError("Camera display surface not set!")
        
        self.moveCamera(keys, mousePos)
        self.cameraSurf.fill((0,0,0))
        
        
        visible_w = self.w / self.zoomScale
        visible_h = self.h / self.zoomScale
        cameraRect = pygame.Rect(self.offset.x, self.offset.y, visible_w, visible_h)
        renderedSprites = 0 # for debugging
        if self.zoomScale > 1:
            for group in self.groups:
                for sprite in group:
                    if cameraRect.colliderect(sprite.rect):
                        zoomedImg = sprite.getScaledImg(self.zoomScale)
                        spriteOffsetPos = (sprite.rect.topleft - self.offset) * self.zoomScale
                        self.displaySurf.blit(zoomedImg, spriteOffsetPos)
                        renderedSprites += 1
        elif self.zoomScale <= 1 and self.hasWorldSurf:
                
            worldOffsetPos = -self.offset
            if self.zoomScale == 1:
                self.displaySurf.blit(self.worldSurf1x, worldOffsetPos, area= self.cameraRect)
            elif self.zoomScale == 0.5:
                self.displaySurf.blit(self.worldSurf05x, worldOffsetPos, area= self.cameraRect)
        return renderedSprites

        
            

    def moveCamera(self, keys:pygame.key.ScancodeWrapper, mousePos:tuple):
        # checks if shift is pressed and aplies faster speed if so
        if keys[pygame.K_LSHIFT]:
            cameraSpeed = self.speed * self.speedModifier / self.zoomScale
        else:
            cameraSpeed = self.speed / self.zoomScale

        self.moveCameraWithMouse(mousePos)
        self.moveCameraWithKeys(keys)

        # apllies then direction vector to the offset
        if self.direction.length() != 0:
            self.offset += self.direction.normalize() * cameraSpeed
        else:
            self.offset += (0,0)

    #i aplies the bounderys for the camera movement
        if self.offset.x <= 0: 
           self.offset.x = 0
        elif self.offset.x >= self.worldWidth: # type: ignore
           self.offset.x = self.worldWidth# type: ignore

        if self.offset.y <= 0:
            self.offset.y = 0
        elif self.offset.y >= self.worldHeight: # type: ignore
            self.offset.y = self.worldHeight # type: ignore

    def moveCameraWithKeys(self, keys:pygame.key.ScancodeWrapper):
        
        # changes the direction vector to match player input
        if not keys[pygame.K_w]:
            self.direction.y = 0
        elif not keys[pygame.K_s]:
            self.direction.y = 0
        if not keys[pygame.K_a]:
            self.direction.x = 0
        elif not keys[pygame.K_d]:
            self.direction.x = 0
        
        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        if keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_d]:
            self.direction.x = 1

        
    def moveCameraWithMouse(self, mousePos:tuple):
        if pygame.mouse.get_pressed()[1]:
            if not self.dragging:
                self.dragStartMouse = pygame.math.Vector2(mousePos)
                self.dragStartOffset = self.offset.copy()
                self.dragging = True
            dragDelta = pygame.math.Vector2(mousePos) - self.dragStartMouse # type: ignore
            self.offset = self.dragStartOffset - dragDelta / self.zoomScale
        else:
            self.dragging = False




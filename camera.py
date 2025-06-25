import pygame


class CameraGroup(pygame.sprite.Group):
    def __init__(self, groups:list): # sprite groups in render order
        super().__init__()
        self.hasDisplaySurf = False # camera needs display surf to work
        self.displaySurf = None
        self.groups = groups
        self.speed = 600
        self.speedModifier = 3

        # need to render tiles as one surface when zooming out:
        self.hasWorldSurf = False
        self.worldWidth = None
        self.worldHeight = None
        self.worldSurfaces = {}


        self.offset = pygame.math.Vector2()
        self.oldOffset = self.offset.copy()
        self.cameraBorders = {"left": 150, "right": 150, "top": 150, "bottom": 150}
        self.cameraRect = pygame.Rect()
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
        self.worldSurfaces = {
        1.0:worldsurf,
        0.5:pygame.transform.scale(worldsurf, (int(worldsurf.get_width() * 0.5), int(worldsurf.get_height() * 0.5))),
        1.5:pygame.transform.scale(worldsurf, (int(worldsurf.get_width() * 1.5), int(worldsurf.get_height() * 1.5))),
        2.0:pygame.transform.scale(worldsurf, (worldsurf.get_width() * 2.0, worldsurf.get_height() * 2.0)),
        2.5:pygame.transform.scale(worldsurf, (int(worldsurf.get_width() * 2.5), int(worldsurf.get_height() * 2.5))),
        3.0:pygame.transform.scale(worldsurf, (worldsurf.get_width() * 3.0, worldsurf.get_height() * 3.0)),
        3.5:pygame.transform.scale(worldsurf, (int(worldsurf.get_width() * 3.5), int(worldsurf.get_height() * 3.5))),
        4.0:pygame.transform.scale(worldsurf, (worldsurf.get_width() * 4.0, worldsurf.get_height() * 4.0))
        }
        self.hasWorldSurf = True
        self.worldWidth = worldsurf.get_width()
        self.worldHeight = worldsurf.get_height()

    def update(self, keys:pygame.key.ScancodeWrapper, mousePos:tuple, dt:float):
        if not self.hasDisplaySurf:
            raise RuntimeError("Camera display surface not set!")
        self.moveCamera(keys, mousePos, dt)
    
    def customDraw(self):
        if not self.hasDisplaySurf:
            raise RuntimeError("Camera display surface not set!")
        elif not self.hasWorldSurf:
            raise RuntimeError("World surface not set")
        
        self.cameraSurf.fill((0,0,0))

        
        self.offset.x = round(self.offset.x, 0)
        self.offset.y = round(self.offset.y, 0)

        
        visible_w = self.w / self.zoomScale
        visible_h = self.h / self.zoomScale

        self.cameraRect.topleft = (self.offset.x, self.offset.y)
        self.cameraRect.size = (visible_w, visible_h)
        renderedSprites = 0 # for debugging
    
        worldOffsetPos = -self.offset * self.zoomScale
        worldSurf = self.worldSurfaces[self.zoomScale]
        if not worldSurf:
            raise RuntimeError(f"zoom level {self.zoomScale} does not exist!")
        else:
            self.displaySurf.blit(worldSurf, worldOffsetPos) # type:ignore


        for group in self.groups:
            for sprite in group:
                if self.cameraRect.colliderect(sprite.rect):
                    scaledImg = sprite.getScaledImg(self.zoomScale)
                    spriteOffsetPos = (sprite.rect.topleft - self.offset) * self.zoomScale
                    self.displaySurf.blit(scaledImg, spriteOffsetPos) # type:ignore
                    renderedSprites += 1

                
        #if self.zoomScale == 1:
        #    self.displaySurf.blit(self.worldSurf1x, worldOffsetPos) # type:ignore
        #elif self.zoomScale == 0.5:
        #    self.displaySurf.blit(self.worldSurf05x, worldOffsetPos) # type:ignore
        return renderedSprites

        
            

    def moveCamera(self, keys:pygame.key.ScancodeWrapper, mousePos:tuple, dt:float):
        # checks if shift is pressed and aplies faster speed if so
        
        if keys[pygame.K_LSHIFT]:
            cameraSpeed = self.speed * self.speedModifier / (self.zoomScale/2) * dt
        else:
            cameraSpeed = self.speed / (self.zoomScale/2) * dt

        self.moveCameraWithMouse(mousePos)
        self.moveCameraWithKeys(keys)

        # apllies then direction vector to the offset
        if self.direction.length() != 0:
            self.offset += self.direction.normalize() * cameraSpeed
        else:
            self.offset += (0,0)

    #i aplies the bounderys for the camera movement
        visibleW = self.w / self.zoomScale
        visibleH = self.h / self.zoomScale

        maxOffsetX = self.worldWidth - visibleW + self.cameraBorders["right"] * self.zoomScale # type:ignore
        maxOffsetY = self.worldHeight - visibleH + self.cameraBorders["bottom"] * self.zoomScale # type:ignore

        self.offset.x = max(-self.cameraBorders["left"] * self.zoomScale, min(self.offset.x, maxOffsetX))
        self.offset.y = max(-self.cameraBorders["top"] * self.zoomScale, min(self.offset.y, maxOffsetY))

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




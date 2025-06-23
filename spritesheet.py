from config import *

class Spritesheet():
	def __init__(self, img, tilesize_x, tilesize_y):
		self.img = img
		self.tilesize = (tilesize_x, tilesize_y)
		

	def get_img(self, index:int, scale:float = 1.0):
		img = pygame.Surface(self.tilesize).convert_alpha()
		img.fill((1,0,0))
		img.blit(self.img, (0,0), (self.tilesize[0] * index, 0, self.tilesize[0], self.tilesize[1]))
		img = pygame.transform.scale(img, (self.tilesize[0] * scale, self.tilesize[1] * scale))
		img.set_colorkey((1,0,0))

		return img

	def get_img_world(self, index:int):
		cols = self.img.get_width() // self.tilesize[0]
		row = index // cols
		col = index % cols
		surf = pygame.Surface(self.tilesize, pygame.SRCALPHA)
		surf.blit(self.img, (0,0),(col * self.tilesize, row * self.tilesize))

		return surf
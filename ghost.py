# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *

# 残影特效
class Ghost(pygame.sprite.Sprite):
	def __init__(self, x, y, img, group = pygame.sprite.Group()):
		self.x = x
		self.y = y
		self.img = img.convert_alpha()
		self.hide_speed = 120
		self.count = 1
		self.type = "ghost"
		self.live = True
		self.group = group

	def draw(self, surface):
		surface.blit(self.img, (self.x, self.y))

	def update(self, gameObjects):
		for gameObj in gameObjects:
			if gameObj.type == "player":
				pass
		# 变透明
		self.img.set_alpha(255 - self.hide_speed * self.count)
		self.count += 1
		if self.hide_speed * self.count > 255:
			self.live = False
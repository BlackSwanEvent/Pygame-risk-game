# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *

# 背景
class Bg(pygame.sprite.Sprite):
	def __init__(self, x = 0, y = 0, img = pygame.image.load('img/cloud.png'), group = pygame.sprite.Group()):
		super().__init__()
		self.x = x
		self.y = x
		self.img = img.convert_alpha()
		self.type = "bg"
		# 声明非透明区域才会触发碰撞
		self.rect = self.img.get_rect()
		self.mask = pygame.mask.from_surface(self.img)
		self.group = group

	def draw(self, surface):
		surface.blit(self.img, (self.x, self.y))

	def update(self, gameObjects):
		for gameObj in gameObjects:
			if gameObj.type == "player":
				pass
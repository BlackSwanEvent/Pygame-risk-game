# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *

# 激光
class Laser(pygame.sprite.Sprite):
	def __init__(self, x = 0, y = 0, imglist = [], group = pygame.sprite.Group()):
		super().__init__()
		self.imglist = imglist
		#self.img = pygame.image.load('img/lavalist/0.png').convert_alpha()
		self.type = "laser"
		self.index = 0
		# 声明非透明区域才会触发碰撞
		self.rect = self.imglist[self.index].get_rect()
		self.rect.top = x
		self.rect.left = y
		self.mask = pygame.mask.from_surface(self.imglist[self.index])
		self.group = group
		self.show = False
		self.count = 0
		self.wait_time = 20

	def draw(self, surface):
		if self.show:
			surface.blit(self.imglist[self.index], (self.rect.left, self.rect.top))

	def update(self, gameObjects):
		for gameObj in gameObjects:
			if gameObj.type == "player":
				pass
		self.count += 1
		if self.count > self.wait_time:
			self.count = 0
			if self.show:
				self.show = False
			else:
				self.show = True
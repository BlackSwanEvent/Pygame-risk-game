# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *

# 障碍物1
class Obstacle1(pygame.sprite.Sprite):
	def __init__(self, x = 0, y = 0, imglist = [], group = pygame.sprite.Group()):
		super().__init__()
		self.imglist = imglist
		#self.img = pygame.image.load('img/landlist/0.png').convert_alpha()
		self.type = "obstacle1"
		self.index = 0
		# 声明非透明区域才会触发碰撞
		self.rect = self.imglist[self.index].get_rect()
		self.rect.top = x
		self.rect.left = y
		self.mask = pygame.mask.from_surface(self.imglist[self.index])
		self.state = 'down'
		self.speed = 5
		self.group = group

	def draw(self, surface):
			surface.blit(self.imglist[self.index], (self.rect.left, self.rect.top))

	def update(self, gameObjects):
		for gameObj in gameObjects:
			if gameObj.type == "player":
				pass
				
		# 障碍物运动
			if self.state == 'down':
				self.rect.top += self.speed
			else:
				self.rect.top -= self.speed
			if self.rect.top > 50:
				self.state = 'up'
				self.rect.top = 50
			if self.rect.top < -500:
				self.state = 'down'
				self.rect.top = -500
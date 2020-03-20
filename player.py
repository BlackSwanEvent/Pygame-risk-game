# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *

# 玩家
class Player(pygame.sprite.Sprite):
	def __init__(self, bg_width, bg_height, group = pygame.sprite.Group()):
		super().__init__()
		self.type = "player"
		self.gameOver = False
		self.img = pygame.image.load('img/gobo1.png').convert_alpha()
		self.flip_img = pygame.transform.flip(self.img, True, False)
		self.now_img = self.img
		self.width = pygame.Surface.get_width(self.img)
		self.height = pygame.Surface.get_height(self.img)
		self.bg_width = bg_width
		self.bg_height = bg_height
		self.jump_speed = 13
		self.move_speed = 1.5
		self.x_speed = 0
		self.y_speed = 0
		self.gravity = 1
		self.index = 0
		# 声明非透明区域才会触发碰撞
		self.rect = self.now_img.get_rect()
		self.rect.top = 426
		self.rect.left = 0
		self.mask = pygame.mask.from_surface(self.now_img)
		# 进入下一关的位置
		self.next_level_pos_list = (\
		# 第一关
		(668, 426),\
		# 第二关
		(668, 426),\
		# 第三关
		(668, 426),\
		# 第四关
		(668, 297),\
		# 第五关
		(668, 55),\
		# 第六关
		(668, 426),\
		# 第七关
		(668, 426),\
		# 第八关
		(668, 426),\
		# 第九关
		(668, 361),\
		# 第十关
		(668, 16),\
		# 第十一关
		(0, 16),\
		)
		self.group = group
		# 左右是否碰到墙壁
		self.left_is_space = True
		self.right_is_space = True

	def draw(self, surface):
		surface.blit(self.now_img, (self.rect.left, self.rect.top))

	def update(self, gameObjects):
		for gameObj in gameObjects:
			# 碰到岩浆
			if gameObj.type == "lava":
				if pygame.sprite.spritecollide(self, gameObj.group, False, pygame.sprite.collide_mask):
					self.rect.top = 426
					self.rect.left = 0
					# 初始化撞墙状态
					self.right_is_space = True
					self.left_is_space = True
			# 碰到障碍物1
			if gameObj.type == "obstacle1" and (self.index == 5 or self.index == 6):
				if pygame.sprite.spritecollide(self, gameObj.group, False, pygame.sprite.collide_mask):
					self.rect.top = 426
					self.rect.left = 0
					# 初始化撞墙状态
					self.right_is_space = True
					self.left_is_space = True
			# 碰到激光
			if gameObj.type == "laser" and (self.index >= 7 and self.index <= 9) and gameObj.show:
				if pygame.sprite.spritecollide(self, gameObj.group, False, pygame.sprite.collide_mask):
					self.rect.top = 426
					self.rect.left = 0
					# 初始化撞墙状态
					self.right_is_space = True
					self.left_is_space = True
			# 碰撞检测
			if gameObj.type == "land":
				# 重力叠加
				self.y_speed += self.gravity
				# 更新纵坐标
				self.rect.top += self.y_speed
				# 按键检测
				self.keys = pygame.key.get_pressed()
				# 横向阻力
				self.x_speed *= 0.85
				if abs(self.x_speed) < 1:
					self.x_speed = 0
				# 更新横坐标
				self.rect.left += self.x_speed
				# 跳关
				if self.keys[pygame.K_SPACE]:
					self.rect.left = self.next_level_pos_list[self.index][0] - 1
					self.rect.top = self.next_level_pos_list[self.index][1]
				# 地面碰撞检测
				if pygame.sprite.spritecollide(self, gameObj.group, False, pygame.sprite.collide_mask):
					self.rect.top -= self.y_speed
					self.y_speed = 0
				# 横向碰撞检测
				if pygame.sprite.spritecollide(self, gameObj.group, False, pygame.sprite.collide_mask):
					self.rect.top -= 1
					if pygame.sprite.spritecollide(self, gameObj.group, False, pygame.sprite.collide_mask):
						self.rect.top -= 1
						if pygame.sprite.spritecollide(self, gameObj.group, False, pygame.sprite.collide_mask):
							self.rect.top -= 1
							if pygame.sprite.spritecollide(self, gameObj.group, False, pygame.sprite.collide_mask):
								self.rect.top -= 1
								if pygame.sprite.spritecollide(self, gameObj.group, False, pygame.sprite.collide_mask):
									self.rect.top -= 1
									if pygame.sprite.spritecollide(self, gameObj.group, False, pygame.sprite.collide_mask):
										self.rect.top += 5
										if self.x_speed > 0:
											self.right_is_space = False
										elif self.x_speed < 0:
											self.left_is_space = False
										self.x_speed = 0
				# 方向键
				if not (self.keys[pygame.K_LEFT] and self.keys[pygame.K_RIGHT]):
					if self.keys[pygame.K_LEFT] and self.left_is_space:
						self.now_img = self.flip_img
						self.mask = pygame.mask.from_surface(self.now_img)
						self.x_speed -= self.move_speed
						self.right_is_space = True
						if pygame.sprite.spritecollide(self, gameObj.group, False, pygame.sprite.collide_mask):
							self.rect.left -= 5
					elif self.keys[pygame.K_RIGHT] and self.right_is_space:
						self.now_img = self.img
						self.mask = pygame.mask.from_surface(self.now_img)
						self.x_speed += self.move_speed
						self.left_is_space = True
						if pygame.sprite.spritecollide(self, gameObj.group, False, pygame.sprite.collide_mask):
							self.rect.left += 5
				if not self.left_is_space:
					while pygame.sprite.spritecollide(self, gameObj.group, False, pygame.sprite.collide_mask):
						self.rect.left += 1
				if not self.right_is_space:
					while pygame.sprite.spritecollide(self, gameObj.group, False, pygame.sprite.collide_mask):
						self.rect.left -= 1
				# 跳跃
				self.rect.top += 1
				if self.keys[pygame.K_UP] and pygame.sprite.spritecollide(self, gameObj.group, False, pygame.sprite.collide_mask):
					self.y_speed -= self.jump_speed
				self.rect.top -= 1
				# 空中解除左右移动限制
				if (not pygame.sprite.spritecollide(self, gameObj.group, False, pygame.sprite.collide_mask)) and self.y_speed < 0:
						self.left_is_space = True
						self.right_is_space = True
		
		# 边缘检测
		if self.rect.left > self.bg_width - self.width:
			self.rect.left = self.bg_width - self.width
		if self.rect.left < 0:
			self.rect.left = 0
		if self.rect.top > self.bg_height - self.height:
			self.rect.top = self.bg_height - self.height
			self.y_speed = 0
		if self.rect.top < 0:
			self.rect.top = 0
			self.y_speed = 0

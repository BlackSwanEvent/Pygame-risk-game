# -*- coding: utf-8 -*-

import pygame
from random import random
from pygame.locals import *
import player
import ghost
import bg
import land
import lava
import obstacle.obstacle1
import laser.laser

pygame.init()
resolution = width, height = (720, 540)
#resolution = width, height = (int(pygame.display.Info().current_w / 2), int(pygame.display.Info().current_h / 2))
screen = pygame.display.set_mode(resolution, 0)
pygame.display.set_caption("Risk")

# 游戏控制器
class GameController:
    def __init__(self, interval = 5):
        self.inter = interval
        self.next = pygame.time.get_ticks() + (2 * 1000)
        self.type = "game controller"
        self.score = 0
        self.scoreText = pygame.font.Font(None, 12)
        self.x = 0
        self.y = 0
        self.y_speed = 0
        self.x_speed = 0
        self.collide_num = False
        self.left_is_space = True
        self.right_is_space = True

    def update(self, gameObjects):
        pass
        # self.score += 0

    def draw(self, screen):
        screen.blit(self.scoreText.render('y_speed = '+str(self.y_speed), 3, (255, 0, 255)), (50,50))
        screen.blit(self.scoreText.render('collide_num = '+str(self.collide_num), 3, (255, 0, 255)), (50,55))
        screen.blit(self.scoreText.render('x_speed = '+str(self.x_speed), 3, (255, 0, 255)), (50,60))
        screen.blit(self.scoreText.render('x = '+str(self.x), 3, (255, 0, 255)), (50,65))
        screen.blit(self.scoreText.render('y = '+str(self.y), 3, (255, 0, 255)), (50,70))
        screen.blit(self.scoreText.render('left_is_space = '+str(self.left_is_space), 3, (255, 0, 255)), (50,80))
        screen.blit(self.scoreText.render('right_is_space = '+str(self.right_is_space), 3, (255, 0, 255)), (50,90))

class game():
	def __init__(self):
		# 初始化
		self.clock = pygame.time.Clock()
		self.gameOver = False
		self.screen = screen
		# 创建游戏对象列表
		self.gameObjects = []
		# 载入背景
		self.bg = bg.Bg()
		self.gameObjects.append(self.bg)
		# 载入玩家
		self.me = player.Player(width, height)
		self.gameObjects.append(self.me)
		self.me.group.add(self.me)
		# 载入岩浆
		self.lavalist = []
		for i in range(11):
			self.lavalist.append(pygame.image.load('img/lavalist/' + str(i) + '.png').convert_alpha())
		self.lava = lava.Lava(imglist = self.lavalist)
		self.gameObjects.append(self.lava)
		self.lava.group.add(self.lava)
		# 载入地面
		self.landlist = []
		for i in range(11):
			self.landlist.append(pygame.image.load('img/landlist/' + str(i) + '.png').convert_alpha())
		self.land = land.Land(imglist = self.landlist)
		self.gameObjects.append(self.land)
		self.land.group.add(self.land)
		# 载入游戏控制器
		self.gameObjects.append(GameController())

	def handleEvents(self):
		for event in pygame.event.get(pygame.QUIT):
			if event.type == QUIT:
				pygame.quit()
		self.keys = pygame.key.get_pressed()
		if self.keys[pygame.K_q]:
			pygame.quit()

	def run(self):
		while True:
			#用户事件
			self.handleEvents()
			
			if not self.gameOver:
				for gameObj in self.gameObjects:
					# 玩家侦测
					if gameObj.type == "player":
						# 游戏结束标志判断
						self.gameOver = gameObj.gameOver
						# 下一关
						if gameObj.rect[:2] == list(gameObj.next_level_pos_list[self.land.index]):
							self.land.index += 1
							self.lava.index += 1
							gameObj.index += 1
							# 根据关卡的不同出现的物体
							if gameObj.index == 5:
								# 载入障碍物1
								self.obstacle1list = []
								for i in range(2):
									self.obstacle1list.append(pygame.image.load('obstacle/img/obstacle1list/' + str(i) + '.png').convert_alpha())
								self.obstacle1 = obstacle.obstacle1.Obstacle1(imglist = self.obstacle1list)
								self.gameObjects.insert(1, self.obstacle1)
								self.obstacle1.group.add(self.obstacle1)
							elif gameObj.index == 6:
								self.obstacle1.index += 1
								self.obstacle1.mask = pygame.mask.from_surface(self.obstacle1.imglist[self.obstacle1.index])
							elif gameObj.index == 7:
								# 载入激光
								self.laserlist = []
								for i in range(3):
									self.laserlist.append(pygame.image.load('laser/img/laserlist/' + str(i) + '.png').convert_alpha())
								self.laser = laser.laser.Laser(imglist = self.laserlist)
								self.gameObjects.insert(1, self.laser)
								self.laser.group.add(self.laser)
							elif gameObj.index == 8:
								self.laser.index += 1
								self.laser.mask = pygame.mask.from_surface(self.laser.imglist[self.laser.index])
							elif gameObj.index == 9:
								self.laser.wait_time = 40
								self.laser.index += 1
								self.laser.mask = pygame.mask.from_surface(self.laser.imglist[self.laser.index])
							elif gameObj.index == 10:
								pass
							self.land.mask = pygame.mask.from_surface(self.land.imglist[self.land.index])
							self.lava.mask = pygame.mask.from_surface(self.lava.imglist[self.lava.index])
							gameObj.rect.top = 426
							gameObj.rect.left = 0
					# 调试数据与游戏信息
					if gameObj.type == "game controller":
						gameObj.y_speed = self.me.y_speed
						gameObj.collide_num = pygame.sprite.spritecollide(\
						self.me, self.land.group, False, pygame.sprite.collide_mask)
						gameObj.x_speed = self.me.x_speed
						gameObj.x = self.me.rect.left
						gameObj.y = self.me.rect.top
						gameObj.left_is_space = self.me.left_is_space
						gameObj.right_is_space = self.me.right_is_space
					# 残影清除判断
					if gameObj.type == "ghost":
						if not gameObj.live:
							self.gameObjects.remove(gameObj)
					# 清除障碍物1
					if gameObj.type == "obstacle1":
						if self.me.index == 7:
							self.gameObjects.remove(gameObj)
					# 清除激光
					if gameObj.type == "laser":
						if self.me.index == 10:
							self.gameObjects.remove(gameObj)
					# 更新实例属性
					gameObj.update(self.gameObjects)
							
			# 添加玩家残影
			# self.gameObjects.append(ghost.Ghost(self.me.x, self.me.y, self.me.now_img))
			
			for gameObj in self.gameObjects:
				gameObj.draw(self.screen)

			self.clock.tick(60)
			pygame.display.flip()

if __name__ == "__main__":
	try:
		game().run()
	except SystemExit:
		pass
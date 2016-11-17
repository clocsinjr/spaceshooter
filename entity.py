import pygame
import random
import math
import images

#player constants
PSPEED = 5
PSIZE = 16

PDIRL = 0
PDIRR = 1
PDIRN = 2

BDIRU = 0
BDIRD = 1

#projectile constants
KSIZE = 1
KSPEED = 10
KDMG = 5

# enemy types
E_FODDER = 0
E_GRUNT = 1
E_SINE = 2
E_SENTRY = 3

# enemy type size constants
RFODDER = 16
RSINE = 16
RGRUNT = 16
RSENTRY = 16

SINEAMP = 50
class player(pygame.sprite.Sprite):
	def __init__(self, size):
		pygame.sprite.Sprite.__init__(self)
		
		#player stats
		self.score = 0
		self.HP = 100
		self.DMG = 5.0
		self.facing = -(1.0/2.0)*math.pi
		self.alive = True
		
		#movement and position
		self.MS = 1.0		# (multiplier)
		
		self.gunCD = 10
		self.gunTime = 0
		
		self.playerSize = 2 * PSIZE
		self.image = images.playerMoveNone
		self.rect = self.image.get_rect()
		self.rect[0] = size[0] / 2 - PSIZE
		self.rect[1] = (size[1] / 7) * 6 - PSIZE
		
		# buffs
		self.scopeTime =  0
		self.ASTime = 0
		
	def move(self, direction, size):
		if direction == PDIRN:
			self.image = images.playerMoveNone
		elif direction == PDIRL and self.rect[0] > 0:
			self.rect[0] -= self.MS * PSPEED
			self.image = images.playerMoveLeft
		elif direction == PDIRR and self.rect[0] < size[0] - self.playerSize:
			self.rect[0] += self.MS * PSPEED
			self.image = images.playerMoveRight
	
	def updateTimers(self):
		if self.scopeTime > 0: self.scopeTime -= 1
		if self.ASTime > 0: self.ASTime -= 1
		if self.gunTime > 0: self.gunTime -= 1
		


class projectile(pygame.sprite.Sprite):
	def __init__(self, origin):
		pygame.sprite.Sprite.__init__(self)
		
		self.HP = 100
		self.facing = origin.facing
		self.DMG = origin.DMG
		
		projSize = 2*KSIZE + 1
		if self.DMG >= 5.0:
			projSize += 2
		
		self.image = pygame.Surface([projSize, projSize])
		self.image.fill([255, 255, 255, 0])
		
		self.rect = self.image.get_rect()
		
		if self.DMG >= 5.0:
			self.rect[0] = origin.rect[0] + PSIZE - KSIZE -1
			self.rect[1] = origin.rect[1] + PSIZE - KSIZE -1
			
			self.actx = 1.0 * (origin.rect[0] + PSIZE - KSIZE -1)
			self.acty = 1.0 * (origin.rect[1] + PSIZE - KSIZE -1)
		else:
			self.rect[0] = origin.rect[0] + PSIZE - KSIZE
			self.rect[1] = origin.rect[1] + PSIZE - KSIZE
			
			self.actx = 1.0 * (origin.rect[0] + PSIZE - KSIZE)
			self.acty = 1.0 * (origin.rect[1] + PSIZE - KSIZE)
		
		
		
	def moveProjectile(self):
		dx = math.cos(self.facing) * KSPEED
		dy = math.sin(self.facing) * KSPEED
		
		self.actx += dx
		self.acty += dy
		
		self.rect[0] = self.actx
		self.rect[1] = self.acty





class hpup(pygame.sprite.Sprite):
	def __init__(self, size, x, y):
		pygame.sprite.Sprite.__init__(self)
		
		#player stats
		self.HP = 20
		self.image = images.hpup
		self.rect = self.image.get_rect()
		self.rect[0] = x - RFODDER
		self.rect[1] = y
		
	def move(self):
		self.rect[1] += 3

class scope(pygame.sprite.Sprite):
	def __init__(self, size, x, y):
		pygame.sprite.Sprite.__init__(self)
		
		#player stats
		self.time =  15 * 60
		
		self.image = images.scope
		self.rect = self.image.get_rect()
		self.rect[0] = x - RFODDER
		self.rect[1] = y
		
	def move(self):
		self.rect[1] += 3

class AS(pygame.sprite.Sprite):
	def __init__(self, size, x, y):
		pygame.sprite.Sprite.__init__(self)
		
		#player stats
		self.time =  10 * 60
		
		self.image = images.AS
		self.rect = self.image.get_rect()
		self.rect[0] = x - RFODDER
		self.rect[1] = y
		
	def move(self):
		self.rect[1] += 3


class fodder(pygame.sprite.Sprite):
	def __init__(self, size, x, y):
		pygame.sprite.Sprite.__init__(self)
		
		#player stats
		self.HP = 10
		self.points = 10
		
		self.image = images.fodder
		self.rect = self.image.get_rect()
		self.rect[0] = x - RFODDER
		self.rect[1] = y
		
	def move(self):
		self.rect[1] += 2
	

class sine(pygame.sprite.Sprite):
	def __init__(self, size, x, y):
		pygame.sprite.Sprite.__init__(self)
		
		#player stats
		self.HP = 10
		self.points = 25
		self.originx = x
		
		self.image = images.sine
		self.rect = self.image.get_rect()
		self.rect[0] = x - RSINE
		self.rect[1] = y
		
	def move(self):
		self.rect[1] += 2
		self.rect[0] = self.originx + math.sin((1.0/128.0) * math.pi * self.rect[1]) * SINEAMP
	
class grunt(pygame.sprite.Sprite):
	def __init__(self, size, x, y):
		pygame.sprite.Sprite.__init__(self)
		
		#player stats
		self.HP = 15
		self.points = 50
		self.DMG = 5
		self.facing = (1.0/2.0)*math.pi
		
		self.gunCD = 100
		self.gunTime = 0
		
		
		self.image = images.grunt
		self.rect = self.image.get_rect()
		self.rect[0] = x - RGRUNT
		self.rect[1] = y
		
	def move(self):
		self.rect[1] += 1


class sentry(pygame.sprite.Sprite):
	def __init__(self, size, x, y):
		pygame.sprite.Sprite.__init__(self)
		
		#player stats
		self.HP = 15
		self.points = 50
		self.DMG = 2
		self.facing = (1.0/2.0)*math.pi
		
		self.gunCD = 25
		self.gunTime = 0
		
		
		self.image = images.sentry
		self.rect = self.image.get_rect()
		self.rect[0] = x - RGRUNT
		self.rect[1] = y
		
	def move(self):
		self.rect[1] += 1
	
	def detFacing(self, target):
		x0 = self.rect[0] + RSENTRY
		y0 = self.rect[1] + RSENTRY
		x1 = target.rect[0] + PSIZE
		y1 = target.rect[1] + PSIZE
		
		dx = x1 - x0
		dy = y1 - y0
		
		if abs(dy) < 150:
			self.facing = 0.5*math.pi
		else:
			length = math.sqrt(pow(dx, 2) + pow(dy, 2))
			
			spray = random.uniform(-0.05, 0.05)
			yrot = dy / length
			sign = 1.0
			if dx > 0: sign = -1.0
			self.facing = 0.5*math.pi + sign * (math.acos(yrot) + spray)
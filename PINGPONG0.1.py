
import pygame
import random
import os

WIDTH = 960
HEIGHT = 400
FPS = 60

Filedir = os.path.dirname(__file__)
Imgdir = os.path.join(Filedir , 'SoccerBall1.png')

#colours
Black = (0, 0, 0)
White = (255, 255, 255)
Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0, 0 ,255)
Cyan = (0, 255, 255)
Magenta = (255, 0, 255)
Yellow = (255, 255, 0)

# Megdar Dehi avaliye 
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PING PONG")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size , x, y):
	font = pygame.font.Font(font_name, size)
	text_surface = font.render(text, True, White)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surf.blit(text_surface, text_rect)

class PlayerLeft(pygame.sprite.Sprite):

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((10,80))
		self.image.fill(Green)
		self.rect = self.image.get_rect()
		self.rect.centerx = 30
		self.rect.centery = HEIGHT/2
		self.speedy = 0

	def update(self):
		keystate = pygame.key.get_pressed()
		
		if not(keystate[pygame.K_w] or keystate[pygame.K_s]):
			if abs(self.speedy) <= 0.5 :
				self.speedy = 0
			elif self.speedy > 0 :
				self.speedy -= 0.5
			elif self.speedy < 0 :
				self.speedy += 0.5


		if keystate[pygame.K_w]:
			self.speedy -= 0.5
		if keystate[pygame.K_s]:
			self.speedy += 0.5

		self.rect.y += self.speedy
		if self.rect.top < 0 :
			self.rect.top = 0
			self.speedy = 0
		elif self.rect.bottom > HEIGHT:
			self.rect.bottom = HEIGHT
			self.speedy = 0

class PlayerRight(pygame.sprite.Sprite):

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((10,80))
		self.image.fill(Blue)
		self.rect = self.image.get_rect()
		self.rect.centerx = WIDTH - 30
		self.rect.centery = HEIGHT/2
		self.speedy = 0

	def update(self):
		keystate = pygame.key.get_pressed()
		
		if not(keystate[pygame.K_UP] or keystate[pygame.K_DOWN]):
			if abs(self.speedy) <= 0.5 :
				self.speedy = 0
			elif self.speedy > 0 :
				self.speedy -= 0.5
			elif self.speedy < 0 :
				self.speedy += 0.5


		if keystate[pygame.K_UP]:
			self.speedy -= 0.5
		if keystate[pygame.K_DOWN]:
			self.speedy += 0.5

		self.rect.y += self.speedy
		if self.rect.top < 0 :
			self.rect.top = 0
			self.speedy = 0
		elif self.rect.bottom > HEIGHT:
			self.rect.bottom = HEIGHT
			self.speedy = 0

class Ball(pygame.sprite.Sprite):

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(Imgdir).convert()
		self.rect = self.image.get_rect()
		self.speedy = random.randrange(2, 10)
		self.speedx = random.randrange(2, 10)
		self.rect.centerx = WIDTH / 2
		self.rect.centery = HEIGHT / 2 
		self.scoreplayerright = 0
		self.scoreplayerleft = 0

	def update(self):
		self.rect.x += self.speedx
		self.rect.y += self.speedy

		if self.rect.top < 0 :
			self.rect.top = 0
			self.speedy *= -1
		if self.rect.bottom > HEIGHT :
			self.rect.bottom = HEIGHT
			self.speedy *= -1

		if self.rect.left > WIDTH :
			self.scoreplayerleft += 1
			self.speedy = random.randrange(2, 10)
			self.speedx = random.randrange(2, 10)
			self.rect.centerx = WIDTH / 2
			self.rect.centery = HEIGHT / 2 

		if self.rect.right < 0 :
			self.scoreplayerright += 1
			self.speedy = random.randrange(2, 10)
			self.speedx = random.randrange(2, 10)
			self.rect.centerx = WIDTH / 2
			self.rect.centery = HEIGHT / 2 

all_sprits = pygame.sprite.Group()
playerLeft = PlayerLeft()
playerRight = PlayerRight()
ball = Ball()
balls = pygame.sprite.Group()
balls.add(ball)
all_sprits.add(playerRight, playerLeft, ball)

# charge bazi
running = True
collide = True
while running :
	# in right time
	clock.tick(FPS)
	#process
	for event in pygame.event.get():
		# close
		if event.type == pygame.QUIT:
			running = False
	if abs(ball.scoreplayerleft - ball.scoreplayerright) >= 10:
		running = False		
	#update
	all_sprits.update()

	hitplayerLeft = pygame.sprite.spritecollide(playerLeft, balls, False)
	if hitplayerLeft and not(ball.rect.right < playerLeft.rect.centerx) and collide :
		ball.speedx *= -1
		ball.rect.left = playerLeft.rect.right + 1 
		collide = False
	else :
		collide = True

	hitplayerRight = pygame.sprite.spritecollide(playerRight, balls, False)
	if hitplayerRight and not(ball.rect.left > playerRight.rect.centerx) and collide:
		ball.speedx *= -1
		ball.rect.right = playerRight.rect.left - 1
		collide = False
	else :
		collide = True

	#Draw
	screen.fill(Black)
	all_sprits.draw(screen)
	draw_text(screen, str(ball.scoreplayerleft), 40 , WIDTH/4 ,20)
	draw_text(screen, str(ball.scoreplayerright), 40 , 3*WIDTH/4 ,20)
	#show
	pygame.display.flip()

while True :
	for event in pygame.event.get():
		# close
		if event.type == pygame.QUIT:
			pygame.quit()
			break

	draw_text(screen, 'Game Ended', 130 , WIDTH/2 , 78	)
	#show
	pygame.display.flip()	

pygame.quit()

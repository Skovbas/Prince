import pygame, sys
from settings import * 
from level import Level
from game_data import level_0

# Pygame setup 
pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Prince of Persia")
clock = pygame.time.Clock()
level = Level(level_0,screen)

while True:
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	screen.fill('black')
	level.run()
 
	pygame.display.update()
	clock.tick(60)
import pygame, sys
from settings import * 
from level import Level
from game_data import level_0
from menu import Button

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Game Menu")

background_image = pygame.image.load("./graphics/menu/back.png").convert()
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
pygame.display.set_caption("Prince of Persia")

clock = pygame.time.Clock()
level = Level(level_0,screen)

# Create a button
levels_button = Button("Levels", "./graphics/fonts/GARMNDB.ttf", 50, screen_width // 2 - 55, screen_height // 2)
play_button = Button("Play", "./graphics/fonts/GARMNDB.ttf", 50, screen_width // 2 - 40, screen_height // 2 + 100)
exit_button = Button("Exit", "./graphics/fonts/GARMNDB.ttf", 50, screen_width // 2 - 40, screen_height // 2 + 200)

def game():
	while True:
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit()
			elif event.type == pygame.QUIT:
				pygame.quit() 
				sys.exit()

		screen.fill('black')
		level.run()

		clock.tick(60)
		
		pygame.display.update()


# Game menu function
def game_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Update buttons
        levels_button.update()
        play_button.update()
        exit_button.update()

        if pygame.mouse.get_pressed()[0]:
            if levels_button.is_hovered:
                # Handle levels button click
                print("Levels button clicked!")
                # Replace the print statement with your levels logic

            elif play_button.is_hovered:
                # Handle play button click
                game()
                # Replace the print statement with your play logic

            elif exit_button.is_hovered:
                # Exit the menu
                pygame.quit()
                sys.exit()
                
        screen.blit(background_image, (0, 0))
        levels_button.render(screen)
        play_button.render(screen)
        exit_button.render(screen)
    
        # Render the button
        levels_button.render(screen)
        play_button.render(screen)
        exit_button.render(screen)

        pygame.display.update()

# Run the game menu
game_menu()

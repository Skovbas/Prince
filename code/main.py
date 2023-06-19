import pygame, sys, time
from settings import * 
from level import Level
from game_data import level_0
from button import Button

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((screen_width, screen_height))

background_image = pygame.image.load("./graphics/menu/back.png").convert()
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

clock = pygame.time.Clock()

# Sound
intro_sound = pygame.mixer.Sound('./sound/theme.mp3')
play_sound = pygame.mixer.Sound('./sound/embrace.wav')

# Create a button
levels_button = Button("Levels", "./graphics/fonts/GARMNDB.ttf", 50, screen_width // 2 - 55, screen_height // 2)
play_button = Button("Play", "./graphics/fonts/GARMNDB.ttf", 50, screen_width // 2 - 40, screen_height // 2 + 100)
exit_button = Button("Exit", "./graphics/fonts/GARMNDB.ttf", 50, screen_width // 2 - 40, screen_height // 2 + 200)

def game(level1):
    pygame.display.set_caption("Prince of Persia")
    intro_sound.stop()
    play_sound.play()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    play_sound.stop()
                    game_menu()
            elif event.type == pygame.QUIT:
                pygame.quit() 
                sys.exit()

        screen.fill('black')
        level1.run()
        level1.menu_call(game_menu)
        level1.finish(game_menu)

        clock.tick(60)
        
        pygame.display.update()

# Game menu function
def game_menu():
    pygame.display.set_caption("Game menu")
    level = Level(level_0,screen)
    intro_sound.play()
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
                print("Levels button clicked!")
            elif play_button.is_hovered:
                game(level)
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

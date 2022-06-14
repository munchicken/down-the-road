# Down the Road game
# by Sarah Pierce

#imports
import pygame

#initialize game engine
pygame.init()

#constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = 'Down the Road'
WHITE_COLOR = (255,255,255)
BLACK_COLOR = (0,0,0)
TICK_RATE = 60  #FPS

#initialize display
game_screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
game_screen.fill(WHITE_COLOR)
clock = pygame.time.Clock()
pygame.display.set_caption(SCREEN_TITLE)

#load resources
player_image = pygame.image.load('player.png')
player_image = pygame.transform.scale(player_image, (50,50))

#initialize game variables
is_game_over = False

#game loop
while not is_game_over:
    #event loop
    for event in pygame.event.get():
        #check for quit event
        if event.type == pygame.QUIT:
            is_game_over = True
        print(event)
        
    #draw some stuff
    #pygame.draw.rect(game_screen,BLACK_COLOR,[350,350,100,100])
    #pygame.draw.circle(game_screen,BLACK_COLOR,(400,300),50)
    game_screen.blit(player_image, (375,375))

    pygame.display.update()
    clock.tick(TICK_RATE)
#end game
pygame.quit()
quit()

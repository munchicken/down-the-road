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

#initialize display
clock = pygame.time.Clock()

#classes
class Game:

    #constants
    TICK_RATE = 60  #FPS

    #load resources
    player_image = pygame.image.load('player.png')
    player_image = pygame.transform.scale(player_image, (50,50))

    #initializer
    def __init__(self, title, width, height):
        self.title = title
        self.width = width
        self.height = height
        
        #initialize display
        self.game_screen = pygame.display.set_mode((width,height))
        self.game_screen.fill(WHITE_COLOR)
        pygame.display.set_caption(title)

    #game loop method
    def run_game_loop(self):
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
            self.game_screen.blit(self.player_image, (375,375))
            
            pygame.display.update()  #update display
            clock.tick(self.TICK_RATE)  #update clock

#create game
new_game = Game(SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)
new_game.run_game_loop()

#end game
pygame.quit()
quit()

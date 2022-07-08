# Down the Road game
# by Sarah Pierce

#imports
import pygame
import random
import spritesheet

#initialize game engine
pygame.init()

#constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = 'Down the Road'
WHITE = (255,255,255)
BLACK = (0,0,0)
MAX_ENEMIES = 6

#initialize display
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont('comicsans', 75)

#classes
#main game
class Game:

    #constants
    TICK_RATE = 60  #FPS

    #initializer
    def __init__(self, image_path, title, width, height, enemies):
        self.title = title
        self.width = width
        self.height = height
        self.max_enemies = enemies
        
        #initialize display
        self.game_screen = pygame.display.set_mode((width,height))
        pygame.display.set_caption(title)
        background_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(background_image, (width,height))

    #game loop method
    def run_game_loop(self, level):
        #initialize game variables
        is_game_over = False
        direction = 0  #stopped
        win = False

        #create game objects
        player = Player('Fox_walk.png', (self.width/2) - (100/2), self.height - 100, 100, 100,384,384,4,4,1)  # sending in spritesheet now
        treasure = GameObject('box.png', (self.width/2) - (100/2), 50, 100, 100,32,32,1,1,1)
        enemies = []  #empty list of enemies
        #find random lanes for enemies (out of 6 lanes)
        lane = random.sample(range(6),6)
        #create enemies
        for i in range(self.max_enemies):
            #figure out x - even lanes on right, odd on left
            if ((lane[i] +1) % 2) == 0:
                x = self.width - 20  # right
            else:
                x = 20  # left
            #figure out y - 6 random lanes
            y = lane[i] * 80 + 200  #80 between each for player clearance, start at 200, end at 600
            #create & place enemy, & add to enemy list
            enemies.append (Enemy('monster.png', x, y, 50, 50,32,32,1,1,1))

        #set enemy speed
        for enemy in enemies:
            #every 4 levels
            if level % 4 == 0:
                enemy.speed *= (2 / 4)  #reset enemy speed each time new ones spawn (based on class original speed)
            else:
                enemy.speed *= (level / 4)  #enemy speed increased by a quarter each level

        #game loop
        while not is_game_over:
            #event loop
            for event in pygame.event.get():
                #check for quit event
                if event.type == pygame.QUIT:
                    is_game_over = True
                #handle user controls
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        direction = 1  #up
                    elif event.key == pygame.K_DOWN:
                        direction = -1  #down
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        direction = 0  #stop

            #create background (also clears screen)
            self.game_screen.blit(self.image, (0,0))
            
            #update player
            player.move(direction, self.height)
            player.draw(self.game_screen)

            #update enemies
            enemies[0].move(self.width)
            enemies[0].draw(self.game_screen)
            if level > 3:
                enemies[1].move(self.width)
                enemies[1].draw(self.game_screen)
            if level > 7:
                enemies[2].move(self.width)
                enemies[2].draw(self.game_screen)
            if level > 11:
                enemies[3].move(self.width)
                enemies[3].draw(self.game_screen)
            if level > 15:
                enemies[4].move(self.width)
                enemies[4].draw(self.game_screen)
            if level > 19:
                enemies[5].move(self.width)
                enemies[5].draw(self.game_screen)

            #update treasure
            treasure.draw(self.game_screen)

            #check for collisions
            #with treasure = win
            if player.detect_collision(treasure):
                is_game_over = True
                win = True
                text = font.render('You win! :)', True, BLACK)
                self.game_screen.blit(text, (300,350))
                pygame.display.update()
                clock.tick(1)
            #with enemy = lose
            else:
                for enemy in enemies:
                    if player.detect_collision(enemy):
                        is_game_over = True
                        text = font.render('You lose! :(', True, BLACK)
                        self.game_screen.blit(text, (300,350))
                        pygame.display.update()
                        clock.tick(1)

            #restart if won / quit if lose
            if is_game_over:
                if win:
                    self.run_game_loop(level + 1)  #increase level
                else:
                    return
            
            pygame.display.update()  #update display
            clock.tick(self.TICK_RATE)  #update clock

#objects in game (image, position, & size)
class GameObject:
    def __init__(self, image_path, x, y, width, height, sheet_width, sheet_height, rows, cols, frame):
        self.sheet_image = pygame.image.load(image_path).convert_alpha()  # load the spritesheet
        self.sheet = spritesheet.Spritesheet(self.sheet_image, sheet_width,sheet_height,rows,cols)  # instantiate spritesheet object (w/h,rows/cols)
        self.object_image = self.sheet.get_frame(0,0,frame,BLACK)  # grab desired frame
        self.image = pygame.transform.scale(self.object_image, (width, height)).convert_alpha()

        self.x_pos = x
        self.y_pos = y

        self.width = width
        self.height = height

    def draw(self, background):
        background.blit(self.image, (self.x_pos, self.y_pos))

#player object
class Player(GameObject):

    SPEED = 10  #tiles per sec

    def __init__(self, image_path, x, y, width, height, sheet_width, sheet_height, rows, cols, frame):
        super().__init__(image_path, x, y, width, height, sheet_width, sheet_height, rows, cols, frame)
    
    #move method (direction & height of game)
    def move(self, direction, max_height):
        if direction > 0:
            self.y_pos -= self.SPEED
        elif direction < 0:
            self.y_pos += self.SPEED
        #bounds checking (bottom only)
        if self.y_pos >= max_height - self.height:
            self.y_pos = max_height - self.height  #keeps character at game height - character height
    
    #character collision detection        
    def detect_collision(self, other_object):
        #check Y - if completely above or below other object
        if self.y_pos > other_object.y_pos + other_object.height:
            return False
        elif self.y_pos + self.height < other_object.y_pos:
            return False
        #check x - if completely to the right or left of other object
        if self.x_pos > other_object.x_pos + other_object.width:
            return False
        elif self.x_pos + self.width < other_object.x_pos:
            return False
        #colliding
        return True

#enemy object
class Enemy(GameObject):

    speed = 2  #tiles per sec

    def __init__(self, image_path, x, y, width, height, sheet_width, sheet_height, rows, cols, frame):
        super().__init__(image_path, x, y, width, height, sheet_width, sheet_height, rows, cols, frame)

    #moves enemy back and forth across screen
    def move(self, max_width):
        #at left edge - change dir to right - 20 for padding
        if self.x_pos <= 20:
            self.speed = abs(self.speed)
        #at right edge - change dir to left - 20 for padding
        elif self.x_pos >= max_width - (20 + self.width):
            self.speed = -abs(self.speed)
        #move
        self.x_pos += self.speed

#create game
new_game = Game('level1.png', SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT, MAX_ENEMIES)

new_game.run_game_loop(1)  #start at level 1

#end game
pygame.quit()
quit()

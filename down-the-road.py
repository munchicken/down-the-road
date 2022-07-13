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
        self.win = False
        
        #initialize display
        self.game_screen = pygame.display.set_mode((width,height))
        pygame.display.set_caption(title)
        background_image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(background_image, (width,height))

    #game loop method
    def run_game_loop(self, level):
        #initialize game variables
        is_game_over = False
        direction = 0  #stopped
        self.win = False

        #create game objects
        player = Player('Fox_walk.png', (self.width/2), self.height, 2,384,384,4,4,3,1)  # sending in spritesheet now
        treasure = Treasure('Box_breaking.png', (self.width/2), 50, 2,480,96,1,5,0,0)
        enemies = []  #empty list of enemies
        #find random lanes for enemies (out of 6 lanes)
        lane = random.sample(range(6),6)
        #create enemies
        for i in range(self.max_enemies):
            #figure out x - even lanes on right, odd on left
            if ((lane[i] +1) % 2) == 0:
                x = self.width - 50  # right
            else:
                x = 50  # left
            #figure out y - 6 random lanes
            y = lane[i] * 80 + 200  #80 between each for player clearance, start at 200, end at 600
            #create & place enemy, & add to enemy list
            enemies.append (Enemy('monster.png', x, y, 2,32,32,1,1,0,0))

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

            

            #check for collisions
            #with treasure = win
            if player.detect_collision(treasure):
                is_game_over = True
                self.win = True
                text = font.render('You win! :)', True, BLACK)
                self.game_screen.blit(text, (300,350))
                #update treasure
                treasure.draw(self.game_screen)
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

            #update treasure
            treasure.draw(self.game_screen)
                        
            #restart if won / quit if lose
            if is_game_over:
                if self.win:
                    self.run_game_loop(level + 1)  #increase level
                else:
                    return
            
            pygame.display.update()  #update display
            clock.tick(self.TICK_RATE)  #update clock

#objects in game (image, position, & size)
class GameObject:
    def __init__(self, image_path, x, y, scale, sheet_width, sheet_height, rows, cols, frame_row, frame_col):
        self.sheet_image = pygame.image.load(image_path).convert_alpha()  # load the spritesheet
        self.sheet = spritesheet.Spritesheet(self.sheet_image, sheet_width,sheet_height,rows,cols)  # instantiate spritesheet object (w/h,rows/cols)
        self.object_image = self.sheet.get_frame(frame_row,frame_col,scale,BLACK)  # grab desired frame
        self.rect = self.object_image.get_bounding_rect()  # find image size without extra padding
        self.crop = self.object_image.subsurface(self.rect) # crop image to remove extra padding


        self.width = self.crop.get_size()[0]  # set size to cropped size
        self.height = self.crop.get_size()[1]

        self.x_pos =  x - (self.width/2)  # put in middle
        self.y_pos = y

    def draw(self, background):
        background.blit(self.crop, (self.x_pos, self.y_pos))

#player object
class Player(GameObject):

    SPEED = 10  #tiles per sec

    def __init__(self, image_path, x, y, scale, sheet_width, sheet_height, rows, cols, frame_row, frame_col):
        super().__init__(image_path, x, y, scale, sheet_width, sheet_height, rows, cols, frame_row, frame_col)
        self.y_pos = y - self.height  # up from bottom so complete character shows
        self.frames = self.sheet.get_frames(scale,BLACK)
        self.rect = self.frames[12].get_bounding_rect()  # find image size without extra padding
        self.up = self.frames[12].subsurface(self.rect) # crop image to remove extra padding
        self.rect = self.frames[0].get_bounding_rect()  # find image size without extra padding
        self.down = self.frames[0].subsurface(self.rect) # crop image to remove extra padding
        self.dir = 1  # start looking up
    
    #move method (direction & height of game)
    def move(self, direction, max_height):
        if direction > 0:
            self.y_pos -= self.SPEED
            self.dir = 1  # up
        elif direction < 0:
            self.y_pos += self.SPEED
            self.dir = -1  # down
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

    def draw(self, background):
        if self.dir > 0:
            background.blit(self.up, (self.x_pos, self.y_pos))
        elif self.dir < 0:
            background.blit(self.down, (self.x_pos, self.y_pos))

#enemy object
class Enemy(GameObject):

    speed = 2  #tiles per sec

    def __init__(self, image_path, x, y, scale, sheet_width, sheet_height, rows, cols, frame_row, frame_col):
        super().__init__(image_path, x, y, scale, sheet_width, sheet_height, rows, cols, frame_row, frame_col)

    #moves enemy back and forth across screen
    def move(self, max_width):
        #at left edge - change dir to right - 20 for padding
        if self.x_pos <= 50:
            self.speed = abs(self.speed)
        #at right edge - change dir to left - 20 for padding
        elif self.x_pos >= max_width - (50 + self.width):
            self.speed = -abs(self.speed)
        #move
        self.x_pos += self.speed

#treasure object
class Treasure(GameObject):

    def __init__(self, image_path, x, y, scale, sheet_width, sheet_height, rows, cols, frame_row, frame_col):
        super().__init__(image_path, x, y, scale, sheet_width, sheet_height, rows, cols, frame_row, frame_col)
        self.frames = self.sheet.get_frames(scale,BLACK)
        self.rect = self.frames[0].get_bounding_rect()  # find image size without extra padding
        self.whole = self.frames[0].subsurface(self.rect) # crop image to remove extra padding
        self.rect = self.frames[4].get_bounding_rect()  # find image size without extra padding
        self.broken = self.frames[4].subsurface(self.rect) # crop image to remove extra padding

    def draw(self, background):
        if new_game.win:
            background.blit(self.broken, (self.x_pos, self.y_pos))
        else:
            background.blit(self.whole, (self.x_pos, self.y_pos))

#create game
new_game = Game('level1.png', SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT, MAX_ENEMIES)

new_game.run_game_loop(1)  #start at level 1

#end game
pygame.quit()
quit()

# Down the Road game
# by Sarah Pierce

#imports
from posixpath import supports_unicode_filenames
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
        self.is_game_over = False
        direction = 0  #stopped
        self.win = False

        #create game objects
        player = Player(['Fox_idle.png','Fox_walk.png'], (self.width/2), self.height, 2,384,384,4,4)  # sending in spritesheet now
        treasure = Treasure(['Box_breaking.png'], (self.width/2), 50, 2,480,96,1,5)
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
            enemies.append (Enemy(['Skeleton 01_walk.png','Skeleton 02_walk.png','Skeleton 03_walk.png'], x, y, 2,128,128,4,4))

        #set enemy speed
        for enemy in enemies:
            #every 4 levels
            if level % 4 == 0:
                enemy.speed *= (2 / 4)  #reset enemy speed each time new ones spawn (based on class original speed)
            else:
                enemy.speed *= (level / 4)  #enemy speed increased by a quarter each level

        #game loop
        while not self.is_game_over:
            #event loop
            for event in pygame.event.get():
                #check for quit event
                if event.type == pygame.QUIT:
                    self.is_game_over = True
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
                
                if treasure.current_frame == treasure.range[1]:
                    self.is_game_over = True
                
                self.win = True
                text = font.render('You win! :)', True, BLACK)
                self.game_screen.blit(text, (300,350))
                #update treasure
                treasure.draw(self.game_screen)
                pygame.display.update()
                clock.tick(15)  # slow to 15 FPS for end screen
            #with enemy = lose
            else:
                for enemy in enemies:
                    if player.detect_collision(enemy):
                        self.is_game_over = True
                        text = font.render('You lose! :(', True, BLACK)
                        self.game_screen.blit(text, (300,350))
                        pygame.display.update()
                        clock.tick(1)

            #update treasure
            treasure.draw(self.game_screen)
                        
            #restart if won / quit if lose
            if self.is_game_over:
                if self.win:
                    self.run_game_loop(level + 1)  #increase level
                else:
                    return
            
            pygame.display.update()  #update display
            clock.tick(self.TICK_RATE)  #update clock

#objects in game (image, position, & size)
class GameObject:
    def __init__(self, image_paths, x, y, scale, sheet_width, sheet_height, rows, cols):
        # load each image into image list
        sheet_images = []
        for image_path in image_paths:
            sheet_images.append(pygame.image.load(image_path).convert_alpha())  # load the spritesheets

        # create spritesheet for each image in spritesheet list
        sheets = []
        for sheet_image in sheet_images:
            sheets.append(spritesheet.Spritesheet(sheet_image, sheet_width,sheet_height,rows,cols,True))  # instantiate spritesheet object (w/h,rows/cols with cropping)
        
        # get all the frames from each sheet and put into a list of frames lists
        self.frames = []
        for sheet in sheets:
            self.frames.append(sheet.get_frames(scale,BLACK))
        
        self.x_pos =  x
        self.y_pos = y

        # animation stuff
        self.last_update = pygame.time.get_ticks()  # get time
        self.cooldown = 200  # millisec before next animation update

#player object
class Player(GameObject):

    SPEED = 5  #tiles per sec

    def __init__(self, image_paths, x, y, scale, sheet_width, sheet_height, rows, cols):
        super().__init__(image_paths, x, y, scale, sheet_width, sheet_height, rows, cols)

        #track movement
        self.moving = False  # start not moving
        
        #sheet names (indexs in sheet list)
        self.idle = 0
        self.walk = 1

        #animations
        self.down = (0,3)  # frame range for all down animations
        self.up = (12,15)  # frame range for all up animations
        self.current_down_frame = self.down[0]  # current displayed frame from down, starting at bottom
        self.current_up_frame = self.up[0]  # current displayed frame from up, starting at bottom

        self.dir = 1  # start looking up
        # just use one image for the sizing
        self.width = self.frames[self.idle][0].get_size()[0]
        self.height = self.frames[self.idle][0].get_size()[1]
        #  player specific placement
        self.x_pos =  x - (self.width/2)  # put in middle
        self.y_pos = y - self.height  # up from bottom so complete character shows

        #shadow
        self.shadow = pygame.image.load("Shadow.png").convert_alpha()
        self.shadow = pygame.transform.scale2x(self.shadow)  # scales x2, might need to change later
        
    #move method (direction & height of game)
    def move(self, direction, max_height):
        if direction > 0:
            self.y_pos -= self.SPEED
            self.dir = 1  # up
            self.moving = True
        elif direction < 0:
            self.y_pos += self.SPEED
            self.dir = -1  # down
            self.moving = True
        else:
            self.moving = False # no longer moving
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
        current_time = pygame.time.get_ticks()  # check the time for animations
        # going up
        if self.dir > 0:
            # update animation frame after cooldown
            if current_time - self.last_update >= self.cooldown:
                self.current_up_frame += 1  # increment to next frame
                self.last_update = current_time  # reset cooldown
                # reset range if past end
                if self.current_up_frame > self.up[1]:
                    self.current_up_frame = self.up[0]  # reset back to range start

            if self.moving:
                background.blit(self.frames[self.walk][self.current_up_frame], (self.x_pos, self.y_pos))
            else:
                background.blit(self.frames[self.idle][self.current_up_frame], (self.x_pos, self.y_pos))
        # going down
        elif self.dir < 0:
            # update animation frame after cooldown
            if current_time - self.last_update >= self.cooldown:
                self.current_down_frame += 1  # increment to next frame
                self.last_update = current_time  # reset cooldown
                # reset range if past end
                if self.current_down_frame > self.down[1]:
                    self.current_down_frame = self.down[0]  # reset back to range start

            if self.moving:
                background.blit(self.frames[self.walk][self.current_down_frame], (self.x_pos, self.y_pos))
            else:
                background.blit(self.frames[self.idle][self.current_down_frame], (self.x_pos, self.y_pos))
        
        # display shadow below fox
        background.blit(self.shadow, (self.x_pos + 4, self.y_pos + self.height - 15))

#enemy object
class Enemy(GameObject):

    speed = 2  #tiles per sec

    def __init__(self, image_paths, x, y, scale, sheet_width, sheet_height, rows, cols):
        super().__init__(image_paths, x, y, scale, sheet_width, sheet_height, rows, cols)

        self.type = random.randint(0,2)  # white, brown, red
        
        #animations
        self.walk = (0,3)  # frame range for sideways walking animations
        self.current_frame = self.walk[0]  # current displayed frame, starting at bottom

        self.width = self.frames[0][0].get_size()[0]
        self.height = self.frames[0][0].get_size()[1]

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

    def draw(self, background):
        current_time = pygame.time.get_ticks()  # check the time for animations

        # update animation frame after cooldown
        if current_time - self.last_update >= self.cooldown:
            self.current_frame += 1  # increment to next frame
            self.last_update = current_time  # reset cooldown
            # reset range if past end
            if self.current_frame > self.walk[1]:
                self.current_frame = self.walk[0]  # reset back to range start

        background.blit(self.frames[self.type][self.current_frame], (self.x_pos, self.y_pos))

#treasure object
class Treasure(GameObject):

    def __init__(self, image_paths, x, y, scale, sheet_width, sheet_height, rows, cols):
        super().__init__(image_paths, x, y, scale, sheet_width, sheet_height, rows, cols)

        # load each image into image list
        sheet_images = []
        for image_path in image_paths:
            sheet_images.append(pygame.image.load(image_path).convert_alpha())  # load the spritesheets
        
        # create spritesheet for each image in spritesheet list
        sheets = []
        for sheet_image in sheet_images:
            sheets.append(spritesheet.Spritesheet(sheet_image,sheet_width,sheet_height,rows,cols,False))  # instantiate spritesheet object (w/h,rows/cols with cropping)

        # get all the frames from each sheet and put into a list of frames lists
        self.frames = []
        for sheet in sheets:
            self.frames.append(sheet.get_frames(scale,BLACK))

        self.whole = self.frames[0][0]
        self.broken = self.frames[0][4]

        #animations
        self.range = (0,4)  # frame range for box breaking animation
        self.current_frame = self.range[0]  # current displayed frame, starting at bottom

        # crop image
        rect = self.whole.get_bounding_rect()
        self.whole = self.whole.subsurface(rect)
        rect = self.broken.get_bounding_rect()
        self.broken = self.broken.subsurface(rect)
        
        for i in range(1,5):
            self.frames[0][i] = self.frames[0][i].subsurface(rect)

        # set size to the whole one for collisions and placement
        self.width = self.whole.get_size()[0]
        self.height = self.whole.get_size()[1]

        # for placement of broken
        self.broken_width = self.broken.get_size()[0]

        self.x_pos =  x

    def draw(self, background):

        current_time = pygame.time.get_ticks()  # check the time for animations

        if new_game.win:

            # update animation frame after cooldown
            if current_time - self.last_update >= self.cooldown:
                self.current_frame += 1  # increment to next frame
                self.last_update = current_time  # reset cooldown
                # reset range if past end
                if self.current_frame > self.range[1]:
                    self.current_frame = self.range[1]

            background.blit(self.frames[0][self.current_frame], (self.x_pos - (self.broken_width/2), self.y_pos))
        else:
            background.blit(self.whole, (self.x_pos - (self.width/2), self.y_pos))

#create game
new_game = Game('level1.png', SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT, MAX_ENEMIES)

new_game.run_game_loop(1)  #start at level 1

#end game
pygame.quit()
quit()

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
pygame.font.init()
font = pygame.font.SysFont('comicsans', 75)

#classes
class Game:

    #constants
    TICK_RATE = 60  #FPS

    #initializer
    def __init__(self, image_path, title, width, height):
        self.title = title
        self.width = width
        self.height = height
        
        #initialize display
        self.game_screen = pygame.display.set_mode((width,height))
        self.game_screen.fill(WHITE_COLOR)
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
        player = Player('player.png', 375, 700, 50, 50)
        enemy0 = Enemy('monster.png', 20, 200, 50, 50)
        enemy1 = Enemy('monster.png', self.width - 20, 400, 50, 50)
        enemy2 = Enemy('monster.png', 20, 600, 50, 50)
        treasure = GameObject('box.png', 375, 50, 50, 50)
        enemies = [enemy0, enemy1, enemy2]  #list of enemies

        #set enemy speed
        for enemy in enemies:
            if level == 4 or level == 6:
                enemy.speed *= (1 / 4)  #reset enemy speed each time new ones spawn
            else:
                enemy.speed *= (level / 4)  #enemy speed increased by a quarter each level

        #game loop
        while not is_game_over:
            #event loop
            for event in pygame.event.get():
                #check for quit event
                if event.type == pygame.QUIT:
                    is_game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        direction = 1  #up
                    elif event.key == pygame.K_DOWN:
                        direction = -1  #down
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        direction = 0  #stop

            #screen clear
            self.game_screen.fill(WHITE_COLOR)

            #create background
            self.game_screen.blit(self.image, (0,0))
            
            #update player
            player.move(direction, self.height)
            player.draw(self.game_screen)

            #update enemy
            enemy0.move(self.width)
            enemy0.draw(self.game_screen)
            if level > 3:
                enemy1.move(self.width)
                enemy1.draw(self.game_screen)
            if level > 5:
                enemy2.move(self.width)
                enemy2.draw(self.game_screen)
            

            #update treasure
            treasure.draw(self.game_screen)

            #check for collisions
            #with treasure = win
            #with enemy = lose
            if player.detect_collision(treasure):
                is_game_over = True
                win = True
                text = font.render('You win! :)', True, BLACK_COLOR)
                self.game_screen.blit(text, (300,350))
                pygame.display.update()
                clock.tick(1)
            else:
                for enemy in enemies:
                    if player.detect_collision(enemy):
                        is_game_over = True
                        text = font.render('You lose! :(', True, BLACK_COLOR)
                        self.game_screen.blit(text, (300,350))
                        pygame.display.update()
                        clock.tick(1)

            #restart if won / quit if lose
            if is_game_over:
                if win:
                    self.run_game_loop(level + 1)
                else:
                    return
            
            pygame.display.update()  #update display
            clock.tick(self.TICK_RATE)  #update clock

class GameObject:
    def __init__(self, image_path, x, y, width, height):
        object_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(object_image, (width, height))

        self.x_pos = x
        self.y_pos = y

        self.width = width
        self.height = height

    def draw(self, background):
        background.blit(self.image, (self.x_pos, self.y_pos))

class Player(GameObject):

    SPEED = 10  #tiles per sec

    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)

    def move(self, direction, max_height):
        if direction > 0:
            self.y_pos -= self.SPEED
        elif direction < 0:
            self.y_pos += self.SPEED
        #bounds checking
        if self.y_pos >= max_height - self.height:
            self.y_pos = max_height - self.height
    def detect_collision(self, other_object):
        #check Y
        if self.y_pos > other_object.y_pos + other_object.height:
            return False
        elif self.y_pos + self.height < other_object.y_pos:
            return False
        #check x
        if self.x_pos > other_object.x_pos + other_object.width:
            return False
        elif self.x_pos + self.width < other_object.x_pos:
            return False
        #colliding
        return True

class Enemy(GameObject):

    speed = 10

    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)

    def move(self, max_width):
        if self.x_pos <= 20:
            self.speed = abs(self.speed)
        elif self.x_pos >= max_width - (20 + self.width):
            self.speed = -abs(self.speed)
        self.x_pos += self.speed

#create game
new_game = Game('level1.png', SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)

new_game.run_game_loop(1)  #start at level 1

#end game
pygame.quit()
quit()

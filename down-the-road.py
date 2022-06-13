# Down the Road game
# by Sarah Pierce

#variable practice
game_name = 'Down the Road'  #string
version = 1  #integer
player_speed = 2.5  #float
game_over = False  #boolean

print (type(game_name))
print (type(version))
print (type(player_speed))
print (type(game_over))

#input/output practice
user_name = input('Please enter your name ')

salutation = 'Hello ' + user_name + ', welcome to Down the Road game!'

print(salutation)

#operator practice
game_state = not game_over
player_position = 1 + player_speed
obstacle_position = 15 - 2
lives = 2 * 50
middle = 100 / 2
is_third_time = (2 % 3 == 0)
the_floor = 5 // 2
two_squared = 2 ** 2
version += 1
time = 60
time -= 1
player_speed *= 2
magic = 50
magic /= 2

print(game_state)
print(player_position)
print(obstacle_position)
print(lives)
print(middle)
print(is_third_time)
print(the_floor)
print(two_squared)
print(version)
print(time)
print(player_speed)
print(magic)

#collection practice
#tuples
screen_size = (640, 480)
width = screen_size[0]
height = screen_size[1]
added_screen_number = screen_size + (1,)

print(screen_size)
print(width)
print(height)
print(added_screen_number)

del added_screen_number

print(len(screen_size))
print(max(screen_size))
print(min(screen_size))
print(100 in screen_size)

#arrays
treasure_amount = [50, 100, 100, 25, 1, 100]
print('first treasure ' + str(treasure_amount[0]))
treasure_amount.append(0)
print(treasure_amount)
treasure_amount.remove(1)
print(treasure_amount)

#dictionaries
player_lives = {'player1': 100, 'player2': 50, 'player3':25}
print(player_lives)
print(player_lives['player1'])
print(player_lives.keys())
player_lives['player3'] = 30
print(player_lives['player3'])
del player_lives['player2']
print(player_lives)

#flow control
#if statement
if not game_over:
    player_lives['player1'] = 100
    player_lives['player2'] = 100
    player_lives['player3'] = 100
if player_speed > 50:
    player_speed = 50
elif player_speed < 1:
    player_speed = 1
else:
    player_speed += 1

#loops
#while
run_game = True
turns = 0
while run_game:
    turns += 1
    print(turns)
    if turns == 3:
        run_game = False

#for-in
for amount in treasure_amount:
    print(amount)

#functions
def print_treasure_amounts():
    for amount in treasure_amount:
        print(amount)
        return('done')

print(print_treasure_amounts())

#classes
class Weapon:
    damage = 50

    def __init__(self, name):
        self.name = name
    def take_damage(self, amount):
        self.damage -= amount

sword = Weapon('sword')
print(sword.name)
sword.name = 'baseball bat'
print(sword.name)
print(sword.damage)

#subclasses
class Gun(Weapon):
    ammo = 100

    def __init__(self, name):
        super().__init__(name)

ak47 = Gun('AK47')
print(ak47.name)
print(ak47.damage)
print(ak47.ammo)

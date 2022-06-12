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

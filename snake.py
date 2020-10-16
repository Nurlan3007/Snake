# CREATE index: 16.06.2020
# USER: Nurlan

############## ПЛАН ##############
# 1: Создать поля
# 2: Нарисовать змейку
# 3: Научить змейку ходить
# 4: Написать проверки на нахождение змейки в полях
# 5: Создавать яблоки в рандомных местах
# 6: Написать проверки на нахождение змейки в полях
# и т.д...
############################

# Библиотеки которые нам нажны
import pygame
import random as r
import sys

pygame.init()

# Start window
sizeWindow = [450,500]
nameGame = 'Snake Pygame'
window = pygame.display.set_mode(( sizeWindow[0],sizeWindow[1] ))
pygame.display.set_caption(nameGame)


#### Colors ####
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (108, 0, 0)
BLUE  = (52, 82, 235)
GREEN = (131, 212, 138)
FRAME = (52, 220, 235)
################

COUNT_BLOCKS = 20
SIZE_BLOCK = 20
margin = 1

# FUNCTIONS and CLASS
class SnakeBlocks:
	def __init__(self,x,y):
		self.x = x
		self.y = y
	def isInside(self):
		if 0 <= self.x < COUNT_BLOCKS and 0 <= self.y < COUNT_BLOCKS:
			return True
		else:
			return False
	def __eq__(self, other):
		return isinstance(other,SnakeBlocks) and other.x == self.x and other.y == self.y


def randomSpawn():
	x = r.randint(0,COUNT_BLOCKS - 1)
	y = r.randint(0,COUNT_BLOCKS - 1)
	random_spawn = SnakeBlocks(x,y)
	return random_spawn

def draw_blocks(color,column,row):
	pygame.draw.rect(
		window,
		color,
		[
			10 + column * COUNT_BLOCKS + margin * (column + 1),  # postion X
			20 + row * COUNT_BLOCKS + margin * (row + 1),  # positon Y
			SIZE_BLOCK,
			SIZE_BLOCK,
		]
	)
def write(text,color,x,y,size):
	font = pygame.font.SysFont('serif',size)
	text = font.render(text,1,color)
	window.blit(text,(x,y))

###############################################

speed = 300
total = 0

apple = randomSpawn()
snake_blocks = [
	SnakeBlocks(9,9),
	SnakeBlocks(10,9),
	SnakeBlocks(11, 9),
]

d_row = 0
d_column = 1

run = True
while run:
	pygame.time.delay(speed)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT and d_row != 0:
				d_row = 0
				d_column = -1
			if event.key == pygame.K_RIGHT and d_row != 0:
				d_row = 0
				d_column = 1
			if event.key == pygame.K_UP and d_column != 0:
				d_row = -1
				d_column = 0
			if event.key == pygame.K_DOWN and d_column != 0:
				d_row = 1
				d_column = 0

	window.fill(WHITE)
	########### TEXT ############
	write("Total: " + str(total) + ", ",BLACK,20,460,30)
	write("Speed: " + str(speed),BLACK, 150, 460, 30)

	# Создание полей
	for column in range(COUNT_BLOCKS):
		for row in range(COUNT_BLOCKS):
			if (column + row) % 2 == 0:
				color = ((152, 222, 227))
			else:
				color = ((46, 204, 217))
			draw_blocks(color,column,row)

	head = snake_blocks[-1]

	# Есть ли змейка в поле
	if head.isInside() == False:
		print("\033[31m {}".format('CRASH'))
		sys.exit()

	# Рисуем яблоко
	draw_blocks(RED,apple.x,apple.y)
	if apple == head:
		total += 1
		snake_blocks.append(apple)
		apple = randomSpawn()
		draw_blocks(RED, apple.x, apple.y)

	if total % 5 == 0 and total != 0 and speed >= 130:
		speed -= 40


	for block in snake_blocks:
		x = block.x
		y = block.y
		draw_blocks(BLACK,x,y)

	new_head = SnakeBlocks(head.x + d_column,head.y + d_row)

	if new_head in snake_blocks:
		print("\033[31m {}".format('CRASH'))
		sys.exit()

	snake_blocks.append(new_head)
	snake_blocks.pop(0)


	pygame.display.update()

# Выход из pygame
pygame.quit()
























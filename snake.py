import pygame
from sys import exit
from random import randrange
import sqlite3


def connect_db():
    global db,cursor
    db = sqlite3.connect("server")
    cursor = db.cursor()

# Functions
def saveInDatabase(count):
    connect_db()
    cursor.execute('''CREATE TABLE IF NOT EXISTS score (
        id integer primary key AUTOINCREMENT,
        count varchar(150) DEFAULT 0
    )''')

    db.commit()

    cursor.execute("SELECT count FROM score")
    score = cursor.fetchall()
    if count > score[0][0]:
        cursor.execute("UPDATE score SET count = ?",[count])
        db.commit()

connect_db()    
highScore = cursor.execute("SELECT count FROM score")
highScore = cursor.fetchall()
highScore = highScore[0][0]

# Options
colors = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'red' : (255, 0, 0),
    'blue': (0, 0, 255),
    'green': (0, 200, 0),
}

MARGIN = 1
SIZE_BLOCK = 20
COUNT_BLOCKS = 20

WIDTH = SIZE_BLOCK * COUNT_BLOCKS
HEIGHT = WIDTH + 100

snakeX = 180
snakeY = 180 + 100
snake = [[snakeX,snakeY]]
dx,dy = 0,0

appleX,appleY = randrange(0,WIDTH,20),randrange(100,HEIGHT,20)

count,length = 0,2

pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Snake")

while True:
    pygame.time.delay(120)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            length -= 2
            saveInDatabase(length)
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and dx == 0:
                dx,dy = -20,0
            elif event.key == pygame.K_RIGHT and dx == 0:
                dx,dy = 20,0
            elif event.key == pygame.K_UP and dy == 0:
                dx,dy = 0,-20
            elif event.key == pygame.K_DOWN and dy == 0:
                dx,dy = 0,20

    pygame.draw.rect(screen, colors['white'], [0, 0, WIDTH, 100])    

    for row in range(COUNT_BLOCKS):
        for col in range(COUNT_BLOCKS):
            if (row + col) % 2 == 0:
                color = (175,171,255)
            else:
                color = (175,116,253)
            x = row * SIZE_BLOCK
            y = col * SIZE_BLOCK + 100
            pygame.draw.rect(screen, color, [x, y, SIZE_BLOCK, SIZE_BLOCK])

    snakeX += dx
    snakeY += dy
    snake.append([snakeX,snakeY])
    snake = snake[-length:]
    body = snake[:-2]
    head = snake[-1]

    if head[0] == appleX and head[1] == appleY:
        count += 1
        length += 1
        appleX,appleY = randrange(0,WIDTH,20),randrange(100,HEIGHT,20)

    if head[0] < 0:
        snakeX = WIDTH - 20 
    elif head[0] > WIDTH:
        snakeX = 0
    elif head[1] < 120:
        snakeY = HEIGHT
    elif head[1] > HEIGHT:
        snakeY = 100

    for i,j in body:
        if i == head[0] and j == head[1]:
            length -= 2
            saveInDatabase(length)
            pygame.quit()
            exit()

    for i,j in snake:
        pygame.draw.rect(screen, colors['green'], [i, j, SIZE_BLOCK, SIZE_BLOCK])
    pygame.draw.rect(screen, colors['red'], [appleX, appleY, SIZE_BLOCK, SIZE_BLOCK]) 
    
    font = pygame.font.SysFont('sans-serif',35)
    text1 = font.render("Score: " + str(count),True,colors['black'])
    text2 = font.render("High Score: " + str(highScore),True,colors['black'])
    screen.blit(text1,(20,20))
    screen.blit(text2,(20,60))       

    pygame.display.update()



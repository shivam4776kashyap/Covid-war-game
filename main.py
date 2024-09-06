import pygame
import random
import math
from pygame import mixer

# initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((700, 600))

# background image
background = pygame.image.load("lnea.png")

# Title and TOP Icon
pygame.display.set_caption("COVID W@R")
uppericon = pygame.image.load("virus.png")
pygame.display.set_icon(uppericon)

# player
playerimg = pygame.image.load("injection.png")
playerX = 300
playerY = 520
playerX_changes = 1
playerY_changes = 1

# ENEMY
enemyimg = []
enemyX = []
enemyY = []
enemyX_changes = []
enemyY_changes = []
num_of_enemies = 3

for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load("virus.png"))
    enemyX.append(random.randint(0, 636))
    enemyY.append(random.randint(10, 150))
    enemyX_changes.append(1)
    enemyY_changes.append(0)

# BUllet
# ready means you can't see the bullet on the screen
# fire means the bullet is currently moving

bulletimg = pygame.image.load("virusvaccine.png")
bulletX = 0
bulletY = 520
bulletX_changes = 0
bulletY_changes = 2
bullet_state = "ready"

# score board
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10
# background music
mixer.music.load('background.wav')
mixer.music.play(-1)

# game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (0, 0, 0))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (0, 0, 0))
    screen.blit(over_text, (150, 200))


def player(x, y):
    screen.blit(playerimg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 25, y + 10))


def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# game loop
running = True
while running:
    # SETTING BACKGROUD COLOR(limits of the color is from 0 to 255
    screen.fill((0, 59, 119))

    # BACKGROUND IMAGE
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # KEYS TESTING THAT WHICH KEY IS PRESSED OR NOT
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                print("LEFT KEY IS PRESSED")
                playerX_changes = -1.8
            # if event.key == pygame.K_UP:
            #    playerY_changes = -0.5
            # if event.key == pygame.K_DOWN:
            #    playerY_changes = 0.5
            if event.key == pygame.K_RIGHT:
                print("RIGHT KEY IS PRESSED")
                playerX_changes = 1.8
            if event.key == pygame.K_SPACE:
                bullet_sound = mixer.Sound('laser.wav')
                bullet_sound.play()
                if bullet_state == "ready":
                    bulletX = playerX
                    print("SPACE is pressed")
                    fire_bullet(playerX, playerY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                print("KEY RELEASED")
                playerX_changes = 0
                playerY_changes = 0

    # if player hit the boundary stop them there
    playerX += playerX_changes
    if playerX <= -25:
        playerX = -25
    elif playerX >= 636:
        playerX = 636

    # move the enemy when it touch the boundary
    for i in range(num_of_enemies):
        # GAME OVER
        if enemyY[i] > 220:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_changes[i]
        if enemyX[i] <= 0:
            enemyX_changes[i] = 1
            enemyY[i] += 14
        elif enemyX[i] >= 636:
            enemyX_changes[i] = -1
            enemyY[i] += 10
        # Collision
        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 520
            bullet_state = "ready"
            score_value += 1
            print(score_value)
            enemyX[i] = random.randint(0, 636)
            enemyY[i] = random.randint(10, 150)
        enemy(enemyX[i], enemyY[i], i)

    # BUllet fire
    if bulletY <= 0:
        bulletY = 520
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_changes

    # elif playerY <= 0:
    #    playerY = 0
    # elif playerY >= 520:
    #    playerY = 520
    # playerY += playerY_changes
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()

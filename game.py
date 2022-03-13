import pygame
import random
import math
from pygame import mixer

# initialize the pygame before creating games
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load("Space-Invaders-background.png")

# Background music
mixer.music.load("Mega Man 2- Mecha.wav")
mixer.music.play(-1)

# Title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("minimalspaceship1.png")
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# The invader
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 20

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("alien_invader.png"))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(3)
    enemyY_change.append(14)

# Bullet
# ready - You can't see the bullet
# fire - bullet is going to shoot
bulletImg = pygame.image.load("bullet.png")
explosionImg = pygame.image.load("explosion.png")
bulletX = playerX
bulletY = playerY
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',28)
textX = 10
textY = 10

# game over text
game_over_font = pygame.font.Font('freesansbold.ttf',70)

# Vitory text

vitory = pygame.font.Font('freesansbold.ttf',70)

def show_score(x, y):
    score = font.render("Score : "+ str(score_value),True,(255,255,255))
    screen.blit(score, (x, y))

def game_over_text():
    game_over = game_over_font.render("GAME OVER",True,(255, 255, 255))
    screen.blit(game_over ,(200, 250))

def vitory_text():
    vit = vitory.render("VITORY",True,(255, 255, 255))
    screen.blit(vit , (250, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))
    # .blit mean draw something on screen.


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

# coordinate function
def isCollision(enemyX,enemyY,bulletX,bulletY):
    d = math.sqrt(math.pow(enemyX-bulletX,2)+ math.pow(enemyY-bulletY,2))
    if d < 27:
        return True
    else:
        return False
score_value = 0

# collision with enemyship
def isCollision_e(enemyX, enemyY, playerX, playerY):
    d = math.sqrt(math.pow(enemyX-playerX,2)+math.pow(enemyY-playerY,2))
    if d < 27:
        return True

# This is the loop that will keep open the window of the game screen.
# Game loop
running = True
while running:
    screen.fill((0, 0, 0))
    # background Image
    screen.blit(background,(0,0))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
             running = False

        # if condition for key_stroke pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                playerX_change = -4
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                playerX_change = 4
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                playerX_change = 0

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                playerY_change = 4
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                playerY_change = -4
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("WU9GKZW-laser-noise-06.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    bulletY = playerY
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_w or event.key == pygame.K_s:
                playerY_change = 0

        # condition statement for bullet



    playerX += playerX_change
    # condition statement for spaceship going beyond boundaries
    if playerX <= 0:
        playerX = 768
    elif playerX >= 768:
        playerX = 0
    playerY -= playerY_change
    # condition statement for Y coordinate
    if playerY <= 400:
        playerY = 400
    elif playerY >= 535:
        playerY = 535
    player(playerX, playerY)

    # Enemy movement
    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 448:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        # Vitory text
        if score_value == 20:
            vitory_text()

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 768:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]

        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explode_sound = mixer.Sound("76H365G-explosion.wav")
            explode_sound.play()
            screen.blit(explosionImg, (enemyX[i], enemyY[i]))
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            print(f"score: ", str(score_value))
            # enemyX[i] = random.randint(0, 735)
            # enemyY[i] = random.randint(50, 150)
            enemyY[i] = -20000
        enemy(enemyX[i], enemyY[i],i)

        # collision with player
        collision_e = isCollision_e(enemyX[i],enemyY[i],playerX,playerY)
        if collision_e:
            playerImg = pygame.image.load("explosion.png")
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break


    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":

        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    show_score(textX, textY)


    pygame.display.update()
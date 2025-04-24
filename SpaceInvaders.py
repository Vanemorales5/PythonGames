import pygame
import random
import math
from pygame import mixer

# Initialize the pygame
pygame.init()

# Create screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')
# Resize background to fit screen
background = pygame.transform.scale(background, (800, 600))

# Sound
mixer.music.load('background.wav')
mixer.music.play(-1)  # -1 means play on loop

# Caption and icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
# Resize player image
playerImg = pygame.transform.scale(playerImg, (64, 64))
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_img = pygame.image.load('enemy.png')
    # Resize enemy image
    enemy_img = pygame.transform.scale(enemy_img, (50, 50))
    enemyImg.append(enemy_img)
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load('bullet.png')
# Resize bullet image
bulletImg = pygame.transform.scale(bulletImg, (16, 32))
bulletX = []
bulletY = []
bulletY_change = []
bullet_state = []
max_bullets = 5

for i in range(max_bullets):
    bulletX.append(0)
    bulletY.append(480)
    bulletY_change.append(10)
    bullet_state.append("ready")  # Ready - You can't see the bullet on the screen
    # Fire - The bullet is currently moving

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y, i):
    global bullet_state
    bullet_state[i] = "fire"
    screen.blit(bulletImg, (x + 24, y))  # Adjusted offset for centered bullet


def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX + 25 - (bulletX + 8), 2) + math.pow(enemyY + 25 - (bulletY + 16), 2))
    if distance < 35:  # Adjusted collision distance based on new sprite sizes
        return True
    return False


# Game loop
running = True
while running:

    # RGB = red, green, blue
    screen.fill((0, 0, 0))

    # Background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # If keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                # Find the first ready bullet and fire it
                for i in range(max_bullets):
                    if bullet_state[i] == "ready":
                        bulletX[i] = playerX
                        bulletY[i] = playerY
                        fire_bullet(bulletX[i], bulletY[i], i)
                        bullet_sound = mixer.Sound('laser.wav')
                        bullet_sound.play()
                        break

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Checking for boundaries of spaceship so it doesn't go out of bounds
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement
    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 750:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # Collision
        for j in range(max_bullets):
            if bullet_state[j] == "fire":
                if is_collision(enemyX[i], enemyY[i], bulletX[j], bulletY[j]):
                    explosion_sound = mixer.Sound('explosion.wav')
                    explosion_sound.play()
                    bulletY[j] = 480
                    bullet_state[j] = "ready"
                    score_value += 1
                    enemyX[i] = random.randint(0, 735)
                    enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    for i in range(max_bullets):
        if bulletY[i] <= 0:
            bulletY[i] = 480
            bullet_state[i] = "ready"

        if bullet_state[i] == "fire":
            fire_bullet(bulletX[i], bulletY[i], i)
            bulletY[i] -= bulletY_change[i]

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
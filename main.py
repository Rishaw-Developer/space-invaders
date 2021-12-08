import pygame
import random
import os
from pygame.constants import USEREVENT

pygame.init()
WIDTH, HEIGHT = 500, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

FPS = 60
VEL_PLAYER = 5
MAX_BULLETS = 5
INVADER_DIE = pygame.USEREVENT + 1
INCREASE_SCORE = pygame.USEREVENT + 2
DECREASE_SCORE = pygame.USEREVENT + 3
SCORE_FONT = pygame.font.SysFont("comicsans", 30)

BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))

PLAYER_SHIP = pygame.transform.scale(pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png")), (50, 50))

PLAYER_BULLET_IMG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png")), (50, 50))

# ENEMY SHIPS
BLUE_SHIP = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png")), (40, 40)), 180)
GREEN_SHIP = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png")), (40, 40)), 180)
RED_SHIP = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png")), (40, 40)), 180)


def drawWindow(player, player_bullet, invaders, player_score):
    WIN.blit(BACKGROUND, (0, 0))
    WIN.blit(PLAYER_SHIP, (player.x, HEIGHT - PLAYER_SHIP.get_height() - 10))
    for bullets in player_bullet:
        WIN.blit(PLAYER_BULLET_IMG, (bullets.x, bullets.y))
    for enemy in invaders:
        WIN.blit(BLUE_SHIP, (enemy.x, enemy.y))
    health = SCORE_FONT.render(f"Score: {player_score}", 1, (255, 255, 255))
    WIN.blit(health, (WIDTH - health.get_width() - 10, 10))
    pygame.display.update()

def player_movement(player):
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_LEFT] and player.x > 0:
        player.x -= VEL_PLAYER
    if keys_pressed[pygame.K_RIGHT] and player.x < WIDTH - PLAYER_SHIP.get_width():
        player.x += VEL_PLAYER

def player_handle_bullets(player_bullet, invaders):
    for bullet in player_bullet:
        bullet.y -= 3
        if bullet.y < 0:
            player_bullet.remove(bullet)
        for invader in invaders:
            if bullet.colliderect(invader):
                # player_score += 1
                pygame.event.post(pygame.event.Event(INVADER_DIE))
                pygame.event.post(pygame.event.Event(INCREASE_SCORE))
                player_bullet.remove(bullet)
                invaders.remove(invader)
                break

def enemy_handle_movement(invaders, player_score):
    for invader in invaders:
        invader.y += 1
        if invader.y > HEIGHT - BLUE_SHIP.get_height():
            pygame.event.post(pygame.event.Event(DECREASE_SCORE))
            invaders.remove(invader)
            pygame.event.post(pygame.event.Event(INVADER_DIE))
            print("Remove invaders")

def main():
    player = pygame.Rect(WIDTH/2, HEIGHT - PLAYER_SHIP.get_height() - 10, 50, 50)
    invaders = []

    run = True
    clock = pygame.time.Clock()

    player_bullet = []
    player_score = 0

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(player_bullet) < MAX_BULLETS:
                    player_bullet.append(pygame.Rect(player.x , player.y, 50, 50))

            if event.type == INVADER_DIE or len(invaders) < 5:
                invader_new = pygame.Rect(random.randint(0, WIDTH - BLUE_SHIP.get_width()), 0, 40, 40)
                invaders.append(invader_new)

            if event.type == INCREASE_SCORE:
                player_score += 1

            if event.type == DECREASE_SCORE:
                player_score -= 2

        if player_score < 0:
            pygame.quit()

        player_handle_bullets(player_bullet, invaders)
        player_movement(player)
        enemy_handle_movement(invaders, player_score)  
        drawWindow(player, player_bullet, invaders, player_score)

    pygame.quit()

if __name__ == '__main__':
    main()
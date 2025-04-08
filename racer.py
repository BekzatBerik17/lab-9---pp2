import pygame, sys
from pygame.locals import *
import random, time

pygame.init()


collision_sound = pygame.mixer.Sound("collision.wav")
coin_sound = pygame.mixer.Sound("coin.wav")


BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
ENEMY_SPEED = 10
GG_SPEED = 10
SCORE = 0
COIN_SIZE = (64, 64)
COINS_COLLECTED = 0


font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)


BG_IMG = pygame.image.load("AnimatedStreet.png")
coin_images = {
    1: pygame.transform.scale(pygame.image.load("Bronze coin.png"), COIN_SIZE),
    2: pygame.transform.scale(pygame.image.load("Silver coin.png"), COIN_SIZE),
    3: pygame.transform.scale(pygame.image.load("Gold coin.png"), COIN_SIZE)
}


display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
display.fill(WHITE)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, ENEMY_SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-GG_SPEED, 0)
        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(GG_SPEED, 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.weight = random.randint(1, 3)
        self.image = coin_images[self.weight]
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        self.rect.move_ip(0, ENEMY_SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.reset_position()

    def reset_position(self):
        self.weight = random.randint(1, 3)
        self.image = coin_images[self.weight]
        self.rect.top = 0
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

P1 = Player()
E1 = Enemy()
coin = Coin()

enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(coin)
coins = pygame.sprite.Group()
coins.add(coin)

INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            ENEMY_SPEED += 0.5
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    display.blit(BG_IMG, (0, 0))
    
    score_text = font_small.render(str(SCORE), True, BLACK)
    display.blit(score_text, (10, 10))
    coins_text = font_small.render(f"Coins: {COINS_COLLECTED}", True, BLACK)
    display.blit(coins_text, (300, 10))

    for entity in all_sprites:
        display.blit(entity.image, entity.rect)
        entity.move()

    if pygame.sprite.spritecollideany(P1, enemies):
        collision_sound.play()
        time.sleep(0.5)
        display.fill(RED)
        display.blit(game_over, (30, 250))
        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    if pygame.sprite.spritecollideany(P1, coins):
        coin_sound.play()
        COINS_COLLECTED += coin.weight
        coin.reset_position()

      
        if COINS_COLLECTED % 5 == 0:
            ENEMY_SPEED += 1

    pygame.display.update()
    pygame.time.Clock().tick(50)
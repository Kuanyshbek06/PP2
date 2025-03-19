import pygame, sys
from pygame.locals import *
import random, time
 
pygame.init()

# Загрузка фоновой музыки
try:
    pygame.mixer.music.load(r"C:\Users\kuany\OneDrive\Рабочий стол\PP2\lab8\background.wav")  
    pygame.mixer.music.play(-1)  
except pygame.error:
    print("Ошибка загрузки фоновой музыки")


FPS = 60
FramePerSec = pygame.time.Clock()
 

BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)  
 

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COINS_COLLECTED = 0 
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
font_coin = pygame.font.SysFont("Verdana", 20)  
game_over = font.render("Game Over", True, BLACK)

try:
    background = pygame.image.load("/Users\kuany\OneDrive\Рабочий стол\PP2\lab8\AnimatedStreet.png")  
except pygame.error:
    print("Ошибка загрузки фона")
    sys.exit()
 
try:
    player_image = pygame.image.load(r"C:\Users\kuany\OneDrive\Рабочий стол\PP2\lab8\Player.png") 
except pygame.error:
    print("Ошибка загрузки изображения игрока")
    sys.exit()
 
try:
    enemy_image = pygame.image.load("/Users\kuany\OneDrive\Рабочий стол\PP2\lab8\Enemy.png")  
except pygame.error:
    print("Ошибка загрузки изображения врага")
    sys.exit()
 

DISPLAYSURF = pygame.display.set_mode((400,600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")
 

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_image 
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)  
 
    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
 

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image  
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
 
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)
 

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))  
        pygame.draw.circle(self.image, YELLOW, (15, 15), 15)  
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), random.randint(0, SCREEN_HEIGHT-300))  
    def move(self):
        pass 
 

P1 = Player()
E1 = Enemy()
 
enemies = pygame.sprite.Group()
enemies.add(E1)  

coins = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)
while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5  
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
 
    DISPLAYSURF.blit(background, (0,0)) 
    scores = font_small.render(f"Score: {SCORE}", True, BLACK)
    DISPLAYSURF.blit(scores, (10,10))
    coin_count = font_coin.render(f"Coins: {COINS_COLLECTED}", True, BLACK)
    DISPLAYSURF.blit(coin_count, (SCREEN_WIDTH - 100, 10))  
 
 
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()
 

    if random.randint(1, 50) == 1: 
        new_coin = Coin()
        coins.add(new_coin)
        all_sprites.add(new_coin)
 
  
    for coin in coins:
        coin.rect.move_ip(0, SPEED)
        if pygame.sprite.collide_rect(P1, coin):  
            coins.remove(coin)
            all_sprites.remove(coin)
            COINS_COLLECTED += 1 
 
        if coin.rect.top > SCREEN_HEIGHT: 
            coins.remove(coin)
            all_sprites.remove(coin)
 
   
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound(r"C:\Users\kuany\OneDrive\Рабочий стол\PP2\lab8\crash.wav").play()
        time.sleep(0.5)
 
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30,250))
 
        pygame.display.update()
        for entity in all_sprites:
            entity.kill() 
        time.sleep(2)
        pygame.quit()
        sys.exit()        
 
    pygame.display.update()  
    FramePerSec.tick(FPS)  
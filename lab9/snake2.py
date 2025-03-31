import pygame
import random
import sys
pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

font = pygame.font.SysFont('Arial', 20)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

class Snake:
    def __init__(self):
        self.body = [(100, 100), (80, 100), (60, 100)]  
        self.direction = (GRID_SIZE, 0) 
        self.grow = False  
    
    def move(self):
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
    
    def grow_snake(self):
        self.grow = True 
    
    def check_collision(self):
        head_x, head_y = self.body[0]
        if head_x < 0 or head_x >= SCREEN_WIDTH or head_y < 0 or head_y >= SCREEN_HEIGHT:
            return True
        return False
    
    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, GREEN, pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE))

class Food:
    def __init__(self, snake_body):
        self.generate_new_food(snake_body)
    
    def generate_new_food(self, snake_body):
        self.food_types = [(RED, 1), (YELLOW, 2), (ORANGE, 3)]
        self.color, self.value = random.choice(self.food_types)
        self.position = self.random_position(snake_body)
        self.timer = pygame.time.get_ticks()
    
    def random_position(self, snake_body):
        while True:
            food_x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
            food_y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            if (food_x, food_y) not in snake_body:
                return (food_x, food_y)
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, pygame.Rect(self.position[0], self.position[1], GRID_SIZE, GRID_SIZE))

def game_loop():
    snake = Snake()
    food = Food(snake.body)
    clock = pygame.time.Clock()
    score = 0
    level = 1
    speed = 7
    food_lifetime = 5000 #Еда исчезает через 5 секунд
    
    while True:
        screen.fill(BLACK) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and snake.direction != (GRID_SIZE, 0):
                    snake.direction = (-GRID_SIZE, 0)
                if event.key == pygame.K_RIGHT and snake.direction != (-GRID_SIZE, 0):
                    snake.direction = (GRID_SIZE, 0)
                if event.key == pygame.K_UP and snake.direction != (0, GRID_SIZE):
                    snake.direction = (0, -GRID_SIZE)
                if event.key == pygame.K_DOWN and snake.direction != (0, -GRID_SIZE):
                    snake.direction = (0, GRID_SIZE)
        
        snake.move()
        
        if snake.check_collision():
            game_over(score, level)
            return 
        
        if snake.body[0] == food.position:
            snake.grow_snake()
            score += food.value  
            food.generate_new_food(snake.body)  
            if score % 4 == 0:  
                level += 1
                speed += 2
        
        if pygame.time.get_ticks() - food.timer > food_lifetime:
            food.generate_new_food(snake.body)
        
        snake.draw(screen)
        food.draw(screen)
        
        score_text = font.render(f"Score: {score}", True, WHITE)
        level_text = font.render(f"Level: {level}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (SCREEN_WIDTH - level_text.get_width() - 10, 10))
        pygame.display.update()  
        
        clock.tick(speed)

def game_over(score, level):
    screen.fill(BLACK)
    game_over_text = font.render("Game Over", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 4))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
    screen.blit(level_text, (SCREEN_WIDTH // 2 - level_text.get_width() // 2, SCREEN_HEIGHT // 2 + 30))
    pygame.display.update()
    pygame.time.wait(2000) 
    pygame.quit()
    sys.exit()
game_loop()
import pygame
import random
import sys
import psycopg2
import configparser


def config(filename='database.ini', section='postgresql'):
    parser = configparser.ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        for param in parser.items(section):
            db[param[0]] = param[1]
    return db

def connect():
    return psycopg2.connect(**config())

def get_or_create_user(conn, username):
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    if user:
        return user[0]
    cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING id", (username,))
    conn.commit()
    return cur.fetchone()[0]

def get_last_score(conn, user_id):
    cur = conn.cursor()
    cur.execute("SELECT level, score FROM user_scores WHERE user_id = %s ORDER BY id DESC LIMIT 1", (user_id,))
    return cur.fetchone()

def save_score(conn, user_id, level, score):
    cur = conn.cursor()
    cur.execute("INSERT INTO user_scores (user_id, level, score) VALUES (%s, %s, %s)", (user_id, level, score))
    conn.commit()



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
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

font = pygame.font.SysFont('Arial', 20)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game with PostgreSQL")

# ============ GAME CLASSES ============

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
        return (
            head_x < 0 or head_x >= SCREEN_WIDTH or
            head_y < 0 or head_y >= SCREEN_HEIGHT or
            self.body[0] in self.body[1:]
        )
    
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
            x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            if (x, y) not in snake_body:
                return (x, y)
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, pygame.Rect(self.position[0], self.position[1], GRID_SIZE, GRID_SIZE))

# ============ MAIN GAME LOOP ============

def game_loop(user_id, conn, start_level=1, start_score=0):
    snake = Snake()
    food = Food(snake.body)
    clock = pygame.time.Clock()
    score = start_score
    level = start_level
    speed = 7 + (level - 1) * 2
    food_lifetime = 5000

    while True:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_score(conn, user_id, level, score)
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
                if event.key == pygame.K_p:
                    save_score(conn, user_id, level, score)
                    print("Game paused and progress saved.")

        snake.move()

        if snake.check_collision():
            save_score(conn, user_id, level, score)
            game_over(score, level)

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
    over_text = font.render("Game Over", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(over_text, (SCREEN_WIDTH // 2 - over_text.get_width() // 2, 100))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 160))
    screen.blit(level_text, (SCREEN_WIDTH // 2 - level_text.get_width() // 2, 200))
    pygame.display.update()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    conn = connect()
    username = input("Enter your username: ")
    user_id = get_or_create_user(conn, username)
    last = get_last_score(conn, user_id)
    if last:
        start_level, start_score = last
        print(f"Welcome back {username}, Level {start_level}, Score {start_score}")
    else:
        start_level, start_score = 1, 0
        print(f"New player {username}. Starting from scratch.")
    game_loop(user_id, conn, start_level, start_score)

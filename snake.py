import pygame
import random
import time


pygame.init()


WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)


UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")


snake = [(WIDTH // 2, HEIGHT // 2)]
direction = RIGHT


class Food:
    def __init__(self):
        self.position = self.generate_position()
        self.weight = random.choice([1, 2, 3])  
        self.spawn_time = time.time()
        self.duration = random.randint(5, 10) 
        self.color = {1: RED, 2: YELLOW, 3: BLUE}[self.weight]

    def generate_position(self):
        while True:
            pos = (random.randint(1, (WIDTH // GRID_SIZE) - 2) * GRID_SIZE,
                   random.randint(1, (HEIGHT // GRID_SIZE) - 2) * GRID_SIZE)
            if pos not in snake:
                return pos

    def is_expired(self):
        return time.time() - self.spawn_time > self.duration

foods = [Food()]  


score = 0
level = 1
speed = 10
clock = pygame.time.Clock()

FOOD_SPAWN_INTERVAL = 4
last_food_spawn_time = time.time()

running = True
while running:
    screen.fill(BLACK)

   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != DOWN:
                direction = UP
            elif event.key == pygame.K_DOWN and direction != UP:
                direction = DOWN
            elif event.key == pygame.K_LEFT and direction != RIGHT:
                direction = LEFT
            elif event.key == pygame.K_RIGHT and direction != LEFT:
                direction = RIGHT


    head_x, head_y = snake[0]
    new_head = (head_x + direction[0] * GRID_SIZE, head_y + direction[1] * GRID_SIZE)


    if (new_head[0] < 0 or new_head[0] >= WIDTH or
        new_head[1] < 0 or new_head[1] >= HEIGHT or
        new_head in snake):
        running = False

    snake.insert(0, new_head)

    
    food_eaten = None
    for food in foods:
        if new_head == food.position:
            score += food.weight
            food_eaten = food
            if score % 4 == 0:
                level += 1
                speed += 2
            break

    if food_eaten:
        foods.remove(food_eaten)
    else:
        snake.pop()

  
    if time.time() - last_food_spawn_time > FOOD_SPAWN_INTERVAL:
        foods.append(Food())
        last_food_spawn_time = time.time()

    foods = [f for f in foods if not f.is_expired()]

    for food in foods:
        pygame.draw.rect(screen, food.color, (food.position[0], food.position[1], GRID_SIZE, GRID_SIZE))

    
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], GRID_SIZE, GRID_SIZE))


    font = pygame.font.Font(None, 24)
    score_text = font.render(f"Score: {score}  Level: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()
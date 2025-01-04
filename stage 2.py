import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Clock and FPS
clock = pygame.time.Clock()
FPS = 10

# Snake and Food Dimensions
BLOCK_SIZE = 20

# Fonts
font = pygame.font.Font(None, 36)

# Snake class
class Snake:
    def __init__(self):
        self.body = [[100, 50], [80, 50], [60, 50]]  # List of [x, y] positions
        self.direction = "RIGHT"  # Initial direction
        self.grow = False

    def move(self):
        head_x, head_y = self.body[0]
        if self.direction == "UP":
            head_y -= BLOCK_SIZE
        elif self.direction == "DOWN":
            head_y += BLOCK_SIZE
        elif self.direction == "LEFT":
            head_x -= BLOCK_SIZE
        elif self.direction == "RIGHT":
            head_x += BLOCK_SIZE

        # Add new head position
        new_head = [head_x, head_y]
        self.body.insert(0, new_head)

        # If not growing, remove the last segment
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def change_direction(self, new_direction):
        # Prevent reversing direction
        if (new_direction == "UP" and self.direction != "DOWN") or \
           (new_direction == "DOWN" and self.direction != "UP") or \
           (new_direction == "LEFT" and self.direction != "RIGHT") or \
           (new_direction == "RIGHT" and self.direction != "LEFT"):
            self.direction = new_direction

    def check_collision(self):
        head = self.body[0]
        # Check collision with walls
        if head[0] < 0 or head[0] >= SCREEN_WIDTH or head[1] < 0 or head[1] >= SCREEN_HEIGHT:
            return True
        # Check collision with itself
        if head in self.body[1:]:
            return True
        return False

    def draw(self):
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))

# Food class
class Food:
    def __init__(self):
        self.position = [random.randint(0, (SCREEN_WIDTH // BLOCK_SIZE) - 1) * BLOCK_SIZE,
                         random.randint(0, (SCREEN_HEIGHT // BLOCK_SIZE) - 1) * BLOCK_SIZE]

    def respawn(self):
        self.position = [random.randint(0, (SCREEN_WIDTH // BLOCK_SIZE) - 1) * BLOCK_SIZE,
                         random.randint(0, (SCREEN_HEIGHT // BLOCK_SIZE) - 1) * BLOCK_SIZE]

    def draw(self):
        pygame.draw.rect(screen, RED, (self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE))

# Initialize game objects
snake = Snake()
food = Food()

# Score
score = 0

# Main game loop
running = True
while running:
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.change_direction("UP")
            elif event.key == pygame.K_DOWN:
                snake.change_direction("DOWN")
            elif event.key == pygame.K_LEFT:
                snake.change_direction("LEFT")
            elif event.key == pygame.K_RIGHT:
                snake.change_direction("RIGHT")

    # Update snake
    snake.move()

    # Check for collisions
    if snake.check_collision():
        running = False  # Game over

    # Check if snake eats food
    if snake.body[0] == food.position:
        snake.grow = True
        food.respawn()
        score += 1

    # Draw snake and food
    snake.draw()
    food.draw()

    # Display score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

pygame.quit()

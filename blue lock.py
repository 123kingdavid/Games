import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Blue Lock Soccer Game")

# Colors
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Clock
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, 36)

# Game Objects
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5

    def move(self, keys, up, down, left, right):
        if keys[up]:
            self.rect.y -= self.speed
        if keys[down]:
            self.rect.y += self.speed
        if keys[left]:
            self.rect.x -= self.speed
        if keys[right]:
            self.rect.x += self.speed

        # Keep within screen bounds
        self.rect.x = max(0, min(SCREEN_WIDTH - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(SCREEN_HEIGHT - self.rect.height, self.rect.y))

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, WHITE, (10, 10), 10)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = [random.choice([-3, 3]), random.choice([-3, 3])]

    def move(self):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]

        # Bounce off walls
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speed[0] = -self.speed[0]
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.speed[1] = -self.speed[1]

# Goal Zones
goal_left = pygame.Rect(0, SCREEN_HEIGHT // 3, 10, SCREEN_HEIGHT // 3)
goal_right = pygame.Rect(SCREEN_WIDTH - 10, SCREEN_HEIGHT // 3, 10, SCREEN_HEIGHT // 3)

# Initialize player, ball, and sprites
player = Player(100, SCREEN_HEIGHT // 2, BLUE)
opponent = Player(SCREEN_WIDTH - 100, SCREEN_HEIGHT // 2, RED)
ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

all_sprites = pygame.sprite.Group()
all_sprites.add(player, opponent, ball)

# Game Variables
player_score = 0
opponent_score = 0

# Main Game Loop
running = True
while running:
    screen.fill(GREEN)

    # Draw the field
    pygame.draw.rect(screen, WHITE, goal_left)
    pygame.draw.rect(screen, WHITE, goal_right)
    pygame.draw.line(screen, WHITE, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT), 5)

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get keys for player movement
    keys = pygame.key.get_pressed()
    player.move(keys, pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d)
    opponent.move(keys, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)

    # Move the ball
    ball.move()

    # Check for collisions
    if player.rect.colliderect(ball.rect):
        ball.speed[0] = -ball.speed[0]
        ball.speed[1] += random.choice([-1, 1])

    if opponent.rect.colliderect(ball.rect):
        ball.speed[0] = -ball.speed[0]
        ball.speed[1] += random.choice([-1, 1])

    # Check for goals
    if ball.rect.colliderect(goal_left):
        opponent_score += 1
        ball.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        ball.speed = [random.choice([-3, 3]), random.choice([-3, 3])]

    if ball.rect.colliderect(goal_right):
        player_score += 1
        ball.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        ball.speed = [random.choice([-3, 3]), random.choice([-3, 3])]

    # Draw scores
    player_score_text = font.render(f"Player Score: {player_score}", True, WHITE)
    opponent_score_text = font.render(f"Opponent Score: {opponent_score}", True, WHITE)
    screen.blit(player_score_text, (20, 20))
    screen.blit(opponent_score_text, (SCREEN_WIDTH - 200, 20))

    # Draw all sprites
    all_sprites.draw(screen)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()

import pygame
import random

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
ANT_SPEED = 5
PREDATOR_SPEED = 2
FOOD_COUNT = 5
PREDATOR_COUNT = 3

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Setup screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ant Game")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Classes
class Ant:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, GRID_SIZE, GRID_SIZE)
        self.color = BLUE
        self.score = 0

    def move(self, keys):
        if keys[pygame.K_UP]:
            self.rect.y -= ANT_SPEED
        if keys[pygame.K_DOWN]:
            self.rect.y += ANT_SPEED
        if keys[pygame.K_LEFT]:
            self.rect.x -= ANT_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += ANT_SPEED

        # Keep ant inside the screen
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - GRID_SIZE))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - GRID_SIZE))

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

class Food:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, SCREEN_WIDTH // GRID_SIZE - 1) * GRID_SIZE,
                                random.randint(0, SCREEN_HEIGHT // GRID_SIZE - 1) * GRID_SIZE,
                                GRID_SIZE, GRID_SIZE)
        self.color = GREEN

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

class Predator:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, SCREEN_WIDTH // GRID_SIZE - 1) * GRID_SIZE,
                                random.randint(0, SCREEN_HEIGHT // GRID_SIZE - 1) * GRID_SIZE,
                                GRID_SIZE, GRID_SIZE)
        self.color = RED
        self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])

    def move(self):
        if self.direction == "UP":
            self.rect.y -= PREDATOR_SPEED
        elif self.direction == "DOWN":
            self.rect.y += PREDATOR_SPEED
        elif self.direction == "LEFT":
            self.rect.x -= PREDATOR_SPEED
        elif self.direction == "RIGHT":
            self.rect.x += PREDATOR_SPEED

        # Keep predator inside the screen
        if self.rect.x < 0 or self.rect.x >= SCREEN_WIDTH or self.rect.y < 0 or self.rect.y >= SCREEN_HEIGHT:
            self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

# Initialize game objects
ant = Ant()
foods = [Food() for _ in range(FOOD_COUNT)]
predators = [Predator() for _ in range(PREDATOR_COUNT)]

# Game loop
running = True
while running:
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle input
    keys = pygame.key.get_pressed()
    ant.move(keys)

    # Move predators
    for predator in predators:
        predator.move()

    # Check collisions
    for food in foods[:]:
        if ant.rect.colliderect(food.rect):
            foods.remove(food)
            foods.append(Food())
            ant.score += 1

    for predator in predators:
        if ant.rect.colliderect(predator.rect):
            print(f"Game Over! Final Score: {ant.score}")
            running = False

    # Draw everything
    ant.draw()
    for food in foods:
        food.draw()
    for predator in predators:
        predator.draw()

    # Display score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {ant.score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Update display
    pygame.display.flip()

    # Frame rate control
    clock.tick(30)

pygame.quit()

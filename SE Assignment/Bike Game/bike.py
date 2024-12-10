import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Initialize Pygame mixer for sound
pygame.mixer.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bike Race Game")

# Clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 60

# Load assets
bike_image = pygame.image.load("bike.png")
bike_width, bike_height = 100, 100  # Resize bike dimensions
bike_image = pygame.transform.scale(bike_image, (bike_width, bike_height))

obstacle_image = pygame.image.load("obstacle.png")
obstacle_width, obstacle_height = 50, 100  # Resize obstacle dimensions
obstacle_image = pygame.transform.scale(obstacle_image, (obstacle_width, obstacle_height))

# Load sounds
start_sound = pygame.mixer.Sound("start_sound.wav")  # Replace with your sound file
end_sound = pygame.mixer.Sound("end_sound.wav")      # Replace with your sound file
pygame.mixer.music.load("background_music.wav")      # Replace with your background music file

# Fonts
font = pygame.font.Font(None, 36)

# Variables
bike_x = SCREEN_WIDTH // 2
bike_y = SCREEN_HEIGHT - bike_height - 20
bike_speed = 7

obstacles = []
obstacle_speed = 5
spawn_timer = 0

score = 0
game_over = False

# Functions
def draw_text(text, color, x, y):
    """Draw text on the screen."""
    render = font.render(text, True, color)
    screen.blit(render, (x, y))

def draw_bike(x, y):
    """Draw the player's bike."""
    screen.blit(bike_image, (x, y))

def spawn_obstacle():
    """Spawn a new obstacle at a random position."""
    x = random.randint(0, SCREEN_WIDTH - obstacle_width)
    obstacles.append(pygame.Rect(x, -obstacle_height, obstacle_width, obstacle_height))

def draw_obstacles():
    """Draw all obstacles."""
    for obstacle in obstacles:
        screen.blit(obstacle_image, obstacle.topleft)

def check_collision():
    """Check if the bike collides with any obstacles."""
    bike_rect = pygame.Rect(bike_x, bike_y, bike_width, bike_height)
    for obstacle in obstacles:
        if bike_rect.colliderect(obstacle):
            return True
    return False

# Play the start sound
start_sound.play()

# Start the background music (loop indefinitely)
pygame.mixer.music.play(-1)

# Main Game Loop
while True:
    screen.fill(WHITE)

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Player input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and bike_x > 0 and not game_over:
        bike_x -= bike_speed
    if keys[pygame.K_RIGHT] and bike_x < SCREEN_WIDTH - bike_width and not game_over:
        bike_x += bike_speed

    # Update game state
    if not game_over:
        spawn_timer += 1
        if spawn_timer > 30:  # Spawn a new obstacle every 30 frames
            spawn_obstacle()
            spawn_timer = 0

        # Move obstacles
        for obstacle in obstacles:
            obstacle.y += obstacle_speed

        # Remove obstacles that go off-screen
        obstacles = [ob for ob in obstacles if ob.y < SCREEN_HEIGHT]

        # Check for collisions
        if check_collision():
            game_over = True
            end_sound.play()  # Play the end sound when the game ends
            pygame.mixer.music.stop()  # Stop the background music

        # Update score
        score += 1

    # Draw everything
    draw_bike(bike_x, bike_y)
    draw_obstacles()
    draw_text(f"Score: {score}", BLACK, 10, 10)

    if game_over:
        draw_text("Game Over! Press R to Restart", RED, SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2)

    # Restart game
    if game_over and keys[pygame.K_r]:
        bike_x = SCREEN_WIDTH // 2
        bike_y = SCREEN_HEIGHT - bike_height - 20
        obstacles = []
        score = 0
        game_over = False
        start_sound.play()  # Play the start sound when restarting
        pygame.mixer.music.play(-1)  # Restart background music

    # Update display
    pygame.display.flip()

    # Control frame rate
    clock.tick(FPS)

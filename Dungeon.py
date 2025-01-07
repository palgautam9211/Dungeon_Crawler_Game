import pygame
import random

pygame.init()

# Screen/window size
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Dungeon Crawler")

# Defining the colors
Black = (0, 0, 0)
White = (255, 255, 255)
Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0, 0, 255)

# Wall Size
Tile_Size = 32

# Clock object
clock = pygame.time.Clock()

# Load the files/images
player_image = pygame.image.load("Photo.png")  # Replace "player.png" with your player image
player_image = pygame.transform.scale(player_image, (Tile_Size, Tile_Size))
enemy_image = pygame.image.load("Demon.jpg")  # Replace "demon.png" with your demon image
enemy_image = pygame.transform.scale(enemy_image, (Tile_Size, Tile_Size))

# Displaying the Survival time
font = pygame.font.Font(None, 36)

# Create the Player
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0
        if keys[pygame.K_LEFT]:
            dx -= self.speed
        if keys[pygame.K_RIGHT]:
            dx += self.speed
        if keys[pygame.K_UP]:
            dy -= self.speed
        if keys[pygame.K_DOWN]:
            dy += self.speed

        # Collision with walls
        self.rect.x += dx
        if pygame.sprite.spritecollideany(self, walls):
            self.rect.x -= dx
        self.rect.y += dy
        if pygame.sprite.spritecollideany(self, walls):
            self.rect.y -= dy

        # Keep player within outer wall
        self.rect.x = max(0, min(self.rect.x, screen_width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, screen_height - self.rect.height))

# Creating the Wall
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((Tile_Size, Tile_Size))
        self.image.fill(Red)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Create the Enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2

    def update(self, target):
        dx = self.speed if self.rect.x < target.rect.x else -self.speed
        dy = self.speed if self.rect.y < target.rect.y else -self.speed
        self.rect.x += dx
        self.rect.y += dy

#Function to Generate the dungeon layout
def generate_dungeon():
    walls = pygame.sprite.Group()
    # Create outer walls
    for x in range(0, screen_width, Tile_Size):
        walls.add(Wall(x, 0))  # Top
        walls.add(Wall(x, screen_height - Tile_Size))  # Bottom
    for y in range(0, screen_height, Tile_Size):
        walls.add(Wall(0, y))  # Left
        walls.add(Wall(screen_width - Tile_Size, y))  # Right

    # Add internal walls with random module
    for i in range(20):  # Adjust this number to control the density of walls
        x = random.randint(Tile_Size, screen_width - 2 * Tile_Size)
        y = random.randint(Tile_Size, screen_height - 2 * Tile_Size)
        walls.add(Wall(x, y))

    return walls

# Creating the objects
player = Player(100, 100)
walls = generate_dungeon()
enemies = pygame.sprite.Group(Enemy(400, 400))
all_sprites = pygame.sprite.Group(player, *walls, *enemies)

# Main Game loop
running = True
game_over = False
start_time = 0

def reset_game():
    global player, walls, enemies, all_sprites, start_time, game_over
    player = Player(100, 100)
    walls = generate_dungeon()
    enemies = pygame.sprite.Group(Enemy(400, 400))
    all_sprites = pygame.sprite.Group(player, *walls, *enemies)
    game_over = False
    start_time = pygame.time.get_ticks()

reset_game()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        player.update()

        for enemy in enemies:
            enemy.update(player)

        # Check for player-enemy collision
        if pygame.sprite.spritecollideany(player, enemies):
            game_over = True

        # Fill the screen with black
        screen.fill(Black)

        # Draw all sprites
        all_sprites.draw(screen)

        # Calculate Survival time
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000  # Convert milliseconds to seconds

        # Display time on the screen
        time_text = font.render(f"Time: {elapsed_time}s", True, White)
        screen.blit(time_text, (10, 10))

    else:
        # Game Over screen
        screen.fill(Black)
        game_over_text = font.render("Game Over!", True, White)
        score_text = font.render(f"You Survived: {elapsed_time} seconds", True, White)
        play_again_text = font.render("Press Space to Play Again", True, White)
        text_rect_game_over = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2 - 30))
        text_rect_score = score_text.get_rect(center=(screen_width // 2, screen_height // 2))
        text_rect_play_again = play_again_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))  # Increased vertical spacing
        screen.blit(game_over_text, text_rect_game_over)
        screen.blit(score_text, text_rect_score)
        screen.blit(play_again_text, text_rect_play_again)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            reset_game()

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)

pygame.quit()
quit()

import pygame
import webbrowser
import random
import pygame.freetype  # Import the freetype module.

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 800, 600
PLAYER_SPEED = 5
NUM_OBSTACLES = 10
NUM_POWERUPS = 5
POWERUP_TIME = 10  # Seconds that the speed powerup lasts
GAME_TIME = 60  # Seconds that the player has to reach the goal

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

# Create a player, goal, obstacles, and power-ups
player = pygame.Rect(WIDTH // 2, HEIGHT // 2, 50, 50)
goal = pygame.Rect(WIDTH - 100, HEIGHT - 100, 50, 50)
obstacles = [pygame.Rect(random.randrange(WIDTH), random.randrange(HEIGHT), 50, 50) for _ in range(NUM_OBSTACLES)]
powerups = [pygame.Rect(random.randrange(WIDTH), random.randrange(HEIGHT), 30, 30) for _ in range(NUM_POWERUPS)]

player_health = 100
powerup_active = False
powerup_time_remaining = 0
game_time_remaining = GAME_TIME
score = 0


def rickroll():
    webbrowser.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ')


def main_menu():
    menu_font = pygame.freetype.Font(None, 50)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game()

        screen.fill((0, 0, 0))
        menu_font.render_to(screen, (WIDTH // 2 - 100, HEIGHT // 2 - 50), "Press SPACE to start", (255, 255, 255))
        menu_font.render_to(screen, (WIDTH // 2 - 150, HEIGHT // 2 + 50), "Made by ArriesIsHier", (255, 255, 255))
        pygame.display.flip()


def game():
    global player_health, powerup_active, powerup_time_remaining, game_time_remaining, score
    clock = pygame.time.Clock()
    running = True
    start_ticks = pygame.time.get_ticks()

    while running:
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        game_time_remaining = GAME_TIME - seconds

        if game_time_remaining <= 0:
            print("Time's up! Game Over.")
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        speed = PLAYER_SPEED * 2 if powerup_active else PLAYER_SPEED
        if keys[pygame.K_a]:
            player.x -= speed
        if keys[pygame.K_d]:
            player.x += speed
        if keys[pygame.K_w]:
            player.y -= speed
        if keys[pygame.K_s]:
            player.y += speed

        if player.colliderect(goal):
            running = False
            score += 100  # Bonus points for reaching the goal
            rickroll()

        for obstacle in obstacles:
            if player.colliderect(obstacle):
                player_health -= 1
                if player_health <= 0:
                    print("You hit too many obstacles! Game Over.")
                    running = False

        for powerup in powerups:
            if player.colliderect(powerup):
                powerups.remove(powerup)
                powerup_active = True
                powerup_time_remaining = POWERUP_TIME
                score += 10  # Points for collecting a powerup

        if powerup_active:
            powerup_time_remaining -= 1 / 60  # Decrease the time remaining by the time since the last frame
            if powerup_time_remaining <= 0:
                powerup_active = False

        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (0, 255, 0), player)
        pygame.draw.rect(screen, (255, 0, 0), goal)
        for obstacle in obstacles:
            pygame.draw.rect(screen, (255, 255, 255), obstacle)
        for powerup in powerups:
            pygame.draw.rect(screen, (0, 0, 255), powerup)

        # Display player status
        status_font = pygame.freetype.Font(None, 30)
        status_font.render_to(screen, (10, 10), f"Health: {player_health}", (255, 255, 255))
        status_font.render_to(screen, (10, 40), f"Power Up: {'Active' if powerup_active else 'Inactive'}",
                              (255, 255, 255))
        status_font.render_to(screen, (10, 70), f"Score: {score}", (255, 255, 255))

        pygame.display.flip()
        clock.tick(60)

    # Display game over message and score
    game_over_font = pygame.freetype.Font(None, 50)


# Display game over message and score
game_over_font = pygame.freetype.Font(None, 50)
game_over_font.render_to(screen, (WIDTH // 2 - 100, HEIGHT // 2 - 50), "Game Over", (255, 255, 255))
game_over_font.render_to(screen, (WIDTH // 2 - 100, HEIGHT // 2), f"Final Score: {score}", (255, 255, 255))
pygame.display.flip()

# Wait a few seconds before returning to the main menu
pygame.time.wait(3000)

if __name__ == "__main__":
    main_menu()

pygame.quit()

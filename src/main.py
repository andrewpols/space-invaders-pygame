import pygame
from pygame.locals import *
import sys
import asyncio
import random

# Initialize Pygame
pygame.init()

# Initialize the font module to display text
pygame.font.init()
pygame.mixer.init()

# Create a font to render later
font = pygame.font.Font(None, 36)


# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (219, 213, 18)

# Initial variables for spaceship
x = 400  # Spaceship X position
y = 500  # Spaceship Y position
count = 0  # Laser count
move_right = False  # Flag to move spaceship right
move_left = False  # Flag to move spaceship left
laser = False  # Flag to indicate laser firing
spaceship_lasers = []  # List of rectangles (lasers)
health = 3  # Player starting health
score = 0  # Starting score
laser_time = 0  # Countdown timer for laser recharge

# Init variables for aliens
alien_rect = []  # List of alien rectangles
alien_x = 100  # Starting x-coordinate for alien
alien_y = 60  # Starting y-coordinate for alien
moving_right = True  # Flag to indicate aliens moving right
moving_left = False  # Flag to indicate aliens moving left
laser_cooldown = 120  # Cooldown for alien laser firing
alien_lasers = []  # List to store alien lasers
aliens = []  # List of all aliens on-screen

music_stop = 0


# Initialize the font module to display text
pygame.font.init()

# Create a font to render later
font = pygame.font.Font(None, 36)


# Function to display player's health on the screen
def display_health():
    health_text = font.render("Health: " + str(health), True, YELLOW)
    screen.blit(health_text, (10, 10))


# Function to display score on screen
def display_score():
    score_text = font.render("Score: " + str(score), True, YELLOW)
    screen.blit(score_text, (10, 40))


# Load images
spaceship = pygame.image.load("images/spaceship.png")
extra_alien_surface = pygame.image.load("images/extra_alien.png")
alien_image = pygame.image.load("images/alien.png")


# Draw the aliens
for column in range(5):
    for row in range(8):
        # Get the hitbox of the alien and put it into a list of alien rectangles
        alien_rect = pygame.Rect(alien_x + row * 50, alien_y + column * 60, 40, 40)
        aliens.append(alien_rect)


# Bonus Alien Flying at the top
extra_time = 2000  # Countdown timer for the extra alien to fly across screen
extra_x = 600  # Starting x_cooridnate for the extra alien


# Have the extra alien spawn every so often and reset the alien after it passes
def extra_alien():
    global extra_time, extra_x, health, count, score

    # Count down from 2000 to 0 by 5
    extra_time -= 5

    # Once it reaches 0, make the alien move left across the screen
    if extra_time <= 0:
        extra_x -= 5

    # Once it reaches the end of the screen, reset the x-coordinate and countdown
    if extra_x <= -20:
        extra_time = 900
        extra_x = 600

    # Draw the alien on the screen
    screen.blit(extra_alien_surface, (extra_x, 50))

    # Check collision between spaceship and bonus alien
    for item in spaceship_lasers:
        # Make a rectangle for all the lasers in the laser list
        laser_collision = pygame.Rect(item)

        # Make a rectangle for the extra alien
        extra_alien_collision = pygame.Rect(
            extra_x,
            50,
            extra_alien_surface.get_width(),
            extra_alien_surface.get_height(),
        )

        # Check if the laser's rectangle collides with the extra alien's rectangle
        if laser_collision.colliderect(extra_alien_collision):
            # Add a life/health
            health += 1

            # Reset x-coordinate and countdown
            extra_time = 900
            extra_x = 600

            # Rapid Fire
            count -= 10

            # Add to score
            score += 50

            break

    return health, score


# Set the width and height of the screen
size = (600, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Space Invaders")

# Music
music = "audio/space_invaders.ogg"
pygame.mixer.init()
pygame.mixer.music.load(music)
pygame.mixer.music.play(-1)

laser_sound = pygame.mixer.Sound("audio/laser.ogg")
damage_sound = pygame.mixer.Sound("audio/damage.ogg")

# Make a list for each obstacle (individualized to count each health level)
obstacles = []
for i in range(4):
    obstacle = pygame.Rect(25 + 150 * i, 450, 60, 10)
    obstacles.append(obstacle)

# Starting health for each obstacle (3)
obstacle_health = [3] * 4


# Function to detect collisions with lasers colliding with the obstacles
def laser_obstacle_collision():
    global obstacles, obstacle_health, alien_lasers

    # Alien Lasers colliding with obstacles

    # Iterate through every laser and every obstacle to check if an obstacle was hit

    # Check all rectangle lasers in the alien lasers list
    for laser in alien_lasers:
        # Check all rectangles in the obstacles list
        for i in range(len(obstacles)):
            # Check to see if laser rect collided with obstacle rect
            if laser.colliderect(obstacles[i]):
                # Remove the laser from the screen
                alien_lasers.remove(laser)
                # Lower the obstacle health
                obstacle_health[i] -= 1
                break  # Exit the loop since collision happened

    # Spaceship laser colliding with obstacles
    for laser in spaceship_lasers:
        laser_collision = pygame.Rect(laser)
        for i in range(len(obstacles)):
            if laser_collision.colliderect(obstacles[i]):
                spaceship_lasers.remove(laser)
                break

    # Create a copy of obstacles that don't have health equal to 0
    # to avoid index errors when those obstacles are removed.
    obstacles_copy = []

    # Create a copy of the health of each obstacle to match the obstacle copy to the obstacle health
    obstacle_health_copy = []

    # Only add the remaining obstacles and their respective health to the list if health is greater than 0
    for i in range(len(obstacles)):
        if obstacle_health[i] > 0:
            obstacles_copy.append(obstacles[i])
            obstacle_health_copy.append(obstacle_health[i])

    # Set each list to equal the new copy so that it can iterate again
    obstacles = obstacles_copy  # Update the obstacles list
    obstacle_health = obstacle_health_copy  # Update the obstacle_health list

    return obstacle_health, alien_lasers, obstacles


# Load and scale the background image
background_image = pygame.image.load("images/galaxy.png")
background_image = pygame.transform.scale(background_image, size)


# Use a game_over loop as well so that we can add a game over/game won screen at the end
# without ending the program completely (removes all other images)
game_over = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()


def playGame():
    global x, y, count, move_right, move_left, laser, spaceship_lasers, health, score, laser_time, alien_rect, alien_x, alien_y, moving_right, moving_left, laser_cooldown, alien_lasers, aliens, game_over, obstacles, obstacle_health, music_stop, laser_sound, damage_sound
    # Only check to recharge every 2 shots
    if count == 2:
        # Increase laser_time until it reaches 180
        if laser_time < 180:
            laser_time += 1
        # Reset the count and countdown when laser_time reaches 60
        else:
            count = 0

    # Use game_over just to organize between game_win and game_over
    if not game_over:
        # Draw obstacles
        for obstacle in obstacles:
            pygame.draw.rect(screen, GREEN, obstacle)

        # Move the spaceship if right or left key is pressed
        if move_right and x < 565:
            x += 5
        elif move_left and x > 10:
            x -= 5

        # Draw the spaceship
        screen.blit(spaceship, [x, y])

        # Move the aliens horizontally
        if moving_right:
            for alien_rect in aliens:
                alien_rect[0] += 1
        elif moving_left:
            for alien_rect in aliens:
                alien_rect[0] -= 1

        # When the rightmost alien hits the right side of the screen (max x value),
        # move down & switch direction to left.
        if aliens and max(alien_rect[0] for alien_rect in aliens) > 550:
            moving_right = False
            moving_left = True
            for alien_rect in aliens:
                alien_rect[1] += 7

        # When the leftmost alien hits the screen(min x), move right and down
        if aliens and min(alien_rect[0] for alien_rect in aliens) < 10:
            moving_right = True
            moving_left = False
            for alien_rect in aliens:
                alien_rect[1] += 7

        # Display each alien, starting in the top left
        if not game_over:
            for alien_rect in aliens:
                screen.blit(alien_image, alien_rect.topleft)

        # Check collisions with lasers and aliens

        # Iterate through every laser in the list
        for laser in spaceship_lasers:
            # Iterate through every alien in the list
            for alien_rect in aliens:
                # Check if the alien rectangle collides with the laser rectangle
                if alien_rect.colliderect(pygame.Rect(laser[0], laser[1], 5, 10)):
                    # Remove the alien and laser from the list
                    aliens.remove(alien_rect)
                    spaceship_lasers.remove(laser)
                    # Increase score
                    score += 20
                    break

        # Remove aliens that have moved beyond the screen
        aliens = [alien_rect for alien_rect in aliens if alien_rect.top < 600]

        # Draw the remaining lasers
        for laser in spaceship_lasers:
            # Make the y-coordinate of each laser go up 5 when fired
            laser[1] -= 5
            # Draw laser
            pygame.draw.rect(screen, RED, laser)

        # Alien laser firing logic

        # Only shoot if there are even aliens on the screen and if the cooldown is 0
        if laser_cooldown <= 0 and aliens:
            # Select a random alien to shoot
            alien_to_shoot = random.choice(aliens)
            # Create a new alien laser with the position aligned with the selected alien
            alien_laser = pygame.Rect(
                alien_to_shoot[0] + 20, alien_to_shoot[1] + 40, 2, 10
            )
            # Add it to the list of alien lasers
            alien_lasers.append(alien_laser)

            # Reset the cooldown for the next alien laser
            laser_cooldown = 60

            # Shoot faster if score is higher
            for i in range(3):
                if score >= 100 + i * 150:
                    laser_cooldown = 55 - i * 7

        #  If cooldown isn't 0, subtract until 0 as normal
        else:
            laser_cooldown -= 1

        # Move and draw alien lasers
        # Iterate through every laser in the alien_lasers list
        for alien_laser in alien_lasers:
            # Move the alien laser downward
            alien_laser[1] += 5
            pygame.draw.rect(screen, GREEN, alien_laser)

        # Check collision with the spaceship
        # Iterate through each laser in the list
        for alien_laser in alien_lasers:
            # Check if the spaceship rectangle (with coordinates of x & y) collides
            # with the alien laser
            if pygame.Rect(x, y, 40, 40).colliderect(alien_laser):
                # Decrease player's health when hit
                health -= 1
                damage_sound.play()

                # Game over logic
                if health <= 0:
                    game_over = True

                # Remove alien laser when game over
                alien_lasers.remove(alien_laser)

        # Only include lasers in the alien_lasers list if the y-coordinate
        # is less than 600 (on the screen); remove off-screen lasers
        for laser in alien_lasers:
            if laser[1] > 600:
                alien_lasers.remove(laser)

        # Draw every remaining spaceship laser
        for item in spaceship_lasers:
            # Make the spaceship laser move up
            item[1] -= 5
            # Draw laser
            pygame.draw.rect(screen, RED, item)

        # Draw the bonus alien
        extra_alien()

        # Check collision between spaceship and aliens
        for alien_rect in aliens:
            if alien_rect.colliderect(pygame.Rect(x, y + 20, 40, 40)):
                game_over = True
                break

        # Alien laser collision with obstacle
        laser_obstacle_collision()

        # Show health and score
        display_health()
        display_score()

    # Has the game ended?
    # Check if there are any aliens on the screen or if health has run out
    if not aliens or health < 0:
        game_over = True

    # If the game has ended because health ran out, display the game over message
    if health <= 0:
        if music_stop == 0:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("audio/game_over.ogg")
            pygame.mixer.music.play(-1)
            pygame.draw.rect(screen, BLACK, (150, 220, 480, 70))
            pygame.draw.rect(screen, BLACK, (210, 270, 380, 70))
            pygame.draw.rect(screen, BLACK, (150, 380, 340, 70))

        music_stop += 1

        # Display "GAME OVER: YOU LOSE" message
        end_font = pygame.font.Font(None, 50)
        game_over_text = end_font.render("GAME OVER: YOU LOSE", True, RED)
        screen.blit(game_over_text, (150, 250))

        # Display final score
        final_score = end_font.render("FINAL SCORE: " + str(score), True, RED)
        screen.blit(final_score, (200, 300))

        pygame.display.flip()

    # If it has ended because there are no aliens,
    if not aliens:
        if music_stop == 0:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("audio/game_won.ogg")
            pygame.mixer.music.play(-1)
            pygame.draw.rect(screen, BLACK, (150, 400, 300, 30))
            pygame.draw.rect(screen, BLACK, (150, 250, 300, 30))
            pygame.draw.rect(screen, BLACK, (200, 300, 300, 30))

        music_stop += 1

        # Display "GAME WIN" message
        end_font = pygame.font.Font(None, 50)
        game_win_text = end_font.render("GAME WON!", True, GREEN)
        screen.blit(game_win_text, (150, 250))

        # Display final score
        final_score = end_font.render("FINAL SCORE: " + str(score), True, GREEN)
        screen.blit(final_score, (200, 300))

        pygame.display.flip()

    # Set the frames per second
    clock.tick(60)

    # Update the screen
    pygame.display.flip()


# Main Program Loop
async def main():
    global x, y, count, move_right, move_left, laser, spaceship_lasers, health, score, laser_time, alien_rect, alien_x, alien_y, moving_right, moving_left, laser_cooldown, alien_lasers, aliens, game_over, obstacles, obstacle_health, music_stop, laser_sound, damage_sound
    while True:
        laser_time += 1
        # Background Image
        screen.blit(background_image, (0, 0))
        # Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    move_right = True
                elif event.key == pygame.K_LEFT:
                    move_left = True
                # When user hits space, rectangle is added to spaceship_lasers. This is the users' laser
                # Laser only appears if the count (recharge control) is less than 2.
                elif event.key == pygame.K_SPACE:
                    if count < 2:
                        laser_sound.play()
                        new_rect = [x + 5, y, 5, 10]
                        spaceship_lasers.append(new_rect)
                        # Control laser fire by increasing count
                        count += 1
                        laser_time = 0
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    move_right = False
                elif event.key == pygame.K_LEFT:
                    move_left = False
        playGame()

        while game_over == True:
            restart_font = pygame.font.Font(None, 50)
            restart_text = restart_font.render("Click RETURN to restart", True, BLUE)
            screen.blit(restart_text, (150, 400))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # Define colors
                        # Initial variables for spaceship
                        x = 400  # Spaceship X position
                        y = 500  # Spaceship Y position
                        count = 0  # Laser count
                        move_right = False  # Flag to move spaceship right
                        move_left = False  # Flag to move spaceship left
                        laser = False  # Flag to indicate laser firing
                        spaceship_lasers = []  # List of rectangles (lasers)
                        health = 3  # Player starting health
                        score = 0  # Starting score
                        laser_time = 0  # Countdown timer for laser recharge

                        # Init variables for aliens
                        alien_rect = []  # List of alien rectangles
                        alien_x = 100  # Starting x-coordinate for alien
                        alien_y = 60  # Starting y-coordinate for alien
                        moving_right = True  # Flag to indicate aliens moving right
                        moving_left = False  # Flag to indicate aliens moving left
                        laser_cooldown = 120  # Cooldown for alien laser firing
                        alien_lasers = []  # List to store alien lasers
                        aliens = []  # List of all aliens on-screen
                        game_over = False
                        obstacles = []
                        for i in range(4):
                            obstacle = pygame.Rect(25 + 150 * i, 450, 60, 10)
                            obstacles.append(obstacle)
                        obstacle_health = [3] * 4

                        for column in range(5):
                            for row in range(8):
                                # Get the hitbox of the alien and put it into a list of alien rectangles
                                alien_rect = pygame.Rect(
                                    alien_x + row * 50, alien_y + column * 60, 40, 40
                                )
                                aliens.append(alien_rect)
                        pygame.mixer.music.stop()
                        pygame.mixer.music.unload()
                        pygame.mixer.music.load("audio/space_invaders.ogg")
                        pygame.mixer.music.play(-1)
                        music_stop = 0
                        playGame()

            await asyncio.sleep(0)
        await asyncio.sleep(0)


asyncio.run(main())

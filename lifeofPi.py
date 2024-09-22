import random
import pygame
from sys import exit

pygame.init()

# Init game
gameactive = False
first_time = True
gameWin = False

# Function to draw the health bar
def Healthbar(screen, x, y, health):
    BAR_WIDTH = 200
    BAR_HEIGHT = 30
    fill = health / 100 * BAR_WIDTH

    # Draw actual healthbar
    pygame.draw.rect(screen, 'Red', (x, y, BAR_WIDTH, BAR_HEIGHT))

    # Draw fillbar
    pygame.draw.rect(screen, 'Green', (x, y, fill, BAR_HEIGHT))

def Hungerbar(screen, x, y, hunger):
    H_barwidth = 200
    H_barheight = 30
    H_fill = hunger / 100 * H_barwidth

    # Draw Hungerbar
    pygame.draw.rect(screen, 'Red', (x, y, H_barwidth, H_barheight))

    # Draw Fillbar
    pygame.draw.rect(screen, 'Orange', (x, y, H_fill, H_barheight))




# Intro screen
intro_surface = pygame.image.load('ENTER LOCATION')
intro_surface = pygame.transform.scale(intro_surface, (1900, 1000))

# Outro screen
outro_surface = pygame.image.load('ENTER LOCATION')
outro_surface = pygame.transform.scale(outro_surface, (1900, 1000))

#Win screen
win_surface = pygame.image.load ('ENTER LOCATION')
win_surface = pygame.transform.scale(win_surface, (1900, 1000))


# Text
test_font = pygame.font.Font('ENTER LOCATION', 50)
Health_display = test_font.render("Health", False, (0, 0, 0))
Hunger_display = test_font.render("Hunger", False, (0, 0, 0))

# Lifeboat
lifeboat_surface = pygame.image.load('ENTER LOCATION')
lifeboat_surface = pygame.transform.rotozoom(lifeboat_surface, 0, 0.75)
lifeboat_rect = lifeboat_surface.get_rect(center=(200, 540))

# Background
ocean_surface = pygame.image.load('ENTER LOCATION')
ocean_surface = pygame.transform.scale(ocean_surface, (1900, 1000))
screen = pygame.display.set_mode((1900, 1000))

# Fishes
dodaro_surface = pygame.image.load('ENTER LOCATION')
dodaro_surface = pygame.transform.rotozoom(dodaro_surface, 0, 0.2)
dodaro_rect = dodaro_surface.get_rect(center=(1700, 540))  # Adjust the initial position as needed

# Seaturtle
seaturtle_surface = pygame.image.load('ENTER LOCATION')
seaturtle_surface = pygame.transform.rotozoom(seaturtle_surface, 0, 0.2)
seaturtle_rect = seaturtle_surface.get_rect(center=(1700, 540))

# Make the dodaro's rectangle smaller
dodaro_rect = dodaro_rect.inflate(-150, -150)  # Shrink the rectangle by 150 pixels in both width and height
seaturtle_rect = seaturtle_rect.inflate(-150, -150)
pygame.display.set_caption("Title")
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if not gameactive: #respawn 
            if event.type == pygame.KEYDOWN:
                gameactive = True
                health = 100  # Reset health
                hunger = 100  # Reset hunger
                timer = 2  # Reset timer
                dodaro_spawn = False  # Reset dodaro spawn
                seaturtle_spawn = False  # Reset seaturtle spawn
                gameWin = False
                last_spawn_time = pygame.time.get_ticks()  # Reset spawn time
                last_spawn_time_s = pygame.time.get_ticks()  # Reset spawn time
                hunger_timer = pygame.time.get_ticks()  # Reset hunger timer
                hungerhealth_timer = pygame.time.get_ticks()  # Reset hunger health timer
                timer_update_time = pygame.time.get_ticks()  # Reset timer update

    if gameactive:
        # Spawn seaturtle every 50 seconds
        currentS_time = pygame.time.get_ticks()
        if not seaturtle_spawn and currentS_time - last_spawn_time_s >= 50000: # 50 seconds respawn 
            seaturtle_spawn = True
            seaturtle_rect.y = random.randint(100, 900)
            last_spawn_time_s = currentS_time

        # Generate the random number only if dodaro hasn't spawned yet
        current_time = pygame.time.get_ticks()
        if not dodaro_spawn and current_time - last_spawn_time >= 25000:  # 25 seconds have passed
            dodaro_spawn = True
            dodaro_rect.y = random.randint(100, 900)  # Randomize y-position
            last_spawn_time = current_time  # Update the last spawn time

        # Remove hunger every second
        currentH_time = pygame.time.get_ticks()
        if hunger > 0:
            if currentH_time - hunger_timer >= 15000:
                hunger -= 10
                hunger_timer = currentH_time
        else:
            hunger_timer = currentH_time

        # Health depleting from hunger condition
        currentHS_time = pygame.time.get_ticks()
        if hunger <= 0:
            if currentHS_time - hungerhealth_timer >= 2000:
                health -= 10
                hungerhealth_timer = hunger_timer
        elif hunger >= 100: #Healing condition
            if currentHS_time - hungerhealth_timer >= 1000:
                health = min(health + 10, 100)  # Ensure health doesn't exceed 100
                hungerhealth_timer = currentHS_time

        # Update timer
        current_timer_time = pygame.time.get_ticks()
        if current_timer_time - timer_update_time >= 1000:  # Update every second
            if timer <= 0:
                gameWin = True
                gameactive = False
            else:
                timer -= 1
                timer_update_time = current_timer_time

        # User movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            lifeboat_rect.y -= 15
        if keys[pygame.K_a]:
            lifeboat_rect.x -= 15
        if keys[pygame.K_s]:
            lifeboat_rect.y += 15
        if keys[pygame.K_d]:
            lifeboat_rect.x += 15
    
        # Check for collision between lifeboat and dodaro
        if dodaro_spawn and lifeboat_rect.colliderect(dodaro_rect):
            dodaro_spawn = False
            dodaro_rect.x = 1700
            if hunger < 100:
                hunger += 10
                last_spawn_time = current_time
            else:
                last_spawn_time = current_time

        # Check for seaturtle collision
        if seaturtle_spawn and lifeboat_rect.colliderect(seaturtle_rect):
            seaturtle_spawn = False
            seaturtle_rect.x = 1700
            if hunger < 100:
                hunger += 10
                last_spawn_time_s = currentS_time
            else:
                last_spawn_time_s = currentS_time

        # Draw the background and the lifeboat
        screen.blit(ocean_surface, (0, 0))
        screen.blit(lifeboat_surface, lifeboat_rect)

        # Draw dodaro if it has spawned
        if dodaro_spawn:  # if it is true
            screen.blit(dodaro_surface, dodaro_rect)
            if dodaro_rect.x < 0:
                dodaro_rect.x = 1700
                last_spawn_time = current_time  # Reset timer
                dodaro_spawn = False
            else:
                dodaro_rect.x -= 10

        # Seaturtle spawn condition
        if seaturtle_spawn:
            screen.blit(seaturtle_surface, seaturtle_rect)
            if seaturtle_rect.x < 0:
                seaturtle_rect.x = 1700
                last_spawn_time_s = currentS_time
                seaturtle_spawn = False
            else:
                seaturtle_rect.x -= 10

        # Load HealthBar
        Healthbar(screen, 5, 950, health)
        Hungerbar(screen, 300, 950, hunger)
        screen.blit(Health_display, (20, 950))
        screen.blit(Hunger_display, (330, 950))

        # Display timer
        timer_display = test_font.render(f"Time: {timer}", False, (0, 0, 0))
        timer_display = pygame.transform.rotozoom(timer_display, 0, 1.5)
        screen.blit(timer_display, (900, 100))

        if health <= 0:
            gameactive = False
            first_time = False  # Mark first_time as False when player dies
    
    else:
        if gameWin:
            screen.blit(win_surface, (0, 0))
        elif first_time:
            screen.blit(intro_surface, (0, 0))
        else:
            screen.blit(outro_surface, (0, 0))

    pygame.display.update()
    clock.tick(30)

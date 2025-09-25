"""
main.py - the actual game's logic.
"""

## BEGIN SETUP
import pygame
import sys
import random
# easier access to keys
from pygame.locals import (
    RLEACCEL, # image stuff
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# init pygame
try:
    pygame.mixer.init()
except Exception as e:
    print(f"Error initializing sound: {e}")
pygame.init()

# create a player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        # use image
        try:
            self.surf = pygame.image.load("assets/jet.png").convert()
            self.surf.set_colorkey((255, 255, 255), RLEACCEL)
            self.surf = pygame.transform.smoothscale(self.surf, (50, 50))
        except Exception as e:
            print(f"Warning: Could not load 'assets/jet.png': {e}. Using fallback surface.")
            self.surf = pygame.Surface((50, 50))
            self.surf.fill((0, 255, 0))  # bright green fallback
        self.rect = self.surf.get_rect()

        self.speed = 10
    
    # accept user inputs from the main loop
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -self.speed)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, self.speed)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.speed, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# create a simple enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("assets/missile.jpg").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.surf = pygame.transform.smoothscale(self.surf, (50, 50))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

# example background object
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        try:
            self.surf = pygame.image.load("assets/cloud.jpg").convert()
            self.surf.set_colorkey((0, 0, 0), RLEACCEL)
            self.surf = pygame.transform.smoothscale(self.surf, (50, 50))
        except Exception as e:
            print(f"Error loading cloud image: {e}. Using fallback surface.")
            self.surf = pygame.Surface((50, 50))
            self.surf.fill((200, 200, 200))  # light gray fallback
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    # Move the cloud based on a constant speed
    # Remove the cloud when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()

# Define screen width/height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# init custom events
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 500)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

# init entities
player = Player()
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# clock
clock = pygame.time.Clock()

## END SETUP

# Main loop
def main():
    running = True

    while running:
        # update the display
        pygame.display.update()
        # ensure 60fps
        clock.tick(60)
        # Quitting logic
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False
            # add new enemy
            elif event.type == ADDENEMY:
                # Create the new enemy and add it to sprite groups
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)
            elif event.type == ADDCLOUD:
                # Create the new cloud and add it to sprite groups
                new_cloud = Cloud()
                clouds.add(new_cloud)
                all_sprites.add(new_cloud)

        # check for input
        pressed_keys = pygame.key.get_pressed()

        # update entities
        player.update(pressed_keys)
        enemies.update()
        clouds.update()

        # prevent ghosting by resetting the background
        screen.fill((135, 206, 250))

        # draw everything
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        
        # kill the player
        if pygame.sprite.spritecollideany(player, enemies):
            # If so, then remove the player and stop the loop
            player.kill()
            running = False

        

# Once the loop is broken, cleanup and quit
if __name__ == '__main__':
    main()
    try:
        pygame.mixer.music.stop()
        pygame.mixer.quit()
    except Exception as e:
        print(f"Error shutting down sound: {e}")
    pygame.quit()
    sys.exit()
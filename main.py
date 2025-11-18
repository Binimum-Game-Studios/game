"""
main.py - Dungeon Crawler MVP with turn-based combat and room-based navigation
"""

import pygame
import sys
import random
import json
import os
from enum import Enum

# Initialize pygame
try:
    pygame.mixer.init()
except Exception as e:
    print(f"Error initializing sound: {e}")
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 40
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 50, 50)
GREEN = (50, 200, 50)
BLUE = (50, 50, 200)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
LIGHT_GRAY = (180, 180, 180)
YELLOW = (255, 255, 100)

# Game states
class GameState(Enum):
    MENU = 1
    PLAYING = 2
    BATTLE = 3
    CUTSCENE = 4
    GAME_OVER = 5

# Room types for different dungeon areas
class RoomType(Enum):
    NORMAL = 1
    BATTLE = 2
    SHOP = 3
    BOSS = 4

# Save/Load System
class SaveSystem:
    SAVE_FILE = "game_save.json"
    
    @staticmethod
    def get_default_save():
        return {
            "player_hp": 100,
            "player_max_hp": 100,
            "player_attack": 10,
            "player_x": 400,
            "player_y": 300,
            "current_room": (0, 0),
            "inventory": ["Health Potion", "Health Potion"],
            "gold": 50,
            "progress": 0
        }
    
    @staticmethod
    def save_game(game_state):
        """Save the current game state to file"""
        try:
            with open(SaveSystem.SAVE_FILE, 'w') as f:
                json.dump(game_state, f, indent=2)
            print("Game saved successfully!")
            return True
        except Exception as e:
            print(f"Error saving game: {e}")
            return False
    
    @staticmethod
    def load_game():
        """Load game state from file, or return defaults"""
        if os.path.exists(SaveSystem.SAVE_FILE):
            try:
                with open(SaveSystem.SAVE_FILE, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading save file: {e}. Using defaults.")
        return SaveSystem.get_default_save()

# Player class
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.speed = 5
        self.hp = 100
        self.max_hp = 100
        self.attack = 10
        self.inventory = ["Health Potion", "Health Potion"]
        self.gold = 50
        
        # Try to load player sprite
        try:
            self.image = pygame.image.load("assets/player/textures/player.png")
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        except:
            # Fallback to colored rectangle
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill(BLUE)
    
    def move(self, dx, dy, room):
        """Move player and check collisions with walls"""
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        
        # Check boundaries
        if new_x >= 0 and new_x <= SCREEN_WIDTH - self.width:
            if not room.check_wall_collision(new_x, self.y, self.width, self.height):
                self.x = new_x
        
        if new_y >= 0 and new_y <= SCREEN_HEIGHT - self.height:
            if not room.check_wall_collision(self.x, new_y, self.width, self.height):
                self.y = new_y
    
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
    
    def use_item(self, item_name):
        """Use an item from inventory"""
        if item_name in self.inventory:
            self.inventory.remove(item_name)
            if item_name == "Health Potion":
                heal_amount = 30
                self.hp = min(self.hp + heal_amount, self.max_hp)
                return f"Healed {heal_amount} HP!"
        return "Item not found!"

# Enemy class for battles
class Enemy:
    def __init__(self, name, hp, attack, defense=0):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defense = defense
        self.attack_pattern = ["slash", "charge", "slash"]
        self.turn = 0
        
    def get_next_attack(self):
        """Get the next attack in the predetermined pattern"""
        attack = self.attack_pattern[self.turn % len(self.attack_pattern)]
        self.turn += 1
        return attack
    
    def take_damage(self, damage):
        actual_damage = max(1, damage - self.defense)
        self.hp -= actual_damage
        return actual_damage

# Room class for dungeon navigation
class Room:
    def __init__(self, room_type=RoomType.NORMAL, has_enemies=False):
        self.room_type = room_type
        self.has_enemies = has_enemies
        self.tiles = self.generate_tiles()
        self.doors = {
            'north': (SCREEN_WIDTH // 2 - 20, 0, 40, 20),
            'south': (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT - 20, 40, 20),
            'east': (SCREEN_WIDTH - 20, SCREEN_HEIGHT // 2 - 20, 20, 40),
            'west': (0, SCREEN_HEIGHT // 2 - 20, 20, 40)
        }
        
    def generate_tiles(self):
        """Generate a simple tile map for the room"""
        tiles = []
        # Create walls around the perimeter
        for x in range(0, SCREEN_WIDTH, TILE_SIZE):
            tiles.append(('wall', x, 0))
            tiles.append(('wall', x, SCREEN_HEIGHT - TILE_SIZE))
        for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
            tiles.append(('wall', 0, y))
            tiles.append(('wall', SCREEN_WIDTH - TILE_SIZE, y))
        return tiles
    
    def check_wall_collision(self, x, y, width, height):
        """Check if position collides with walls"""
        player_rect = pygame.Rect(x, y, width, height)
        for tile_type, tx, ty in self.tiles:
            if tile_type == 'wall':
                tile_rect = pygame.Rect(tx, ty, TILE_SIZE, TILE_SIZE)
                if player_rect.colliderect(tile_rect):
                    return True
        return False
    
    def check_door_collision(self, x, y, width, height):
        """Check if player is touching a door"""
        player_rect = pygame.Rect(x, y, width, height)
        for direction, door_rect in self.doors.items():
            if player_rect.colliderect(pygame.Rect(door_rect)):
                return direction
        return None
    
    def draw(self, screen):
        """Draw the room tiles"""
        # Draw floor
        screen.fill(DARK_GRAY)
        
        # Draw walls
        for tile_type, x, y in self.tiles:
            if tile_type == 'wall':
                pygame.draw.rect(screen, GRAY, (x, y, TILE_SIZE, TILE_SIZE))
                pygame.draw.rect(screen, BLACK, (x, y, TILE_SIZE, TILE_SIZE), 2)
        
        # Draw doors
        for direction, (dx, dy, dw, dh) in self.doors.items():
            pygame.draw.rect(screen, GREEN, (dx, dy, dw, dh))

# Battle System
class BattleSystem:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.player_turn = True
        self.battle_log = []
        self.selected_option = 0
        self.options = ["Fight", "Act", "Item", "Mercy"]
        self.in_submenu = False
        self.victory = False
        self.defeat = False
        
    def handle_input(self, keys_pressed):
        """Handle battle input"""
        if self.in_submenu:
            return
            
        if keys_pressed[pygame.K_LEFT]:
            self.selected_option = (self.selected_option - 1) % len(self.options)
        elif keys_pressed[pygame.K_RIGHT]:
            self.selected_option = (self.selected_option + 1) % len(self.options)
        elif keys_pressed[pygame.K_RETURN] or keys_pressed[pygame.K_z]:
            self.execute_action()
    
    def execute_action(self):
        """Execute the selected action"""
        action = self.options[self.selected_option]
        
        if action == "Fight":
            damage = random.randint(self.player.attack - 2, self.player.attack + 5)
            actual_damage = self.enemy.take_damage(damage)
            self.battle_log.append(f"You dealt {actual_damage} damage!")
            if self.enemy.hp <= 0:
                self.victory = True
                self.battle_log.append(f"You defeated {self.enemy.name}!")
            else:
                self.enemy_turn()
        
        elif action == "Act":
            # Check enemy, sometimes offers peaceful solution
            if random.random() < 0.3:
                self.battle_log.append(f"{self.enemy.name} is sparing you!")
                self.victory = True
            else:
                self.battle_log.append(f"You check {self.enemy.name}...")
                self.enemy_turn()
        
        elif action == "Item":
            if self.player.inventory:
                result = self.player.use_item("Health Potion")
                self.battle_log.append(result)
                self.enemy_turn()
            else:
                self.battle_log.append("No items available!")
        
        elif action == "Mercy":
            # Spare the enemy (green option)
            if self.enemy.hp < self.enemy.max_hp * 0.3:
                self.battle_log.append(f"You spared {self.enemy.name}!")
                self.victory = True
            else:
                self.battle_log.append(f"{self.enemy.name} refuses mercy!")
                self.enemy_turn()
    
    def enemy_turn(self):
        """Execute enemy turn"""
        attack_type = self.enemy.get_next_attack()
        damage = random.randint(self.enemy.attack - 2, self.enemy.attack + 3)
        self.player.hp -= damage
        self.battle_log.append(f"{self.enemy.name} attacks with {attack_type}! {damage} damage!")
        
        if self.player.hp <= 0:
            self.defeat = True
            self.battle_log.append("You have been defeated...")
    
    def draw(self, screen):
        """Draw the battle screen"""
        screen.fill(BLACK)
        
        # Draw enemy
        enemy_x = SCREEN_WIDTH // 2 - 50
        enemy_y = 100
        try:
            enemy_img = pygame.Surface((100, 100))
            enemy_img.fill(RED)
        except:
            enemy_img = pygame.Surface((100, 100))
            enemy_img.fill(RED)
        screen.blit(enemy_img, (enemy_x, enemy_y))
        
        # Draw enemy info
        font = pygame.font.Font(None, 36)
        name_text = font.render(self.enemy.name, True, WHITE)
        screen.blit(name_text, (SCREEN_WIDTH // 2 - 80, 50))
        
        # Enemy HP bar
        hp_ratio = self.enemy.hp / self.enemy.max_hp
        pygame.draw.rect(screen, RED, (SCREEN_WIDTH // 2 - 100, 220, 200, 20))
        pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH // 2 - 100, 220, 200 * hp_ratio, 20))
        
        # Draw player info
        player_y = SCREEN_HEIGHT - 150
        player_font = pygame.font.Font(None, 32)
        
        hp_text = player_font.render(f"HP: {self.player.hp}/{self.player.max_hp}", True, WHITE)
        screen.blit(hp_text, (50, player_y))
        
        # Draw options
        option_y = SCREEN_HEIGHT - 100
        for i, option in enumerate(self.options):
            color = YELLOW if i == self.selected_option else WHITE
            if option == "Mercy":
                color = GREEN if i == self.selected_option else (100, 200, 100)
            option_text = player_font.render(option, True, color)
            screen.blit(option_text, (100 + i * 150, option_y))
        
        # Draw battle log
        log_y = 280
        log_font = pygame.font.Font(None, 24)
        for i, log in enumerate(self.battle_log[-3:]):
            log_text = log_font.render(log, True, WHITE)
            screen.blit(log_text, (50, log_y + i * 30))

# Main Menu
class MainMenu:
    def __init__(self):
        self.options = ["Start Game", "Continue", "Settings", "Quit"]
        self.selected = 0
        
    def handle_input(self, keys_pressed):
        if keys_pressed[pygame.K_UP]:
            self.selected = (self.selected - 1) % len(self.options)
        elif keys_pressed[pygame.K_DOWN]:
            self.selected = (self.selected + 1) % len(self.options)
        elif keys_pressed[pygame.K_RETURN]:
            return self.options[self.selected]
        return None
    
    def draw(self, screen):
        screen.fill(BLACK)
        
        # Title
        font_large = pygame.font.Font(None, 74)
        title = font_large.render("DUNGEON CRAWLER", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - 250, 100))
        
        # Options
        font = pygame.font.Font(None, 48)
        for i, option in enumerate(self.options):
            color = YELLOW if i == self.selected else WHITE
            text = font.render(option, True, color)
            screen.blit(text, (SCREEN_WIDTH // 2 - 100, 250 + i * 60))

# Cutscene System
class Cutscene:
    def __init__(self, cutscene_id):
        self.cutscene_id = cutscene_id
        self.events = self.load_cutscene(cutscene_id)
        self.current_event = 0
        self.finished = False
        
    def load_cutscene(self, cutscene_id):
        """Load cutscene events based on ID"""
        cutscenes = {
            "intro": [
                "Welcome to the Dungeon...",
                "You awaken in a dark chamber.",
                "Your quest begins now."
            ],
            "victory": [
                "You have defeated the enemy!",
                "The path forward is clear.",
                "Continue your journey..."
            ]
        }
        return cutscenes.get(cutscene_id, ["..."])
    
    def next_event(self):
        """Move to next cutscene event"""
        self.current_event += 1
        if self.current_event >= len(self.events):
            self.finished = True
    
    def draw(self, screen):
        """Draw the current cutscene"""
        screen.fill(BLACK)
        
        if self.current_event < len(self.events):
            font = pygame.font.Font(None, 36)
            text = font.render(self.events[self.current_event], True, WHITE)
            screen.blit(text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2))
            
            # Prompt
            prompt_font = pygame.font.Font(None, 24)
            prompt = prompt_font.render("Press ENTER to continue", True, GRAY)
            screen.blit(prompt, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100))

# Main Game Class
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Dungeon Crawler MVP")
        self.clock = pygame.time.Clock()
        self.state = GameState.MENU
        
        # Load or create save data
        save_data = SaveSystem.load_game()
        
        # Initialize game objects
        self.player = Player(save_data["player_x"], save_data["player_y"])
        self.player.hp = save_data["player_hp"]
        self.player.max_hp = save_data["player_max_hp"]
        self.player.attack = save_data["player_attack"]
        self.player.inventory = save_data["inventory"]
        self.player.gold = save_data["gold"]
        
        self.current_room_coords = tuple(save_data["current_room"])
        self.rooms = {(0, 0): Room(RoomType.NORMAL, has_enemies=True)}
        self.current_room = self.rooms[self.current_room_coords]
        
        self.menu = MainMenu()
        self.battle_system = None
        self.cutscene = None
        
        self.keys_pressed_last_frame = {}
        
    def handle_input(self):
        """Handle input with key press detection"""
        keys = pygame.key.get_pressed()
        keys_just_pressed = {}
        
        for key in range(len(keys)):
            if keys[key] and not self.keys_pressed_last_frame.get(key, False):
                keys_just_pressed[key] = True
        
        self.keys_pressed_last_frame = {k: keys[k] for k in range(len(keys))}
        
        return keys, keys_just_pressed
    
    def save_game_state(self):
        """Save the current game state"""
        save_data = {
            "player_hp": self.player.hp,
            "player_max_hp": self.player.max_hp,
            "player_attack": self.player.attack,
            "player_x": self.player.x,
            "player_y": self.player.y,
            "current_room": list(self.current_room_coords),
            "inventory": self.player.inventory,
            "gold": self.player.gold,
            "progress": 0
        }
        SaveSystem.save_game(save_data)
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            self.clock.tick(FPS)
            
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.state == GameState.PLAYING:
                            self.save_game_state()
                            self.state = GameState.MENU
                        elif self.state == GameState.MENU:
                            running = False
            
            keys, keys_just_pressed = self.handle_input()
            
            # State machine
            if self.state == GameState.MENU:
                choice = None
                if keys_just_pressed.get(pygame.K_UP) or keys_just_pressed.get(pygame.K_DOWN):
                    self.menu.handle_input(keys_just_pressed)
                elif keys_just_pressed.get(pygame.K_RETURN):
                    choice = self.menu.handle_input(keys_just_pressed)
                
                if choice == "Start Game":
                    self.cutscene = Cutscene("intro")
                    self.state = GameState.CUTSCENE
                elif choice == "Continue":
                    self.state = GameState.PLAYING
                elif choice == "Settings":
                    pass  # Settings not implemented in MVP
                elif choice == "Quit":
                    running = False
                
                self.menu.draw(self.screen)
            
            elif self.state == GameState.CUTSCENE:
                if keys_just_pressed.get(pygame.K_RETURN):
                    self.cutscene.next_event()
                    if self.cutscene.finished:
                        self.state = GameState.PLAYING
                        self.cutscene = None
                
                if self.cutscene:
                    self.cutscene.draw(self.screen)
            
            elif self.state == GameState.PLAYING:
                # Player movement
                dx = dy = 0
                if keys[pygame.K_w] or keys[pygame.K_UP]:
                    dy = -1
                if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                    dy = 1
                if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                    dx = -1
                if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                    dx = 1
                
                self.player.move(dx, dy, self.current_room)
                
                # Check for door transitions
                door_direction = self.current_room.check_door_collision(
                    self.player.x, self.player.y, self.player.width, self.player.height
                )
                
                if door_direction:
                    # Move to new room
                    room_changes = {
                        'north': (0, -1),
                        'south': (0, 1),
                        'east': (1, 0),
                        'west': (-1, 0)
                    }
                    dx, dy = room_changes[door_direction]
                    new_coords = (self.current_room_coords[0] + dx, self.current_room_coords[1] + dy)
                    
                    # Create room if it doesn't exist
                    if new_coords not in self.rooms:
                        has_enemies = random.random() < 0.5
                        self.rooms[new_coords] = Room(RoomType.NORMAL, has_enemies=has_enemies)
                    
                    self.current_room_coords = new_coords
                    self.current_room = self.rooms[new_coords]
                    
                    # Reposition player at opposite door
                    if door_direction == 'north':
                        self.player.y = SCREEN_HEIGHT - 60
                    elif door_direction == 'south':
                        self.player.y = 60
                    elif door_direction == 'east':
                        self.player.x = 60
                    elif door_direction == 'west':
                        self.player.x = SCREEN_WIDTH - 60
                    
                    # Random enemy encounter
                    if self.current_room.has_enemies and random.random() < 0.4:
                        enemy = Enemy("Goblin", 50, 8)
                        self.battle_system = BattleSystem(self.player, enemy)
                        self.state = GameState.BATTLE
                
                # Draw game
                self.current_room.draw(self.screen)
                self.player.draw(self.screen)
                
                # Draw HUD
                font = pygame.font.Font(None, 28)
                hp_text = font.render(f"HP: {self.player.hp}/{self.player.max_hp}", True, WHITE)
                gold_text = font.render(f"Gold: {self.player.gold}", True, YELLOW)
                self.screen.blit(hp_text, (10, 10))
                self.screen.blit(gold_text, (10, 40))
            
            elif self.state == GameState.BATTLE:
                if keys_just_pressed.get(pygame.K_LEFT) or keys_just_pressed.get(pygame.K_RIGHT):
                    self.battle_system.handle_input(keys_just_pressed)
                elif keys_just_pressed.get(pygame.K_RETURN) or keys_just_pressed.get(pygame.K_z):
                    self.battle_system.handle_input(keys_just_pressed)
                
                self.battle_system.draw(self.screen)
                
                # Check battle end conditions
                if self.battle_system.victory:
                    self.player.gold += 20
                    self.state = GameState.PLAYING
                    self.battle_system = None
                elif self.battle_system.defeat:
                    self.state = GameState.GAME_OVER
            
            elif self.state == GameState.GAME_OVER:
                self.screen.fill(BLACK)
                font = pygame.font.Font(None, 74)
                text = font.render("GAME OVER", True, RED)
                self.screen.blit(text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2))
                
                font_small = pygame.font.Font(None, 36)
                restart_text = font_small.render("Press ESC to return to menu", True, WHITE)
                self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 80))
            
            pygame.display.flip()
        
        # Cleanup
        try:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        except Exception as e:
            print(f"Error shutting down sound: {e}")
        pygame.quit()
        sys.exit()

# Run the game
if __name__ == '__main__':
    game = Game()
    game.run()
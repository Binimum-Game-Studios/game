# Copilot Instructions for 'Game' - Dungeon Crawler Project

## Project Overview

**Game Name:** Game

**Description:** A dungeon crawler game built with PyGame, incorporating puzzle elements inspired by "Baba is You", roguelike/lite mechanics, and turn-based combat.

**Target Duration:** 15-20 minutes for initial vertical slice (including cutscenes)

**Expansion Goals:** If time permits, expand with more bosses, detailed story, and extended gameplay.

## Tech Stack

- **Primary Language:** Python
- **Game Framework:** PyGame

## Core Game Elements

### 1. Combat System
- **Turn-based battles** with the following flow:
  - Player's turn: Fight, Act, Item, or Mercy options
  - Enemy turn with predetermined attack patterns
  - Battle continues until player wins or is defeated
  - Green options available for non-combat resolution
  - Stats update after each action

### 2. Room & Dungeon System
- **Room-based navigation** with coordinate system
- Load room subroutines when player enters a room
- Display tiles from room's coordinate system in a loop
- Render player at starting position within each room
- Door interaction triggers room transitions
- Generate random enemy encounters in applicable rooms

### 3. Game Flow (Based on Flowchart)

#### Main Menu (H2 responsibility)
- Start game
- Settings display
- Load/save system with default values

#### Save System
- Check for existing save file
- Create save file with default values if none exists
- Load save data at game start
- Store player position, stats, inventory, and progress

#### Input/Output System (H1+H3 responsibility - runs every frame)
- **Input:** Capture pressed keys each frame
- **Directional keys:** Move player in specified direction (pwu/wasd)
- **Interaction key (y):** Start interaction with objects/NPCs
- **Door interaction:** Check if door is touched, generate random enemy encounter if room has enemies enabled

#### Cutscene System (H2 responsibility)
- Cutscene subroutine with Cutscene ID argument
- Reset player position (using case/switch logic)
- Ignore player update and camera movement during cutscenes
- Play next event in cutscene sequence (for loop)

#### Battle System (H3 responsibility)
- In-Battle subroutine with Enemy ID argument
- Get battle variables (player stats, enemy HP, available items)
- Player turn options: Fight, Act, Item, Mercy
- Enemy turn with special player controls and predetermined attack patterns
- Check win/loss conditions
- End battle and update permanent player stats if needed

### 4. Additional Features
- **NPCs:** Interactive non-player characters
- **Quests:** Quest system for progression
- **Shops:** Item purchasing and inventory management
- **Puzzles:** "Baba is You"-style puzzle mechanics integrated into dungeon rooms

### 5. Roguelike/lite Elements (To Be Explored)
- Procedural generation considerations
- Permadeath or run-based progression
- Random loot and enemy encounters
- Meta-progression systems

## Current Code Structure

The repository currently contains:
- `main.py` - Basic PyGame setup with sprite system (player, enemies, clouds)
- `assets/` - Directory for game assets (images, sounds, etc.)
- Basic collision detection and movement system

## Development Guidelines

### Branching Strategy
- Create individual feature branches
- Work on personal branches
- Use the [project kanban board](https://github.com/orgs/Binimum-Game-Studios/projects/1/views/1)
- Create pull requests when changes are complete

### Code Organization Responsibilities
Based on the flowchart annotations:
- **H1:** Room loading subroutines, input/output system (every frame)
- **H2:** Main menu, save system, cutscene system
- **H3:** Battle system with enemy interactions, input/output integration

### Coding Standards
- Follow existing PyGame patterns in `main.py`
- Use sprite classes for game entities
- Implement proper error handling (as shown with image loading fallbacks)
- Comment code sections clearly
- Maintain 60 FPS target performance

## Key Implementation Tasks

1. **Replace placeholder game logic** in `main.py` with dungeon crawler mechanics
2. **Implement room system** with coordinate-based tile rendering
3. **Create battle system** with turn-based combat
4. **Develop cutscene engine** for story sequences
5. **Build save/load system** for game state persistence
6. **Design puzzle mechanics** inspired by "Baba is You"
7. **Add NPC interaction system**
8. **Implement shop and inventory management**
9. **Create quest tracking system**

## Asset Requirements

Store all game assets in the `assets/` directory:
- Character sprites
- Enemy sprites
- Tile sets for dungeon rooms
- UI elements
- Sound effects and music
- Cutscene assets

## Testing & Iteration

- Playtest the 15-20 minute vertical slice thoroughly
- Balance combat difficulty for turn-based system
- Ensure puzzle difficulty is appropriate
- Verify save/load functionality works correctly
- Test all interaction systems (doors, NPCs, items)

## Future Expansion Ideas

- Additional bosses with unique mechanics
- Expanded story with more cutscenes
- More complex puzzle rooms
- Enhanced roguelike elements
- Additional items and equipment
- More diverse enemy types
- Extended dungeon areas

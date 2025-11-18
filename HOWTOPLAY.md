# Dungeon Crawler MVP - How to Play

## Installation

1. Install Python 3.8 or higher
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Game

```bash
python main.py
```

## Controls

### Main Menu
- **Arrow Keys (Up/Down)**: Navigate menu options
- **Enter**: Select menu option
- **ESC**: Quit game or return to menu

### Playing
- **WASD** or **Arrow Keys**: Move player
- **Y**: Interact with objects/NPCs (when implemented)
- **ESC**: Save and return to main menu

### Battle
- **Left/Right Arrow Keys**: Select action
- **Enter** or **Z**: Confirm action
- **Actions**:
  - **Fight**: Attack the enemy
  - **Act**: Check enemy or attempt peaceful solution
  - **Item**: Use items from inventory (Health Potions)
  - **Mercy**: Spare the enemy (green option - works when enemy is weak)

## Game Features

### Main Menu
- **Start Game**: Begin a new game with intro cutscene
- **Continue**: Load saved game and resume
- **Settings**: Placeholder for future features
- **Quit**: Exit the game

### Exploration
- Navigate through dungeon rooms
- Walk through doors to discover new areas
- Watch for random enemy encounters
- Collect gold from defeated enemies

### Combat System
Turn-based battles with:
- Player HP tracking
- Enemy HP bar
- Four action types
- Predetermined enemy attack patterns
- Victory rewards (gold)

### Save System
- Auto-saves when returning to menu (ESC key)
- Saves player stats, position, inventory, and progress
- Automatic save file creation with defaults

### Cutscenes
- Story sequences at key moments
- Press Enter to advance dialogue

## Fallback Graphics

The game uses colored rectangles as fallback graphics when asset files are missing:
- **Player**: Blue rectangle
- **Enemies**: Red rectangle  
- **Walls**: Gray rectangles
- **Doors**: Green rectangles
- **Floor**: Dark gray background

## Tips

1. Use **Health Potions** wisely - they heal 30 HP
2. **Mercy** option becomes more effective when enemies are weak
3. **Act** has a small chance of peaceful resolution
4. Explore multiple rooms to find encounters and gain gold
5. Return to menu frequently to save your progress

## Technical Details

- Built with **pygame-ce** (Community Edition)
- 60 FPS target
- 800x600 resolution
- JSON-based save system
- Room-based coordinate system for dungeon navigation

## Future Enhancements

- More enemy types with unique abilities
- Shop system for buying items
- Quest system
- Boss battles
- Puzzle mechanics inspired by "Baba is You"
- Extended story with more cutscenes
- Sound effects and music
- More detailed graphics

Enjoy your adventure!

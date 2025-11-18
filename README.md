# Dungeon Crawler - BINIMUM GAME

A dungeon crawler game built with PyGame-CE, incorporating turn-based combat, room-based navigation, and roguelike elements.

[kanban](https://github.com/orgs/Binimum-Game-Studios/projects/1/views/1)

## Quick Start

### Installation
```bash
pip install -r requirements.txt
```

### Run the Game
```bash
python main.py
```

## Features

### ✅ MVP Complete
- **Main Menu**: Start, Continue, Settings, Quit
- **Room-Based Navigation**: Explore dungeon rooms with wall collision
- **Turn-Based Combat**: Fight, Act, Item, Mercy actions
- **Save/Load System**: JSON-based game state persistence
- **Cutscene System**: Story sequences
- **Fallback Graphics**: Works without asset files

### 🎮 Gameplay
- Navigate rooms using WASD or Arrow keys
- Enter doors to discover new areas
- Random enemy encounters
- Collect gold from victories
- Use Health Potions to survive

### ⚔️ Combat
- **Fight**: Attack enemies
- **Act**: Check enemy or find peaceful solutions
- **Item**: Use inventory items
- **Mercy**: Spare weak enemies (green option)

## Controls

**Menu**: Arrow Keys + Enter  
**Movement**: WASD or Arrow Keys  
**Battle**: Left/Right + Enter/Z  
**Save & Exit**: ESC (during gameplay)

## Documentation

See [HOWTOPLAY.md](HOWTOPLAY.md) for detailed instructions.

## Development

Can we please all:
- Create our own branch
- Work on that branch
- When a change is done, use the [kanban](https://github.com/orgs/Binimum-Game-Studios/projects/1/views/1) and create a PR

Many thanks

## Architecture

See [Flowchart.png](Flowchart.png) for game flow architecture.

## Tech Stack
- Python 3.8+
- pygame-ce (Community Edition)

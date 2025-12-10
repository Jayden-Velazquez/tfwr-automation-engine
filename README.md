# tfr-automation-engine

A structured automation engine for organizing movement logic, crop behavior, and harvesting cycles in *The Farmer Was Replaced*.  
This repository keeps all gameplay scripts clean, modular, and version-controlled, while allowing individual functions or modules to be copied into the game’s script folder as needed.

---

## Overview

This project provides:

- A standardized layout for all in-game automation code  
- A movement module for toroidal routing and position handling  
- Crop-specific harvesting logic, including complex behaviors (pumpkins, sunflowers, trees)  
- A plot-planning system that evenly divides the world into crop regions  
- Math and helper utilities for routing and coordinate operations  
- Small test files for validating movement and fast-travel behavior  

The goal is maintainability, clarity, and the ability to evolve these systems as the game or strategies change.

---

## Project Structure

```
tfr-automation-engine/
│
├── src/
│   Core automation code used in-game.
│
├── tests/
│   Simple scripts for validating movement and routing.
│
└── docs/
    Reserved for future notes or explanations.
```

### src/ directory (summary of modules)

- **harvest.py**  
  Main harvesting loop and crop logic for all supported entities.

- **dm.py**  
  Movement engine: routing, toroidal travel, coordinate stepping.

- **pumpkin.py**  
  Pumpkin-specific rules, including border logic and growth tracking.

- **watering.py**  
  Watering and hydration utilities (as applicable).

- **constants.py**  
  Shared constants, entity types, and configuration values.

- **math_utils.py**  
  Helper functions for distances, scaling, routing, and coordinate math.

- **main.py**  
  Optional orchestration entry point.

---

## Design Goals

- Keep all game automation code in one structured place  
- Allow scripts to be copied selectively into the game’s save-folder  
- Maintain readable and modular systems  
- Support complex crop behaviors without cluttering the codebase  
- Provide an easy foundation to build new automation logic  

The repository is not intended to run as a standalone Python package.

---

## License

This project uses the MIT License.  
See `LICENSE` for full terms.

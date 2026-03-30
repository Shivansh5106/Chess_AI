
# ♟️ Python Chess with Stockfish AI

A fully functional, interactive chess application built from scratch using Python and Pygame. This project features complete standard chess logic, smooth animations, tournament timers, and a fully integrated Stockfish AI that scales from absolute beginner to Grandmaster.

## ✨ Features

* **Complete Chess Rules:** Fully compliant with all standard chess mechanics, including Castling, En Passant, Pawn Promotion, and Insufficient Material draws.
* **Dual Game Modes:** Play locally against a friend (PvP) or challenge the computer (PvAI).
* **Dynamic AI Difficulty:** Powered by the Stockfish engine with three distinct levels:
  * **Easy:** Simulates a beginner player (makes random blunders and takes time to "think").
  * **Medium:** Solid club-level player.
  * **Hard:** Grandmaster-level calculation.
* **Tournament Timers:** Choose between 1-minute, 5-minute, or 10-minute time controls. The game automatically tracks timeouts.
* **Polished UI/UX:** Features smooth piece-sliding animations, valid move highlighting, and Check/Checkmate overlays.
* **Quality of Life:** Press `Z` to undo moves and `R` to return to the main menu at any time.

## 🛠️ Prerequisites

To run this game on your machine, you will need:
* Python 3.x
* Pygame
* Python-Chess
* Stockfish Engine

## 🚀 Installation & Setup

**1. Clone the repository**
```bash
git clone [https://github.com/Shivansh5106/python-chess-ai.git](https://github.com/Shivansh5106/python-chess-ai.git)
cd python-chess-ai
```

**2. Install the required Python libraries**
```bash
pip install pygame chess
```

**3. Install Stockfish**
You must have the Stockfish engine installed on your system. 
* **Mac (via Homebrew):** `brew install stockfish`
* **Windows/Linux:** Download the executable directly from the [Stockfish website](https://stockfishchess.org/download/).

**4. Update the Engine Path**
Open `aibot.py` and ensure the file path points to your local Stockfish installation. 
*(Note: The default path in this repository is set for Mac Homebrew: `/opt/homebrew/bin/stockfish`)*.

**5. Launch the game**
```bash
python ChessMain.py
```

## 🎮 Controls
* **Left Click:** Select and move pieces.
* **Z:** Undo your last move.
* **R:** Forfeit the current game and return to the Main Menu.

## 📁 Project Structure
* `ChessMain.py`: Handles the Pygame window, UI rendering, event loops, and animations.
* `ChessEngine.py`: The brain of the game. Validates legal moves, generates FEN strings, and tracks board states (Checks, Castling rights, En Passant).
* `aibot.py`: Manages the connection to the Stockfish engine and restricts its depth/skill level based on the selected difficulty.
* `/images`: Contains the high-resolution piece sprites.

---
*Created by [Shivansh5106](https://github.com/Shivansh5106)*

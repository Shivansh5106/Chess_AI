# ♟️ Python Chess with Stockfish AI

A fully functional, interactive chess application built from scratch using Python and Pygame. This project combines strict standard chess rules, a graphical interface, and the world-class Stockfish engine to create a dynamic playing experience that scales from absolute beginner to Grandmaster.

---

## 🚀 Features

* ♟️ **Complete Chess Rules:** Fully compliant with Castling, En Passant, Pawn Promotion, and Insufficient Material draws.
* 🤖 **Dynamic AI Difficulty:** Three distinct levels (Easy, Medium, Hard) that actually change how the bot thinks and blunders.
* 🎮 **Dual Game Modes:** Play Player vs. Player (PvP) locally, or challenge the AI (PvAI).
* ⏱️ **Tournament Timers:** Built-in clocks for 1-minute, 5-minute, or 10-minute games with automatic time-outs.
* 🔄 **Quality of Life:** Press `Z` to undo moves, reset the board instantly, and view move history.
* ✨ **Polished UI:** Smooth piece-sliding animations, valid move highlighting, and Check/Checkmate overlays.

---

## 🛠️ Tech Stack

* **Python 3**
* **Pygame** (Graphics and UI)
* **python-chess** (Move generation and validation)
* **Stockfish** (External AI engine)

---

## 📂 Project Structure

```text
python-chess-ai/
│
├── ChessMain.py        # Main Pygame loop, UI rendering, and animations
├── ChessEngine.py      # Core game logic, FEN generation, and board states
├── aibot.py            # AI integration and difficulty scaling
├── images/             # High-resolution chess piece sprites
├── .gitignore          # Hidden files and cache exclusion
└── README.md           # Project documentation
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone [https://github.com/Shivansh5106/python-chess-ai.git](https://github.com/Shivansh5106/python-chess-ai.git)
cd python-chess-ai
```

### 2. Install dependencies
```bash
pip install pygame chess
```

### 3. Install the Stockfish Engine
You must have the Stockfish engine installed on your local machine for the AI to work.
* **Mac (via Homebrew):** `brew install stockfish`
* **Windows/Linux:** Download the executable directly from the [Stockfish website](https://stockfishchess.org/download/).

### 4. Update the Engine Path
Open `aibot.py` and ensure the file path on line 5 points to your local Stockfish installation. *(Note: The default path in this repository is set for Mac Homebrew: `/opt/homebrew/bin/stockfish`)*.

---

## ▶️ Run the Game

```bash
python ChessMain.py
```

---

## 🎮 Controls

* **Left Click:** Select a piece / Drop a piece
* **Z:** Undo your last move
* **R:** Forfeit the current game and return to the Main Menu

---

## 📌 Author

**Shivansh**
GitHub: https://github.com/Shivansh5106

---

⭐ If you like this project or found it helpful, consider giving it a star!

# 🧠 Memory Puzzle Game

*Test Your Memory, Discover Fun!*

---

## 🎮 Project Overview

**Memory Puzzle Game** is an interactive, customizable card-matching puzzle game developed using **Python** and **Pygame**. Designed to enhance memory, concentration, and strategic thinking, the game combines classic card-matching mechanics with rich customization options, multiple game modes, sound effects, and a persistent high-score tracking system powered by **SQLite**.

This project was developed as a Computer Engineering 2nd Year Engineering Project at **Beykoz University**.

---

## ✨ Features

* 🎨 **6 UI Color Themes:** Personalize the interface look with *Default, Pink, Blue, Nature, Night,* and *Retro* themes.
* 🃏 **6 Card Themes:** Enjoy diverse visual sets including *Weather, Magic, Space, Animal, Law,* and *Halloween*.
* 📊 **3 Difficulty Levels:** Challenge yourself across different grid sizes:
  * **Easy:** $2 \times 2$ grid
  * **Medium:** $4 \times 4$ grid
  * **Hard:** $6 \times 6$ grid
* ⚔️ **Multiple Game Modes:**
  * **Normal Mode:** Classic relaxed card matching.
  * **Penalty Mode:** Strategic high-stakes mode where wrong matches deduct points—if your score drops below $0$, you lose!
* 🏆 **Leaderboard & Stat Tracker:** Tracks player usernames, scores, completion times, and total moves in a local SQLite database (`scores.db`), filterable by difficulty.
* 💡 **In-Game Hint System:** Need a quick boost? Use the built-in **Hint** feature during gameplay.
* 🔊 **Audio & Volume Controls:** Fun sound effects and background audio with a dedicated in-game volume slider and mute toggle.

---

## 🕹️ How to Play

1. **Enter Username:** Start the game and type in your player username to track your records.
2. **Customize Your Game:**
   * Choose your preferred **UI Color Theme** from the settings.
   * Select a **Card Theme** (e.g., Animals, Space, Magic).
   * Pick a **Difficulty Level** (Easy, Medium, or Hard).
   * Choose between **Normal** or **Penalty** game mode.
3. **Flip & Match:** Click on any two face-down cards to reveal them.
4. **Clear the Board:** If the cards match, they stay revealed and you earn points. If they do not match, they flip back over—remember their positions!
5. **Win the Game:** Match all pairs on the board to win and see your ranking on the **High Scores** leaderboard.

---

## 🎯 Game Objectives

* Match all pairs of hidden cards in the **shortest time** and with the **fewest moves** possible.
* Keep your score above $0$ in **Penalty Mode** to avoid a Game Over.
* Climb to the top of the **High Scores** table across all difficulty levels.

---

## 🛠️ Technologies Used

* **Python 3.x** – Core programming language
* **Pygame** – 2D game engine, graphics rendering, event handling, and audio management
* **SQLite3** – Lightweight relational database (`scores.db`) for storing player high scores and statistics

---

## 📦 Installation

Follow these steps to set up the project locally on your machine:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ylmzrem/Memory-Puzzle-Game.git
   cd Memory-Puzzle-Game
   ```

2. **(Optional) Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install the required dependencies:**
   ```bash
   pip install pygame
   ```

---

## 🚀 Getting Started

Once Pygame is installed, run the main Python script from the root project directory:

```bash
python game.py
```

---

## 🎮 Controls

| Action | Control |
| :--- | :--- |
| **Flip Cards / Navigate Menus** | `Left Mouse Click` |
| **Enter Username** | `Keyboard Typing` |
| **Use Hint** | Click the `HINT` button (bottom-left during gameplay) |
| **Pause / Resume / Volume** | Click the `Pause (II)` or `Audio` icons (top-right during gameplay) |

---

## 📁 Project Structure

```text
game/
├── assets/          # Game images, card icons, and sound effects
├── fonts/           # Custom typography files used in the UI
├── game.py          # Main game loop, UI screens, and game logic
├── scores.db        # SQLite database storing player high scores
├── .gitignore       # Specifies files/folders excluded from Git
└── README.md        # Project documentation
```

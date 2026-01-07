# Slot Machine Game

A fun and interactive slot machine game built with Python and Streamlit.  Test your luck and try to hit the jackpot!

## Features

- **Interactive Web Interface**: Beautiful UI built with Streamlit
- **Realistic Slot Animation**: Three-reel slot machine with acceleration and deceleration effects
- **Persistent Game State**: Your progress is automatically saved between sessions
- **Dynamic Betting**:  Bet any amount within your coin balance
- **Multiple Win Conditions**:
  - 🎉 **Jackpot**: Match all 3 symbols (10x multiplier)
  - ✨ **Partial Win**: Match 2 symbols (2x multiplier)
- **High Score Tracking**: Keep track of your best coin balance
- **Game Over Detection**: Automatic game over when you run out of coins

## Symbols

The game features 6 different symbols:
- 🍒 Cherry
- 🍋 Lemon
- 🔔 Bell
- 💎 Diamond
- 7️⃣ Lucky Seven
- 🍀 Clover

## Getting Started

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/rohitraj22/slot-machine.git
cd slot-machine
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

### Running the Game

Start the Streamlit application:
```bash
streamlit run app.py
```

The game will open in your default web browser at `http://localhost:8501`

**Alternative:**
 - Direct Link - https://slot-machine-game.streamlit.app/

## How to Play

1. **Starting Balance**: You begin with 100 coins
2. **Place Your Bet**: Enter the amount you want to bet (must be between 1 and your current balance)
3. **Spin the Reels**: Click the "Spin!" button to start the slot machine
4. **Watch the Animation**: The reels will spin with realistic acceleration and deceleration
5. **Check Your Winnings**:
   - All 3 symbols match → Win 10x your bet
   - 2 symbols match → Win 2x your bet
   - No match → Lose your bet
6. **Stop Anytime**: Click "Stop Playing" to end your game session and see your final score

## Project Structure

```
slot-machine/
├── app.py              # Main Streamlit application with UI and game loop
├── game_logic.py       # Core game logic and win calculations
├── requirements.txt    # Python dependencies
├── game_state.joblib   # Saved game state (auto-generated)
└── README.md          # Project documentation
```

## Technical Details

### Core Components

- **app.py**: 
  - Handles the Streamlit UI and user interactions
  - Manages game state persistence using joblib
  - Implements realistic reel animation with three phases (acceleration, blur, deceleration)
  - Manages the game flow and session state

- **game_logic. py**:
  - Contains the core game mechanics
  - Handles bet validation and win calculations
  - Generates random symbol combinations

### Game State Management

The game automatically saves your progress using joblib serialization. Your coin balance, high score, and game status persist between sessions.

## Animation Details

The slot machine features a sophisticated animation system: 
- **Acceleration Phase**: Reels gradually speed up
- **Blur Phase**: Reels spin at maximum speed
- **Deceleration Phase**: Reels gradually slow down
- **Sequential Stop**: Reels stop one at a time for dramatic effect

## Game Statistics

- Starting coins: 100
- Minimum bet: 1 coin
- Maximum bet: Current balance
- Jackpot multiplier: 10x
- Partial win multiplier: 2x

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## Author

**rohitraj22**
- GitHub: [@rohitraj22](https://github.com/rohitraj22)

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Game state persistence powered by [joblib](https://joblib.readthedocs.io/)

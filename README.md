# Games

A simple Python project for playing games with a GUI and game logic separation.

## Features

- Modular codebase with separate game logic and GUI
- Easy to extend with new games
- Unit tests for core logic

## Project Structure

```
Games/
│
├── src/
│   ├── game_logic.py      # Core game logic
│   ├── gui.py             # GUI implementation
│   └── __pycache__/       # Python cache files
│
├── tests/
│   └── test_game_logic.py # Unit tests for game logic
│
├── Pipfile                # Project dependencies
├── Pipfile.lock           # Locked dependencies
```

## Requirements

- Python 3.12 or newer
- [pipenv](https://pipenv.pypa.io/en/latest/)

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/NahomAl/Games.git
   cd Games
   ```
2. **Install dependencies using pipenv:**
   ```bash
   pipenv install
   ```

## Running the Application

1. **Activate the pipenv shell:**
   ```bash
   pipenv shell
   ```
2. **Run the GUI:**
   ```bash
   python src/gui.py
   ```

## Running Tests

To run the unit tests:

```bash
pipenv run python -m unittest discover -s tests
```

## Adding New Games

- Add your game logic to `src/game_logic.py` or create a new file in `src/`.
- Update `src/gui.py` to integrate your new game.
- Add tests in `tests/` as needed.

## License

This project is licensed under the MIT License.

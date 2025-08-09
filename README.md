# 🎮 Games

```
   _____
  / ____|
 | |  __  __ _ _ __ ___   ___
 | | |_ |/ _` | '_ ` _ \ / _ \
 | |__| | (_| | | | | | |  __/
  \_____|\__,_|_| |_| |_|\___|

```

> **A fun Python project for playing and building games!**

![Python](https://img.shields.io/badge/python-3.12%2B-blue?logo=python)
![Pipenv](https://img.shields.io/badge/pipenv-ready-brightgreen)
![License](https://img.shields.io/badge/license-MIT-yellow)

---

## ✨ Features

- 🧩 **Modular**: Separate game logic and GUI
- 🚀 **Extensible**: Add your own games easily!
- 🧪 **Tested**: Unit tests for core logic
- 🎨 **Fun**: Designed to be playful and easy to hack on!

---

## 🗂️ Project Structure

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

---

## 🛠️ Requirements

- Python 3.12 or newer
- [pipenv](https://pipenv.pypa.io/en/latest/)

---

## ⚡ Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/NahomAl/Games.git
   cd Games
   ```
2. **Install dependencies:**
   ```bash
   pipenv install
   ```

---

## 🕹️ How to Play

1. **Activate pipenv shell:**
   ```bash
   pipenv shell
   ```
2. **Run the GUI:**
   ```bash
   python src/gui.py
   ```

---

## 🧪 Run Tests

```bash
pipenv run python -m unittest discover -s tests
```

---

## ➕ Add Your Own Game!

- Add your logic to `src/game_logic.py` or a new file in `src/`.
- Update `src/gui.py` to connect your game.
- Add tests in `tests/`.

---

## 🎲 Available Games

- **Tic-Tac-Toe**: Classic 2-player or vs AI mode. Try to get three in a row—horizontally, vertically, or diagonally! ❌⭕
- **Snake**: Guide the snake, eat food, and avoid walls and yourself. Choose your difficulty: Easy, Medium, or Hard! 🐍

---

## 💡 Tips & Ideas

- Use emojis in your game messages for extra fun! 😄
- Share your creations with friends or on GitHub!
- PRs welcome—let's make this the most fun repo ever!

---

## 📄 License

MIT License

---

> Made with ❤️ by [NahomAl](https://github.com/NahomAl)

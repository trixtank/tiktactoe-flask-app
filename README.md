# Tik-Tac-Toe Flask Project

This project contains two distinct web-based Tic-Tac-Toe games built with Python and Flask.

1.  **Human vs. Human:** A classic two-player game where players take turns on the same screen.
2.  **Human vs. Bot:** A single-player game where you can test your skills against an AI bot with varying difficulty levels.

## Features

- **Two Game Modes:** Choose between playing against another person or a computer opponent.
- **Interactive Web Interface:** Clean, modern UI built with vanilla HTML, CSS, and JavaScript, served by a Flask backend.
- **Adjustable Bot Difficulty:** The Human vs. Bot game features three AI levels:
    - **🟢 Easy:** A mostly random and unpredictable bot.
    - **🟡 Medium:** A bot that uses a solid, rule-based strategy.
    - **🔴 Hard:** An unbeatable bot that uses the Minimax algorithm.
- **Player Symbol Selection:** In the bot game, choose to play as 'X' (first move) or 'O' (second move).
- **Logging:** The bot application logs server events and errors to `log.txt` for easier debugging.

---

## Project Structure

The project is organized into two main applications:

```
tiktactoe_project/
├── app.py                  # --- Runs the Human vs. Human game
├── app_bot.py              # --- Runs the Human vs. Bot game
├── templates/
│   └── index.html          # (This is generated automatically by the scripts)
├── log.txt                 # Logs events from app_bot.py
├── logic.txt               # Explains the AI logic for the bot
├── api_docs.md             # Basic API documentation for the bot game
└── README.md               # This file
```

- **`app.py`**: Contains the Flask application and game logic for the **Human vs. Human** version.
- **`app_bot.py`**: Contains the Flask application and game logic for the **Human vs. Bot** version, including all difficulty implementations.

---

## Getting Started

### Prerequisites

- Python 3.x
- Flask

### Installation

1.  **Clone the repository or download the project files.**

2.  **Create and activate a virtual environment** (recommended):
    ```shell
    # Create the virtual environment
    python -m venv venv

    # Activate it
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install the required package:**
    ```shell
    pip install Flask
    ```

---

## How to Run

You can run either of the two games. They run on different ports, so you could even run them at the same time.

### Game 1: Human vs. Human

This is a classic two-player game.

1.  Run the `app.py` script from your terminal:
    ```shell
    python app.py
    ```
2.  Open your web browser and navigate to **`http://localhost:5000`**.

### Game 2: Human vs. Bot

This is the single-player game against the AI.

1.  Run the `app_bot.py` script from your terminal:
    ```shell
    python app_bot.py
    ```
2.  Open your web browser and navigate to **`http://localhost:5001`**.
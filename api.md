# TikTacToe Flask API Documentation

## Overview
This API provides endpoints for a TikTacToe game built with Flask. The game supports two players (X and O) taking turns on a 3x3 grid.

## Base URL
```
http://localhost:5000
```

## Game State Object
All API responses include a `game_state` object with the following structure:

```json
{
  "board": ["", "", "", "", "", "", "", "", ""],
  "current_player": "X",
  "game_active": true,
  "winner": null
}
```

### Game State Properties
- `board`: Array of 9 strings representing the 3x3 grid (indices 0-8)
  - Empty string `""` = empty cell
  - `"X"` = cell occupied by player X
  - `"O"` = cell occupied by player O
- `current_player`: String indicating whose turn it is (`"X"` or `"O"`)
- `game_active`: Boolean indicating if the game is still in progress
- `winner`: String indicating the winner (`"X"`, `"O"`, `"Tie"`, or `null`)

## Endpoints

### 1. Get Game Page
**GET** `/`

Returns the main game HTML page.

**Response:**
- **Content-Type:** `text/html`
- **Status:** 200 OK
- **Body:** HTML page with the TikTacToe game interface

---

### 2. Make a Move
**POST** `/make_move`

Attempts to make a move for the current player at the specified position.

**Request Body:**
```json
{
  "position": 0
}
```

**Parameters:**
- `position` (integer, required): Board position (0-8) where to place the move
  - Positions are numbered 0-8 from left to right, top to bottom:
    ```
    0 | 1 | 2
    ---------
    3 | 4 | 5
    ---------
    6 | 7 | 8
    ```

**Response (Success):**
```json
{
  "success": true,
  "game_state": {
    "board": ["X", "", "", "", "", "", "", "", ""],
    "current_player": "O",
    "game_active": true,
    "winner": null
  }
}
```

**Response (Invalid Move):**
```json
{
  "success": false,
  "message": "Invalid move"
}
```

**Status Codes:**
- 200 OK: Move processed (check `success` field)

**Error Conditions:**
- Position already occupied
- Game is not active (already finished)
- Invalid position (not 0-8)

---

### 3. Reset Game
**POST** `/reset_game`

Resets the game to its initial state.

**Request Body:**
```json
{}
```

**Response:**
```json
{
  "success": true,
  "game_state": {
    "board": ["", "", "", "", "", "", "", "", ""],
    "current_player": "X",
    "game_active": true,
    "winner": null
  }
}
```

**Status Codes:**
- 200 OK: Game successfully reset

---

### 4. Get Game State
**GET** `/get_game_state`

Retrieves the current state of the game without making any changes.

**Response:**
```json
{
  "board": ["X", "O", "", "", "X", "", "", "", ""],
  "current_player": "O",
  "game_active": true,
  "winner": null
}
```

**Status Codes:**
- 200 OK: Current game state returned

---

## Game Rules

### Winning Conditions
A player wins by getting three of their marks in a row:
- **Rows:** [0,1,2], [3,4,5], [6,7,8]
- **Columns:** [0,3,6], [1,4,7], [2,5,8]
- **Diagonals:** [0,4,8], [2,4,6]

### Tie Condition
The game ends in a tie when all 9 positions are filled and no player has won.

### Turn System
- Player X always goes first
- Players alternate turns after each valid move
- Game becomes inactive once a winner is determined or a tie occurs

## Example Usage

### Starting a New Game
```bash
curl -X POST http://localhost:5000/reset_game \
  -H "Content-Type: application/json" \
  -d '{}'
```

### Making a Move
```bash
curl -X POST http://localhost:5000/make_move \
  -H "Content-Type: application/json" \
  -d '{"position": 4}'
```

### Checking Game State
```bash
curl http://localhost:5000/get_game_state
```

## JavaScript Integration

The API is designed to work seamlessly with JavaScript fetch requests:

```javascript
// Make a move
async function makeMove(position) {
  const response = await fetch('/make_move', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ position: position })
  });
  const data = await response.json();
  return data;
}

// Reset game
async function resetGame() {
  const response = await fetch('/reset_game', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' }
  });
  const data = await response.json();
  return data;
}

// Get current state
async function getGameState() {
  const response = await fetch('/get_game_state');
  const data = await response.json();
  return data;
}
```

## Error Handling

The API uses standard HTTP status codes and includes error messages in the response body:

- **200 OK**: Request successful
- **400 Bad Request**: Invalid request format
- **500 Internal Server Error**: Server error

For `/make_move` endpoint, always check the `success` field in the response to determine if the move was valid.

## Development Notes

- The game state is stored in memory and will reset when the server restarts
- The server runs in debug mode by default
- CORS is not configured, so cross-origin requests may be blocked
- No authentication or session management is implemented
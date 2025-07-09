from flask import Flask, render_template, request, jsonify, session
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a random string


class TikTacToe:
    def __init__(self):
        self.board = ['' for _ in range(9)]
        self.current_player = 'X'
        self.game_active = True
        self.winner = None

    def reset_game(self):
        self.board = ['' for _ in range(9)]
        self.current_player = 'X'
        self.game_active = True
        self.winner = None

    def make_move(self, position):
        if not self.game_active or self.board[position] != '':
            return False

        self.board[position] = self.current_player

        # Check for winner
        if self.check_winner():
            self.game_active = False
            self.winner = self.current_player
            return True

        # Check for tie
        if '' not in self.board:
            self.game_active = False
            self.winner = 'Tie'
            return True

        # Switch player
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        return True

    def check_winner(self):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]              # diagonals
        ]

        for combo in winning_combinations:
            if (self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]]
                    and self.board[combo[0]] != ''):
                return True
        return False

    def get_game_state(self):
        return {
            'board': self.board,
            'current_player': self.current_player,
            'game_active': self.game_active,
            'winner': self.winner
        }


# Initialize game
game = TikTacToe()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/make_move', methods=['POST'])
def make_move():
    data = request.get_json()
    position = int(data['position'])

    success = game.make_move(position)

    if success:
        return jsonify({
            'success': True,
            'game_state': game.get_game_state()
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Invalid move'
        })


@app.route('/reset_game', methods=['POST'])
def reset_game():
    game.reset_game()
    return jsonify({
        'success': True,
        'game_state': game.get_game_state()
    })


@app.route('/get_game_state', methods=['GET'])
def get_game_state():
    return jsonify(game.get_game_state())


if __name__ == '__main__':
    # Create templates folder if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')

    # Create the HTML template
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Python TikTacToe</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            color: white;
        }

        .game-container {
            text-align: center;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        h1 {
            font-size: 2.5em;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }

        .game-info {
            margin-bottom: 30px;
            font-size: 1.2em;
        }

        .current-player {
            font-weight: bold;
            color: #ffd700;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
        }

        .game-board {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            margin: 30px auto;
            max-width: 300px;
        }

        .cell {
            width: 90px;
            height: 90px;
            background: rgba(255, 255, 255, 0.2);
            border: 2px solid rgba(255, 255, 255, 0.3);
            border-radius: 15px;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 2em;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            backdrop-filter: blur(5px);
        }

        .cell:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: scale(1.05);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }

        .cell.disabled {
            cursor: not-allowed;
            opacity: 0.7;
        }

        .x { color: #ff6b6b; }
        .o { color: #4ecdc4; }

        .game-status {
            margin: 20px 0;
            font-size: 1.3em;
            font-weight: bold;
            min-height: 40px;
        }

        .win-message {
            color: #ffd700;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        }

        .reset-button {
            background: linear-gradient(45deg, #ff6b6b, #ee5a52);
            color: white;
            border: none;
            padding: 15px 30px;
            font-size: 1.1em;
            font-weight: bold;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }

        .reset-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
        }

        .python-badge {
            position: fixed;
            top: 20px;
            right: 20px;
            background: #3776ab;
            color: white;
            padding: 10px 15px;
            border-radius: 10px;
            font-size: 0.9em;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="python-badge">🐍 Powered by Python Flask</div>
    
    <div class="game-container">
        <h1>🎮 Python TikTacToe</h1>
        
        <div class="game-info">
            Current Player: <span class="current-player" id="currentPlayer">X</span>
        </div>

        <div class="game-board" id="gameBoard">
            <div class="cell" data-index="0" onclick="makeMove(0)"></div>
            <div class="cell" data-index="1" onclick="makeMove(1)"></div>
            <div class="cell" data-index="2" onclick="makeMove(2)"></div>
            <div class="cell" data-index="3" onclick="makeMove(3)"></div>
            <div class="cell" data-index="4" onclick="makeMove(4)"></div>
            <div class="cell" data-index="5" onclick="makeMove(5)"></div>
            <div class="cell" data-index="6" onclick="makeMove(6)"></div>
            <div class="cell" data-index="7" onclick="makeMove(7)"></div>
            <div class="cell" data-index="8" onclick="makeMove(8)"></div>
        </div>

        <div class="game-status" id="gameStatus">Make your move!</div>

        <button class="reset-button" onclick="resetGame()">🔄 New Game</button>
    </div>

    <script>
        function makeMove(position) {
            fetch('/make_move', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({position: position})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    updateGameDisplay(data.game_state);
                }
            });
        }

        function resetGame() {
            fetch('/reset_game', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    updateGameDisplay(data.game_state);
                }
            });
        }

        function updateGameDisplay(gameState) {
            const cells = document.querySelectorAll('.cell');
            const currentPlayer = document.getElementById('currentPlayer');
            const gameStatus = document.getElementById('gameStatus');

            // Update board
            cells.forEach((cell, index) => {
                cell.textContent = gameState.board[index];
                cell.className = 'cell';
                if (gameState.board[index] !== '') {
                    cell.classList.add(gameState.board[index].toLowerCase());
                    cell.classList.add('disabled');
                }
            });

            // Update current player
            currentPlayer.textContent = gameState.current_player;

            // Update game status
            if (!gameState.game_active) {
                if (gameState.winner === 'Tie') {
                    gameStatus.innerHTML = '<span class="win-message">🤝 It\\'s a Tie!</span>';
                } else {
                    gameStatus.innerHTML = `<span class="win-message">🎉 Player ${gameState.winner} Wins!</span>`;
                }
            } else {
                gameStatus.textContent = `Player ${gameState.current_player}\\'s turn`;
            }
        }

        // Load initial game state
        fetch('/get_game_state')
            .then(response => response.json())
            .then(data => {
                updateGameDisplay(data);
            });
    </script>
</body>
</html>'''

    # Write the HTML template
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("🎮 Python TikTacToe Server Starting!")
    print("📂 Created templates/index.html")
    print("🌐 Open your browser to: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")

    app.run(debug=True, host='0.0.0.0', port=5000)

from flask import Flask, render_template, request, jsonify
import os
import random
import logging
import math
import time

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-bot'


class TikTacToeBot:
    def __init__(self, difficulty='medium', human_symbol='X'):
        self.board = ['' for _ in range(9)]
        self.human_player = human_symbol
        self.bot_player = 'O' if human_symbol == 'X' else 'X'
        self.current_player = 'X'  # X always starts
        self.game_active = True
        self.winner = None
        self.difficulty = difficulty
        self.move_count = 0

    def reset_game(self, difficulty='medium', human_symbol='X'):
        self.board = ['' for _ in range(9)]
        self.human_player = human_symbol
        self.bot_player = 'O' if human_symbol == 'X' else 'X'
        self.current_player = 'X'  # X always starts
        self.game_active = True
        self.winner = None
        self.difficulty = difficulty
        self.move_count = 0

    def make_human_move(self, position):
        """Make a human move and validate it"""
        if not self.game_active:
            return {'success': False, 'message': 'Game is over'}

        if self.board[position] != '':
            return {'success': False, 'message': 'Cell already occupied'}

        if self.current_player != self.human_player:
            return {'success': False, 'message': 'Not your turn'}

        # Make the move
        self.board[position] = self.human_player
        self.move_count += 1

        # Check for winner
        if self.check_winner():
            self.game_active = False
            self.winner = self.human_player
            return {'success': True, 'game_over': True}

        # Check for tie
        if self.move_count >= 9:
            self.game_active = False
            self.winner = 'Tie'
            return {'success': True, 'game_over': True}

        # Switch to bot
        self.current_player = self.bot_player
        return {'success': True, 'game_over': False}

    def make_bot_move(self):
        """Make a bot move based on difficulty"""
        if not self.game_active or self.current_player != self.bot_player:
            return {'success': False, 'message': 'Not bot\'s turn'}

        # Get bot move based on difficulty
        position = None
        if self.difficulty == 'easy':
            position = self.get_easy_move()
        elif self.difficulty == 'medium':
            position = self.get_medium_move()
        else:  # hard
            position = self.get_hard_move()

        if position is None:
            return {'success': False, 'message': 'No valid moves'}

        # Make the move
        self.board[position] = self.bot_player
        self.move_count += 1

        # Check for winner
        if self.check_winner():
            self.game_active = False
            self.winner = self.bot_player
            return {'success': True, 'game_over': True, 'position': position}

        # Check for tie
        if self.move_count >= 9:
            self.game_active = False
            self.winner = 'Tie'
            return {'success': True, 'game_over': True, 'position': position}

        # Switch to human
        self.current_player = self.human_player
        return {'success': True, 'game_over': False, 'position': position}

    def get_easy_move(self):
        """Easy bot - mostly random with occasional smart moves"""
        available_moves = [i for i, cell in enumerate(
            self.board) if cell == '']
        if not available_moves:
            return None

        # 30% chance to make a smart move
        if random.random() < 0.3:
            smart_move = self.get_smart_move()
            if smart_move is not None:
                return smart_move

        return random.choice(available_moves)

    def get_medium_move(self):
        """Medium bot - balanced strategy"""
        # First check if bot can win
        win_move = self.find_winning_move(self.bot_player)
        if win_move is not None:
            return win_move

        # Then check if need to block human
        block_move = self.find_winning_move(self.human_player)
        if block_move is not None:
            return block_move

        # Otherwise make a strategic move
        return self.get_strategic_move()

    def get_hard_move(self):
        """Hard bot - uses minimax algorithm"""
        return self.minimax_move()

    def get_smart_move(self):
        """Basic smart move logic"""
        # Try to win
        win_move = self.find_winning_move(self.bot_player)
        if win_move is not None:
            return win_move

        # Try to block
        block_move = self.find_winning_move(self.human_player)
        if block_move is not None:
            return block_move

        return None

    def get_strategic_move(self):
        """Strategic move selection"""
        available_moves = [i for i, cell in enumerate(
            self.board) if cell == '']
        if not available_moves:
            return None

        # Prefer center
        if 4 in available_moves:
            return 4

        # Prefer corners
        corners = [0, 2, 6, 8]
        corner_moves = [i for i in corners if i in available_moves]
        if corner_moves:
            return random.choice(corner_moves)

        # Take any available move
        return random.choice(available_moves)

    def find_winning_move(self, player):
        """Find a move that would result in a win for the given player"""
        for i in range(9):
            if self.board[i] == '':
                # Try this move
                self.board[i] = player
                if self.check_winner():
                    self.board[i] = ''  # Undo the move
                    return i
                self.board[i] = ''  # Undo the move
        return None

    def minimax_move(self):
        """Use minimax algorithm to find the best move"""
        best_score = float('-inf')
        best_move = None

        available_moves = [i for i, cell in enumerate(
            self.board) if cell == '']

        for i in available_moves:
            self.board[i] = self.bot_player
            score = self.minimax(0, False)
            self.board[i] = ''

            if score > best_score:
                best_score = score
                best_move = i

        return best_move if best_move is not None else random.choice(available_moves)

    def minimax(self, depth, is_maximizing):
        """Minimax algorithm implementation"""
        # Check for terminal states
        winner = self.check_winner_for_minimax()
        if winner == self.bot_player:
            return 10 - depth
        elif winner == self.human_player:
            return depth - 10

        available_moves = [i for i, cell in enumerate(
            self.board) if cell == '']

        if not available_moves:
            return 0

        if is_maximizing:
            # Bot's turn
            best_score = float('-inf')
            for i in available_moves:
                self.board[i] = self.bot_player
                score = self.minimax(depth + 1, False)
                self.board[i] = ''
                best_score = max(score, best_score)
            return best_score
        else:
            # Human's turn
            best_score = float('inf')
            for i in available_moves:
                self.board[i] = self.human_player
                score = self.minimax(depth + 1, True)
                self.board[i] = ''
                best_score = min(score, best_score)
            return best_score

    def check_winner_for_minimax(self):
        """Check winner for minimax (returns player symbol or None)"""
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]              # diagonals
        ]

        for combo in winning_combinations:
            if (self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]]
                    and self.board[combo[0]] != ''):
                return self.board[combo[0]]
        return None

    def check_winner(self):
        """Check if there's a winner"""
        return self.check_winner_for_minimax() is not None

    def get_game_state(self):
        """Get current game state"""
        return {
            'board': self.board,
            'current_player': self.current_player,
            'game_active': self.game_active,
            'winner': self.winner,
            'difficulty': self.difficulty,
            'human_player': self.human_player,
            'bot_player': self.bot_player,
            'move_count': self.move_count
        }


# Initialize game
game = TikTacToeBot()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/make_move', methods=['POST'])
def make_move():
    """Handle human move and bot response"""
    try:
        data = request.get_json()
        logging.info(f"Received move request: {data}")
        position = int(data['position'])

        # Validate position
        if position < 0 or position > 8:
            return jsonify({
                'success': False,
                'message': 'Invalid position'
            })

        # Make human move
        result = game.make_human_move(position)

        if not result['success']:
            return jsonify(result)

        game_state = game.get_game_state()

        # If game is still active and it's bot's turn, make bot move
        if game.game_active and game.current_player == game.bot_player:
            # Add small delay for better UX (simulate thinking)
            time.sleep(0.3)
            bot_result = game.make_bot_move()
            game_state = game.get_game_state()

            if bot_result['success']:
                game_state['bot_move'] = bot_result.get('position')

        return jsonify({
            'success': True,
            'game_state': game_state
        })

    except Exception as e:
        logging.error(f"Error in /make_move endpoint: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })


@app.route('/reset_game', methods=['POST'])
def reset_game():
    """Reset the game with new settings"""
    try:
        data = request.get_json()
        logging.info(f"Received reset_game request: {data}")
        difficulty = data.get('difficulty', 'medium')
        human_symbol = data.get('human_symbol', 'X')

        # Validate inputs
        if difficulty not in ['easy', 'medium', 'hard']:
            difficulty = 'medium'
        if human_symbol not in ['X', 'O']:
            human_symbol = 'X'

        game.reset_game(difficulty, human_symbol)

        game_state = game.get_game_state()

        # If bot is 'X', it should make the first move right away
        if game.game_active and game.current_player == game.bot_player:
            bot_result = game.make_bot_move()
            game_state = game.get_game_state()
            if bot_result['success']:
                game_state['bot_move'] = bot_result.get('position')

        return jsonify({
            'success': True,
            'game_state': game_state
        })

    except Exception as e:
        logging.error(f"Error in /reset_game endpoint: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })


@app.route('/get_game_state', methods=['GET'])
def get_game_state():
    """Get current game state"""
    return jsonify(game.get_game_state())


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'game_active': game.game_active,
        'current_player': game.current_player
    })


if __name__ == '__main__':
    # Configure basic logging to write to a file
    logging.basicConfig(
        filename='log.txt',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # Create templates folder if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')

    # Create the HTML template
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TikTacToe vs Bot</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            color: white;
            padding: 20px;
        }

        .game-container {
            text-align: center;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.2);
            max-width: 500px;
            width: 100%;
        }

        h1 {
            font-size: 2.5em;
            margin-bottom: 30px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            background: linear-gradient(45deg, #fff, #f0f0f0);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .controls {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 30px;
        }

        .control-group {
            text-align: left;
        }

        .control-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
            color: #e0e0e0;
            font-size: 1.1em;
        }

        .control-group select {
            width: 100%;
            background: rgba(255, 255, 255, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 10px;
            padding: 12px 15px;
            color: white;
            font-size: 1em;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .control-group select:hover {
            background: rgba(255, 255, 255, 0.3);
        }

        .control-group select option {
            background: #2c3e50;
            color: white;
            padding: 10px;
        }

        .player-info {
            display: flex;
            justify-content: space-between;
            margin-bottom: 20px;
            padding: 20px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            border: 2px solid transparent;
            transition: all 0.3s ease;
        }

        .player-info.current-turn {
            border-color: rgba(255, 255, 255, 0.5);
            background: rgba(255, 255, 255, 0.2);
        }

        .player {
            text-align: center;
            flex: 1;
        }

        .player-label {
            font-size: 1em;
            opacity: 0.9;
            margin-bottom: 8px;
            font-weight: bold;
        }

        .player-symbol {
            font-size: 2.5em;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }

        .human { color: #e74c3c; }
        .bot { color: #3498db; }

        .vs-divider {
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5em;
            font-weight: bold;
            color: #f39c12;
            margin: 0 20px;
        }

        .game-board {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
            margin: 30px auto;
            max-width: 320px;
            padding: 20px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 20px;
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
            font-size: 2.5em;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            backdrop-filter: blur(5px);
        }

        .cell:hover:not(.disabled) {
            background: rgba(255, 255, 255, 0.4);
            transform: scale(1.1);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        }

        .cell.disabled {
            cursor: not-allowed;
            opacity: 0.7;
        }

        .cell.thinking {
            background: rgba(52, 152, 219, 0.4);
            animation: pulse 1.5s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 0.7; transform: scale(1); }
            50% { opacity: 1; transform: scale(1.05); }
        }

        .cell.x { color: #e74c3c; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5); }
        .cell.o { color: #3498db; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5); }

        .game-status {
            margin: 25px 0;
            font-size: 1.4em;
            font-weight: bold;
            min-height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 15px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
        }

        .win-message {
            color: #f39c12;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
            font-size: 1.2em;
        }

        .bot-thinking {
            color: #3498db;
            font-style: italic;
            animation: thinking 2s infinite;
        }

        @keyframes thinking {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }

        .controls-buttons {
            display: flex;
            gap: 15px;
            justify-content: center;
            flex-wrap: wrap;
            margin-top: 20px;
        }

        .button {
            background: linear-gradient(45deg, #e74c3c, #c0392b);
            color: white;
            border: none;
            padding: 15px 25px;
            font-size: 1em;
            font-weight: bold;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            min-width: 120px;
        }

        .button:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        }

        .button:active {
            transform: translateY(-1px);
        }

        .button.secondary {
            background: linear-gradient(45deg, #95a5a6, #7f8c8d);
        }

        .stats {
            display: flex;
            justify-content: space-around;
            margin-top: 20px;
            padding: 15px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            font-size: 0.9em;
        }

        .stat-item {
            text-align: center;
        }

        .stat-value {
            font-size: 1.5em;
            font-weight: bold;
            color: #f39c12;
        }

        .difficulty-indicator {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 10px 15px;
            border-radius: 10px;
            font-weight: bold;
            font-size: 0.9em;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }

        .difficulty-easy { background: #27ae60; color: white; }
        .difficulty-medium { background: #f39c12; color: white; }
        .difficulty-hard { background: #e74c3c; color: white; }

        .loading {
            opacity: 0.7;
            pointer-events: none;
        }

        @media (max-width: 600px) {
            .game-container {
                padding: 20px;
            }
            
            .controls {
                grid-template-columns: 1fr;
            }
            
            .cell {
                width: 70px;
                height: 70px;
                font-size: 2em;
            }
            
            .game-board {
                max-width: 250px;
            }
        }
    </style>
</head>
<body>
    <div class="difficulty-indicator" id="difficultyIndicator">Medium</div>
    
    <div class="game-container">
        <h1>🎮 TikTacToe vs Bot</h1>
        
        <div class="controls">
            <div class="control-group">
                <label for="difficulty">🎯 Difficulty:</label>
                <select id="difficulty" onchange="changeDifficulty()">
                    <option value="easy">🟢 Easy - Random</option>
                    <option value="medium" selected>🟡 Medium - Smart</option>
                    <option value="hard">🔴 Hard - Unbeatable</option>
                </select>
            </div>
            
            <div class="control-group">
                <label for="humanSymbol">🎲 Your Symbol:</label>
                <select id="humanSymbol" onchange="changeSymbol()">
                    <option value="X" selected>❌ X (First)</option>
                    <option value="O">⭕ O (Second)</option>
                </select>
            </div>
        </div>
        
        <div class="player-info" id="playerInfo">
            <div class="player">
                <div class="player-label">👤 You</div>
                <div class="player-symbol human" id="humanSymbolDisplay">❌</div>
            </div>
            <div class="vs-divider">VS</div>
            <div class="player">
                <div class="player-label">🤖 Bot</div>
                <div class="player-symbol bot" id="botSymbolDisplay">⭕</div>
            </div>
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

        <div class="game-status" id="gameStatus">🎯 Your turn! Make your move.</div>

        <div class="controls-buttons">
            <button class="button" onclick="resetGame()">🔄 New Game</button>
            <button class="button secondary" onclick="toggleControls()">⚙️ Settings</button>
        </div>
    </div>

    <script>
        let isWaitingForBot = false;
        let gameStats = { wins: 0, losses: 0, ties: 0 };
        let controlsVisible = true;

        function makeMove(position) {
            if (isWaitingForBot) {
                console.log('Waiting for bot, ignoring move');
                return;
            }
            
            const gameStatus = document.getElementById('gameStatus');
            const gameContainer = document.querySelector('.game-container');
            
            // Show loading state
            isWaitingForBot = true;
            gameContainer.classList.add('loading');
            
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
                    if (data.game_state.bot_move !== undefined) {
                        highlightLastMove(data.game_state.bot_move);
                    }
                } else {
                    gameStatus.textContent = data.message;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                gameStatus.textContent = 'Error making move. Please try again.';
            })
            .finally(() => {
                isWaitingForBot = false;
                gameContainer.classList.remove('loading');
            });
        }

        function resetGame() {
            const difficulty = document.getElementById('difficulty').value;
            const humanSymbol = document.getElementById('humanSymbol').value;
            
            fetch('/reset_game', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    difficulty: difficulty,
                    human_symbol: humanSymbol
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    updateGameDisplay(data.game_state);
                    clearHighlights();
                } else {
                    console.error('Error resetting game:', data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }

        function changeDifficulty() {
            const difficulty = document.getElementById('difficulty').value;
            const indicator = document.getElementById('difficultyIndicator');
            
            // Update indicator
            indicator.className = `difficulty-indicator difficulty-${difficulty}`;
            indicator.textContent = difficulty.charAt(0).toUpperCase() + difficulty.slice(1);
            
            // Reset game with new difficulty
            resetGame();
        }

        function changeSymbol() {
            resetGame();
        }

        function toggleControls() {
            const controls = document.querySelector('.controls');
            controlsVisible = !controlsVisible;
            controls.style.display = controlsVisible ? 'grid' : 'none';
            
            const btn = document.querySelector('.button.secondary');
            btn.textContent = controlsVisible ? '🔼 Hide Settings' : '⚙️ Settings';
        }

        function highlightLastMove(position) {
            // Remove previous highlights
            clearHighlights();
            
            // Highlight the last move
            const cell = document.querySelector(`[data-index="${position}"]`);
            if (cell) {
                cell.style.background = 'rgba(52, 152, 219, 0.4)';
                setTimeout(() => {
                    cell.style.background = '';
                }, 2000);
            }
        }

        function clearHighlights() {
            const cells = document.querySelectorAll('.cell');
            cells.forEach(cell => {
                cell.style.background = '';
            });
        }

        function updateGameDisplay(gameState) {
            const cells = document.querySelectorAll('.cell');
            const gameStatus = document.getElementById('gameStatus');
            const playerInfo = document.getElementById('playerInfo');
            const humanSymbolDisplay = document.getElementById('humanSymbolDisplay');
            const botSymbolDisplay = document.getElementById('botSymbolDisplay');

            // Update player symbols
            humanSymbolDisplay.textContent = gameState.human_player === 'X' ? '❌' : '⭕';
            botSymbolDisplay.textContent = gameState.bot_player === 'X' ? '❌' : '⭕';

            // Update board
            cells.forEach((cell, index) => {
                const symbol = gameState.board[index];
                if (symbol === 'X') {
                    cell.textContent = '❌';
                    cell.className = 'cell x';
                } else if (symbol === 'O') {
                    cell.textContent = '⭕';
                    cell.className = 'cell o';
                } else {
                    cell.textContent = '';
                    cell.className = 'cell';
                }
                
                // Disable cells that are occupied or if game is over
                if (symbol !== '' || !gameState.game_active) {
                    cell.classList.add('disabled');
                } else {
                    cell.classList.remove('disabled');
                }
            });

            // Update game status
            if (!gameState.game_active) {
                if (gameState.winner === 'Tie') {
                    gameStatus.innerHTML = '<span class="win-message">🤝 It\\\'s a Tie!</span>';
                } else {
                    const winnerText = gameState.winner === gameState.human_player ? 'You' : 'Bot';
                    gameStatus.innerHTML = `<span class="win-message">🎉 ${winnerText} Win!</span>`;
                }
                playerInfo.classList.remove('current-turn');
            } else {
                if (gameState.current_player === gameState.human_player) {
                    gameStatus.textContent = '🎯 Your turn! Make your move.';
                    playerInfo.classList.add('current-turn');
                } else {
                    gameStatus.innerHTML = '<span class="bot-thinking">🤖 Bot is thinking...</span>';
                    playerInfo.classList.remove('current-turn');
                }
            }
        }

        // Initial setup
        document.addEventListener('DOMContentLoaded', () => {
            // Load initial game state
            fetch('/get_game_state')
                .then(response => response.json())
                .then(data => {
                    updateGameDisplay(data);
                    // Set initial state from server
                    document.getElementById('difficulty').value = data.difficulty;
                    document.getElementById('humanSymbol').value = data.human_player;
                    changeDifficulty(); // Update indicator
                });
        });
    </script>
</body>
</html>'''

    # Write the HTML template to a file
    template_path = os.path.join('templates', 'index.html')
    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    logging.info("Server starting up...")
    print("🎮 TikTacToe Bot Server Starting!")
    print(f"📂 Created/Updated {template_path}")
    print("🌐 Open your browser to: http://localhost:5001")
    print("🛑 Press Ctrl+C to stop the server")

    app.run(debug=True, host='0.0.0.0', port=5001)

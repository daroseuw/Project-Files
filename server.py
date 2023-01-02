from flask import Flask, render_template, request
from logic import Players, Board, Moves, PlayerType, Human, Bot, DataHandling, DataViz
# from cli import RunGame

app = Flask(__name__)

board = [
    [' ',' ',' '],
    [' ',' ',' '],
    [' ',' ',' ']
    ]

game_file = "./data/games.csv"


@app.route('/startgame', methods=['POST'])
def startgame():
    # Unsure if 'get' is specific to the request function
    player_1_name = request.form.get("first_player_name", default="Human", type=str)
    player_1_type = request.form.get("Player 1 Selection", default="Human", type=str)
    player_2_name = request.form.get("second_player_name", default="Human", type=str)
    player_2_type = request.form.get("Player 1 Selection", default="Human", type=str)
    player_1_symbol = 'X'
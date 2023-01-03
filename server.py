# Run with 'flask --app server.py --debug run'

from flask import Flask, render_template, request, redirect
from logic import Players, Board, Moves, PlayerType, Human, Bot, DataHandling, DataViz
# from cli import RunGame

app = Flask(__name__)

game_file = "./data/games.csv"
move_file = ".data/moves.csv"
gameboard = Board()
board = gameboard.new_board()
moves = Moves()
human = Human()
bot = Bot()
get_user_info = PlayerType()
data_handling = DataHandling(game_file, move_file)

@app.route('/', methods= ['POST','GET'])
def start():
    start_game = ("Game Start" in request.form.getlist('start_game'))
    if request.method == 'POST' and start_game:
        player_1_name = request.form.get("first_player_name", default="Human", type=str)
        player_1_type = request.form.get("Player 1 Selection", default="Human", type=str)
        player_2_name = request.form.get("second_player_name", default="Human", type=str)
        player_2_type = request.form.get("Player 1 Selection", default="Human", type=str)
        player_1_symbol = 'X'
        current_player = 'X'
        player_2_symbol = 'O'
        first_player_vars = [player_1_symbol, player_1_type, player_1_name]
        second_player_vars = ['O', player_2_type, player_2_name]
        player_vars = [first_player_vars, second_player_vars]
        if player_1_name and player_1_type and player_2_name and player_2_type:
            return redirect('/play') 
    # elif request.method == 'GET':
    #     pass #start a new game
    return render_template('index.html')

@app.route('/play', methods=['POST', 'GET'])
def play_game(player_1_name, player_1_symbol, player_1_type, player_2_name, player_2_symbol, player_2_type, player_vars):
    moves.winner = moves.check_for_win(board)
    gameboard.full = gameboard.board_full(board)
    while moves.winner == False and gameboard.full == False:
        #REPLACE PRINT BOARD
        # gameboard.print_board()
        # Return current player type:
        current_player_type = get_user_info.get_player_type(current_player, player_vars)
        current_player_name = get_user_info.get_player_name(current_player, player_vars)
        message = ("It is " + current_player + "'s turn.")
        if current_player_type == 'Human':
            move_tup = human.play_move(board, current_player)
        elif current_player_type == 'Bot':
            move_tup = bot.play_move(board, current_player)
        else:
            message = 'There is an error with human v. bot play logic'
        data_handling.record_move_data(move_num, current_player_name, current_player_type, current_player, move_tup)
        move_num = move_num + 1
        # move_data_prep = data_handling.record_move_data(move_data, 1, current_player_name, current_player_type, current_player, human.move)
        # move_data_prep.to_csv(moves_file)
        moves.winner = moves.check_for_win(board)
        if moves.winner == True:
            break
        gameboard.full = gameboard.board_full(board)
        if gameboard.full == True:
            break
        current_player = moves.advance_turn(current_player)
    if moves.winner == True:
        # REPLACE PRINT BOARD
        # gameboard.print_board()
        message = (current_player + " won the game!")
    elif gameboard.full == True:
        # REPLACE PRINT BOARD
        # gameboard.print_board()
        message = "The game resulted in a draw."
    else:
        message = "An error occurred when checking for winner or draw."
    data_handling.record_game_data(moves.winner, player_1_name, player_1_symbol, player_1_type, player_2_name, player_2_symbol, player_2_type, current_player, move_num - 1)
    return render_template("play.html", gameboard=gameboard)

# @app.route('/', methods= ['POST','GET'])
# def start():
#     start_game = ("Game Start" in request.form.getlist('start_game'))
#     if request.method == 'POST' and start_game:
#         player_1_name = request.form.get("first_player_name", default="Human", type=str)
#         player_1_type = request.form.get("Player 1 Selection", default="Human", type=str)
#         player_2_name = request.form.get("second_player_name", default="Human", type=str)
#         player_2_type = request.form.get("Player 1 Selection", default="Human", type=str)
#         player_1_symbol = 'X'
#         current_player = 'X'
#         player_2_symbol = 'O'
#         first_player_vars = [player_1_symbol, player_1_type, player_1_name]
#         second_player_vars = ['O', player_2_type, player_2_name]
#         player_vars = [first_player_vars, second_player_vars]
#         if player_1_name and player_1_type and player_2_name and player_2_type:
            
#             return redirect('/play') 
#     # elif request.method == 'GET':
#     #     pass #start a new game
#     return render_template('index.html')

# @app.route('/play', methods=['POST', 'GET'])
# def play_game(player_1_name, player_1_symbol, player_1_type, player_2_name, player_2_symbol, player_2_type, player_vars):
#     moves.winner = moves.check_for_win(board)
#     gameboard.full = gameboard.board_full(board)
#     while moves.winner == False and gameboard.full == False:
#         #REPLACE PRINT BOARD
#         # gameboard.print_board()
#         # Return current player type:
#         current_player_type = get_user_info.get_player_type(current_player, player_vars)
#         current_player_name = get_user_info.get_player_name(current_player, player_vars)
#         message = ("It is " + current_player + "'s turn.")
#         if current_player_type == 'Human':
#             move_tup = human.play_move(board, current_player)
#         elif current_player_type == 'Bot':
#             move_tup = bot.play_move(board, current_player)
#         else:
#             message = 'There is an error with human v. bot play logic'
#         data_handling.record_move_data(move_num, current_player_name, current_player_type, current_player, move_tup)
#         move_num = move_num + 1
#         # move_data_prep = data_handling.record_move_data(move_data, 1, current_player_name, current_player_type, current_player, human.move)
#         # move_data_prep.to_csv(moves_file)
#         moves.winner = moves.check_for_win(board)
#         if moves.winner == True:
#             break
#         gameboard.full = gameboard.board_full(board)
#         if gameboard.full == True:
#             break
#         current_player = moves.advance_turn(current_player)
#     if moves.winner == True:
#         # REPLACE PRINT BOARD
#         # gameboard.print_board()
#         message = (current_player + " won the game!")
#     elif gameboard.full == True:
#         # REPLACE PRINT BOARD
#         # gameboard.print_board()
#         message = "The game resulted in a draw."
#     else:
#         message = "An error occurred when checking for winner or draw."
#     data_handling.record_game_data(moves.winner, player_1_name, player_1_symbol, player_1_type, player_2_name, player_2_symbol, player_2_type, current_player, move_num - 1)
#     return render_template("play.html", gameboard=gameboard)
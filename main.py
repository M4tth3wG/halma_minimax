from game import Game
import strategies
import heuristics
from halma import FieldType
import sys
import time

def print_board(game):
    field_repr = {
        FieldType.PLAYER_WHITE : "O",
        FieldType.PLAYER_BLACK : "X",
        FieldType.EMPTY : "_"
    }

    board = game.halma.board
    style = "{:2}"
    print(style.format(''), end="\t")
    headers = [style.format(number) for number in range(len(board))]
    print(*headers, sep=" ", end="\n\n")

    for i, row in enumerate(game.halma.board):
        print(style.format(i), end="\t")
        print(*[style.format(field_repr[field]) for field in row], sep=" ")

def print_possible_moves(game):
    count = 0
    elems_in_line = 4

    for start, goal in game.halma.possible_moves:
        print(start, goal, sep=' ==> ', end=',\t')
        count = count + 1

        if count % elems_in_line == 0:
            print()

    print()

def print_selected_move(game, output=sys.__stdout__):
    start, goal = game.last_move
    print(start, goal, sep=' ==> ', file=output)

def print_game_result(game):
    print(f'Number of rounds: {game.halma.round}')
    print(f'Winner: {game.halma.winner.name}')
    print_board(game)

def run(game, verbous=False, move_output=sys.__stdout__):
    separator_length = 50

    game_start_time = time.time()

    while not game.halma.finished:
        print('#' * separator_length, end='\n\n')

        print('-' * separator_length)
        print(f'Round: {game.halma.round}')
        print(f'{game.current_player.name}\'s turn')

        print('-' * separator_length)
        print_board(game)

        if verbous:
            print('-' * separator_length)
            print('Possible moves:')
            print_possible_moves(game)

        move_start_time = time.time()
        game.next_move()
        move_end_time = time.time()

        print('-' * separator_length)
        print('Selected move:', end=' ')
        print_selected_move(game, move_output)

        print('-' * separator_length)
        print(f'Move computation time: {move_end_time - move_start_time}s')

    game_end_time = time.time()

    print('%' * separator_length)
    print_game_result(game)
    print(f'Total game duration: {game_end_time - game_start_time}s')
    print('%' * separator_length)

def main():
    # player_white_strategy = strategies.BestCurrentMoveStrategy(heuristics.manhattan_end_positon_heuristic)
    # player_white_strategy = strategies.BestNextStateStrategy(heuristics.manhattan_state_heuristic)
    # player_white_strategy = strategies.MinimaxStrategy(heuristics.manhattan_state_heuristic, 1)
    # player_white_strategy = strategies.AlphaBetaStrategy(heuristics.manhattan_state_heuristic, 2)
    player_white_strategy = strategies.BestNextStateStrategy(heuristics.manhattan_state_heuristic)
    player_black_strategy = strategies.BestNextStateStrategy(heuristics.euclides_state_heuristic)

    game = Game(player_white_strategy, player_black_strategy)
    run(game, verbous=False)

if __name__ == '__main__':
    main()
from game import Game
import strategies
import heuristics
from halma import FieldType

def print_board(game):
    for row in game.halma.board:
        for field in row:
            print(field.value, end=" ")
        print()

def print_possible_moves(game):
    count = 0
    elems_in_line = 4

    for start, goal in game.halma.possible_moves:
        print(start, goal, sep=' ==> ', end=',\t')
        count = count + 1

        if count % elems_in_line == 0:
            print()

    print()

def print_selected_move(game):
    start, goal = game.last_move
    print(start, goal, sep=' ==> ')

def print_game_result(game):
    print(f'Number of rounds: {game.halma.round}')
    print(f'Winner: {game.halma.winner.name}')
    print_board(game)

def run(game):
    separator_length = 50

    while not game.halma.finished:
        print('#' * separator_length, end='\n\n')

        print('-' * separator_length)
        print(f'Round: {game.halma.round}')
        print(f'{game.current_player.name}\'s turn')

        print('-' * separator_length)
        print_board(game)

        print('-' * separator_length)
        print('Possible moves:')
        print_possible_moves(game)

        game.next_move()

        print('-' * separator_length)
        print('Selected move:', end=' ')
        print_selected_move(game)

    print('%' * separator_length)
    print_game_result(game)
    print('%' * separator_length)

def main():
    player_white_strategy = strategies.BestCurrentMoveStrategy(heuristics.manhattan_end_positon_heuristic)
    # player_white_strategy = strategies.AlfaBetaStrategy(heuristics.manhattan_state_heuristic)
    player_black_strategy = strategies.RandomStrategy()

    game = Game(player_white_strategy, player_black_strategy)
    run(game)

if __name__ == '__main__':
    main()
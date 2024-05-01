from game import Game
import strategies
import strategies.random_strategy

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

def main():
    player_white_strategy = strategies.random_strategy.RandomStrategy()
    player_black_strategy = strategies.random_strategy.RandomStrategy()

    game = Game(player_white_strategy, player_black_strategy)
    run(game)

if __name__ == '__main__':
    main()
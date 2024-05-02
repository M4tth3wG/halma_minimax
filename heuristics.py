from halma import FieldType
import halma

def winning_coordinates(player):
    coordinates = []

    if player == FieldType.PLAYER_WHITE:
        coordinates = halma.Halma.camp_coordinates[FieldType.PLAYER_BLACK]
    else:
        coordinates = halma.Halma.camp_coordinates[FieldType.PLAYER_WHITE]

    return coordinates

PLAYER_WHITE_WINNING_COORDINATES = winning_coordinates(FieldType.PLAYER_WHITE)
PLAYER_BLACK_WINNING_COORDINATES = winning_coordinates(FieldType.PLAYER_BLACK)

def manhattan_end_positon_heuristic(move, halma_game):
    player = halma_game.current_player
    (start_x, start_y), (end_x, end_y) = move

    if player == FieldType.PLAYER_WHITE:
        goal_x, goal_y = halma.BOARD_SIZE - 1, halma.BOARD_SIZE - 1
        winning_coordinates = PLAYER_WHITE_WINNING_COORDINATES
    else:
        goal_x, goal_y = 0, 0
        winning_coordinates = PLAYER_BLACK_WINNING_COORDINATES

    if (start_x, start_y) in winning_coordinates:
        return -1 * float('inf')

    for goal_x, goal_y in winning_coordinates:
        if halma_game.board[goal_y][goal_x] != player:
            start_factor = (abs(start_x - goal_x) + abs(start_y - goal_y))
            end_factor = 2 * (halma.BOARD_SIZE - 1) - (abs(end_x - goal_x) + abs(end_y - goal_y))
            
            return start_factor + end_factor

def main():
    print(f'White {PLAYER_WHITE_WINNING_COORDINATES}')
    print(f'Black {PLAYER_BLACK_WINNING_COORDINATES}')

if __name__ == '__main__':
    main()
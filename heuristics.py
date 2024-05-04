from halma import FieldType
import halma
import matplotlib.pyplot as plt
import numpy as np

def winning_coordinates(player):
    coordinates = []

    if player == FieldType.PLAYER_WHITE:
        coordinates = halma.Halma.camp_coordinates[FieldType.PLAYER_BLACK]
    else:
        coordinates = halma.Halma.camp_coordinates[FieldType.PLAYER_WHITE]

    return coordinates

def create_heatmap(maximizing_player):
    shift = 5
    multiplier = 2
    
    if maximizing_player == FieldType.PLAYER_WHITE:
        initial_value = 0
    else:
        initial_value = 2 * (halma.BOARD_SIZE - 1)
    
    heatmap = [[abs(initial_value - (x + y)) for x in range(halma.BOARD_SIZE)] for y in range(halma.BOARD_SIZE)]

    for x, y in halma.Halma.camp_coordinates[maximizing_player]:
        heatmap[y][x] = (heatmap[y][x] - shift) * multiplier
    
    for x, y in halma.Halma.camp_coordinates[halma.get_next_player(maximizing_player)]:
        heatmap[y][x] = (heatmap[y][x] + shift) * multiplier

    return heatmap

def print_heatmap(grid):
    data = np.array(grid)
    
    plt.imshow(data, cmap='viridis', interpolation='nearest')
    plt.colorbar()
    plt.show()

HEATMAPS = {player : create_heatmap(player) for player in halma.Halma.players}
PLAYER_WHITE_WINNING_COORDINATES = winning_coordinates(FieldType.PLAYER_WHITE)
PLAYER_BLACK_WINNING_COORDINATES = winning_coordinates(FieldType.PLAYER_BLACK)

def manhattan_distance(point_a, point_b):
    point_a_x, point_a_y = point_a
    point_b_x, point_b_y = point_b

    return abs(point_a_x - point_b_x) + abs(point_a_y - point_b_y)

def manhattan_end_positon_heuristic(move, halma_game):
    player = halma_game.current_player
    (start_x, start_y), (end_x, end_y) = move

    if player == FieldType.PLAYER_WHITE:
        corner_x, corner_y = halma.BOARD_SIZE - 1, halma.BOARD_SIZE - 1
        winning_coordinates = PLAYER_WHITE_WINNING_COORDINATES
    else:
        corner_x, corner_y = 0, 0
        winning_coordinates = PLAYER_BLACK_WINNING_COORDINATES

    if (start_x, start_y) in winning_coordinates:
        start_factor = (abs(start_x - corner_x) + abs(start_y - corner_y))
        end_factor = 2 * (halma.BOARD_SIZE - 1) - (abs(end_x - corner_x) + abs(end_y - corner_y))
            
        return start_factor + end_factor

    for goal_x, goal_y in winning_coordinates:
        if halma_game.board[goal_y][goal_x] != player:
            start_factor = (abs(start_x - goal_x) + abs(start_y - goal_y))
            end_factor = 2 * (halma.BOARD_SIZE - 1) - (abs(end_x - goal_x) + abs(end_y - goal_y))
            
            return start_factor + end_factor

def calculate_distance_to_camp(field_coordinates, camp_coordinates, distance_function):
    distances = [distance_function(field_coordinates, camp_field) for camp_field in camp_coordinates]
    return min(distances) # changed

# def manhattan_state_heuristic(board, maximizing_player):
#     player_white_fields = halma.calculate_player_fields(board, FieldType.PLAYER_WHITE)
#     player_black_fields = halma.calculate_player_fields(board, FieldType.PLAYER_BLACK)

#     player_white_sum = sum([calculate_distance_to_camp(field, halma.Halma.camp_coordinates[FieldType.PLAYER_WHITE], manhattan_distance) for field in player_white_fields])
#     player_black_sum = sum([calculate_distance_to_camp(field, halma.Halma.camp_coordinates[FieldType.PLAYER_BLACK], manhattan_distance) for field in player_black_fields])
    
#     if maximizing_player == FieldType.PLAYER_WHITE:
#         player_black_sum = -1 * player_black_sum
#     else:
#         player_white_sum = -1 * player_white_sum

#     return player_white_sum + player_black_sum

# def manhattan_state_heuristic(board, maximizing_player):
#     player_white_fields = halma.calculate_player_fields(board, FieldType.PLAYER_WHITE)
#     player_black_fields = halma.calculate_player_fields(board, FieldType.PLAYER_BLACK)

#     player_white_free_end_zone_fields = list(set(PLAYER_WHITE_WINNING_COORDINATES) - set(player_white_fields))
#     player_black_free_end_zone_fields = list(set(PLAYER_BLACK_WINNING_COORDINATES) - set(player_black_fields))

#     player_white_sum = 0
#     player_black_sum = 0

#     for field in player_white_fields:
#         player_white_sum = player_white_sum + 2 * (halma.BOARD_SIZE - 1)
        
#         if field not in PLAYER_WHITE_WINNING_COORDINATES:
#             player_white_sum = player_white_sum - calculate_distance_to_camp(field, player_white_free_end_zone_fields, manhattan_distance)

#     for field in player_black_fields:
#         player_black_sum = player_black_sum + 2 * (halma.BOARD_SIZE - 1)
        
#         if field not in PLAYER_BLACK_WINNING_COORDINATES:
#             player_black_sum = player_black_sum - calculate_distance_to_camp(field, player_black_free_end_zone_fields, manhattan_distance)

#     if maximizing_player == FieldType.PLAYER_WHITE:
#         player_black_sum = -1 * player_black_sum
#     else:
#         player_white_sum = -1 * player_white_sum

#     return player_white_sum + player_black_sum

def manhattan_state_heuristic(board, maximizing_player):
    player_white_fields = halma.calculate_player_fields(board, FieldType.PLAYER_WHITE)
    player_black_fields = halma.calculate_player_fields(board, FieldType.PLAYER_BLACK)

    player_white_free_end_zone_fields = list(set(PLAYER_WHITE_WINNING_COORDINATES) - set(player_white_fields))
    player_black_free_end_zone_fields = list(set(PLAYER_BLACK_WINNING_COORDINATES) - set(player_black_fields))

    player_white_sum = 0
    player_black_sum = 0

    for field in player_white_fields:
        player_white_sum = player_white_sum + 4 * (halma.BOARD_SIZE - 1)
        
        if field not in PLAYER_WHITE_WINNING_COORDINATES:
            player_white_sum = player_white_sum - calculate_distance_to_camp(field, player_white_free_end_zone_fields, manhattan_distance)
        
        player_white_sum = player_white_sum - manhattan_distance(field, (15,15))

    for field in player_black_fields:
        player_black_sum = player_black_sum + 4 * (halma.BOARD_SIZE - 1)
        
        if field not in PLAYER_BLACK_WINNING_COORDINATES:
            player_black_sum = player_black_sum - calculate_distance_to_camp(field, player_black_free_end_zone_fields, manhattan_distance)

        player_black_sum = player_black_sum - manhattan_distance(field, (0,0))

    if maximizing_player == FieldType.PLAYER_WHITE:
        player_black_sum = -1 * player_black_sum
    else:
        player_white_sum = -1 * player_white_sum

    return player_white_sum + player_black_sum

def heatmap_heuristic(board, maximizing_player):
    heatmap = HEATMAPS[maximizing_player]
    
    player_fields = []

    for player in halma.Halma.players:
        player_fields.extend(halma.calculate_player_fields(board, player))

    return sum([heatmap[y][x] for x, y in player_fields])

def main():
    game = halma.Halma()
    board = game.board

    # for x in range(halma.BOARD_SIZE):
    #     for y in range(halma.BOARD_SIZE):
    #         if board[y][x] == FieldType.PLAYER_WHITE:
    #             board[y][x] = FieldType.PLAYER_BLACK
    #         elif board[y][x] == FieldType.PLAYER_BLACK:
    #             board[y][x] = FieldType.PLAYER_WHITE
    
    # print(halma.check_winning_condition(board, FieldType.PLAYER_WHITE))
    # print(halma.check_winning_condition(board, FieldType.PLAYER_BLACK))
    # print(manhattan_state_heuristic(board, FieldType.PLAYER_BLACK))

    print_heatmap(HEATMAPS[FieldType.PLAYER_WHITE])
    # print_heatmap(HEATMAPS[FieldType.PLAYER_BLACK])

    print(heatmap_heuristic(board, FieldType.PLAYER_BLACK))

if __name__ == '__main__':
    main()
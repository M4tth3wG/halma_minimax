from halma import FieldType
import halma
import matplotlib.pyplot as plt
import numpy as np
import math
from itertools import chain

CAMP_EDGES = {
    FieldType.PLAYER_WHITE : [(halma.START_AREA_SIZE + 1 - y, y) for y in range(1, halma.START_AREA_SIZE + 1)],
    FieldType.PLAYER_BLACK : [(halma.BOARD_SIZE - halma.START_AREA_SIZE + y - 2, halma.BOARD_SIZE - y - 1) for y in range(1, halma.START_AREA_SIZE + 1)]
}

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

    for index, (x, y) in enumerate(CAMP_EDGES[maximizing_player]):
        heatmap[y][x] = heatmap[y][x] - index * 0.1
    
    for x, y in halma.Halma.camp_coordinates[halma.get_next_player(maximizing_player)]:
        heatmap[y][x] = (heatmap[y][x] + shift) * multiplier

    minimizer_edge = CAMP_EDGES[halma.get_next_player(maximizing_player)].copy()
    minimizer_edge.reverse()

    for index, (x, y) in enumerate(minimizer_edge):
        heatmap[y][x] = heatmap[y][x] + index * 0.1

    return heatmap

def print_heatmap(grid):
    data = np.array(grid)
    
    plt.imshow(data, cmap='viridis', interpolation='nearest')
    plt.colorbar()
    plt.show()

HEATMAPS = {player : create_heatmap(player) for player in halma.Halma.players}
WINNING_COORDINATES = {player : halma.Halma.camp_coordinates[halma.get_next_player(player)] for player in halma.Halma.players}

def manhattan_distance(point_a, point_b):
    point_a_x, point_a_y = point_a
    point_b_x, point_b_y = point_b

    return abs(point_a_x - point_b_x) + abs(point_a_y - point_b_y)

def euclides_distance(point_a, point_b):
    return math.dist(point_a, point_b)

def combined_distance(point_a, point_b, *distance_functions):
    return sum(func(point_a, point_b) for func in distance_functions)

def manhattan_end_positon_heuristic(move, halma_game):
    player = halma_game.current_player
    (start_x, start_y), (end_x, end_y) = move

    if player == FieldType.PLAYER_WHITE:
        corner_x, corner_y = halma.BOARD_SIZE - 1, halma.BOARD_SIZE - 1
        winning_coordinates = WINNING_COORDINATES[FieldType.PLAYER_WHITE]
    else:
        corner_x, corner_y = 0, 0
        winning_coordinates = WINNING_COORDINATES[FieldType.PLAYER_BLACK]

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

def distance_state_heuristic(board, maximizing_player, distance_function):
    player_fields = {player : halma.calculate_player_fields(board, player) for player in halma.Halma.players}
    free_end_zone_fields = {player : list(set(WINNING_COORDINATES[player]) - set(player_fields[player])) for player in halma.Halma.players}
    heuristic_value = {player : 0 for player in halma.Halma.players}
    player_goal_corner = {
        FieldType.PLAYER_WHITE : (15, 15),
        FieldType.PLAYER_BLACK : (0,0)
    }

    for player in halma.Halma.players:
        for field in player_fields[player]:
            heuristic_value[player] = heuristic_value[player] + 2 * distance_function(player_goal_corner[player], player_goal_corner[halma.get_next_player(player)])
            
            if field not in WINNING_COORDINATES[player]:
                heuristic_value[player] = heuristic_value[player] - calculate_distance_to_camp(field, free_end_zone_fields[player], distance_function)
            
            heuristic_value[player] = heuristic_value[player] - distance_function(field, player_goal_corner[player])

    minimizing_player = halma.get_next_player(maximizing_player)
    heuristic_value[minimizing_player] = heuristic_value[minimizing_player] * -1
    
    return sum(heuristic_value[player] for player in halma.Halma.players)

def manhattan_state_heuristic(board, maximizing_player):
    return distance_state_heuristic(board, maximizing_player, manhattan_distance)

def euclides_state_heuristic(board, maximizing_player):
    return distance_state_heuristic(board, maximizing_player, euclides_distance)

def manhattan_euclides_state_heuristic(board, maximizing_player):
    return distance_state_heuristic(board, maximizing_player, lambda a, b : combined_distance(a, b, manhattan_distance, euclides_distance))

def adaptive_heatmap_heuristic(board, maximizing_player):
    end_zone_threshold = 3
    player_fields = {player : halma.calculate_player_fields(board, player) for player in halma.Halma.players}
    heatmap = HEATMAPS[maximizing_player]
    free_end_zone_fields = {player : list(set(WINNING_COORDINATES[player]) - set(player_fields[player])) for player in halma.Halma.players}

    if len(free_end_zone_fields[maximizing_player]) <= end_zone_threshold:
        return manhattan_state_heuristic(board, maximizing_player)
    else:
        return sum([heatmap[y][x] for x, y in list(chain.from_iterable(player_fields.values()))])

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

    print_heatmap(HEATMAPS[FieldType.PLAYER_BLACK])
    # print_heatmap(HEATMAPS[FieldType.PLAYER_BLACK])

    #print(heatmap_heuristic(board, FieldType.PLAYER_BLACK))

if __name__ == '__main__':
    main()
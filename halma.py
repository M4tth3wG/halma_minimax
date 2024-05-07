from enum import Enum
from collections import deque
import copy

class FieldType(Enum):
    EMPTY = 0
    PLAYER_WHITE = 1
    PLAYER_BLACK = 2

BOARD_SIZE = 16
NUMBER_OF_PAWNS = 19
START_AREA_SIZE = 5
STARTING_PLAYER_INDEX = 0

def calculate_camp_coordinates(player):
    coordinates = []
    
    for i in range(START_AREA_SIZE):
        if player == FieldType.PLAYER_WHITE:
            x = 0
            y = i 
        else:
            x = BOARD_SIZE - 1
            y = BOARD_SIZE - i - 1

        coordinates.append((x, y))

    for i in range(1, START_AREA_SIZE):
        for j in range(START_AREA_SIZE - i + 1):
            if player == FieldType.PLAYER_WHITE:
                x = i
                y = j
            else:
                x = BOARD_SIZE - i - 1
                y = BOARD_SIZE - j - 1

            coordinates.append((x, y))

    return coordinates

def calculate_player_fields(board, player):
    coordinates = []
    
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if board[y][x] == player:
                coordinates.append((x, y))

    return coordinates

def calculate_normal_moves(board, coordinates):
        x, y = coordinates
        moves = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                if x + i >= 0 and y + j >= 0 and x + i < BOARD_SIZE and y + j < BOARD_SIZE \
                    and board[y + j][x + i] == FieldType.EMPTY:
                    move = ((x, y), (x + i, y + j))
                    moves.append(move)
        
        return moves

def calculate_next_jump_fields(board, coordinates):
    x, y = coordinates
    fields = []

    for i in range(-1, 2):
        for j in range(-1, 2):

            if x + i >= 0 and y + j >=0 and x + i < BOARD_SIZE and y + j < BOARD_SIZE \
                and board[y + j][x + i] != FieldType.EMPTY:

                if x + 2 * i >= 0 and y + 2 * j >= 0 and x + 2 * i < BOARD_SIZE and y + 2 * j < BOARD_SIZE \
                    and board[y + 2 * j][x + 2 * i] == FieldType.EMPTY:
                        field = ((x + 2 * i, y + 2 * j))
                        fields.append(field)
    
    return fields

def calculate_jump_moves(board, coordinates):
    jump_fields = set()
    queue = deque([coordinates])

    while queue:
        field = queue.popleft()
        if field not in jump_fields:
            jump_fields.add(field)
            queue.extend(calculate_next_jump_fields(board, field))

    return [(coordinates, field) for field in jump_fields if field != coordinates]

def calculate_possible_moves(board, player):
    possible_moves = []

    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            
            if board[y][x] == player:
                normal_moves = calculate_normal_moves(board, (x, y))
                jump_moves = calculate_jump_moves(board, (x, y))

                possible_moves.extend(normal_moves)
                possible_moves.extend(jump_moves)

    return possible_moves

def check_winning_condition(board, player):
    if player == FieldType.PLAYER_WHITE:
        winning_coordinates = Halma.camp_coordinates[FieldType.PLAYER_BLACK]
    else:
        winning_coordinates = Halma.camp_coordinates[FieldType.PLAYER_WHITE]
    
    for x, y in winning_coordinates:
        if board[y][x] != player:
            return False 

    return True

def move_pawn(board, move, player):
    (start_x, start_y), (goal_x, goal_y) = move

    board[start_y][start_x] = FieldType.EMPTY
    board[goal_y][goal_x] = player

def lookahead_move(board, move, player):
    board_copy = copy.deepcopy(board)
    
    move_pawn(board_copy, move, player)

    return board_copy

def get_next_player(current_player):
    players = Halma.players
    current_index = players.index(current_player)
    return players[(current_index + 1) % len(players)]

class Halma:
    players = [FieldType.PLAYER_WHITE, FieldType.PLAYER_BLACK]
    camp_coordinates = {player : calculate_camp_coordinates(player) for player in players}

    def create_init_board(self):    
        board = [[FieldType.EMPTY for j in range(BOARD_SIZE)] for i in range(BOARD_SIZE)]

        for player, camp_coords in self.camp_coordinates.items():
            for x, y in camp_coords:
                board[y][x] = player

        return board
    
    def __init__(self) -> None:
        self.finished = False
        self.winner = None
        self.current_player = Halma.players[STARTING_PLAYER_INDEX]
        self.round = 1
        self.board = self.create_init_board()
        self.possible_moves = self.get_possible_moves()

    def get_possible_moves(self):
        return calculate_possible_moves(self.board, self.current_player)

    def perform_move(self, move):
        if self.finished:
            raise Exception("Game is finished!")

        if move not in self.possible_moves:
            raise ValueError("Move not allowed!")

        move_pawn(self.board, move, self.current_player)
        
        if check_winning_condition(self.board, self.current_player):
            self.finished = True
            self.winner = self.current_player
            return

        self.round = self.round + 1

        if self.current_player == FieldType.PLAYER_WHITE:
            self.current_player = FieldType.PLAYER_BLACK
        else:
            self.current_player = FieldType.PLAYER_WHITE

        self.possible_moves = self.get_possible_moves()

def main():
    game = Halma()
    print(check_winning_condition(game.board, game.current_player))

if __name__ == '__main__':
    main()

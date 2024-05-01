from enum import Enum
from collections import deque

class FieldType(Enum):
    EMPTY = 0
    PLAYER_WHITE = 1
    PLAYER_BLACK = 2

BOARD_SIZE = 16
NUMBER_OF_PAWNS = 19
START_AREA_SIZE = 5
STARTING_PLAYER = FieldType.PLAYER_WHITE

class Halma:
    def create_init_board():    
        board = [[FieldType.EMPTY for j in range(BOARD_SIZE)] for i in range(BOARD_SIZE)]

        for i in range(START_AREA_SIZE):
            board[0][i] = FieldType.PLAYER_WHITE
            board[-1][-i - 1] = FieldType.PLAYER_BLACK

        for i in range(1, START_AREA_SIZE):
            for j in range(START_AREA_SIZE - i + 1):
                board[i][j] = FieldType.PLAYER_WHITE
                board[-i - 1][-j - 1] = FieldType.PLAYER_BLACK

        return board
    
    def __init__(self, board=create_init_board()) -> None:
        self.finished = False
        self.winner = None
        self.current_player = STARTING_PLAYER
        self.round = 1
        self.board = board
        self.possible_moves = self.get_possible_moves(self.current_player)

    def get_normal_moves(self, coordinates):
        x, y = coordinates
        moves = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                if x + i >= 0 and y + j >= 0 and x + i < BOARD_SIZE and y + j < BOARD_SIZE \
                    and self.board[x + i][y + j] == FieldType.EMPTY:
                    move = ((x, y), (x + i, y + j))
                    moves.append(move)
        
        return moves

    def get_next_jump_fields(self, coordinates):
        x, y = coordinates
        fields = []

        for i in range(-1, 2):
            for j in range(-1, 2):

                if x + i >= 0 and y + j >=0 and x + i < BOARD_SIZE and y + j < BOARD_SIZE \
                    and self.board[x + i][y + j] != FieldType.EMPTY:

                    if x + 2 * i >= 0 and y + 2 * j >= 0 and x + 2 * i < BOARD_SIZE and y + 2 * j < BOARD_SIZE \
                        and self.board[x + 2 * i][y + 2 * j] == FieldType.EMPTY:
                            field = ((x + 2 * i, y + 2 * j))
                            fields.append(field)
        
        return fields

    def get_jump_moves(self, coordinates):
        jump_fields = set()
        queue = deque([coordinates])

        while queue:
            field = queue.popleft()
            if field not in jump_fields:
                jump_fields.add(field)
                queue.extend(self.get_next_jump_fields(field))

        return [(coordinates, field) for field in jump_fields if field != coordinates]

    def get_possible_moves(self, player):
        possible_moves = []

        for x in range(len(self.board[0])):
            for y in range(len(self.board)):
                
                if self.board[x][y] == player:
                    normal_moves = self.get_normal_moves((x, y))
                    jump_moves = self.get_jump_moves((x, y))

                    possible_moves.extend(normal_moves)
                    possible_moves.extend(jump_moves)

        return possible_moves

    def check_winning_condition(self):
        for i in range(START_AREA_SIZE):
            if self.current_player == FieldType.PLAYER_WHITE:
                x = -1
                y = -i - 1
            else:
                x = 0
                y = i
            
            if self.board[x][y] != self.current_player:
                return False

        for i in range(1, START_AREA_SIZE):
            for j in range(START_AREA_SIZE - i + 1):
                if self.current_player == FieldType.PLAYER_WHITE:
                    x = -i - 1
                    y = -j - 1
                else:
                    x = i
                    y = j

                if self.board[x][y] != self.current_player:
                    return False
        return True

    def perform_move(self, move):
        if self.finished:
            raise Exception("Game is finished!")

        if move not in self.possible_moves:
            raise ValueError("Move not allowed!")

        (start_x, start_y), (goal_x, goal_y) = move

        self.board[start_x][start_y] = FieldType.EMPTY
        self.board[goal_x][goal_y] = self.current_player
        
        if self.check_winning_condition():
            self.finished = True
            self.winner = self.current_player
            return

        self.round = self.round + 1

        if self.current_player == FieldType.PLAYER_WHITE:
            self.current_player = FieldType.PLAYER_BLACK
        else:
            self.current_player = FieldType.PLAYER_WHITE

        self.possible_moves = self.get_possible_moves(self.current_player)

from enum import Enum
from collections import deque

BOARD_SIZE = 16
NUMBER_OF_PAWNS = 19
START_AREA_SIZE = 5

class FieldType(Enum):
    EMPTY = 0
    PLAYER_WHITE = 1
    PLAYER_BLACK = 2

class Game:
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
        self.board = board

    def get_normal_moves(self, coordinates):
        x, y = coordinates
        moves = []
        length = len(self.board[0])
        height = len(self.board)

        for i in range(-1, 2):
            for j in range(-1, 2):
                if x + i >= 0 and y + j >= 0 and x + i < length and y + j < height \
                    and self.board[x + i][y + j] == FieldType.EMPTY:
                    move = ((x, y), (x + i, y + j))
                    moves.append(move)
        
        return moves

    def get_next_jump_fields(self, coordinates):
        x, y = coordinates
        fields = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                length = len(self.board[0])
                height = len(self.board)

                if x + i >= 0 and y + j >=0 and x + i < length and y + j < height \
                    and self.board[x + i][y + j] != FieldType.EMPTY:

                    if x + 2 * i >= 0 and y + 2 * j >= 0 and x + 2 * i < length and y + 2 * j < height \
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

    def print_board(self):
        for row in self.board:
            for field in row:
                print(field.value, end=" ")
            print()

game = Game()
game.print_board()
print(len(game.get_possible_moves(FieldType.PLAYER_BLACK)))
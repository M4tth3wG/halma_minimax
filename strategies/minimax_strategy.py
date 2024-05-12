from .abstract_strategy import HalmaStrategy
import halma
import copy

def get_children(node):
    board, move_acc, current_player = node
    players = halma.Halma.players
    player_index = players.index(current_player)
    next_player = players[(player_index + 1) % len(players)]
    children = []

    for move in halma.calculate_possible_moves(board, current_player):
        new_board = halma.lookahead_move(board, move, current_player)
        new_move_acc = copy.deepcopy(move_acc)
        new_move_acc.append(move)
        children.append((new_board, new_move_acc, next_player))

    return children

class MinimaxStrategy(HalmaStrategy):
    def __init__(self, heuristic, depth) -> None:
        super().__init__()
        self.heuristic = heuristic
        self.depth = depth
        self.nodes_visited = []
        self.current_nodes_visited = 0

    def minimax(self, node, depth, maximizing_player, heuristic):
        board, move_acc, current_player = node
        self.current_nodes_visited = self.current_nodes_visited + 1

        if depth == 0 or halma.check_winning_condition(board, current_player):
            return (heuristic(board, maximizing_player), move_acc[0])
        
        children = get_children(node)
        
        if maximizing_player == current_player:
            move_graded = (-1 * float('inf'), [])
            for child in children:
                move_graded = max(move_graded, self.minimax(child, depth - 1, maximizing_player, heuristic), key=lambda x: x[0])
            return move_graded
        else:
            move_graded = (float('inf'), [])
            for child in children:
                move_graded = min(move_graded, self.minimax(child, depth - 1, maximizing_player, heuristic), key=lambda x: x[0])
            return move_graded

    def move(self, halma_game):
        start_node = (halma_game.board, [], halma_game.current_player)
        
        grade, best_move = self.minimax(start_node, self.depth, halma_game.current_player, self.heuristic)
        self.nodes_visited.append(self.current_nodes_visited)
        self.current_nodes_visited = 0

        halma_game.perform_move(best_move)

        return best_move
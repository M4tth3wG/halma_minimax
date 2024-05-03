from .abstract_strategy import HalmaStrategy
from .minimax_strategy import get_children
import halma

def minimax(node, depth, maximizing_player, heuristic, alpha, beta):
    board, move_acc, current_player = node

    if depth == 0 or halma.check_winning_condition(board, current_player):
        return (heuristic(board, maximizing_player), move_acc[0])
    
    children = get_children(node)
    
    if maximizing_player == current_player:
        move_graded = (-1 * float('inf'), [])
        for child in children:
            move_graded = max(move_graded, minimax(child, depth - 1, maximizing_player, heuristic, alpha, beta), key=lambda x: x[0])
            if move_graded[0] > beta:
                break
            alpha = max(alpha, move_graded[0])
        return move_graded
    else:
        move_graded = (float('inf'), [])
        for child in children:
            move_graded = min(move_graded, minimax(child, depth - 1, maximizing_player, heuristic, alpha, beta), key=lambda x: x[0])
            if move_graded[0] < alpha:
                break
            beta = min(beta, move_graded[0])
        return move_graded

class AlphaBetaStrategy(HalmaStrategy):
    def __init__(self, heuristic, depth) -> None:
        super().__init__()
        self.heuristic = heuristic
        self.depth = depth

    def move(self, halma_game):
        start_node = (halma_game.board, [], halma_game.current_player)
        alpha, beta = -1 * float('inf'), float('inf')
        grade, best_move = minimax(start_node, self.depth, halma_game.current_player, self.heuristic, alpha, beta)

        halma_game.perform_move(best_move)

        return best_move
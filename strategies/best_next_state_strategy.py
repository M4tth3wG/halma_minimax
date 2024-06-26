from .abstract_strategy import HalmaStrategy
import halma

class BestNextStateStrategy():
    def __init__(self, heuristic) -> None:
        super().__init__()
        self.heuristic = heuristic

    def move(self, halma_game):
        moves_graded = [(self.heuristic(halma.lookahead_move(halma_game.board, move, halma_game.current_player), halma_game.current_player), move) for move in halma_game.possible_moves]
        grade, best_move = max(moves_graded, key=lambda x: x[0])

        halma_game.perform_move(best_move)

        return best_move
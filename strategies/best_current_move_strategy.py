from abstract_strategy import HalmaStrategy

class BestCurrentMoveStrategy(HalmaStrategy):
    def __init__(self, heuristic) -> None:
        super().__init__()
        self.heuristic = heuristic

    def move(self, halma_game):
        moves_graded = [(self.heuristic(move), move) for move in halma_game.possible_moves]
        best_move = max(moves_graded, key=lambda x: x[0])

        halma_game.perform_move(best_move)

        return best_move


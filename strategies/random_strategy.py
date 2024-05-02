from .abstract_strategy import HalmaStrategy
import random
from halma import FieldType
import heuristics

class RandomStrategy(HalmaStrategy):
    def move(self, halma_game):
        player = halma_game.current_player

        if player == FieldType.PLAYER_WHITE:
            camp_coordinates = heuristics.PLAYER_BLACK_WINNING_COORDINATES
        else:
            camp_coordinates = heuristics.PLAYER_WHITE_WINNING_COORDINATES

        camp_exit_moves = [(start, end) for start, end in halma_game.possible_moves if start in camp_coordinates]
        camp_exit_moves_graded = [(1, (start, end)) if end not in camp_coordinates else (0, (start, end)) for start, end in camp_exit_moves]

        if camp_exit_moves_graded:
            _, move = max(camp_exit_moves_graded, key=lambda x: x[0])
            halma_game.perform_move(move)
            return move

        desired_moves = [(start, end) for start, end in halma_game.possible_moves if end not in camp_coordinates]
        random_move = random.choice(desired_moves)
        halma_game.perform_move(random_move)

        return random_move
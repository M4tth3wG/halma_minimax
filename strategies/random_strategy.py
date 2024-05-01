from .abstract_strategy import HalmaStrategy
import random

class RandomStrategy(HalmaStrategy):
    def move(self, halma_game):
        random_move = random.choice(halma_game.possible_moves)

        halma_game.perform_move(random_move)

        return random_move
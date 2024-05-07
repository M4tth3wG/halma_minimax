from .abstract_strategy import HalmaStrategy
from halma import FieldType
import sys
import re

class InputStrategy(HalmaStrategy):
    def __init__(self, source=sys.__stdin__) -> None:
        super().__init__()
        self.source = source
    
    def move(self, halma_game):
        sys.stdin = self.source
        punctuation_pattern = r'[\s,;:.!?()=<>]+'

        move_input = input("Move: ")

        move_input = re.sub(f"^{punctuation_pattern}|{punctuation_pattern}$", "", move_input)
        move = re.split(punctuation_pattern, move_input)
        move = tuple([(int(move[i]), int(move[i+1])) for i in range(0, len(move), 2)])

        try:
            halma_game.perform_move(move)
        except Exception as error:
            print(error)
            self.move(halma_game)

        return move
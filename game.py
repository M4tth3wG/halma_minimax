from halma import Halma, FieldType

class Game:
    def __init__(self, player_white_strategy, player_black_strategy):
        self.halma = Halma()
        self.last_move = None
        self.current_player = self.halma.current_player
        self.player_white_strategy = player_white_strategy
        self.player_black_strategy = player_black_strategy

    def next_move(self):
        if not self.halma.finished:
            if self.halma.current_player == FieldType.PLAYER_WHITE:
                self.last_move = self.player_white_strategy.move(self.halma)
            else:
                self.last_move = self.player_black_strategy.move(self.halma)

            self.current_player = self.halma.current_player
        else:
            raise Exception("Game is finished!")

        
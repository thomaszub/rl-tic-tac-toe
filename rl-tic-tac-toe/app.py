from copy import deepcopy

from tqdm import trange

from agent_player import QAgentPlayer, RandomAgentPlayer
from domain.marker import Marker
from game import Game
from human_player import HumanPlayer


def train(playerO: QAgentPlayer) -> None:
    num_won = 0
    num_lost = 0

    playerX = RandomAgentPlayer(Marker.X)
    playerO.training_mode(True)
    with trange(1, 20000) as tr:
        for _ in tr:
            game = Game((playerX, playerO), False)
            result = game.start()
            if result == Marker.X:
                num_lost += 1
            elif result == Marker.O:
                num_won += 1

            tr.set_postfix(num_lost=num_lost, num_won=num_won)
    playerO.training_mode(False)


def main():
    playerX = HumanPlayer(Marker.X)

    playerO = QAgentPlayer(Marker.O, 0.1, 1024, 32, 8)
    train(playerO)
    game = Game((playerX, playerO))
    game.start()


if __name__ == "__main__":
    main()

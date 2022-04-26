from tqdm import trange

from agent_player import QAgentPlayer, RandomAgentPlayer
from domain.marker import Marker
from game import Game
from human_player import HumanPlayer


def train(playerO: QAgentPlayer) -> None:
    num_won = 0
    num_lost = 0

    playerX = RandomAgentPlayer(Marker.Cross)
    playerO.training_mode(True)
    with trange(0, 50000) as tr:
        for _ in tr:
            game = Game((playerX, playerO), False)
            result = game.start()
            if result == Marker.Cross:
                num_lost += 1
            elif result == Marker.Circle:
                num_won += 1

            tr.set_postfix(num_lost=num_lost, num_won=num_won)
    playerO.training_mode(False)


def main():
    filename = "QAgentPlayer.pickle"
    try:
        with open(filename, "rb") as f:
            print(f"Info: Loading agent from {filename}")
            playerO = QAgentPlayer.load(f)
    except FileNotFoundError:
        print("Info: Creating a new agent")
        playerO = QAgentPlayer(Marker.Circle, 0.1, 2048, 32, 8)

    train(playerO)
    playerX = HumanPlayer(Marker.Cross)
    game = Game((playerX, playerO))
    game.start()

    try:
        with open(filename, "wb") as f:
            print(f"Info: Saving agent to {filename}")
            playerO.save(f)
    except OSError:
        print(f"Error: Could not save agent to {filename}")


if __name__ == "__main__":
    main()

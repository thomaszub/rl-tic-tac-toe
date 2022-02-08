from enum import Enum


class GameResult(Enum):
    Won = 1
    Lost = -1
    Draw = 0

    def opposite(self) -> "GameResult":
        if self == GameResult.Won:
            return GameResult.Lost
        if self == GameResult.Lost:
            return GameResult.Won
        return GameResult.Draw

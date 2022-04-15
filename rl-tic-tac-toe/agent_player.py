import pickle
from typing import BinaryIO, Dict, List, Optional, Tuple

import numpy as np

from domain.board import Board
from domain.gameresult import GameResult
from domain.marker import Marker
from domain.player import Player

_State = List[List[Optional[Marker]]]
_StateHash = int


def _state_hash(state: _State) -> int:
    flatten = tuple([field for col in state for field in col])
    return hash(flatten)


class QAgentPlayer(Player):
    _state: _State
    _action_values: Dict[_StateHash, Dict[Tuple[int, int], float]]

    def __init__(self, marker: Marker, epsilon: float, learning_rate: float) -> None:
        super().__init__(marker)
        self._state = []
        self._action_values = {}
        self._epsilon = epsilon
        self._learning_rate = learning_rate
        self._training_mode = False

    def training_mode(self, flag: bool) -> None:
        self._training_mode = flag

    def take_turn(self, board: Board) -> Tuple[int, int]:
        self._state = board.get_fields()
        free_positions = board.get_free_positions()
        if self._training_mode and np.random.random() < self._epsilon:
            action = np.random.choice(free_positions)
        else:
            action_values_for_state = self._action_values_for_state(
                self._state, free_positions
            )
            action = max(action_values_for_state, key=action_values_for_state.get)
        self._action = action
        return action

    def board_changed(
        self, new_board: Board, game_result: Optional[GameResult]
    ) -> None:
        if game_result == None:
            new_state = new_board.get_fields()
            free_positions = new_board.get_free_positions()
            action_values_for_new_state = self._action_values_for_state(
                new_state, free_positions
            )
            target = max(action_values_for_new_state.values())
        else:
            target = float(game_result.value)
        action_values_for_state = self._action_values.get(_state_hash(self._state))
        action_values_for_state[self._action] += self._learning_rate * (
            target - action_values_for_state[self._action]
        )

    def _action_values_for_state(
        self, state: _State, free_positions: List[Tuple[int, int]]
    ) -> Dict[Tuple[int, int], float]:
        state_hash = _state_hash(state)
        action_values_for_state = self._action_values.get(state_hash)
        if action_values_for_state == None:
            init_values = {action: 0.0 for action in free_positions}
            self._action_values[state_hash] = init_values
            action_values_for_state = init_values
        return action_values_for_state

    def save(self, file: BinaryIO) -> None:
        pickle.dump(self, file)

    @staticmethod
    def load(file: BinaryIO) -> "QAgentPlayer":
        return pickle.load(file)

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"Q-Agent {self.marker()}"

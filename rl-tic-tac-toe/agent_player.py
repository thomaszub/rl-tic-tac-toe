import pickle
from copy import deepcopy
from typing import BinaryIO, Dict, List, Optional, Tuple

import numpy as np
import torch
from torch.utils.data import DataLoader, TensorDataset

from domain.board import Board
from domain.gameresult import GameResult
from domain.marker import Marker
from domain.player import Player


class RandomAgentPlayer(Player):
    def __init__(
        self,
        marker: Marker,
    ) -> None:
        super().__init__(marker)

    def take_turn(self, board: Board) -> Tuple[int, int]:
        free_positions = board.get_free_positions()
        return free_positions[np.random.choice(range(0, len(free_positions)))]

    def board_changed(
        self, new_board: Board, game_result: Optional[GameResult]
    ) -> None:
        pass

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"Random Agent {self.marker()}"


class QAgentPlayer(Player):
    def __init__(
        self,
        marker: Marker,
        epsilon: float,
        learning_rate: float,
        replay_buffer_size: int,
        batch_size: int,
        update_target_after_num_buffers: int,
    ) -> None:
        super().__init__(marker)
        self._state = None
        self._epsilon = epsilon
        self._learning_rate = learning_rate
        self._training_mode = False
        self._replay_buffer_input = []
        self._replay_buffer_target = []
        self._replay_buffer_size = replay_buffer_size
        self._batch_size = batch_size
        self._update_target_after_num_buffers = update_target_after_num_buffers
        self._num_trainings = 0
        self._model = torch.nn.Sequential(
            torch.nn.Linear(9 + 9, 32),
            torch.nn.ReLU(),
            torch.nn.Linear(32, 16),
            torch.nn.ReLU(),
            torch.nn.Linear(16, 1),
        )
        self._target_model = deepcopy(self._model)
        self._loss = torch.nn.MSELoss()
        self._optimizer = torch.optim.Adam(params=self._model.parameters())

    def training_mode(self, flag: bool) -> None:
        self._training_mode = flag
        if not self._training_mode:
            self._replay_buffer_input = []
            self._replay_buffer_target = []

    def take_turn(self, board: Board) -> Tuple[int, int]:
        self._state = self._board_encoded(board)
        free_positions = board.get_free_positions()
        if self._training_mode and np.random.random() < self._epsilon:
            action = free_positions[np.random.choice(range(0, len(free_positions)))]
        else:
            action_values = [
                self._predict(self._model, self._state, action)
                for action in free_positions
            ]
            action = free_positions[np.argmax(action_values)]
        self._action = self._field_one_hot_encoded(action)
        return action

    @torch.no_grad()
    def _predict(
        self, model: torch.nn.Module, state: List[int], action: Tuple[int, int]
    ) -> float:
        enc_action = self._field_one_hot_encoded(action)
        input = torch.tensor(np.concatenate((state, enc_action))).float().view(1, -1)
        return model(input).detach().numpy()

    def _board_encoded(self, board: Board) -> List[int]:
        def field_to_int(field: Optional[Marker]) -> int:
            if field == None:
                return 0
            elif field == self.marker():
                return 1
            else:
                return -1

        return [field_to_int(field) for col in board.get_fields() for field in col]

    def _field_one_hot_encoded(self, field: Tuple[int, int]) -> List[int]:
        one_hot = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        one_hot[field[1] - 1 + 3 * (field[0] - 1)] = 1
        return one_hot

    def board_changed(
        self, new_board: Board, game_result: Optional[GameResult]
    ) -> None:
        self._replay_buffer_input.append(np.concatenate((self._state, self._action)))

        if game_result == None:
            next_state = self._board_encoded(new_board)
            next_free_positions = new_board.get_free_positions()
            next_action_values = [
                self._predict(self._target_model, next_state, action)
                for action in next_free_positions
            ]
            target = np.max(next_action_values)
        else:
            target = game_result.value

        self._replay_buffer_target.append([target])

        if len(self._replay_buffer_input) >= self._replay_buffer_size:
            self._num_trainings += 1
            self._train()
            self._replay_buffer_input = []
            self._replay_buffer_target = []

        if self._num_trainings >= self._update_target_after_num_buffers:
            self._num_trainings = 0
            self._target_model = deepcopy(self._model)

    def _train(self) -> None:
        input = torch.tensor(np.array(self._replay_buffer_input)).float()
        target = torch.tensor(np.array(self._replay_buffer_target)).float()
        dataset = TensorDataset(input, target)
        loader = DataLoader(dataset, batch_size=self._batch_size, shuffle=True)
        for X, y in loader:
            self._optimizer.zero_grad()
            self._loss(self._model(X), y).backward()
            self._optimizer.step()

    def save(self, file: BinaryIO) -> None:
        self._replay_buffer_input = []
        self._replay_buffer_target = []
        pickle.dump(self, file)

    @staticmethod
    def load(file: BinaryIO) -> "QAgentPlayer":
        return pickle.load(file)

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"Q-Agent {self.marker()}"

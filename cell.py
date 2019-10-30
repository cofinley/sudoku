from typing import Set


class Cell:
    def __init__(self, row: int, col: int, grid: int, value: int, is_immutable=False):
        self.row = row
        self.col = col
        self.grid = grid
        self._value = value
        self.is_immutable = is_immutable
        if self.value == 0:
            self._possibilities = set(range(1, 10))
        else:
            self._possibilities = set()

    @property
    def is_empty(self):
        return self.value == 0

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if value in range(0, 10) and not self.is_immutable:
            self._value = value

    @property
    def possibilities(self):
        return self._possibilities

    @possibilities.setter
    def possibilities(self, possibilities: Set[int]):
        self._possibilities = possibilities

    def __repr__(self):
        if self.is_empty:
            return '.'
        else:
            return str(self.value)

from typing import List

from cell import Cell


class UniqueCellArea:
    allowed_numbers = list(range(1, 10))

    def __init__(self, number: int, cells: List[Cell]):
        self.number = number
        self.cells = cells

    def get_missing(self):
        return set([num for num in __class__.allowed_numbers if num not in [cell.value for cell in self.cells]])

    def get_present(self):
        return set(__class__.allowed_numbers) - self.get_missing()

    def check(self):
        return set([cell.value for cell in self.cells]) == set(__class__.allowed_numbers) and not self.has_duplicates()

    def has_duplicates(self):
        return any([cell.value for cell in self.cells if not cell.is_empty].count(x) > 1 for x in __class__.allowed_numbers)

    def __repr__(self):
        return str(self.__name__) + " " + str(self.number) + ": " + str(self.cells)


class Row(UniqueCellArea):
    __name__ = "Row"


class Col(UniqueCellArea):
    __name__ = "Col"


class Grid(UniqueCellArea):
    __name__ = "Grid"

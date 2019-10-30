import functools

from cell import Cell
from cell_area import Row, Col, Grid


class Puzzle:
    def __init__(self, puzzle_string):
        self._rows = {}
        self._cols = {}
        self._grids = {}
        self._cell_list = []
        self.parse_puzzle(puzzle_string)
        self.count = 0

    def parse_puzzle(self, puzzle_string):
        rows = {}
        cols = {}
        grids = {}
        for row_num in range(9):
            for col_num in range(9):
                string_value = puzzle_string[row_num*9 + col_num]
                cell_value = 0 if string_value == '.' else int(string_value)
                is_immutable = bool(cell_value)

                if 0 <= row_num <= 2:
                    if 0 <= col_num <= 2:
                        grid_num = 0
                    elif 3 <= col_num <= 5:
                        grid_num = 1
                    else:
                        grid_num = 2
                elif 3 <= row_num <= 5:
                    if 0 <= col_num <= 2:
                        grid_num = 3
                    elif 3 <= col_num <= 5:
                        grid_num = 4
                    else:
                        grid_num = 5
                else:
                    if 0 <= col_num <= 2:
                        grid_num = 6
                    elif 3 <= col_num <= 5:
                        grid_num = 7
                    else:
                        grid_num = 8

                cell = Cell(row_num, col_num, grid_num, int(cell_value), is_immutable)

                rows.setdefault(row_num, []).append(cell)
                cols.setdefault(col_num, []).append(cell)
                grids.setdefault(grid_num, []).append(cell)
                self._cell_list.append(cell)

        for row_num, row_cells in rows.items():
            self._rows[row_num] = Row(row_num, row_cells)
        for col_num, col_cells in cols.items():
            self._cols[col_num] = Col(col_num, col_cells)
        for grid_num, grid_cells in grids.items():
            self._grids[grid_num] = Grid(grid_num, grid_cells)

    def solve(self):
        self.get_possibilities()
        self.check_unique_possibilities_in_area(self._rows)
        self.check_unique_possibilities_in_area(self._cols)
        self.check_unique_possibilities_in_area(self._grids)
        if self.is_solved():
            return True
        else:
            return self.dfs([cell for cell in self._cell_list if cell.is_empty])

    def is_solved(self):
        grid_check = all(grid.check() for grid in self._grids.values())
        row_check = all(row.check() for row in self._rows.values())
        col_check = all(col.check() for col in self._cols.values())
        return grid_check and row_check and col_check

    def get_possibilities(self):
        for row_num, row in self._rows.items():
            for cell in row.cells:
                if not cell.is_empty:
                    continue
                cell_col = self._cols[cell.col]
                cell_grid = self._grids[cell.grid]
                present_in_col = cell_col.get_present()
                present_in_row = row.get_present()
                present_in_grid = cell_grid.get_present()
                present_in_all = present_in_col.union(present_in_row).union(present_in_grid)
                cell.possibilities = set(cell.possibilities) - present_in_all
                if len(cell.possibilities) == 1:
                    value = cell.possibilities.pop()
                    if not self.has_peer_conflicts(cell, value):
                        cell.value = value
                        self.remove_possibilities_from_peers(cell)

    def check_unique_possibilities_in_area(self, areas: dict):
        for area_rid_num, area in areas.items():
            for cell in area.cells:

                if len(cell.possibilities) == 1:
                    cell.value = cell.possibilities.pop()

                if area.check():
                    break
                if not cell.is_empty:
                    continue

                other_cells_in_area = [c for c in area.cells if c != cell and c.is_empty]
                other_cell_possibilities = [p for p in [other_cell.possibilities for other_cell in other_cells_in_area]]
                if not other_cell_possibilities:
                    value = area.get_missing().pop()
                    if not self.has_peer_conflicts(cell, value):
                        cell.value = value
                        self.remove_possibilities_from_peers(cell)
                        continue

                other_cell_possibilities = functools.reduce(lambda x, y: {*x, *y}, other_cell_possibilities)
                unique_possibilities_for_cell = set([p for p in cell.possibilities if p not in other_cell_possibilities])
                if len(unique_possibilities_for_cell) == 1:
                    value = unique_possibilities_for_cell.pop()
                    if not self.has_peer_conflicts(cell, value):
                        cell.value = value
                        self.remove_possibilities_from_peers(cell)

    def dfs(self, empty_cell_list):
        # try one
        # check
        # if pass, recur on tail
        # if fail, back up, try next
        self.count += 1
        if self.is_solved():
            return True
        for cell in empty_cell_list:
            for possibility in cell.possibilities:
                if self.has_peer_conflicts(cell, possibility):
                    continue
                cell.value = possibility
                if self.dfs(empty_cell_list[1:]):
                    return True
                else:
                    # Set back to empty to reset any potential conflict checks
                    cell.value = 0
            # All possibilities exhausted, something wrong with previous cell choices, back up using return False
            return False
        return False

    def get_peers(self, cell):
        cell_row = self._rows[cell.row]
        cell_col = self._cols[cell.col]
        cell_grid = self._grids[cell.grid]
        return [c for c in set(cell_row.cells).union(set(cell_col.cells)).union(set(cell_grid.cells)) if c != cell]

    def has_peer_conflicts(self, cell, value):
        peers = self.get_peers(cell)
        peer_values = [c.value for c in peers if not c.is_empty]
        return value in peer_values

    def remove_possibilities_from_peers(self, cell):
        peers = self.get_peers(cell)
        all_cells = [c for c in peers if c.is_empty]
        for c in all_cells:
            c.possibilities.discard(cell.value)

    def __repr__(self):
        output = []
        for row_num, row in self._rows.items():
            if row_num % 3 == 0:
                output.append('----+---+----')

            line = []
            for col_num, cell in enumerate(row.cells, 1):
                if col_num % 3 == 1:
                    line.append("|")
                line.append(str(cell))
                if col_num == 9:
                    line.append('|')
            output.append("".join(line))

        output.append('----+---+----')
        return "\n".join(output)

from puzzle import Puzzle
from cell import Cell
from cell_area import UniqueCellArea

import unittest


class TestCellAreaMethods(unittest.TestCase):
    def setUp(self):
        cells = []
        cell_string = '1.73...5.'
        for i, cell_value in enumerate(cell_string):
            int_val = 0 if cell_value == '.' else int(cell_value)
            c = Cell(0, i, 0, int_val)
            cells.append(c)
        self.u = UniqueCellArea(0, cells)

    def test_get_missing(self):
        self.assertSetEqual({2, 4, 6, 8, 9}, self.u.get_missing())

    def test_get_present(self):
        self.assertSetEqual({1, 3, 5, 7}, self.u.get_present())

    def test_has_duplicates(self):
        self.assertFalse(self.u.has_duplicates())

    def test_has_duplicates_positive(self):
        self.u.cells[1].value = 7
        self.assertTrue(self.u.has_duplicates())

    def test_check_does_not_pass(self):
        self.assertFalse(self.u.check())

    def test_check_does_not_pass_with_duplicates(self):
        self.u.cells[1].value = 7
        self.u.cells[4].value = 4
        self.u.cells[5].value = 6
        self.u.cells[6].value = 8
        self.u.cells[8].value = 9
        self.assertFalse(self.u.check())

    def test_check_passes(self):
        self.u.cells[1].value = 2
        self.u.cells[4].value = 4
        self.u.cells[5].value = 6
        self.u.cells[6].value = 8
        self.u.cells[8].value = 9
        self.assertTrue(self.u.check())


class TestPuzzles(unittest.TestCase):
    def setUp(self):
        self.puzzle_string = \
        ".....45.." \
        "4.8...6.." \
        "13..8...." \
        "...8.9..5" \
        "7...1...2" \
        "3..6.5..." \
        "....6..14" \
        "..4...7.8" \
        "..17....."

    def test_solve_puzzle(self):
        p = Puzzle(self.puzzle_string)
        solved = p.solve()
        actual = \
        "----+---+----\n" \
        "|967|234|581|\n" \
        "|458|197|623|\n" \
        "|132|586|479|\n" \
        "----+---+----\n" \
        "|246|879|135|\n" \
        "|785|413|962|\n" \
        "|319|625|847|\n" \
        "----+---+----\n" \
        "|573|968|214|\n" \
        "|624|351|798|\n" \
        "|891|742|356|\n" \
        "----+---+----"
        if solved:
            self.assertEqual(str(p), actual)
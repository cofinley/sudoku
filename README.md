# Sudoku w/Python

I like Sudoku but I wanted to try automating it. This project combines typical human strategies (e.g. check row, column, grid for number 1-9) and depth-first search (i.e. recursively try all remaining number combinations until the puzzle is solved). Puzzles (and their numbers) are taken from https://websudoku.com.

## Usage

Puzzles go into `./puzzles/` in text form like so:

```
.....45..
4.8...6..
13..8....
...8.9..5
7...1...2
3..6.5...
....6..14
..4...7.8
..17.....
```

Each period represents a blank space.

Save it (e.g. `a-really-hard-puzzle.txt`) and enter the filename (without extension) as the `puzzle_number` in `run.py` like so:

```
puzzle_file = "a-really-hard-puzzle"
```

Run `python3 run.py` or test with `python3 -m unittest tests.py`.

The program will spit out the result:

```
----+---+----
|967|234|581|
|458|197|623|
|132|586|479|
----+---+----
|246|879|135|
|785|413|962|
|319|625|847|
----+---+----
|573|968|214|
|624|351|798|
|891|742|356|
----+---+----
```
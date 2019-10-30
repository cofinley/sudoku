from puzzle import Puzzle

puzzle_path = "./puzzles/"


if __name__ == "__main__":
    puzzle_string = ""
    puzzle_file = "evil-5073457249"
    with open(puzzle_path + str(puzzle_file) + ".txt") as f:
        puzzle_string = "".join(line.strip() for line in f)
    p = Puzzle(puzzle_string)
    print(p)
    print("\n")
    solved = p.solve()
    if solved:
        print(p)

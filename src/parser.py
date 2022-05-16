# Puzzle format:
'''
# This puzzle is solvable
4
 4  14   6   0  
11   8  13  10  
 9   7   1   2  
15   3  12   5  
'''


def run_parser(file_name: str) -> tuple[int]:
    try:
        with open(file_name, "r") as file:
            file.readline()  # skip comment
            size = int(file.readline())
            if size < 3:
                raise ValueError("Error! Row width cannot be less than 3")

            grid = []
            for line in file:
                row = line.split()
                while row and not row[-1].isdigit():
                    row.pop()
                if len(row) != size:
                    raise ValueError("Error! Incorrect matrix's row length")
                grid += [int(val) for val in row]

            values = set()
            for val in grid:
                values.add(val)

            for i in range(1, size * size):
                if i not in values:
                    raise ValueError(
                        "Error! Numbers should be in [1, n], but {} is missing".format(i))
            return tuple(grid)
    except ValueError:
        raise
    except OSError:
        raise RuntimeError("Error! Something wrong with the file")

import math


def manhattan_distance(grid: tuple[int], x1: int, y1: int, x2: int, y2: int, mapping_curr_pos_to_next: dict[tuple[int], tuple[int]]) -> int:
    size = int(len(grid) ** 0.5)
    current_idx = x1 * size + y1
    if grid[current_idx] == 0:
        return 0
    return abs(x1 - x2) + abs(y1 - y2)


def euclidean_distance(grid: tuple[int], x1: int, y1: int, x2: int, y2: int, iteration_order: dict) -> int:
    size = int(len(grid) ** 0.5)
    current_idx = x1 * size + y1
    if grid[current_idx] == 0:
        return 0
    return math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))


def out_of_place(grid: tuple[int], x1: int, y1: int, x2: int, y2: int, iteration_order: dict) -> int:
    size = int(len(grid) ** 0.5)
    current_idx = x1 * size + y1
    if grid[current_idx] == 0:
        return 0
    return (x1, y1) != (x2, y2)


def out_of_row_and_col(grid: tuple[int], x1: int, y1: int, x2: int, y2: int, iteration_order: dict) -> int:
    size = int(len(grid) ** 0.5)
    current_idx = x1 * size + y1
    if grid[current_idx] == 0:
        return 0
    return (x1 != x2) + (y1 != y2)


def nilsson_sequence_score(grid: tuple[int], x1: int, y1: int, x2: int, y2: int, iteration_order: dict) -> int:
    score = manhattan_distance(grid, x1, y1, x2, y2, iteration_order)
    size = int(len(grid) ** 0.5)
    current_idx = x1 * size + y1
    middle = (len(grid) + 1) // 2
    if current_idx == middle:
        score += 3
    else:
        next_i, next_j = iteration_order[(x1, y1)]
        next_idx = next_i * size + next_j
        score += 6 if grid[current_idx] + 1 != grid[next_idx] else 0
    return score

from src.State import State


def generate_new_states(current_state: State, puzzle_info: dict, matrix_traversal_info: dict, puzzle_params: dict, ) -> list[State]:
    new_states = []
    size = puzzle_info['size']

    try:
        idx = current_state.grid.index(0)
    except:
        raise ValueError("Error! Empty cell should be present in the grid")

    i, j = idx // size, idx - (idx // size) * size
    for di, dj in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        new_i = i + di
        new_j = j + dj
        if 0 <= new_i < size and 0 <= new_j < size:
            new_grid = list(current_state.grid)
            new_idx = new_i * size + new_j
            new_grid[idx], new_grid[new_idx] = new_grid[new_idx], new_grid[idx]
            new_states.append(State(
                tuple(new_grid), puzzle_info, matrix_traversal_info, puzzle_params, current_state.g + 1))
    return new_states

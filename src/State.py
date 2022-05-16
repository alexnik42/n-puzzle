class State:
    def __init__(self, grid: tuple[int], puzzle_info: dict, matrix_traversal_info: dict, puzzle_params: dict, g: int = 0) -> None:
        self.grid = grid
        self.puzzle_info = puzzle_info
        self.matrix_traversal_info = matrix_traversal_info
        self.puzzle_params = puzzle_params

        self.g = g if not self.puzzle_params['uniform_cost_search_only'] else 0
        self.h = self._get_h_value(
        ) if not self.puzzle_params['greedy_search_only'] else 0

    def __lt__(self, other) -> bool:
        return self.g + self.h < other.g + other.h

    def _get_h_value(self) -> int:
        size = self.puzzle_info['size']
        h = 0
        for idx, val in enumerate(self.grid):
            i, j = idx // size, idx - (idx // size) * size
            target_value_idx = self.matrix_traversal_info['values_target_positions'][val]
            target_i, target_j = target_value_idx // size, target_value_idx - \
                (target_value_idx // size) * size
            h += self.puzzle_params['heuristic_function'](
                self.grid, i, j, target_i, target_j, self.matrix_traversal_info['iteration_order'])
        return h

import pytest
import os
import src.parser as puzzle_parser
from src.Solution import Solution
import src.helpers.grid_helpers as grid_helpers


def test_puzzle_not_valid_grid() -> None:
    for grid in ['non_valid_grid_small', 'non_valid_grid_wrong_size',
                 'non_valid_grid_different_rows', 'non_valid_grid_duplicates']:

        with pytest.raises(Exception) as exc_info:
            puzzle_parser.run_parser(
                "../resources/puzzles/{}.txt".format(grid))

        assert exc_info.value is not None


def test_puzzle_solvability_unsolvable() -> None:
    args = {
        'visualizer': False,
        'uniform_cost_search_only': False,
        'greedy_search_only': False,
        'non_admissible_heuristics': False,
        'heuristic_function': 'manhattan'
    }

    for size in range(3, 20):
        os.system(
            "python3 ../src/generator.py -u {} > ../tests/test.txt".format(size))

        initial_grid = puzzle_parser.run_parser('test.txt')
        solution = Solution(initial_grid, args)

        assert not solution.is_puzzle_solvable()

    os.remove("../tests/test.txt")


def test_puzzle_solvability_solvable() -> None:
    args = {
        'visualizer': False,
        'uniform_cost_search_only': False,
        'greedy_search_only': False,
        'non_admissible_heuristics': False,
        'heuristic_function': 'manhattan'
    }

    for size in range(3, 20):
        os.system(
            "python3 ../src/generator.py -s {} > ../tests/test.txt".format(size))

        initial_grid = puzzle_parser.run_parser('test.txt')
        solution = Solution(initial_grid, args)

        assert solution.is_puzzle_solvable()

    os.remove("../tests/test.txt")


def test_puzzle_solution_admissible_heuristics() -> None:
    args = {
        'visualizer': False,
        'uniform_cost_search_only': False,
        'greedy_search_only': False,
        'non_admissible_heuristics': False,
        'heuristic_function': 'manhattan'
    }

    for heuristics in ['manhattan', 'euclid', 'out_of_place', 'out_of_row_and_col']:
        args['heuristic_function'] = heuristics
        for _ in range(3):
            os.system(
                "python3 ../src/generator.py -s 3 > ../tests/test.txt")

            initial_grid = puzzle_parser.run_parser('test.txt')
            target_grid = grid_helpers.generate_target_snail_matrix(3)
            solution = Solution(initial_grid, args)
            solution.solve_puzzle()
            solution.solution_info['sequence'][-1] == target_grid

            assert solution.is_puzzle_solvable()

    os.remove("../tests/test.txt")


def test_puzzle_solution_non_admissible_heuristics() -> None:
    args = {
        'visualizer': False,
        'uniform_cost_search_only': False,
        'greedy_search_only': False,
        'non_admissible_heuristics': True,
        'heuristic_function': 'manhattan'
    }

    for size in range(3, 5):
        for _ in range(3):
            os.system(
                "python3 ../src/generator.py -s {} > ../tests/test.txt".format(size))

            initial_grid = puzzle_parser.run_parser('test.txt')
            target_grid = grid_helpers.generate_target_snail_matrix(size)
            solution = Solution(initial_grid, args)
            solution.solve_puzzle()
            solution.solution_info['sequence'][-1] == target_grid

            assert solution.is_puzzle_solvable()

    os.remove("../tests/test.txt")


def test_puzzle_solution_uniform_cost_search_only() -> None:
    args = {
        'visualizer': False,
        'uniform_cost_search_only': False,
        'greedy_search_only': True,
        'non_admissible_heuristics': False,
        'heuristic_function': 'manhattan'
    }

    for heuristics in ['manhattan', 'euclid', 'out_of_place', 'out_of_row_and_col']:
        args['heuristic_function'] = heuristics
        for _ in range(3):
            os.system(
                "python3 ../src/generator.py -s 3 > ../tests/test.txt")

            initial_grid = puzzle_parser.run_parser('test.txt')
            target_grid = grid_helpers.generate_target_snail_matrix(3)
            solution = Solution(initial_grid, args)
            solution.solve_puzzle()
            solution.solution_info['sequence'][-1] == target_grid

            assert solution.is_puzzle_solvable()

    os.remove("../tests/test.txt")


def test_puzzle_solution_greedy_search_only() -> None:
    args = {
        'visualizer': False,
        'uniform_cost_search_only': False,
        'greedy_search_only': True,
        'non_admissible_heuristics': False,
        'heuristic_function': 'manhattan'
    }

    for _ in range(3):
        os.system(
            "python3 ../src/generator.py -s 3 > ../tests/test.txt")

        initial_grid = puzzle_parser.run_parser('test.txt')
        target_grid = grid_helpers.generate_target_snail_matrix(3)
        solution = Solution(initial_grid, args)
        solution.solve_puzzle()
        solution.solution_info['sequence'][-1] == target_grid

        assert solution.is_puzzle_solvable()

    os.remove("../tests/test.txt")

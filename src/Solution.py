# https://stackoverflow.com/questions/55454496/is-it-possible-to-check-if-the-15-puzzle-is-solvable-with-a-different-goal-state

from heapq import heappush, heappop
import colorama
from termcolor import colored

from src.State import State
import src.helpers.utils as utils
import src.helpers.grid_helpers as grid_helpers
import src.heuristics.functions as heuristics


class Solution:
    def __init__(self, initial_grid: tuple[int], args: dict) -> None:
        self.puzzle_info = {}
        self.solution_info = {}
        self.matrix_traversal_info = {}
        self.puzzle_params = {}

        self._parse_arguments(initial_grid, args)

    def _parse_arguments(self, initial_grid: tuple[int], args: dict) -> None:
        self.puzzle_info = {
            'initial_grid': initial_grid,
            'size': int(len(initial_grid) ** 0.5),
            'target_grid': grid_helpers.generate_target_snail_matrix(int(len(initial_grid) ** 0.5))
        }

        self.solution_info = {
            'selected_states': 1,  # at least we keep initial grid in memory
            'max_states_in_memory': 1,  # at least we keep initial grid in memory
            'moves': 0,
            'sequence': []
        }

        self.matrix_traversal_info = {
            'parents_data': {initial_grid: None},
            'iteration_order': grid_helpers.generate_snail_matrix_iteration_order(self.puzzle_info['size']),
            'values_target_positions': {self.puzzle_info['target_grid'][idx]: idx for idx in range(len(self.puzzle_info['target_grid']))}
        }

        self.puzzle_params = {
            'visualizer': False,
            'uniform_cost_search_only': False,
            'greedy_search_only': False,
            'non_admissible_heuristics': False,
            'heuristic_name': args['heuristic_function'] if 'heuristic_function' in args else 'Not applicable',
            'heuristic_function': None
        }

        if args['greedy_search_only']:
            self.puzzle_params['greedy_search_only'] = True
        elif args['non_admissible_heuristics']:
            self.puzzle_params['non_admissible_heuristics'] = True
            self.puzzle_params['heuristic_function'] = heuristics.nilsson_sequence_score
        else:
            if args['uniform_cost_search_only']:
                self.puzzle_params['uniform_cost_search_only'] = True

            if args['heuristic_function'] == 'manhattan':
                self.puzzle_params['heuristic_function'] = heuristics.manhattan_distance
            elif args['heuristic_function'] == 'euclid':
                self.puzzle_params['heuristic_function'] = heuristics.euclidean_distance
            elif args['heuristic_function'] == 'out_of_place':
                self.puzzle_params['heuristic_function'] = heuristics.out_of_place
            elif args['heuristic_function'] == 'out_of_row_and_col':
                self.puzzle_params['heuristic_function'] = heuristics.out_of_row_and_col
            elif args['heuristic_function'] == 'nilsson':
                self.puzzle_params['heuristic_function'] = heuristics.nilsson_sequence_score
            else:
                raise SyntaxError("Error! Heuristic function '{}' is not supported".format(
                    args['heuristic_function']))

        if args['visualizer']:
            self.puzzle_params['visualizer'] = True

    def _create_sequence(self) -> None:
        current_grid = self.puzzle_info['target_grid']
        while current_grid:
            self.solution_info['sequence'].append(current_grid)
            current_grid = self.matrix_traversal_info['parents_data'][current_grid]
        self.solution_info['sequence'].reverse()

    def is_puzzle_solvable(self) -> bool:
        size = self.puzzle_info['size']
        initial_grid = self.puzzle_info['initial_grid']
        target_grid = self.puzzle_info['target_grid']

        initial_grid_inversions = 0
        for i in range(len(initial_grid)):
            for j in range(i + 1, len(initial_grid)):
                if initial_grid[i] == 0:
                    continue
                elif initial_grid[i] > initial_grid[j] and initial_grid[j] != 0:
                    initial_grid_inversions += 1

        target_grid_inversions = 0
        for i in range(len(target_grid)):
            for j in range(i + 1, len(target_grid)):
                if target_grid[i] == 0:
                    continue
                elif target_grid[i] > target_grid[j] and target_grid[j] != 0:
                    target_grid_inversions += 1

        if size % 2 == 1:
            return (initial_grid_inversions % 2 + target_grid_inversions % 2) % 2 == 0
        else:
            empty_cell_row_in_initial_grid = initial_grid.index(0) // size
            empty_cell_row_in_target_grid = target_grid.index(0) // size
            if target_grid_inversions % 2 == 0:
                return (initial_grid_inversions % 2 + abs(empty_cell_row_in_target_grid - empty_cell_row_in_initial_grid) % 2) % 2 == 0
            else:
                return not (initial_grid_inversions % 2 + abs(empty_cell_row_in_target_grid - empty_cell_row_in_initial_grid) % 2) % 2 == 0

    def solve_puzzle(self) -> None:
        initial_state = State(
            self.puzzle_info['initial_grid'], self.puzzle_info, self.matrix_traversal_info, self.puzzle_params)

        if initial_state.grid == self.puzzle_info['target_grid']:
            self._create_sequence()
            self.solution_info['moves'] = len(self.solution_info['sequence'])
            return

        opened_list = [initial_state]
        closed_list = {initial_state.grid}

        while opened_list:
            state = heappop(opened_list)
            self.solution_info['selected_states'] += 1
            for generated_state in utils.generate_new_states(state, self.puzzle_info, self.matrix_traversal_info, self.puzzle_params):
                if generated_state.grid not in closed_list:
                    closed_list.add(generated_state.grid)
                    self.matrix_traversal_info['parents_data'][generated_state.grid] = state.grid
                    if generated_state.grid == self.puzzle_info['target_grid']:
                        self.solution_info['selected_states'] += 1
                        self._create_sequence()
                        self.solution_info['moves'] = len(
                            self.solution_info['sequence'])
                        return
                    heappush(opened_list, generated_state)
                    self.solution_info['max_states_in_memory'] = max(
                        self.solution_info['max_states_in_memory'], len(closed_list))
        raise RuntimeError("Error! N-puzzle has no solutions")

    def print_result(self, execution_time: float, is_solvable: bool) -> None:
        print(
            colored("\n##### N-PUZZLE BY CRENDEHA @ 42 SCHOOL #####\n", attrs=['bold']))

        print(colored("Heuristic function: " + colorama.Fore.MAGENTA +
              self.puzzle_params['heuristic_name'] + colorama.Style.RESET_ALL, attrs=['bold']))
        print(colored("Grid size: " + colorama.Fore.MAGENTA +
              str(self.puzzle_info['size']) + ' x ' + str(self.puzzle_info['size']) + colorama.Style.RESET_ALL, attrs=['bold']))
        print(colored("Solvable: " + (colorama.Fore.LIGHTGREEN_EX if is_solvable else colorama.Fore.LIGHTRED_EX) + str(
            is_solvable) + colorama.Style.RESET_ALL, attrs=['bold']))

        print(colored("\nA* search: " + (colorama.Fore.LIGHTGREEN_EX if not self.puzzle_params['greedy_search_only'] and not self.puzzle_params['uniform_cost_search_only'] else colorama.Fore.LIGHTRED_EX) + str(
            not self.puzzle_params['greedy_search_only'] and not self.puzzle_params['uniform_cost_search_only']) + colorama.Style.RESET_ALL, attrs=['bold']))
        print(colored("Greedy search only: " + (colorama.Fore.LIGHTGREEN_EX if self.puzzle_params['greedy_search_only'] else colorama.Fore.LIGHTRED_EX) + str(
            self.puzzle_params['greedy_search_only']) + colorama.Style.RESET_ALL, attrs=['bold']))
        print(colored("Uniform cost search only: " + (colorama.Fore.LIGHTGREEN_EX if self.puzzle_params['uniform_cost_search_only'] else colorama.Fore.LIGHTRED_EX) + str(
            self.puzzle_params['uniform_cost_search_only']) + colorama.Style.RESET_ALL, attrs=['bold']))
        print(colored("\nVisualizer: " + (colorama.Fore.LIGHTGREEN_EX if self.puzzle_params['visualizer'] else colorama.Fore.LIGHTRED_EX) + str(
            self.puzzle_params['visualizer']) + colorama.Style.RESET_ALL, attrs=['bold']))
        print(colored("\nInitial grid: " + colorama.Fore.MAGENTA +
              str(self.puzzle_info['initial_grid']) + colorama.Style.RESET_ALL, attrs=['bold']))

        if is_solvable:
            print(colored("\nTotal number of selected states (time complexity): " +
                  colorama.Fore.GREEN + format(self.solution_info['selected_states'], ',d').replace(',', ' ') + colorama.Style.RESET_ALL, attrs=['bold']))
            print(colored("Total number of states in memory (space complexity): " + colorama.Fore.GREEN +
                  format(self.solution_info['max_states_in_memory'], ',d').replace(',', ' ') + colorama.Style.RESET_ALL, attrs=['bold']))
            print(colored("Total number of moves: " + colorama.Fore.GREEN +
                  format(self.solution_info['moves'], ',d').replace(',', ' ') + colorama.Style.RESET_ALL, attrs=['bold']))
            print(colored("Search time: " + colorama.Fore.GREEN +
                  format(execution_time, ".3f") + " secs" + colorama.Style.RESET_ALL, attrs=['bold']))
            print(colored("Sequence of moves: ", attrs=['bold']))
            for state in self.solution_info['sequence']:
                print(colored(state, attrs=['dark']))

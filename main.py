import os
from telnetlib import NAOCRD  # noqa
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"  # noqa

import argparse
import sys
import time
import src.parser as puzzle_parser
import src.visualizer as visualizer
from src.Solution import Solution
import colorama
from termcolor import colored

if __name__ == "__main__" or __name__ == "__tester__":
    parser = argparse.ArgumentParser(description='n-puzzle 42 @ crendeha')

    search_type_group = parser.add_mutually_exclusive_group()
    search_type_group.add_argument(
        '-u', help='enable only uniform cost search', dest='uniform_cost_search_only', action='store_true')
    search_type_group.add_argument(
        '-g', help='enable only greedy search', dest='greedy_search_only', action='store_true')
    search_type_group.add_argument(
        '-n', help='enable non-admissible heuristics (Nilsson sequence score)', dest='non_admissible_heuristics', action='store_true')

    parser.add_argument('-v', help='use visualizer',
                        dest='visualizer', action='store_true')

    if '-g' not in sys.argv and '-n' not in sys.argv:
        parser.add_argument('heuristic_function', metavar='heuristic_function', default='manhattan', choices=[
                            'manhattan', 'euclid', 'out_of_place', 'out_of_row_and_col', 'nilsson'], help='specifies heuristic function (not specified if -g or -n flag is enabled)')
    parser.add_argument('file', metavar='file',
                        help='file, which contains the initial grid')

    try:
        args = vars(parser.parse_args())
        initial_grid = puzzle_parser.run_parser(args['file'])

        solution = Solution(initial_grid, args)

        if not solution.is_puzzle_solvable():
            solution.print_result(0, False)
            sys.exit()

        if not args['non_admissible_heuristics'] and solution.puzzle_info['size'] > 4 and ('heuristic_function' in args and args['heuristic_function'] not in ['manhattan', 'nilsson']):
            print(colored(colorama.Fore.LIGHTRED_EX + "WARNING! Solving n-puzzle bigger than 4x4 with admissible heuristics other than Manhattan distance may take a lot of time..." +
                  colorama.Style.RESET_ALL, attrs=['bold']))

        start_time = time.time()
        solution.solve_puzzle()
        end_time = time.time()

        solution.print_result(end_time - start_time, True)

        if args['visualizer']:
            visualizer.run_visualizer(solution.solution_info['sequence'])

    except ValueError as e:
        print("{}".format(e))
        sys.exit()
    except RuntimeError as e:
        print("{}".format(e))
        sys.exit()
    except SyntaxError as e:
        print("{}".format(e))
        sys.exit()
    except KeyError as e:
        print("{}".format(e))
        sys.exit()

import sys
import time

from astar import AStar
from grid import Grid
from binary_tree import BinaryTree
from sidewinder import Sidewinder
from aldous_broder import AldousBroder
from recursive_backtracker import RecursiveBacktracker


# Calcola tempo di esecuzione per ogni algoritmo generativo
def execution_time_generation(rows=100, columns=100, tries=100,
                              algorithms=None, show_every_try=False):

    print("-----CALCOLO ALGORITMI GENERATIVI-----")

    if algorithms is None:
        algorithms = [BinaryTree, Sidewinder, RecursiveBacktracker, AldousBroder]

    averages = {}

    # ------------------------------------- #
    for algo in algorithms:

        print(f"\nAnalisi: {algo.__name__}")

        execution_time = []

        # ------------------------------------- #
        for i in range(tries):

            testgrid = Grid(rows, columns)

            start_time = time.perf_counter()
            algo.apply(testgrid)
            end_time = time.perf_counter()

            if show_every_try:
                print(f"Try {i + 1}: [ {end_time - start_time:.3f}s | {(1000 * (end_time - start_time)):.1f}ms ]")

            execution_time.append(end_time - start_time)
        # ------------------------------------- #

        averages[algo.__name__] = sum(execution_time) / len(execution_time)
    # ------------------------------------- #

    print(f"\nMedia di esecuzione per ({rows}x{columns}): ({tries} tentativi)")

    sorted_algorithms = sorted(algorithms, key=lambda alg: averages.get(alg.__name__, float('inf')))

    # ------------------------------------- #
    for algo in sorted_algorithms:

        average_time = averages.get(algo.__name__, 0)

        if average_time >= 60:
            print(f"{algo.__name__}: [ {average_time / 60:.3f}m | {average_time:.3f}s | {average_time * 1000:.3f}ms ]")
        else:
            print(f"{algo.__name__}: [ {average_time:.3f}s | {average_time * 1000:.3f}ms ]")
    # ------------------------------------- #


    print("\n")
# ---------------------------------------------------------------------------- #



# Calcola tempo di esecuzione per l'algoritmo A* applicato ad ogni algoritmo generativo
def execution_time_resolution(rows=100, columns=100, tries=100,
                              maze_solvers=None, maze_generator=BinaryTree, show_every_try=False):

    print("-----CALCOLO ALGORITMO RISOLUTIVO-----")

    if maze_solvers is None:
        maze_solvers = [AStar]

    performance_metrics = {}

    # ------------------------------------- #
    for algo in maze_solvers:

        print(f"\nAnalisi {algo.__name__} per {maze_generator.__name__}")

        execution_times = []
        path_lengths = []

        # ------------------------------------- #
        for i in range(tries):

            testgrid = Grid(rows, columns)
            maze_generator.apply(testgrid)
            start_cell = testgrid.random_cell()
            end_cell = testgrid.random_cell()

            solve_start_time = time.perf_counter()
            solution_path = algo.apply(testgrid, start_cell, end_cell)
            solve_end_time = time.perf_counter()

            exec_time = solve_end_time - solve_start_time
            execution_times.append(exec_time)

            path_len = len(solution_path)
            path_lengths.append(path_len)

            if show_every_try:
                if exec_time >= 60:
                    print(f"  Try {i + 1}: [ {exec_time / 60:.3f}m | {exec_time:.3f}s | {(exec_time * 1000):.3f}ms ] | Lunghezza soluzione: {solution_path.__len__()}")
                else:
                    print(f"  Try {i + 1}: [ {exec_time:.3f}s | {(exec_time * 1000):.3f}ms ] | Lunghezza soluzione: {solution_path.__len__()}")
        # ------------------------------------- #

        avg_time = float('inf')
        if execution_times:
            avg_time = sum(execution_times) / len(execution_times)

        avg_length = 0
        if path_lengths:
            avg_length = sum(path_lengths) / len(path_lengths)

        performance_metrics[algo.__name__] = {
            "average_time": avg_time,
            "average_length": avg_length
        }
    # ------------------------------------- #

    print(f"\nMedia di esecuzione per ({rows}x{columns}): ({tries} tentativi)")

    sorted_solvers = sorted(maze_solvers, key=lambda s: performance_metrics.get(s.__name__, {"average_time": float('inf')})["average_time"])

    # ------------------------------------- #
    for algo in sorted_solvers:

        metrics = performance_metrics.get(algo.__name__)

        metric_time = metrics["average_time"]
        metric_path = metrics["average_length"]

        print(f"{algo.__name__}: \n\t"
              f"[ {metric_time / 60:.3f}m | {metric_time:.3f}s | {(metric_time * 1000):.3f}ms ] \n\t"
              f"Lunghezza media soluzione: {metric_path} \n")
    # ------------------------------------- #

    print("\n")
# ---------------------------------------------------------------------------- #



# Calcola la lunghezza del cammino più lungo per ogni algoritmo generativo
def longest_path_length(rows=100, columns=100, tries=100,
                        algorithms=None, show_every_try=False):

    print("-----CALCOLO PERCORSO PIU' LUNGO-----")

    if algorithms is None:
        algorithms = [BinaryTree, Sidewinder, RecursiveBacktracker, AldousBroder]

    performance_metrics = {}

    # ------------------------------------- #
    for algo in algorithms:

        execution_times = []
        path_lengths = []

        print(f"\nAnalisi {algo.__name__}")

        # ------------------------------------- #
        for i in range(tries):

            testgrid = Grid(rows, columns)
            algo.apply(testgrid)
            root = testgrid[0,0]

            # Calcola tutte le distanze dalla root
            maze_distances = root.calc_all_distances()

            # Calcolo percorso più lungo dalla radice
            start_time = time.perf_counter()

            longest_path_root, _ = maze_distances.longest_path_from()
            distances_from_longest_path_root = longest_path_root.calc_all_distances()

            # Calcolo percorso più lungo dalla nuova radice
            longest_path_goal, max_dist_longest_path = distances_from_longest_path_root.longest_path_from()
            end_time = time.perf_counter()

            exec_time = end_time - start_time
            execution_times.append(exec_time)

            path_len = max_dist_longest_path
            path_lengths.append(path_len)

            if show_every_try:
                if exec_time >= 60:
                    print(f"  Try {i + 1}: [ {exec_time / 60:.3f}m | {exec_time:.3f}s | {(exec_time * 1000):.3f}ms ] | Lunghezza percorso più lungo: {path_len}")
                else:
                    print(f"  Try {i + 1}: [ {exec_time:.3f}s | {(exec_time * 1000):.3f}ms ] | Lunghezza percorso più lungo: {path_len}")
        # ------------------------------------- #

        avg_time = float('inf')
        if execution_times:
            avg_time = sum(execution_times) / len(execution_times)

        avg_length = 0
        if path_lengths:
            avg_length = sum(path_lengths) / len(path_lengths)

        performance_metrics[algo.__name__] = {
            "average_time": avg_time,
            "average_length": avg_length
        }
    # ------------------------------------- #

    print(f"\nMedia di esecuzione per ({rows}x{columns}): ({tries} tentativi)")

    sorted_solvers = sorted(algorithms, key=lambda s: performance_metrics.get(s.__name__, {"average_time": float('inf')})["average_time"])

    # ------------------------------------- #
    for algo in sorted_solvers:

        metrics = performance_metrics.get(algo.__name__)

        metric_time = metrics["average_time"]
        metric_path = metrics["average_length"]
        print(f"{algo.__name__}: \n\t"
              f"[ {metric_time / 60:.3f}m | {metric_time:.3f}s | {(metric_time * 1000):.3f}ms ] \n\t"
              f"Lunghezza media percorso più lungo: {metric_path} \n")
    # ------------------------------------- #

    print("\n")
# ---------------------------------------------------------------------------- #



# Calcola media vicoli ciechi per ogni algoritmo generativo
def count_deadends(rows=100, columns=100, tries=100, algorithms=None):

    print("-----CALCOLO VICOLI CIECHI-----")

    if algorithms is None:
        algorithms = [BinaryTree, Sidewinder, RecursiveBacktracker, AldousBroder]

    averages = {}

    # ------------------------------------- #
    for algo in algorithms:

        print(f"\nAnalisi: {algo.__name__} ({rows}x{columns})")

        count_deadends = []

        # ------------------------------------- #
        for i in range(tries):

            print(f"Try {i}: ")

            testgrid = Grid(rows, columns)
            algo.apply(testgrid)

            count_deadends.append(len(testgrid.deadends()))
        # ------------------------------------- #

        averages[algo.__name__] = sum(count_deadends) / len(count_deadends)
    # ------------------------------------- #

    print(f"\nMedia di vicoli ciechi totali per ({rows}x{columns}): ({tries} tentativi)")

    sorted_algorithms = sorted(algorithms, key=lambda alg: averages.get(alg.__name__, float('inf')))

    # ------------------------------------- #
    for algo in sorted_algorithms:

        average_count = averages[algo.__name__]
        percentage = (average_count * 100.0) / (rows * columns)

        print(f"{algo.__name__}: {average_count}/{(rows * columns)} | {percentage:.3f}%")
    # ------------------------------------- #

    print("\n")
# ---------------------------------------------------------------------------- #


# Scrivi le metriche su un file
def write_on_file(filepath, rows=100, cols=100, tries=100, show_every_try=False):

    original_stdout = sys.stdout

    try:
        with open(filepath, "w") as f:

            sys.stdout = f

            #gen = [BinaryTree, Sidewinder, RecursiveBacktracker, AldousBroder]


    finally:
        sys.stdout = original_stdout
# ---------------------------------------------------------------------------- #



if __name__ == "__main__":

    rows = 100
    columns = 100
    tries = 10


    count_deadends(rows, columns, tries)
    #longest_path_length(rows, columns, tries, show_every_try=True)

    #gen = [RecursiveBacktracker]
    #execution_time_generation(rows, columns, tries, gen, show_every_try=True)

    #execution_time_resolution(rows, columns, tries, maze_generator=AldousBroder, show_every_try=True)
    #execution_time_resolution(rows, columns, tries, maze_generator=BinaryTree, show_every_try=True)
    #execution_time_resolution(rows, columns, tries, maze_generator=Sidewinder, show_every_try=True)
    #execution_time_resolution(rows, columns, tries, maze_generator=RecursiveBacktracker, show_every_try=True)


    #write_on_file("analysis_results.txt", rows, columns, tries, show_every_try=False)

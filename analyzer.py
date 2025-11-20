import sys
import time

from SolverAlgos.astar import AStar
from Core.grid import Grid
from GeneratorAlgos.binary_tree import BinaryTree
from GeneratorAlgos.recursive_division import RecursiveDivision
from GeneratorAlgos.sidewinder import Sidewinder
from GeneratorAlgos.aldous_broder import AldousBroder
from GeneratorAlgos.recursive_backtracker import RecursiveBacktracker


# Calculate the execution time of the generative algorithms.
def execution_time_generation(rows=100, columns=100, tries=100,
                              algorithms=None, show_every_try=False):

    print("-----GENERATIVE ALGORITHMS EXECUTION TIME-----")

    if algorithms is None:
        algorithms = [BinaryTree, Sidewinder, RecursiveBacktracker, AldousBroder, RecursiveDivision]

    averages = {}

    # ------------------------------------- #
    for algo in algorithms:

        print(f"\nAnalysis: {algo.__name__}")

        execution_time = []

        # ------------------------------------- #
        for i in range(tries):
            testgrid = Grid(rows, columns)

            start_time = time.perf_counter()
            algo.apply(testgrid)
            end_time = time.perf_counter()

            exec_time = end_time - start_time

            if show_every_try:
                print(f"Try {i + 1}: [ {exec_time:.3f}s | {(exec_time * 1000):.3f}ms ]")

            execution_time.append(exec_time)
        # ------------------------------------- #

        averages[algo.__name__] = sum(execution_time) / len(execution_time)
    # ------------------------------------- #

    print(f"\nAverage execution time for ({rows}x{columns}): ({tries} tries)")
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



# Calculate the execution time of the resolution algorithm A* applied on every maze generated.
def execution_time_resolution(rows=100, columns=100, tries=100,
                              maze_solvers=None, maze_generator=BinaryTree, show_every_try=False):

    print("-----RESOLUTION ALGORITHM EXECUTION TIME-----")

    if maze_solvers is None:
        maze_solvers = [AStar]

    performance_metrics = {}

    # ------------------------------------- #
    for algo in maze_solvers:

        print(f"\nAnalysis {algo.__name__} for maze {maze_generator.__name__}")

        execution_times = []
        path_lengths = []

        # ------------------------------------- #
        for i in range(tries):

            testgrid = Grid(rows, columns)
            maze_generator.apply(testgrid)
            start_cell = testgrid.random_cell()
            end_cell = testgrid.random_cell()

            start_time = time.perf_counter()
            solution_path = algo.apply(testgrid, start_cell, end_cell)
            end_time = time.perf_counter()

            exec_time = end_time - start_time
            execution_times.append(exec_time)

            path_len = len(solution_path)
            path_lengths.append(path_len)

            if show_every_try:
                if exec_time >= 60:
                    print(f"  Try {i + 1}: [ {exec_time / 60:.3f}m | {exec_time:.3f}s | {(exec_time * 1000):.3f}ms ] | Solution length: {solution_path.__len__()}")
                else:
                    print(f"  Try {i + 1}: [ {exec_time:.3f}s | {(exec_time * 1000):.3f}ms ] | Solution length: {solution_path.__len__()}")
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

    print(f"\nAverage execution time for ({rows}x{columns}): ({tries} tries)")
    sorted_solvers = sorted(maze_solvers, key=lambda s: performance_metrics.get(s.__name__, {"average_time": float('inf')})["average_time"])
    # ------------------------------------- #
    for algo in sorted_solvers:
        metrics = performance_metrics.get(algo.__name__)
        metric_time = metrics["average_time"]
        metric_path = metrics["average_length"]
        print(f"{algo.__name__}: \n\t"
              f"[ {metric_time / 60:.3f}m | {metric_time:.3f}s | {(metric_time * 1000):.3f}ms ] \n\t"
              f"Average solution length: {metric_path} \n")
    # ------------------------------------- #

    print("\n")
# ---------------------------------------------------------------------------- #



# Calculate the longest path within the maze for every maze generated.
def longest_path_length(rows=100, columns=100, tries=100,
                        algorithms=None, show_every_try=False):

    print("-----LONGEST PATH CALCULATION-----")

    if algorithms is None:
        algorithms = [BinaryTree, Sidewinder, RecursiveBacktracker, AldousBroder, RecursiveDivision]

    performance_metrics = {}

    # ------------------------------------- #
    for algo in algorithms:

        print(f"\nAnalysis: {algo.__name__}")

        execution_times = []
        path_lengths = []

        # ------------------------------------- #
        for i in range(tries):

            testgrid = Grid(rows, columns)
            algo.apply(testgrid)
            root = testgrid[0,0]

            # Calculate all the distances from the root.
            maze_distances = root.calc_all_distances()

            start_time = time.perf_counter()

            # Calculate the farthest cell from the root.
            longest_path_root, _ = maze_distances.longest_path_from()

            # Calculate all the distances from the new rooot (farthest cell from the old root).
            distances_from_longest_path_root = longest_path_root.calc_all_distances()

            # Calculate the farthest cell from the new root.
            longest_path_goal, max_dist_longest_path = distances_from_longest_path_root.longest_path_from()

            end_time = time.perf_counter()

            exec_time = end_time - start_time
            execution_times.append(exec_time)

            path_len = max_dist_longest_path
            path_lengths.append(path_len)

            if show_every_try:
                if exec_time >= 60:
                    print(f"  Try {i + 1}: [ {exec_time / 60:.3f}m | {exec_time:.3f}s | {(exec_time * 1000):.3f}ms ] | Longest path length: {path_len}")
                else:
                    print(f"  Try {i + 1}: [ {exec_time:.3f}s | {(exec_time * 1000):.3f}ms ] | Longest path length: {path_len}")
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

    print(f"\nAverage execution time for ({rows}x{columns}): ({tries} tries)")
    sorted_solvers = sorted(algorithms, key=lambda s: performance_metrics.get(s.__name__, {"average_time": float('inf')})["average_time"])
    # ------------------------------------- #
    for algo in sorted_solvers:
        metrics = performance_metrics.get(algo.__name__)
        metric_time = metrics["average_time"]
        metric_path = metrics["average_length"]
        print(f"{algo.__name__}: \n\t"
              f"[ {metric_time / 60:.3f}m | {metric_time:.3f}s | {(metric_time * 1000):.3f}ms ] \n\t"
              f"Average longest path length: {metric_path} \n")
    # ------------------------------------- #

    print("\n")
# ---------------------------------------------------------------------------- #



# Calculate the average number of dead ends for every maze generated.
def count_deadends(rows=100, columns=100, tries=100, algorithms=None):

    print("-----DEAD ENDS CALCULATION-----")

    if algorithms is None:
        algorithms = [BinaryTree, Sidewinder, RecursiveBacktracker, AldousBroder, RecursiveDivision]

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

    print(f"\nAverage number of dead ends for ({rows}x{columns}): ({tries} tries)")
    sorted_algorithms = sorted(algorithms, key=lambda alg: averages.get(alg.__name__, float('inf')))
    # ------------------------------------- #
    for algo in sorted_algorithms:
        average_count = averages[algo.__name__]
        percentage = (average_count * 100.0) / (rows * columns)
        print(f"{algo.__name__}: {average_count}/{(rows * columns)} | {percentage:.3f}%")
    # ------------------------------------- #

    print("\n")
# ---------------------------------------------------------------------------- #



# Write the metrics in a file, instead of showing them in the console.
def write_on_file(filepath, rows=100, cols=100, tries=100, show_every_try=False):

    original_stdout = sys.stdout

    try:
        with open(filepath, "w") as f:

            sys.stdout = f

            algos = [BinaryTree, Sidewinder, AldousBroder, RecursiveBacktracker, RecursiveDivision]
            full_analysis(rows, columns, tries, algos, show_every_try=True)

    finally:
        sys.stdout = original_stdout
# ---------------------------------------------------------------------------- #



# Calculate all metric for every try.
def full_analysis(rows=100, columns=100, tries=100, algorithms=None, show_every_try=False):

    print(f"----- ANALISI COMPLETA -----")

    if algorithms is None:
        algorithms = [BinaryTree, Sidewinder, RecursiveBacktracker, AldousBroder, RecursiveDivision]

    metrics = {
        algo.__name__: {
            "generative_time": [],
            "resolution_time": [],
            "solution_length": [],
            "longest_path_length": [],
            "deadends": []
        }
        for algo in algorithms
    }

    # ------------------------------------- #
    for algo in algorithms:

        print(f"\nAnalysis: {algo.__name__}")

        # ------------------------------------- #
        for i in range(tries):

            if show_every_try:
                print(f"Try {i + 1}: ")

            testgrid = Grid(rows, columns)

            # Generative algorithm execution time.
            start_time = time.perf_counter()
            algo.apply(testgrid)
            end_time = time.perf_counter()
            metrics[algo.__name__]["generative_time"].append(end_time - start_time)


            # Resolutive algorithm execution time.
            start_cell = testgrid.random_cell()
            end_cell = testgrid.random_cell()

            start_time = time.perf_counter()
            solution_path = AStar.apply(testgrid, start_cell, end_cell)
            end_time = time.perf_counter()

            metrics[algo.__name__]["resolution_time"].append(end_time - start_time)
            metrics[algo.__name__]["solution_length"].append(len(solution_path))


            # Longest path.
            root = testgrid[0,0]
            distances = root.calc_all_distances()

            new_root, _, _= distances.longest_path_from()
            new_distances = new_root.calc_all_distances()
            _, longest_path, _ = new_distances.longest_path_from()

            metrics[algo.__name__]["longest_path_length"].append(longest_path)


            # Dead ends count.
            dead_ends = len(testgrid.deadends())
            metrics[algo.__name__]["deadends"].append(dead_ends)
        # ------------------------------------- #
    # ------------------------------------- #

    print(f"\nAverage execution time for ({rows}x{columns}): ({tries} tries)")
    averages = {}
    # ------------------------------------- #
    for algo_name, metric in metrics.items():
        avg_gen_time = sum(metric["generative_time"]) / tries
        avg_res_time = sum(metric["resolution_time"]) / tries
        avg_solution_path = sum(metric["solution_length"]) / tries
        avg_longest_path = sum(metric["longest_path_length"]) / tries
        avg_deadends = sum(metric["deadends"]) / tries

        averages[algo_name] = {
            "generative_time": avg_gen_time,
            "resolution_time": avg_res_time,
            "solution_length": avg_solution_path,
            "longest_path_length": avg_longest_path,
            "deadends": avg_deadends
        }
    # ------------------------------------- #

    sorted_algorithms = sorted(averages.keys(), key=lambda name: averages[name]["generative_time"])
    for algo_name in sorted_algorithms:
        stats = averages[algo_name]
        total_cells = rows * columns
        solution_percentage = (stats["solution_length"] * 100) / total_cells
        longestpath_percentage = (stats["longest_path_length"] * 100) / total_cells
        deadends_percentage = (stats["deadends"] * 100) / total_cells

        print(f"\n----- {algo_name} ({rows}x{columns}) -----")
        print(f"    Average generative time: [ {stats['generative_time']:.3f}s ] [ {stats['generative_time']*1000:.3f}ms ]")
        print(f"    Average resolution time: [ {stats['resolution_time']:.3f}s ] [ {stats['resolution_time']*1000:.3f}ms ]")
        print(f"    Average solution length: {stats['solution_length']:.3f} / {total_cells} ({solution_percentage:.3f}%)")
        print(f"    Average longest path length: {stats['longest_path_length']:.3f} / {total_cells} ({longestpath_percentage:.3f}%)")
        print(f"    Average number of dead ends: {stats['deadends']:.3f} / {total_cells} ({deadends_percentage:.3f}%)")
# ---------------------------------------------------------------------------- #



if __name__ == "__main__":

    rows = 50
    columns = 50
    tries = 100

    algos = [BinaryTree, Sidewinder, AldousBroder, RecursiveBacktracker, RecursiveDivision]
    full_analysis(rows, columns, tries, algos, show_every_try=True)

    #gen = [BinaryTree, Sidewinder, AldousBroder, RecursiveBacktracker, RecursiveDivision]
    #execution_time_generation(rows, columns, tries, gen, show_every_try=True)

    #execution_time_resolution(rows, columns, tries, maze_generator=BinaryTree, show_every_try=True)
    #execution_time_resolution(rows, columns, tries, maze_generator=Sidewinder, show_every_try=True)
    #execution_time_resolution(rows, columns, tries, maze_generator=RecursiveBacktracker, show_every_try=True)
    #execution_time_resolution(rows, columns, tries, maze_generator=RecursiveDivision, show_every_try=True)
    #execution_time_resolution(rows, columns, tries, maze_generator=AldousBroder, show_every_try=True)

    #longest_path_length(rows, columns, tries, show_every_try=True)
    #count_deadends(rows, columns, tries)


    # write_on_file("analysis_results.txt", rows, columns, tries, show_every_try=False)

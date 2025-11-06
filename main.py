import time


from grid import Grid
from distances import Distances
from astar import AStar
from binary_tree import BinaryTree
from sidewinder import Sidewinder
from aldous_broder import AldousBroder
from recursive_backtracker import RecursiveBacktracker
from recursive_division import RecursiveDivision

def main():


    # ----------------------------------------------- #
    # Set the grid parameters and create the maze.
    maze_rows = 20
    maze_columns = 20
    MazeGrid = Grid(maze_rows,maze_columns)

    start_time = time.perf_counter()
    RecursiveBacktracker.apply(MazeGrid)
    end_time = time.perf_counter()

    execution_time = end_time - start_time

    if execution_time >= 60:
        print(f"Maze generated with {MazeGrid.size()} cells ({MazeGrid.rows} x {MazeGrid.columns}) in : [ {(execution_time / 60):.3f}m | {execution_time:.3f}s | {(execution_time * 1000):.3f}ms ]\n")
    else:
        print(f"Maze generated with {MazeGrid.size()} cells ({MazeGrid.rows} x {MazeGrid.columns}) in : [ {execution_time:.3f}s | {(execution_time * 1000):.3f}ms ]\n")
    # ----------------------------------------------- #


    # Choose arbitrarily the root cell and the goal cell.
    root_cell = MazeGrid[0,0]
    goal_cell = MazeGrid[maze_rows - 1, maze_columns - 1]


    # ----------------------------------------------- #
    # Calculate all the distances from the root cell.
    start_time = time.perf_counter()
    maze_distances = root_cell.calc_all_distances()
    end_time = time.perf_counter()

    execution_time = end_time - start_time

    if execution_time >= 60:
        print(f"Distances from the root {root_cell} calculated in: [ {(execution_time/60):.3f}m | {execution_time:.3f}s | {(execution_time * 1000):.3f}ms ]\n")
    else:
        print(f"Distances from the root {root_cell} calculated in: [ {execution_time:.3f}s | {(execution_time * 1000):.3f}ms ]\n")
    # ----------------------------------------------- #


    # ----------------------------------------------- #
    # Calculate the longest path from the root.
    start_time = time.perf_counter()

    # Calculate the farthest cell from the root, making it the new root.
    longest_path_root, _ = maze_distances.longest_path_from()

    # Calculate all the distances from the new root (the farthest cell from the original root).
    distances_from_longest_path_root = longest_path_root.calc_all_distances()

    # Calculate the farthest cell from the root.
    longest_path_goal, max_dist_longest_path = distances_from_longest_path_root.longest_path_from()

    # Calculate the shortest path between the root and the farthest cell from the root.
    longest_path_distances = distances_from_longest_path_root.shortest_path_to(longest_path_goal)

    end_time = time.perf_counter()

    execution_time = end_time - start_time

    if execution_time >= 60:
        print(f"Longest path in the maze: from {longest_path_root} to {longest_path_goal} with distance {max_dist_longest_path} in: [ {(execution_time/60):.3f}s | {execution_time:.3f}s | {(execution_time * 1000):.3f}ms ]\n")
    else:
        print(f"Longest path in the maze: from {longest_path_root} to {longest_path_goal} with distance {max_dist_longest_path} in: [ {execution_time:.3f}s | {(execution_time * 1000):.3f}ms ]\n")
    # ----------------------------------------------- #


    # ----------------------------------------------- #
    # Solving the maze with the A* algorithm.

    start_time = time.perf_counter()

    solution_path = AStar.apply(MazeGrid, root_cell, goal_cell)

    end_time = time.perf_counter()
    execution_time = end_time - start_time

    if solution_path:
        print(f"Solution path found with A*: {len(solution_path)} cells in: [ {execution_time:.3f}s | {(execution_time * 1000):.3f}ms ] \n")
    else:
        print("No solution path found. \n")
    # ----------------------------------------------- #


    # -------------------------------------------------------------------- #
    cell_size = 30
    full_color = (255,255,255)               # white
    checkerboard_color_1 = (255, 255, 255)   # white
    checkerboard_color_2 = (220, 220, 220)   # gray
    text_color = (240, 50, 255)              # purple
    path_color = (240, 50, 255)              # purple
    gradient_start = (235, 235, 235)         # gray
    gradient_middle = (0, 180, 0)            # light green
    gradient_end = (0, 30, 0)                # dark green
    smooth_exp = 0.65
    start_cell_color = (255,200,0)           # yellow
    end_cell_color = (0,255,255)             # cyan
    deadend_color = (255,0,0)                # red


    # Generate a PNG image of the maze with the cells colored like a checkerboard.
    img_maze = MazeGrid.to_png(
        cell_size=cell_size,
        background_type="checkerboard")
    img_maze.save("images/checkerboard.png")
    img_maze.show()

    # Generate a PNG image of the maze with all the cells colored the same color.
    img_maze = MazeGrid.to_png(
        cell_size=cell_size,
        background_type="full_color")
    img_maze.save("images/full_color.png")
    img_maze.show()


    # -------------------------------------------------------------------- #

    MazeGrid.distances = maze_distances

    # Generate a PNG image of the maze with the cells colored based on the distances from the root.
    img_maze = MazeGrid.to_png(
        cell_size,
        show_distances_gradient=True, distances_obj=maze_distances)
    img_maze.save("images/distances_gradient.png")
    img_maze.show()


    # Generate a PNG image of the maze with the cells colored based on the distances from the root
    # and the distance of every cell is written above it.
    img_maze = MazeGrid.to_png(
        cell_size,
        show_distances_gradient=True, distances_obj=maze_distances, show_distance_text=True)
    img_maze.save("images/distances_gradient_and_text.png")
    img_maze.show()


    # -------------------------------------------------------------------- #


    # Generate a PNG image of the maze with the solution path highlighted.
    img_maze = MazeGrid.to_png(
        cell_size,
        #background_type="checkerboard",
        show_solution=True, solution_path=solution_path,
        start_cell=solution_path[0], end_cell=solution_path[-1])
    img_maze.save("images/solution_astar.png")
    img_maze.show()


    # Generate a PNG image of the maze with the solution path and the cells colored based on the distances.
    img_maze = MazeGrid.to_png(
        cell_size,
        distances_obj=maze_distances,
        show_subset_gradient=True, subset_cells=solution_path)
    img_maze.save("images/solution_astar_gradient.png")
    img_maze.show()


    # Generate a PNG image of the maze with the solution and the cells colored based on the distances,
    # and the distance of every cell is written above it.
    img_maze = MazeGrid.to_png(
        cell_size,
        show_distance_text=True, distances_obj=maze_distances,
        show_subset_gradient=True, subset_cells=solution_path)
    img_maze.save("images/solution_astar_gradient_and_text.png")
    img_maze.show()


    # -------------------------------------------------------------------- #


    # Generate a PNG image of the maze with the longest path in the maze highlighted as a gradient.
    img_maze = MazeGrid.to_png(
        cell_size,
        show_distances_gradient=True, distances_obj=longest_path_distances)
    img_maze.save("images/longest_path_gradient.png")
    img_maze.show()


    # Generate a PNG image of the maze with the longest path in the maze highlighted as a gradient
    # and the distance of every cell of the path is written above it.
    img_maze = MazeGrid.to_png(
        cell_size,
        show_distances_gradient=True, distances_obj=longest_path_distances, show_distance_text=True)
    img_maze.save("images/longest_path_gradient_and_text.png")
    img_maze.show()


    # Generate a PNG image of the maze with the longest path in the maze highlighted.
    longest_path = AStar.apply(MazeGrid, longest_path_root, longest_path_goal)
    img_maze = MazeGrid.to_png(
        cell_size,
        #background_type="checkerboard",
        show_solution=True, solution_path=longest_path,
        start_cell=longest_path[0], end_cell=longest_path[-1])
    img_maze.save("images/longest_path_solution.png")
    img_maze.show()
    # ---------------------------------------------------------- #


# Print which cells are linked to every cell.
def print_cells(grid):
    for cell in grid.each_cell():
        print(cell, "linked to:", list(cell._links))


# Copy the source maze to a target maze.
# The mazes must be of the same size.
def copy_maze_structure(source_grid: Grid, target_grid: Grid):

    if source_grid.rows != target_grid.rows or source_grid.columns != target_grid.columns:
        print(f"The mazes are not of the same size. Copy impossible to perform.")

    for row in range(source_grid.rows):
        for col in range(source_grid.columns):

            source_cell = source_grid[row, col]
            target_cell = target_grid[row, col]  # get the corresponding cell in the target grid

            # For every cell to which the source cell is linked in the source maze.
            for linked_source_cell in source_cell.all_linked():

                # Get the corresponding linked cell in the target grid.
                target_linked_cell = target_grid[linked_source_cell.row, linked_source_cell.column]

                # Link the target cell to the target linked cell.
                # Check if the cells are already linked (not actually necessary!).
                if not target_cell.is_linked(target_linked_cell):
                    target_cell.link(target_linked_cell)



# Execute this file as the main entry point of the application.
if __name__ == "__main__":
    main()

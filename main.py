import time

from astar import AStar
from distances import Distances
from grid import Grid
from binary_tree import BinaryTree
from sidewinder import Sidewinder
from aldous_broder import AldousBroder
from recursive_backtracker import RecursiveBacktracker


def main():


    # ----------------------------------------------- #
    maze_row = 50
    maze_col = 50
    MazeGrid = Grid(maze_row,maze_col)

    start_time = time.perf_counter()
    RecursiveBacktracker.apply(MazeGrid)
    end_time = time.perf_counter()


    # Griglia per calcoli delle distanze e visualizzazione PNG
    GridVisualize = Grid(maze_row, maze_col)
    copy_maze_structure(MazeGrid, GridVisualize)


    # Scelgo arbitrariamente celle root e goal
    root = GridVisualize[0,0]
    goal_cell = GridVisualize.random_cell()
    #goal_cell = GridVisualize[maze_row-1, maze_col-1]


    execution_time = end_time - start_time
    if execution_time >= 60:
        print(f"Labirinto generato con {MazeGrid.size()} celle ({MazeGrid.rows} x {MazeGrid.columns}) in : [ {(execution_time / 60):.3f}m | {execution_time:.3f}s | {(execution_time * 1000):.3f}ms ]\n")
    else:
        print(f"Labirinto generato con {MazeGrid.size()} celle ({MazeGrid.rows} x {MazeGrid.columns}) in : [ {execution_time:.3f}s | {(execution_time * 1000):.3f}ms ]\n")
    # ----------------------------------------------- #



    # ----------------------------------------------- #
    # Calcolo distanze: tutte le distanze da root
    start_time = time.perf_counter()
    maze_distances = root.calc_all_distances()
    end_time = time.perf_counter()

    execution_time = end_time - start_time
    if execution_time >= 60:
        print(f"Calcolo distanze dalla root {root} in: [ {(execution_time/60):.3f}m | {execution_time:.3f}s | {(execution_time * 1000):.3f}ms ]\n")
    else:
        print(f"Calcolo distanze dalla root {root} in: [ {execution_time:.3f}s | {(execution_time * 1000):.3f}ms ]\n")
    # ----------------------------------------------- #



    # ----------------------------------------------- #
    # Calcolo percorso più lungo dalla radice.
    start_time = time.perf_counter()
    longest_path_root, _ = maze_distances.longest_path_to()
    distances_from_longest_path_root = longest_path_root.calc_all_distances()

    # Calcolo percorso più lungo dalla nuova radice
    longest_path_goal, max_dist_longest_path = distances_from_longest_path_root.longest_path_to()

    # Calcolo il percorso più corto tra le due celle
    longest_path_distances = distances_from_longest_path_root.shortest_path_to(longest_path_goal)
    end_time = time.perf_counter()

    execution_time = end_time - start_time
    if execution_time >= 60:
        print(f"Calcolo del percorso più lungo nel labirinto: da {longest_path_root} a {longest_path_goal} con distanza {max_dist_longest_path} in: [ {(execution_time/60):.3f}s | {execution_time:.3f}s | {(execution_time * 1000):.3f}ms ]\n")
    else:
        print(f"Calcolo del percorso più lungo nel labirinto: da {longest_path_root} a {longest_path_goal} con distanza {max_dist_longest_path} in: [ {execution_time:.3f}s | {(execution_time * 1000):.3f}ms ]\n")
    # ----------------------------------------------- #



    # ----------------------------------------------- #
    # Un valore di 2 o 3 pixel è spesso sufficiente per cell_size=20
    #cell_inset = 6
    #cell_size = 22
    cell_inset = 7
    cell_size = 30

    # MazeGrid, grid_distances e grid_colored non cambiano nulla se non applico le distanze
    # grid_xxx.distances = maze_distances

    img_maze_checkerboard = MazeGrid.to_png(cell_size=cell_size, background_type="checkerboard")
    img_maze_checkerboard.save("maze_checkerboard.png")
    img_maze_checkerboard.show()

    img_maze_all_white = MazeGrid.to_png(cell_size=cell_size, background_type="plain-white")
    img_maze_all_white.save("maze_all_white.png")
    img_maze_all_white.show()
    # ----------------------------------------------- #



    # ---------------------------------------------------------- #
    # Applicazione Distanze
    start_time = time.perf_counter()

    GridVisualize.distances = maze_distances

    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(f"Applicazione distanze su griglia: [ {execution_time:.3f}s | {(execution_time * 1000):.3f}ms ]")
    # ----------------------------------------------- #


    # Distanze base (colorata, senza distanze)
    img_distances_color = GridVisualize.to_png(cell_size, background_type="plain_white", show_distances=False)
    img_distances_color.save("maze_distances_color.png")
    img_distances_color.show()
    # ----------------------------------------------- #


    # Distanze base (colorata con distanze)
    img_distances_distance = GridVisualize.to_png(cell_size, background_type="plain_white",
                                                              show_distances=True, distances_obj=maze_distances)
    img_distances_distance.save("maze_distances_distance.png")
    img_distances_distance.show()
    # ----------------------------------------------- #



    # Risoluzione con A*
    #root = GridVisualize[0, 0]
    #goal_cell = GridVisualize[maze_row - 1, maze_col - 1]

    solution_path = AStar.apply(MazeGrid, root, goal_cell)
    if solution_path:
        print(f"Percorso trovato con A*: {len(solution_path)} celle.")
    else:
        print("Nessun percorso trovato.")

    img_solution_path_astar = GridVisualize.to_png(cell_size, background_type="plain_white",
                                                   show_solution=True, solution_path=solution_path,
                                                   start_cell = root, end_cell = goal_cell)
    img_solution_path_astar.save("maze_solution_path_astar.png")
    img_solution_path_astar.show()
    # ----------------------------------------------- #



    # ---------------------------------------------------------- #
    # Percorso più lungo (colorato senza distanze)
    GridVisualize.distances = longest_path_distances
    img_longest_path_default = GridVisualize.to_png(cell_size, background_type="plain_white", show_distances=False)
    img_longest_path_default.save("maze_longest_path_color.png")
    img_longest_path_default.show()


    # Percorso più lungo (colorato con distanze)
    img_longest_path_distances = GridVisualize.to_png(cell_size, background_type="plain_white",
                                                                 show_distances=True, distances_obj=longest_path_distances)
    img_longest_path_distances.save("maze_longest_path_distance.png")
    img_longest_path_distances.show()


    longest_path = AStar.apply(MazeGrid, longest_path_root, longest_path_goal)
    # Percorso più lungo (colorato con percorso)
    img_longest_path_solution = GridVisualize.to_png(cell_size, background_type="plain_white",
                                                                 show_distances=False,
                                                                 show_solution=True, solution_path=longest_path,
                                                                 start_cell = longest_path_root, end_cell = longest_path_goal)
    img_longest_path_solution.save("maze_longest_path_solution.png")
    img_longest_path_solution.show()
    # ---------------------------------------------------------- #



def print_cells(grid):
    for cell in grid.each_cell():
        print(cell, "linked to:", list(cell._links))


# Copia i collegamenti del labirinto (links) dalla griglia source a quella di target.
# Assume che entrambe le griglie abbiano le stesse dimensioni.
def copy_maze_structure(source_grid: Grid, target_grid: Grid):

    for row in range(source_grid.rows):
        for col in range(source_grid.columns):

            source_cell = source_grid[row, col]
            target_cell = target_grid[row, col]  # Ottieni la cella corrispondente nella griglia di destinazione

            # Per ogni cella a cui 'source_cell' è collegata nella griglia sorgente
            for linked_source_cell in source_cell.links_as_list():

                # Ottieni la cella collegata corrispondente nella griglia di destinazione
                target_linked_cell = target_grid[linked_source_cell.row, linked_source_cell.column]

                # Collega la cella di destinazione alla sua cella collegata corrispondente.
                # Il metodo 'link' gestisce la bidirezionalità, quindi basta chiamarlo una volta per coppia.
                # Controlla se il link esiste già per evitare collegamenti ridondanti.
                if not target_cell.is_linked(target_linked_cell):
                    target_cell.link(target_linked_cell)



# Eseguo il seguente file come main dell'applicazione.
if __name__ == "__main__":
    main()

import time

from astar import AStar
from colorgrid import ColoredGrid
from analyzer import count_deadends
from analyzer import execution_time_generation
from distance_grid import DistanceGrid
from distances import Distances
from grid import Grid
from binary_tree import BinaryTree
from sidewinder import Sidewinder
from aldous_broder import AldousBroder
from recursive_backtracker import RecursiveBacktracker


def main():


    # ----------------------------------------------- #
    maze_row = 200
    maze_col = 200
    MazeGrid = Grid(maze_row,maze_col)

    start_time = time.perf_counter()
    RecursiveBacktracker.apply(MazeGrid)
    end_time = time.perf_counter()


    # Griglia per calcoli delle distanze e visualizzazione PNG
    GridVisualize = ColoredGrid(maze_row, maze_col)
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
    maze_distances = root.distances()
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
    distances_from_longest_path_root = longest_path_root.distances()

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
    # Calcolo lo shortest path
    shortest_path_goal = goal_cell

    shortest_path_distances = None  # Inizializza a None per sicurezza

    if root and shortest_path_goal:

        start_time = time.perf_counter()

        distances_from_shortest_path_root = root.distances()
        shortest_path_distances = distances_from_shortest_path_root.shortest_path_to(shortest_path_goal)

        end_time = time.perf_counter()
        execution_time = end_time - start_time

        if execution_time >= 60:
            print(f"Calcolo del percorso più corto da {root} a {shortest_path_goal} : {shortest_path_distances[shortest_path_goal]} in: [ {(execution_time/60):.3f}s | {execution_time:.3f}s | {(execution_time * 1000):.3f}ms ]\n")
        else:
            print(f"Calcolo del percorso più corto da {root} a {shortest_path_goal} : {shortest_path_distances[shortest_path_goal]} in: [ {execution_time:.3f}s | {(execution_time * 1000):.3f}ms ]\n")
    else:
        print("Errore: Le celle di root/goal per lo shortest path non sono valide.\n")
    # ----------------------------------------------- #



    # ----------------------------------------------- #
    # Un valore di 2 o 3 pixel è spesso sufficiente per cell_size=20
    #cell_inset = 6
    #cell_size = 22
    cell_inset = 7
    cell_size = 30

    # MazeGrid, grid_distances e grid_colored non cambiano nulla se non applico le distanze
    # grid_xxx.distances = maze_distances

    img_maze_checkerboard = MazeGrid.to_png(cell_size=cell_size, inset=cell_inset, background_type="checkerboard")
    img_maze_checkerboard.save("maze_checkerboard.png")
    img_maze_checkerboard.show()

    img_maze_all_white = MazeGrid.to_png(cell_size=cell_size, inset=cell_inset, background_type="plain-white")
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



    # ---------------------------------------------------------- #
    # Distanze base (colorata, senza numeri)
    img_distances_colored_only = GridVisualize.to_png(cell_size,inset=cell_inset,background_type="checkerboard")
    img_distances_colored_only.save("maze_distances_color.png")
    img_distances_colored_only.show()
    # ----------------------------------------------- #



    # ---------------------------------------------------------- #
    # Distanze base (colorata con numeri)
    img_distances_colored_with_numbers = GridVisualize.to_png_distances(maze_distances, cell_size, inset=cell_inset, background_type="checkerboard")
    img_distances_colored_with_numbers.save("maze_distances_color_distance.png")
    img_distances_colored_with_numbers.show()
    # ----------------------------------------------- #



    # ---------------------------------------------------------- #
    # Risoluzione con A*
    #root = GridVisualize[0, 0]
    #goal_cell = GridVisualize[maze_row - 1, maze_col - 1]

    solution_path = AStar.apply(MazeGrid, root, goal_cell)
    if solution_path:
        print(f"Percorso trovato con A*: {len(solution_path)} celle.")
    else:
        print("Nessun percorso trovato.")

    img_solution_path_astar = GridVisualize.to_png_solution_path(cell_size, cell_inset, solution_path, root, goal_cell)
    img_solution_path_astar.save("maze_solution_path_astar.png")
    img_solution_path_astar.show()
    # ----------------------------------------------- #



    # ---------------------------------------------------------- #
    # Percorso più lungo (colorato senza numeri)
    GridVisualize.distances = longest_path_distances
    img_longest_path_colored_only = GridVisualize.to_png(cell_size, inset=cell_inset)
    img_longest_path_colored_only.save("maze_longest_path_color.png")
    img_longest_path_colored_only.show()

    # Percorso più lungo (colorato con numeri)
    img_longest_path_colored_with_numbers = GridVisualize.to_png_distances(longest_path_distances, cell_size, inset=cell_inset)
    img_longest_path_colored_with_numbers.save("maze_longest_path_color_distance.png")
    img_longest_path_colored_with_numbers.show()

    # Percorso più lungo (con freccie)
    img_longest_path_arrows = GridVisualize.to_pgn_arrows(longest_path_distances, cell_size, inset=cell_inset)
    img_longest_path_arrows.save("maze_longest_path_arrow.png")
    img_longest_path_arrows.show()
    # ---------------------------------------------------------- #



    # ---------------------------------------------------------- #
    # Percorso più breve tra root e goal (colorato senza numeri)
    GridVisualize.distances = shortest_path_distances
    img_shortest_path_colored_only = GridVisualize.to_png(cell_size, inset=cell_inset)
    img_shortest_path_colored_only.save("maze_shortest_path_color.png")
    img_shortest_path_colored_only.show()

    # Percorso più breve tra root e goal (colorato con numeri)
    img_shortest_path_colored_only = GridVisualize.to_png_distances(shortest_path_distances, cell_size, inset=cell_inset)
    img_shortest_path_colored_only.save("maze_shortest_path_distance.png")
    img_shortest_path_colored_only.show()

    # Percorso più breve tra root e goal (con freccie)
    img_shortest_path_arrows = GridVisualize.to_pgn_arrows(shortest_path_distances, cell_size, inset=cell_inset)
    img_shortest_path_arrows.save("maze_shortest_path_arrow.png")
    img_shortest_path_arrows.show()
    # ----------------------------------------------- #



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
            for linked_source_cell in source_cell.all_links():

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

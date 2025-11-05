import random


# Generative algorithm Recursive Backtracker.
#
# Choose a random cell, explore the unvisited cells among the neighbors.
# If no more unvisited neighbors cells are available, the algorithm
# backtracks the path and finds a new cell with unvisited neighbors.
class RecursiveBacktracker:


    # The algorithm cuts through the maze creating the corridors.
    # Cutting means linking a cell to another one.
    #
    # - Choose a random cell.
    # - Initialize the stack of cells to be visited and add the first cell.
    # - Loop through the stack of visited cells, and for every cell visit its neighbors
    #   that are still not linked to the current cell.
    #   - If there are no more neighbor cells still not linked,
    #     remove the current cell from the stack of the visited cells.
    #   - Else choose randomly a neighbor cell, link the current cell to the neighbor cell
    #     and add the neighbor cell to the stack of the visited cells.
    @staticmethod
    def apply(grid):

        starting_cell = grid.random_cell()

        visited_cells = []
        visited_cells.append(starting_cell)

        # Loop through the visited cells and visit their neighbors.
        # Get the last cell on the stack (without removing it).
        while visited_cells:

            current_cell = visited_cells[-1]

            # Look for neighbors cells still not linked with the current one.
            unlinked_neighbors = [
                neighbor for neighbor in current_cell.all_neighbors()
                if not neighbor.all_linked()
            ]

            # No more neighbor cells still not linked.
            if not unlinked_neighbors:
                visited_cells.pop()
            else:
                neighbor_cell = random.choice(unlinked_neighbors)
                current_cell.link(neighbor_cell)
                visited_cells.append(neighbor_cell)

        return grid
    # ----------------------------------------------- #
import random


# Generative algorithm Aldous-Broder.
#
# Choose to move towards a random direction.
# If the cell now visited was never visited before,
# link it to the previous cell.
# If the cell now visited was already visited, simply
# choose a new random neighbor from it.
class AldousBroder:


    # The algorithm cuts through the maze creating the corridors.
    # Cutting means linking a cell to another one.
    #
    # - Initialize a set of unvisited cells as all the cells of the grid.
    # - Choose a random cell of the grid as the starting cell.
    # - Loop through the set and for every current cell, visit a random neighbor of it,
    #   if the neighbor cell is still in the set of the unvisited cells then this is
    #   the first time visiting it, so the neighbor cell is linked to the current cell and
    #   removed from the set of unvisited cells.
    #   The neighbor cell is now visited, making it the new current cell, so we move on with a new random neighbor.
    @staticmethod
    def apply(grid):

        # Initialize a set of all the cells of the grid.
        # Using a set makes the operation of checking if a cell is still in the set
        # computationally O(1).
        unvisited_cells = set(grid.each_cell())

        current_cell = grid.random_cell()

        # The starting cell is already visited.
        unvisited_cells.remove(current_cell)

        # Choose a random neighbor from the current cell.
        # If the random neighbor was never visited before, then link it to the current cell.
        # Make the random neighbor the new current cell.
        while unvisited_cells:

            neighbor_cell = random.choice(current_cell.all_neighbors())

            if neighbor_cell in unvisited_cells:
                current_cell.link(neighbor_cell)
                unvisited_cells.remove(neighbor_cell)

            current_cell = neighbor_cell

        return grid
    # ----------------------------------------------- #
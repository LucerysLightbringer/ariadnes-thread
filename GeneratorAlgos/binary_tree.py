import random


# Generative algorithm Binary Tree.
#
# Starting from the first cell of the maze ([0][0]),
# and looping on the grid row by row, choose randomly to cut north or east.
class BinaryTree:


    # The algorithm cuts through the maze creating the corridors.
    # Cutting means linking a cell to another one.
    #
    # - Loop through the grid row by row.
    #   - Choose randomly to cut towards the north and east neighbors of the current cell.
    @staticmethod
    def apply(grid):

        # Loop through the grid.
        for cell in grid.each_cell():

            # Save the available directions to cut towards to.
            directions = []

            if cell.north:
                directions.append(cell.north)

            if cell.east:
                directions.append(cell.east)

            # Cut towards the direction chosen randomly.
            if directions:
                neighbor = random.choice(directions)
                cell.link(neighbor)

        return grid
    # ----------------------------------------------- #
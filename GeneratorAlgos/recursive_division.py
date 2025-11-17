import random


# Generative algorithm Recursive Division.
#
# Create an empty grid.
# Choose randomly to create a wall horizontally or vertically.
# Repeat recursively on the two subsections created.
class RecursiveDivision:


    # The algorithm generates the maze by creating the walls.
    #
    # - Create an empty grid, linking each cell with its 4 neighbors.
    # - Choose randomly to divide horizontally or vertically.
    # - Choose a random index of a row or column, then create a wall on that index
    #   and lastly, carve a single corridor along a random index of the wall.
    # - Repeat recursively for every subsection created.
    @staticmethod
    def apply(grid):

        # Link every cell with its neighbors.
        for cell in grid.each_cell():
            for neighbor in cell.all_neighbors():
                cell.link(neighbor, bidirectional=False)

        # Start the recursive function.
        RecursiveDivision._divide(grid, 0, 0, grid.rows, grid.columns)

        return grid
    # ----------------------------------------------- #


    # Start the actual division of the grid.
    @staticmethod
    def _divide(grid, row, col, rows, columns):

        # The subsection can't be smaller.
        if rows <= 1 or columns <= 1:
            return

        # Divide horizontally or vertically.
        if rows >= columns:
            RecursiveDivision._divide_horizontal(grid, row, col, rows, columns)
        else:
            RecursiveDivision._divide_vertical(grid, row, col, rows, columns)
    # ----------------------------------------------- #


    # Internal method for horizontal division.
    @staticmethod
    def _divide_horizontal(grid, row, col, rows, columns):

        # Choose a random row on which to create a wall.
        # The index of the row is the NORTH side of that cell.
        wall_south = random.randrange(rows - 1)

        # Choose a random column on which to carve a corridor along the wall created.
        passage = random.randrange(columns)

        # Loop through the index and create the wall and carve the corridor.
        # If the current cell is the entrance of the corridor,
        # then ignore it and continue to the next cell.
        # Create the wall by removing the link.
        for position in range(columns):

            if passage == position:
                continue

            cell = grid[row + wall_south, col + position]
            if cell and cell.south:
                cell.unlink(cell.south)


        # Recursively divide on the two subsections created.
        RecursiveDivision._divide(grid, row, col, wall_south + 1, columns)
        RecursiveDivision._divide(grid, row + wall_south + 1, col, rows - wall_south - 1, columns)
    # ----------------------------------------------- #


    # Internal method for vertical division.
    @staticmethod
    def _divide_vertical(grid, row, col, rows, columns):

        # Choose a random row on which to create a wall.
        # The index of the row is the WEST side of that cell.
        wall_east = random.randrange(columns - 1)

        # Choose a random column on which to carve a corridor along the wall created.
        passage = random.randrange(rows)

        # Loop through the index and create the wall and carve the corridor.
        # If the current cell is the entrance of the corridor,
        # then ignore it and continue to the next cell.
        # Create the wall by removing the link.
        for position in range(rows):

            if passage == position:
                continue

            cell = grid[row + position, col + wall_east]
            if cell and cell.east:
                cell.unlink(cell.east)


        # Recursively divide on the two subsections created.
        RecursiveDivision._divide(grid, row, col, rows, wall_east + 1)
        RecursiveDivision._divide(grid, row, col + wall_east + 1, rows, columns - wall_east - 1)
    # ----------------------------------------------- #
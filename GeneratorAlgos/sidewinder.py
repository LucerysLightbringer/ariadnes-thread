import random


# Generative algorithm Sidewinder.
#
# Starting from the first cell of the maze ([0][0]),
# and looping on the grid row by row, choose randomly
# to continue east or directly cut north.
class Sidewinder:


    # The algorithm cuts through the maze creating the corridors.
    # Cutting means linking a cell to another one.
    #
    # - Loop through the grid row by row.
    #   - Initialize an array of cells, called "group". The group is reset at the start of every row.
    #   - Loop through the cells of the current row.
    #     - Add the current cell to the group.
    #
    #     - If the cell is along the east edge, going east is not possible, and the group is closed.
    #     - If the cell is along the north edge, going north is not possible, and the group is closed.
    #
    #     - Choose randomly to cut towards east or to choose a random cell from the group
    #       and cut towards north through that cell.
    @staticmethod
    def apply(grid):

        # Loop through the grid row by row.
        for row in grid.each_row():

            # Define the current row group.
            group = []

            # Loop through the cells of the row.
            for cell in row:

                group.append(cell)

                east_edge = cell.east is None   # Going east is impossible. Close the group.
                north_edge = cell.north is None # Going north is impossible. Close the group.

                # Randomly choose to directly cut towards east or adding to the group
                # and cut towards north.
                is_group_closed = (east_edge or (not north_edge and random.randint(0,1) == 0))

                # Choose a random cell from the group,
                # cut north of the cell and reset the group,
                # a new cell from the row will be chosen.
                if is_group_closed:

                    new_cell = random.choice(group)

                    if new_cell.north:
                        new_cell.link(new_cell.north)

                    group.clear()

                # Cut east.
                else:
                    cell.link(cell.east)

        return grid
    # ----------------------------------------------- #
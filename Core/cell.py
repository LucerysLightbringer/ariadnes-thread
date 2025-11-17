from Core.distances import Distances # for the function calc_all_distances()

# Define a cell of the grid as a 2D point (row,column).
# Define for every cell its neighbors (north,south,east,west).
# Define for every cell the cells which it is linked to,
# meaning with which it has a corridor to explore.
class Cell:


    # Constructor
    def __init__(self, r, c):

        # Set the position of the cell.
        self.row = r
        self.column = c

        # Set the default neighbors of the cell.
        self.north = None
        self.south = None
        self.east = None
        self.west = None

        # A boolean dictionary (cell,linked) is used
        # to keep track of which cells are linked to the current cell,
        # meaning with which cells the cell creates a corridor with.
        self._links = {}
    # ----------------------------------------------- #


    # Link the current cell to another cell (self -> another_cell).
    # If bidirectional = True, also link another_cell to self (another_cell -> self).
    def link(self, another_cell, bidirectional=True):

        self._links[another_cell] = True

        if bidirectional:
            another_cell.link(self, False)

        return self
    # ----------------------------------------------- #


    # Unlink self from another_cell.
    # If bidirectional = True, also unlink another_cell from self.
    def unlink(self, another_cell, bidirectional=True):

        if another_cell in self._links:
            del self._links[another_cell]

        if bidirectional:
            another_cell.unlink(self, False)

        return self
    # ----------------------------------------------- #


    # Return all the cells linked to the current one.
    def all_linked(self):
        return self._links.keys()
    # ----------------------------------------------- #


    # Return True if the current cell is linked to another cell.
    def is_linked(self, another_cell):
        return another_cell in self._links
    # ----------------------------------------------- #


    # Return all the neighbors cell of the current one.
    # Note that neighbors cells don't have to be linked to the current cell.
    def all_neighbors(self):

        neighbors = []

        if self.north:
            neighbors.append(self.north)

        if self.south:
            neighbors.append(self.south)

        if self.east:
            neighbors.append(self.east)

        if self.west:
            neighbors.append(self.west)

        return neighbors
    # ----------------------------------------------- #


    # Calculate the distances of every cell from the current cell (root cell).
    # The algorithm used is the BFS.
    # Return a Distances object, which is a dictionary (cell,distance).
    def calc_all_distances(self):

        # Create a Distances object.
        # The root is the current cell (self) from which all distances are calculated.
        # The Distances object is a simple dictionary (cell,distance).
        distances = Distances(self)

        # Array of frontier cells, initialized with the current cell (self).
        frontier = [self]

        # While unexplored cells exist, loop through the maze.
        while frontier:

            # Save all unexplored cells that are linked with the cells
            # of the frontier.
            new_frontier = []

            # Loop through the frontier.
            for cell in frontier:

                # For every cell linked to the current one.
                for linked in cell.all_linked():

                    # If the cell was already explored,
                    # exit the current iteration and continue with
                    # the next linked cell.
                    if distances[linked] is not None:
                        continue

                    # If the cell is unexplored, explore it
                    # and calc the distance relative to the previous one.
                    distances[linked] = distances[cell] + 1 # distance from the current cell + 1
                    new_frontier.append(linked)             # add to the frontier the linked cell

            # Reload the frontier with the newly explored cells.
            frontier = new_frontier

        return distances
    # ----------------------------------------------- #


    # Cells must be hashable, otherwise they can't be used
    # as keys in a dictionary.
    def __hash__(self):
        return hash((self.row, self.column))
    # ----------------------------------------------- #


    # Cells must be comparable, otherwise they can't be used
    # as keys in a dictionary.
    def __eq__(self, other):
        return (isinstance(other, Cell) and
                (self.row == other.row) and
                (self.column == other.column))
    # ----------------------------------------------- #


    # String representation of the cell.
    def __str__(self):
        return f"({self.row}, {self.column})"
    # ----------------------------------------------- #


    # Debugging representation of the cell.
    def __repr__(self):
        return f"({self.row}, {self.column})"
    # ----------------------------------------------- #
# Class used to save the distances of every cell of the maze starting from a root cell.
class Distances:


    # Constructor
    def __init__(self, root):

        # The constructor simply initializes a dictionary
        # with distance from the root set to 0.

        self.root = root        # arbitrary root cell is explicit
        self._cells = {root: 0} # a dictionary to save (cell,distance) for every cell
    # ----------------------------------------------- #


    # Define the [index] syntax to get the distance of a single cell from the root.
    # If the cell doesn't exist, return None.
    def __getitem__(self, cell):
        return self._cells.get(cell)
    # ----------------------------------------------- #


    # Define the [index] syntax to set the distance of a single cell from the root.
    def __setitem__(self, cell, distance):
        self._cells[cell] = distance
    # ----------------------------------------------- #


    # Return the dictionary as a read-only variable. Ritorna la lista di tutte le distanze.
    # @property is used to be able to use the getter and setter on _cells.key().
    @property
    def all_cells(self):
        # This is only a "view" of the dictionary.
        # If the distances must be mutable, then return list(self._cells).
        return self._cells.keys()
    # ----------------------------------------------- #


    # Using the distances dictionary, calculate the shortest path
    # from the root to a specified goal cell.
    # Return a dictionary (Distances object) with the path and the list of cells (path_cells).
    def shortest_path_to(self, cell_goal):

        current_cell = cell_goal
        backtrack_dist = Distances(self.root) # get all the distances from the root.
        backtrack_dist[current_cell] = self[current_cell]
        path_cells = [current_cell] # initialize the list path.

        # While the root cell is not visited.
        while current_cell != self.root:

            # Get all the cells linked to the current cell,
            # meaning all the cells for which the current cell has a path to.
            for linked_cell in current_cell.all_linked():

                # Handle the case: linked_cell is None.
                linked_dist = self[linked_cell]
                current_dist = self[current_cell]

                # If a linked cell has a shorter distance than the current cell,
                # the linked cell is the one from which the path came.
                if linked_dist is not None and linked_dist < current_dist:

                    # The linked cell is now the new current cell,
                    # exit this iteration and continue with the new current cell.
                    backtrack_dist[linked_cell] = linked_dist
                    current_cell = linked_cell
                    path_cells.append(current_cell) # update the path.
                    break

        # Return the distances object and the path.
        return backtrack_dist, path_cells
    # ----------------------------------------------- #


    # Calculate the cell with the farthest distance from the root.
    # Return a tuple (cell, distance, path_cells).
    def longest_path_from(self):

        max_distance = 0
        max_cell = self.root  # start from the root

        # Loop through the Distances dictionary.
        for cell, dist in self._cells.items():

            if dist > max_distance:
                max_cell = cell
                max_distance = dist

        # Get the path from root to farthest cell.
        # shortest_path_to returns (distances, path).
        _, path_cells = self.shortest_path_to(max_cell)

        # The path is from farthest cell to root, so reverse it.
        path_cells.reverse()

        # Return the farthest cell, the farthest distance and the longest path.
        return max_cell, max_distance, path_cells
    # ----------------------------------------------- #
import heapq  # priority queue (min-heap)


# Resolutive algorithm A*.
class AStar:


    @staticmethod
    def apply(grid, root, goal_cell):

        # Tie-breaker counter to avoid conflicts in the priority queue
        # for the same f_score value.
        tie_breaker = 0

        # Priority queue of the cells to be explored.
        # Cells with lower f_score (F(n)) have a higher priority.
        visited_cells = []

        # The tuples inserted in the heap are as follows: (f_score, tie_breaker, cell).
        # The starting cell is inserted and the tie-breaker value is increased for the next tuple.
        heapq.heappush(visited_cells, (AStar._manhattan_distance(root, goal_cell), tie_breaker, root))
        tie_breaker += 1

        # Dictionary (cell, parent cell) to save the solution path.
        path = {}

        # Dictionary (cell, cost to reach it).
        # g_score is the cost of path from the starting cell to the current cell.
        # Initialize all costs to infinite.
        # The cost to reach the starting cell from itself is 0.
        g_score = {cell: float('inf') for cell in grid.each_cell()}
        g_score[root] = 0

        # Dictionary (cell, cost to reach it).
        # f_score is the estimated total cost of the path: F(n) = g(n) + h(n).
        # Initialize all costs to infinite.
        # Calculate the f_score of the starting cell.
        f_score = {cell: float('inf') for cell in grid.each_cell()}
        f_score[root] = AStar._manhattan_distance(root, goal_cell)


        # Loop through the priority queue of the cells to be explored.
        while visited_cells:

            # Get the cell with the lowest f_score.
            # If there are more than one cell with the lowest f_score, then the cell
            # with the lowest tie_breaker (the first inserted among them) is extracted.
            # The tie_breaker value is not used, we only need the current_f_score and the current_cell.
            current_f_score, _, current_cell = heapq.heappop(visited_cells)

            # If the current cell is the goal cell,
            # then the solution path is reconstructed.
            if current_cell == goal_cell:

                # Reconstruct the path from the end to the start.
                solution_path = []
                temp = goal_cell

                while temp in path:
                    solution_path.append(temp)
                    temp = path[temp]

                solution_path.append(root)
                return solution_path[::-1] # reverse the path.


            # Else, if the current cell is not the goal cell,
            # visit the cells linked to the current one.
            for neighbor in current_cell.all_linked():

                # The cost to reach the linked cell passing through the current cell.
                # The types of mazes generated only allow for unitary costs.
                current_g_score = g_score[current_cell] + 1

                # If the current path for the linked cell is shorter
                # than the previous path, update the costs of the linked cell
                # and add the linked cell to the priority queue.
                if current_g_score < g_score[neighbor]:

                    # Update the parent cell and the costs of the linked cell.
                    path[neighbor] = current_cell
                    g_score[neighbor] = current_g_score
                    f_score[neighbor] = g_score[neighbor] + AStar._manhattan_distance(neighbor, goal_cell)

                    # Add the linked cell to the priority queue for future exploration
                    # of the maze starting from it.
                    heapq.heappush(visited_cells, (f_score[neighbor], tie_breaker, neighbor))
                    tie_breaker += 1  # increase the tie-breaker for the next tuple.

        # If the while loop finishes and the goal cell is not reached,
        # no solution path exists.
        return []
    # ----------------------------------------------- #


    # Internal method for Manhattan distance.
    @staticmethod
    def _manhattan_distance(cell1, cell2):
        return abs(cell1.row - cell2.row) + abs(cell1.column - cell2.column)
    # ----------------------------------------------- #
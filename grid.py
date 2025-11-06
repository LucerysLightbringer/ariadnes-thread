from random import randrange
from PIL import Image, ImageDraw, ImageFont  # Pillow library for image manipulation functions.
from cell import Cell
from distances import Distances


# Define a maze as a (rows x columns) grid.
class Grid:


    # Constructor
    def __init__(self, rows, columns):

        # Size of the grid.
        self.rows = rows
        self.columns = columns

        # Create an empty grid.
        self._grid = self._create_grid()

        # Set the cells of the grid.
        self._configure_cells()

        self._distances = None      # distances of every cell from the root
        self._max_distance = 0      # max distance from the root
    # ----------------------------------------------- #


    # Create an empty grid.
    def _create_grid(self):

        grid = []

        for row in range(self.rows):

            row_list = []

            for col in range(self.columns):
                cell = Cell(row, col)
                row_list.append(cell)

            grid.append(row_list)

        return grid
    # ----------------------------------------------- #


    # Define every neighbor cell for every cell of the grid.
    def _configure_cells(self):

        for cell in self.each_cell():

            row, col = cell.row, cell.column

            cell.north = self[row - 1, col]
            cell.south = self[row + 1, col]
            cell.west  = self[row, col - 1]
            cell.east  = self[row, col + 1]
    # ----------------------------------------------- #


    # Getter for the 'distances' property.
    @property
    def distances(self):
        return self._distances
    # ----------------------------------------------- #


    # Setter for the 'distances' property.
    @distances.setter
    def distances(self, distances_obj: Distances):

        self._distances = distances_obj

        # Find the most distant cell with the function longest_path_from().
        if distances_obj:
            farthest_cell, self._max_distance = distances_obj.longest_path_from()
        else:
            self._max_distance = 0
    # ----------------------------------------------- #


    # Define the [row][col] syntax to get a single cell.
    # If the indexes are out of bounds, return None.
    def __getitem__(self, position):

        row, column = position

        if 0 <= row < self.rows and 0 <= column < self.columns:
            return self._grid[row][column]

        return None
    # ----------------------------------------------- #


    # Return the rows of the grid one at a time.
    def each_row(self):
        for row in self._grid:
            yield row
    # ----------------------------------------------- #


    # Return the cells of the grid one at a time.
    def each_cell(self):

        for row in self.each_row():
            for cell in row:

                # Return the cell only if it actually exists.
                if cell:
                    yield cell
    # ----------------------------------------------- #


    # Return a random cell within the grid.
    def random_cell(self):

        row = randrange(self.rows)
        column = randrange(self.columns)

        return self[row, column]
    # ----------------------------------------------- #


    # Return the size of the grid as the total number of cells.
    def size(self):
        return self.rows * self.columns
    # ----------------------------------------------- #


    # Return the set of deadends of the maze.
    # A dead end is a cell which is linked to only another cell.
    def deadends(self):

        deadends = []

        for cell in self.each_cell():

            if len(cell.all_linked()) == 1:
                deadends.append(cell)

        return deadends
    # ----------------------------------------------- #


    # Internal method to color the cells based on the distances.
    # Return a map: map[cell] = (r,g,b).
    def _color_by_distances(self, distances_obj,
                                  color_start,
                                  color_middle,
                                  color_end,
                                  smooth_exp,
                                  cell_subset):

        # Get max distance.
        _, max_dist = distances_obj.longest_path_from()

        if max_dist == 0:
            return {} # return empty map.


        # Only a subset must be colored as a gradient.
        if cell_subset is None:
            cells_color = distances_obj.all_cells
        else:
            cells_color = cell_subset

        # The map that associates cells with their color.
        color_map = {}

        for cell in cells_color: #self.each_cell():

            dist = distances_obj[cell]

            if dist is None:
                continue

            intensity = (max_dist - dist) / max_dist
            interpolation = max(0.0, min(1.0, intensity ** smooth_exp))

            if interpolation < 0.5:
                # From dark green to light green.
                local_interpolation = interpolation * 2
                red = int(color_end[0] + (color_middle[0] - color_end[0]) * local_interpolation)
                green = int(color_end[1] + (color_middle[1] - color_end[1]) * local_interpolation)
                blue = int(color_end[2] + (color_middle[2] - color_end[2]) * local_interpolation)
            else:
                # From light green to white.
                local_interpolation = (interpolation - 0.5) * 2
                red = int(color_middle[0] + (color_start[0] - color_middle[0]) * local_interpolation)
                green = int(color_middle[1] + (color_start[1] - color_middle[1]) * local_interpolation)
                blue = int(color_middle[2] + (color_start[2] - color_middle[2]) * local_interpolation)

            color_map[cell] = (red, green, blue)

        return color_map
    # ----------------------------------------------- #


    # Internal method to color the entire maze, cell by cell, considering
    # all possible options.
    # Return a map: map[cell] = (r,g,b).
    def _color_map(self,
                   show_distances_gradient, distances_obj,
                   show_subset_gradient, subset_cells,
                   show_deadends, deadend_color,
                   color_start, color_middle, color_end, smooth_exp):

        global_color_map = {}

        # Color all the cells based on distances if specified.
        if show_distances_gradient and distances_obj:
            gradient_map = self._color_by_distances(
                distances_obj,
                color_start, color_middle, color_end, smooth_exp,
                cell_subset=None)
            global_color_map.update(gradient_map)

        # Color only a subset of cells.
        if show_subset_gradient and subset_cells:
            gradient_map = self._color_by_distances(
                distances_obj,
                color_start, color_middle, color_end, smooth_exp,
                subset_cells)
            global_color_map.update(gradient_map)

        # Color the deadends if specified.
        if show_deadends:
            deadends = self.deadends()
            for cell in deadends:
                global_color_map[cell] = deadend_color


        return global_color_map
    # ----------------------------------------------- #


    # Internal method for drawing the solution path.
    def _draw_solution_details(self,
                            draw,
                            cell_size,
                            show_solution, solution_path,
                            path_color, text_color,
                            start_cell, start_cell_color,
                            end_cell, end_cell_color):

        # Draw the solution path (only if requested).
        if show_solution and solution_path:

            # Define the default starting cell (the root of the solution),
            # and ending cell (the goal cell of the solution).
            if start_cell is None:
                start_cell = solution_path[0]

            if end_cell is None:
                end_cell = solution_path[-1]

            # Draw the solution path.
            for i in range(len(solution_path) - 1):

                cell1 = solution_path[i]
                cell2 = solution_path[i + 1]

                cx1 = cell1.column * cell_size + cell_size // 2
                cy1 = cell1.row * cell_size + cell_size // 2
                cx2 = cell2.column * cell_size + cell_size // 2
                cy2 = cell2.row * cell_size + cell_size // 2

                draw.line((cx1, cy1, cx2, cy2), fill=path_color, width=max(1, cell_size // 10))


            # Load the font for the text (S for the root cell, E for the goal cell).
            try:
                current_font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", size=15)
            except IOError:
                current_font = ImageFont.load_default()


            if start_cell:
                sx1 = start_cell.column * cell_size
                sy1 = start_cell.row * cell_size
                sx2 = (start_cell.column + 1) * cell_size
                sy2 = (start_cell.row + 1) * cell_size
                draw.rectangle((sx1 + 1, sy1 + 1, sx2 - 1, sy2 - 1), fill=start_cell_color)
                text_x = start_cell.column * cell_size + cell_size // 3
                text_y = start_cell.row * cell_size + cell_size // 3
                draw.text((text_x, text_y), "S", fill=text_color, font=current_font)

            if end_cell:
                ex1 = end_cell.column * cell_size
                ey1 = end_cell.row * cell_size
                ex2 = (end_cell.column + 1) * cell_size
                ey2 = (end_cell.row + 1) * cell_size
                draw.rectangle((ex1 + 1, ey1 + 1, ex2 - 1, ey2 - 1), fill=end_cell_color)
                text_x = end_cell.column * cell_size + cell_size // 4
                text_y = end_cell.row * cell_size + cell_size // 4
                draw.text((text_x, text_y), "E", fill=text_color, font=current_font)
    # ----------------------------------------------- #


    # Internal method for drawing the distance value.
    def _draw_distance_value(self,
                             draw,
                             cell, cell_size,
                             show_distance_text, distances_obj,
                             current_font, font_small,text_color):

        if show_distance_text and distances_obj and distances_obj[cell] is not None:

            # Center the text.
            text_position_x = cell.column * cell_size + cell_size // 3
            text_position_y = cell.row * cell_size + cell_size // 3

            if distances_obj[cell] is not None and distances_obj[cell] >= 1000:
                current_font = font_small

            draw.text((text_position_x, text_position_y), str(distances_obj[cell]), fill=text_color, font=current_font)
    # ----------------------------------------------- #


    # Internal method for drawing the walls of every cell.
    def _draw_cell_walls(self,
                         draw,
                         cell_size,
                         thick_wall_width, thick_wall_color):

        for cell in self.each_cell():

            x1 = cell.column * cell_size
            y1 = cell.row * cell_size
            x2 = (cell.column + 1) * cell_size
            y2 = (cell.row + 1) * cell_size

            if not cell.north:
                draw.line([(x1, y1), (x2, y1)], width=thick_wall_width, fill=thick_wall_color)
            if not cell.west:
                draw.line([(x1, y1), (x1, y2)], width=thick_wall_width, fill=thick_wall_color)
            if not cell.is_linked(cell.east):
                draw.line([(x2, y1), (x2, y2)], width=thick_wall_width, fill=thick_wall_color)
            if not cell.is_linked(cell.south):
                draw.line([(x1, y2), (x2, y2)], width=thick_wall_width, fill=thick_wall_color)
    # ----------------------------------------------- #


    # Internal method to choose the cell color.
    def _choose_cell_color(self,
                           global_color_map, cell,
                           background_type, checkerboard_color_1, checkerboard_color_2, full_color):

        cell_color = None

        # Define the color of the cell based on the distance (from the root)
        # as a gradient of three colors.
        if cell in global_color_map:
            cell_color = global_color_map[cell]

        # Else, if the color is not based on the distances,
        # then revert to the default types.
        elif background_type == "checkerboard":
            if (cell.row + cell.column) % 2 == 0:
                cell_color = checkerboard_color_1
            else:
                cell_color = checkerboard_color_2
        elif background_type == "full_color":
            cell_color = full_color

        return cell_color
    # ----------------------------------------------- #


    #  Print the maze as a PNG image.
    def to_png(self,
               cell_size=10,

               background_type="full_color",
               full_color=(255,255,255),
               checkerboard_color_1=(255, 255, 255),
               checkerboard_color_2=(220, 220, 220), # light gray

               thin_wall_color=(50, 50, 50), # black
               thin_wall_width=1,

               thick_wall_color=(0,0,0), # black
               thick_wall_width=3,

               text_color=(240,50,255),       # purple
               path_color=(240,50,255),       # purple

               gradient_start=(235,235,235),  # gray
               gradient_middle=(0,180,0),     # light green
               gradient_end=(0,30,0),         # dark green
               smooth_exp=0.65,

               start_cell_color=(255,200,0),  # yellow
               end_cell_color=(0,255,255),    # cyan
               deadend_color=(255,0,0),       # red

               show_distances_gradient=False, distances_obj=None, show_distance_text=False,
               show_subset_gradient=False, subset_cells=None,
               show_solution=False, solution_path=None,
               show_deadends=False,
               start_cell=None, end_cell=None):


        # Create the default PNG image.
        img_width = cell_size * self.columns
        img_height = cell_size * self.rows
        img = Image.new("RGB", (img_width + 1, img_height + 1), "white")
        draw = ImageDraw.Draw(img)

        # Get the color of every cell of the maze.
        global_color_map = self._color_map(
            show_distances_gradient=show_distances_gradient, distances_obj=distances_obj,
            show_subset_gradient=show_subset_gradient, subset_cells=subset_cells,
            show_deadends=show_deadends,
            deadend_color=deadend_color,
            color_start=gradient_start, color_middle=gradient_middle, color_end=gradient_end, smooth_exp=smooth_exp)

        current_font = None
        font_normal = None
        font_small = None

        # Load fonts only if requested (only if the distances must be written on every cell).
        if show_distance_text and distances_obj:
            try:
                font_normal = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", size=9)
                font_small = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", size=8)
                current_font = font_normal
            except IOError:
                current_font = ImageFont.load_default()


        # Define the position, size and color of every cell.
        for cell in self.each_cell():

            # Vertexes of the cell.
            x1 = cell.column * cell_size
            y1 = cell.row * cell_size
            x2 = (cell.column + 1) * cell_size
            y2 = (cell.row + 1) * cell_size

            cell_color = self._choose_cell_color(global_color_map, cell,
                                                 background_type, checkerboard_color_1, checkerboard_color_2, full_color)

            # Coloring the cell.
            draw.rectangle([x1, y1, x2, y2], fill=cell_color)


            # Draw thin walls around every cell.
            # These walls are only drawn to make it easier to distinguish the cells.
            draw.line([(x1, y1), (x2, y1)], fill=thin_wall_color, width=thin_wall_width)
            draw.line([(x1, y1), (x1, y2)], fill=thin_wall_color, width=thin_wall_width)
            draw.line([(x2, y1), (x2, y2)], fill=thin_wall_color, width=thin_wall_width)
            draw.line([(x1, y2), (x2, y2)], fill=thin_wall_color, width=thin_wall_width)


            # Write the distance value on the cell (only if requested).
            self._draw_distance_value(draw,
                                      cell, cell_size,
                                      show_distance_text, distances_obj,
                                      current_font,
                                      font_small,
                                      text_color)

        # Draw the actual walls that makes the maze.
        self._draw_cell_walls(draw,
                              cell_size,
                              thick_wall_width, thick_wall_color)


        # Draw the solution path and the start and ending cells.
        self._draw_solution_details(draw,
                                    cell_size,
                                    show_solution, solution_path,
                                    path_color, text_color,
                                    start_cell, start_cell_color,
                                    end_cell, end_cell_color)

        return img
    # ----------------------------------------------- #
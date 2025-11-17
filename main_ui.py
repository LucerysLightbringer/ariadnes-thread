import tkinter as tk
from tkinter import ttk, filedialog, colorchooser

from PIL import Image, ImageTk

from Core.grid import Grid
from SolverAlgos.astar import AStar
from GeneratorAlgos.binary_tree import BinaryTree
from GeneratorAlgos.sidewinder import Sidewinder
from GeneratorAlgos.aldous_broder import AldousBroder
from GeneratorAlgos.recursive_backtracker import RecursiveBacktracker
from GeneratorAlgos.recursive_division import RecursiveDivision
from UI import GenerationFrame, DetailsFrame, DisplayFrame, ColorPickerFrame, OptionsFrame, SaveMazeFrame


class MazeApp:


    def __init__(self, window):

        # Window configuration.
        self.window = window
        self.window.title("Ariadne's Thread")
        self.window.geometry("1400x950")
        self.window.wm_iconphoto(False, tk.PhotoImage(file="icons8-clew-32.png"))
        self.window.resizable(False, False)
        self.window.configure(background="white")

        # Default values.
        self.DEFAULT_ROWS = 20
        self.DEFAULT_COLUMNS = 20
        self.DEFAULT_CELL_SIZE = 22
        self.DEFAULT_THIN_WALL = 1
        self.DEFAULT_THICK_WALL = 3
        self.DEFAULT_SMOOTH_EXP = 0.65
        self.DEFAULT_COLORS = {
            "start_cell_color": "#FFFF00",
            "end_cell_color": "#00FFFF",
            "path_color": "#800080",
            "text_color": "#800080",
            "deadend_color": "#FF0000",
            "gradient_start": "#D3D3D3",
            "gradient_middle": "#7CFC00",
            "gradient_end": "#355E3B",
            "thin_wall_color": "#424242",
            "thick_wall_color": "#000000",
            "background_color": "#FFFFFF",
            "checkerboard_color_1": "#FFFFFF",
            "checkerboard_color_2": "#DFDFDF"
        }


        # Status variables.
        self.maze_grid = None
        self.tk_image = None
        self.zoom_level = 1.0
        self.distances_all = None
        self.distance_start_cell = None
        self.subset_path = None
        self.solution_path = None
        self.solution_start_cell = None
        self.solution_end_cell = None
        self.longest_path_start_cell = None
        self.longest_path_end_cell = None
        self.longest_path_distances = None
        self.longest_path = None


        # UI variables.
        self.rows = tk.IntVar(value=self.DEFAULT_ROWS)
        self.columns = tk.IntVar(value=self.DEFAULT_COLUMNS)
        self.cell_size = tk.IntVar(value=self.DEFAULT_CELL_SIZE)
        self.smooth_exp = tk.DoubleVar(value=self.DEFAULT_SMOOTH_EXP)
        self.original_image = self._default_image()
        self.current_image = self._default_image()


        self.start_cell_r = tk.IntVar(value=0)
        self.start_cell_c = tk.IntVar(value=0)
        self.end_cell_r = tk.IntVar(value=19)
        self.end_cell_c = tk.IntVar(value=19)
        self.distance_start_r = tk.IntVar(value=0)
        self.distance_start_c = tk.IntVar(value=0)
        self.thin_wall_width = tk.IntVar(value=self.DEFAULT_THIN_WALL)
        self.thick_wall_width = tk.IntVar(value=self.DEFAULT_THICK_WALL)

        self.algorithm_choice = tk.StringVar(value="Recursive Backtracker")
        self.background_type = tk.StringVar(value="full_color")
        self.show_solution = tk.BooleanVar(value=False)
        self.show_longest_path = tk.BooleanVar(value=False)
        self.show_deadends = tk.BooleanVar(value=False)
        self.show_distances = tk.BooleanVar(value=False)
        self.distances_source_mode = tk.StringVar(value="all_maze") # all_maze, solution_path, longest_path
        self.show_gradient = tk.BooleanVar(value=False)

        self.show_solution_start_end = tk.BooleanVar(value=False)
        self.solution_path_render_mode = tk.StringVar(value="solid") # solid, gradient
        self.show_longest_path_start_end = tk.BooleanVar(value=False)
        self.longest_path_render_mode = tk.StringVar(value="solid") # solid, gradient


        # Colors.
        self.background_color = self.DEFAULT_COLORS["background_color"]
        self.checkerboard_color_1 = self.DEFAULT_COLORS["checkerboard_color_1"]
        self.checkerboard_color_2 = self.DEFAULT_COLORS["checkerboard_color_2"]
        self.start_cell_color = self.DEFAULT_COLORS["start_cell_color"]
        self.end_cell_color = self.DEFAULT_COLORS["end_cell_color"]
        self.path_color = self.DEFAULT_COLORS["path_color"]
        self.text_color = self.DEFAULT_COLORS["text_color"]
        self.deadend_color = self.DEFAULT_COLORS["deadend_color"]
        self.gradient_start = self.DEFAULT_COLORS["gradient_start"]
        self.gradient_middle = self.DEFAULT_COLORS["gradient_middle"]
        self.gradient_end = self.DEFAULT_COLORS["gradient_end"]
        self.thin_wall_color = self.DEFAULT_COLORS["thin_wall_color"]
        self.thick_wall_color = self.DEFAULT_COLORS["thick_wall_color"]


        # Tracing of variables.
        self.cell_size.trace_add("write", lambda *args: self._redraw_maze())
        self.thin_wall_width.trace_add("write", lambda *args: self._redraw_maze())
        self.thick_wall_width.trace_add("write", lambda *args: self._redraw_maze())

        self.start_cell_r.trace_add("write", self._update_solution_path_cells)
        self.start_cell_c.trace_add("write", self._update_solution_path_cells)
        self.end_cell_r.trace_add("write", self._update_solution_path_cells)
        self.end_cell_c.trace_add("write", self._update_solution_path_cells)
        self.distance_start_r.trace_add("write", lambda *args: self._update_distances_source_cell())
        self.distance_start_c.trace_add("write", lambda *args: self._update_distances_source_cell())

        self.smooth_exp.trace_add("write", lambda *args: self._update_smooth_label())


        # Maps.
        self.color_buttons = {}
        self.color_previews = {}
        self.smooth_exp_label = None # initialized by toggle_options_frame


        self.GENERATOR_ALGOS = {
            "Binary Tree": BinaryTree,
            "Sidewinder": Sidewinder,
            "Aldous Broder": AldousBroder,
            "Recursive Backtracker": RecursiveBacktracker,
            "Recursive Division": RecursiveDivision
        }

        self.window.style = ttk.Style()


        # Main layout.
        self.frame_control = ttk.Frame(window, padding="10", width=360)
        self.frame_control.pack(side=tk.LEFT, fill=tk.Y)
        self.frame_control.pack_propagate(False)

        self.frame_colors = ttk.Frame(window, padding="10", width=250)
        self.frame_colors.pack(side=tk.RIGHT, fill=tk.Y)
        self.frame_colors.pack_propagate(False)

        self.frame_image = ttk.Frame(window)
        self.frame_image.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.frame_image, bg="light gray")
        self.canvas.pack(fill=tk.BOTH, expand=True)


        # Initialize widgets.
        # Left panel.
        GenerationFrame(self.frame_control, self).pack(fill=tk.X, pady=(0, 5))
        ttk.Separator(self.frame_control, orient="horizontal").pack(fill=tk.X, pady=5)
        DetailsFrame(self.frame_control, self).pack(fill=tk.X, pady=5)

        # Right panel.
        ColorPickerFrame(self.frame_colors, self).pack(fill=tk.X, pady=(0, 5))
        ttk.Separator(self.frame_colors, orient="horizontal").pack(fill=tk.X, pady=5)
        OptionsFrame(self.frame_colors, self).pack(fill=tk.X, pady=5)
        ttk.Separator(self.frame_colors, orient="horizontal").pack(fill=tk.X, pady=5)
        DisplayFrame(self.frame_colors, self).pack(fill=tk.X, pady=5)
        ttk.Separator(self.frame_colors, orient="horizontal").pack(fill=tk.X, pady=5)
        SaveMazeFrame(self.frame_colors, self).pack(fill=tk.X, pady=5)


        # Events binding and default values loading.
        self.canvas.bind("<MouseWheel>", self._on_mouse_wheel)
        self._load_default_colors()
        self.update_image(self.original_image)
    # ----------------------------------------------- #


    def _default_image(self):

        img_width = self.cell_size.get() * self.columns.get()
        img_height = self.cell_size.get() * self.rows.get()
        img = Image.new("RGB", (img_width + 1, img_height + 1), "white")
        return img
    # ----------------------------------------------- #


    def _update_smooth_label(self, *args):
        try:
            val = self.smooth_exp.get()
            if self.smooth_exp_label:
                self.smooth_exp_label.config(text=f"{val:.2f}")
        except tk.TclError:
            pass
    # ----------------------------------------------- #


    def _update_smooth_slider(self, value_str):
        try:
            val = float(value_str)
            self.smooth_exp.set(val)
        except ValueError:
            pass
        self._redraw_maze()
    # ----------------------------------------------- #


    def _update_color_preview(self, target, hex_color):
        if target in self.color_previews:
            self.color_previews[target].config(bg=hex_color)
    # ----------------------------------------------- #


    def _choose_color(self, target):

        current_color_str = getattr(self, target)

        _, hex_color = colorchooser.askcolor(
            title=f"Choose color for {target.replace('_', ' ').title()}",
            initialcolor=current_color_str)

        if hex_color:
            setattr(self, target, hex_color)
            self._update_color_preview(target, hex_color)
            self._redraw_maze()
    # ----------------------------------------------- #


    def _load_default_colors(self):

        color_targets = list(self.DEFAULT_COLORS.keys())

        for target in color_targets:
            hex_color = self.DEFAULT_COLORS.get(target)

            if hex_color:
                setattr(self, target, hex_color)
                self._update_color_preview(target, hex_color)
    # ----------------------------------------------- #


    def _update_distances_source_cell(self, *args):

        if not self.maze_grid:
            return

        try:
            rows = self.maze_grid.rows
            columns = self.maze_grid.columns

            r = self.distance_start_r.get()
            c = self.distance_start_c.get()

            # Clamp values.
            distance_start_row = max(0, min(r, rows - 1))
            distance_start_col = max(0, min(c, columns - 1))

            if distance_start_row != r:
                self.distance_start_r.set(distance_start_row)
            if distance_start_col != c:
                self.distance_start_c.set(distance_start_col)

            self.distance_start_cell = self.maze_grid[distance_start_row, distance_start_col]

            # Get the new distances.
            self.distances_all = self.distance_start_cell.calc_all_distances()

            # Update the solution path.
            if self.solution_start_cell and self.solution_end_cell:
                self.solution_path = AStar.apply(self.maze_grid, self.solution_start_cell, self.solution_end_cell)

            self._redraw_maze()

        except Exception as e:
            print(f"Error: Cannot update distances source cell: {e}")
    # ----------------------------------------------- #


    def _update_solution_path_cells(self, *args):

        if not self.maze_grid:
            return

        try:
            rows = self.maze_grid.rows
            columns = self.maze_grid.columns

            # Clamp Start cell.
            start_r = max(0, min(self.start_cell_r.get(), rows - 1))
            start_c = max(0, min(self.start_cell_c.get(), columns - 1))
            if start_r != self.start_cell_r.get(): self.start_cell_r.set(start_r)
            if start_c != self.start_cell_c.get(): self.start_cell_c.set(start_c)
            self.solution_start_cell = self.maze_grid[start_r, start_c]

            # Clamp End cell.
            end_r = max(0, min(self.end_cell_r.get(), rows - 1))
            end_c = max(0, min(self.end_cell_c.get(), columns - 1))
            if end_r != self.end_cell_r.get(): self.end_cell_r.set(end_r)
            if end_c != self.end_cell_c.get(): self.end_cell_c.set(end_c)
            self.solution_end_cell = self.maze_grid[end_r, end_c]

            # Get new solution.
            self.solution_path = AStar.apply(self.maze_grid, self.solution_start_cell, self.solution_end_cell)

            self._redraw_maze()

        except Exception as e:
            print(f"Error: Cannot update solution path cells: {e}")
    # ----------------------------------------------- #


    def generate_maze(self):

        try:
            rows = self.rows.get()
            columns = self.columns.get()

            if rows <= 0 or columns <= 0:
                tk.messagebox.showerror("Error", "Rows and Columns must be greater than 0.")
                return

            self.maze_grid = Grid(rows, columns)
            generative_algo = self.GENERATOR_ALGOS[self.algorithm_choice.get()]
            generative_algo.apply(self.maze_grid)

            # Clamp coordinates.
            start_cell_row = max(0, min(self.start_cell_r.get(), rows - 1))
            start_cell_col = max(0, min(self.start_cell_c.get(), columns - 1))
            end_cell_row = max(0, min(self.end_cell_r.get(), rows - 1))
            end_cell_col = max(0, min(self.end_cell_c.get(), columns - 1))
            distance_start_row = max(0, min(self.distance_start_r.get(), rows - 1))
            distance_start_col = max(0, min(self.distance_start_c.get(), columns - 1))

            # Update UI variables.
            self.start_cell_r.set(start_cell_row)
            self.start_cell_c.set(start_cell_col)
            self.end_cell_r.set(end_cell_row)
            self.end_cell_c.set(end_cell_col)
            self.distance_start_r.set(distance_start_row)
            self.distance_start_c.set(distance_start_col)

            # Get the longest path.
            if not self.distances_all: # if _update_distances is not already executed
                self.distance_start_cell = self.maze_grid[distance_start_row, distance_start_col]
                self.distances_all = self.distance_start_cell.calc_all_distances()

            longest_path_root, _, _ = self.distances_all.longest_path_from()
            distances_from_longest_path_root = longest_path_root.calc_all_distances()
            longest_path_goal, _, longest_path_cells = distances_from_longest_path_root.longest_path_from()

            self.longest_path_distances = distances_from_longest_path_root
            self.longest_path_start_cell = longest_path_root
            self.longest_path_end_cell = longest_path_goal
            self.longest_path = longest_path_cells

            # Redraw the maze.
            # if you want to reset the zoom at every generation: self.zoom_level = 1.0
            self._redraw_maze()

        except Exception as e:
            tk.messagebox.showerror("Error", f"Cannot generate the maze: {e}")
            print(f"Error: Cannot generate the maze: {e}")
    # ----------------------------------------------- #


    def _redraw_maze(self):

        if not self.maze_grid:
            return

        try:
            def _get_safe_value(tk_var, default_value):
                try:
                    return tk_var.get()
                except (tk.TclError, ValueError):
                    return default_value

            def hex_to_rgb(hex_color):
                hex_color = hex_color.lstrip("#")
                if len(hex_color) != 6:
                    return (0, 0, 0) # fallback
                return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


            # Set the variables for the draw function.
            active_path_cells = None
            active_path_render_mode = "solid"
            active_path_show_start_end = False
            draw_solid_line_flag = False

            distances_for_gradient = None
            distances_for_text = None
            gradient_scope = "none"

            # Get the active path to be shown and the render mode of the path.
            # Longest path.
            if self.show_longest_path.get() and self.longest_path:
                active_path_cells = self.longest_path
                active_path_render_mode = self.longest_path_render_mode.get()
                active_path_show_start_end = self.show_longest_path_start_end.get()
                distances_for_gradient = self.longest_path_distances

            # Solution path.
            elif self.show_solution.get() and self.solution_path:
                active_path_cells = self.solution_path
                active_path_render_mode = self.solution_path_render_mode.get()
                active_path_show_start_end = self.show_solution_start_end.get()
                if self.solution_start_cell:
                    distances_for_gradient = self.solution_start_cell.calc_all_distances()
                else:
                    distances_for_gradient = self.distances_all # fallback


            # Get the scope of the gradient.
            if active_path_cells and active_path_render_mode == "gradient":
                gradient_scope = "path"
            elif self.show_gradient.get():
                gradient_scope = "full"
                distances_for_gradient = self.distances_all # gradient on all the maze
            else:
                gradient_scope = "none"
                distances_for_gradient = None # no gradient


            # If the path must be shown as a solid line (instead of the gradient).
            if active_path_cells and active_path_render_mode == "solid":
                draw_solid_line_flag = True


            # Get which type of distances to show as text.
            if self.show_distances.get():
                distances_mode = self.distances_source_mode.get()
                try:
                    # The whole maze.
                    if distances_mode == "all_maze":
                        distances_for_text = self.distances_all

                    # Only the distances of the solution.
                    elif distances_mode == "solution_path" and self.solution_path and self.solution_end_cell:
                        solution_distances_obj = self.solution_start_cell.calc_all_distances()
                        distances_for_text, _ = solution_distances_obj.shortest_path_to(self.solution_end_cell)

                    # Only the distances of the longest path.
                    elif distances_mode == "longest_path" and self.longest_path and self.longest_path_end_cell:
                        distances_for_text, _ = self.longest_path_distances.shortest_path_to(self.longest_path_end_cell)
                    else:
                        distances_for_text = self.distances_all # fallback
                except Exception:
                    distances_for_text = self.distances_all # fallback
            else:
                distances_for_text = None


            distances_obj = distances_for_gradient if distances_for_gradient else distances_for_text


            # Args to be passed to Grid.to_png().
            to_png_args = {
                "cell_size": _get_safe_value(self.cell_size, self.DEFAULT_CELL_SIZE),
                "smooth_exp": _get_safe_value(self.smooth_exp, self.DEFAULT_SMOOTH_EXP),

                # Background.
                "background_type": self.background_type.get(),
                "full_color": hex_to_rgb(self.background_color),
                "checkerboard_color_1": hex_to_rgb(self.checkerboard_color_1),
                "checkerboard_color_2": hex_to_rgb(self.checkerboard_color_2),

                # Walls.
                "thin_wall_width": _get_safe_value(self.thin_wall_width, self.DEFAULT_THIN_WALL),
                "thick_wall_width": _get_safe_value(self.thick_wall_width, self.DEFAULT_THICK_WALL),
                "thin_wall_color": hex_to_rgb(self.thin_wall_color),
                "thick_wall_color": hex_to_rgb(self.thick_wall_color),

                # Colors.
                "text_color": hex_to_rgb(self.text_color),
                "deadend_color": hex_to_rgb(self.deadend_color),
                "gradient_start": hex_to_rgb(self.gradient_start),
                "gradient_middle": hex_to_rgb(self.gradient_middle),
                "gradient_end": hex_to_rgb(self.gradient_end),

                # Path Colors.
                "path_color": hex_to_rgb(self.path_color),
                "start_cell_color": hex_to_rgb(self.start_cell_color),
                "end_cell_color": hex_to_rgb(self.end_cell_color),

                # Data/Toggles.
                "show_deadends": self.show_deadends.get(),
                "distances_obj": distances_obj,
                "show_distance_text": self.show_distances.get(),
                "gradient_scope": gradient_scope,
                "path_cells": active_path_cells,
                "draw_solid_path_line": draw_solid_line_flag,
                "show_path_start_end_cells": active_path_show_start_end
            }


            self.original_image = self.maze_grid.to_png(**to_png_args)

            self.update_image(self.original_image)

        except Exception as e:
            tk.messagebox.showerror("Error", f"Cannot redraw maze: {e}")
            print(f"Error: Cannot redraw maze: {e}")
    # ----------------------------------------------- #


    def _on_toggle_solution(self):
        if self.show_solution.get():
            self.show_longest_path.set(False)
        self._redraw_maze()
    # ----------------------------------------------- #


    def _on_toggle_longest_path(self):
        if self.show_longest_path.get():
            self.show_solution.set(False)
        self._redraw_maze()
    # ----------------------------------------------- #


    def update_image(self, image):

        if image is None:
            self.canvas.delete("all")
            return

        try:
            self.original_image = image

            w = int(self.original_image.width * self.zoom_level)
            h = int(self.original_image.height * self.zoom_level)

            if self.zoom_level != 1.0:
                resized_image = self.original_image.resize((w, h), Image.Resampling.NEAREST)
            else:
                resized_image = self.original_image

            self.current_image = resized_image
            self.tk_image = ImageTk.PhotoImage(self.current_image)

            self.canvas.config(scrollregion=(0, 0, w, h))
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, image=self.tk_image, anchor=tk.NW)

        except Exception as e:
            print(f"Error: Cannot update image: {e}")
    # ----------------------------------------------- #


    def adjust_zoom(self, factor, reset=False):

        if self.original_image is None:
            return

        if reset:
            self.zoom_level = 1.0
        else:
            self.zoom_level *= factor
            self.zoom_level = max(0.25, min(10.0, self.zoom_level)) # clamp zoom

        self.update_image(self.original_image)
    # ----------------------------------------------- #


    def _on_mouse_wheel(self, event):
        factor = 1.1 if event.delta > 0 else 1 / 1.1
        self.adjust_zoom(factor)
    # ----------------------------------------------- #


    def save_maze_image(self):

        if self.current_image is None:
            tk.messagebox.showwarning("Warning", "You must generate a maze first")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
            title="Save maze as image"
        )

        if file_path:
            try:
                self.current_image.save(file_path)
            except Exception as e:
                tk.messagebox.showerror("Error", f"Cannot save image: {e}")
    # ----------------------------------------------- #


    def _reset_colors(self):
        self._load_default_colors()
        self._redraw_maze()
    # ----------------------------------------------- #


    def _reset_generation_options(self):

        self.rows.set(self.DEFAULT_ROWS)
        self.columns.set(self.DEFAULT_COLUMNS)
        self.cell_size.set(self.DEFAULT_CELL_SIZE)
        self.thin_wall_width.set(self.DEFAULT_THIN_WALL)
        self.thick_wall_width.set(self.DEFAULT_THICK_WALL)

        self.background_type.set("full_color")
        colors_to_reset = [
            "thin_wall_color",
            "thick_wall_color",
            "background_color",
            "checkerboard_color_1",
            "checkerboard_color_2"
        ]

        for target in colors_to_reset:
            default_hex = self.DEFAULT_COLORS.get(target)
            if default_hex:
                setattr(self, target, default_hex)
                self._update_color_preview(target, default_hex)


        self._redraw_maze()
    # ----------------------------------------------- #


    def _reset_smooth_exp(self):
        self.smooth_exp.set(self.DEFAULT_SMOOTH_EXP)
        self._redraw_maze()
    # ----------------------------------------------- #


    def _get_random_cell(self):

        if not self.maze_grid:
            tk.messagebox.showwarning("Warning", "Generate a maze first.")
            return None
        try:
            return self.maze_grid.random_cell()
        except Exception as e:
            tk.messagebox.showerror("Error", f"Cannot get random cell: {e}")
            return None
    # ----------------------------------------------- #


    def _set_random_solution_start_cell(self):
        cell = self._get_random_cell()
        if cell:
            self.start_cell_r.set(cell.row)
            self.start_cell_c.set(cell.column)
    # ----------------------------------------------- #


    def _set_random_solution_end_cell(self):
        cell = self._get_random_cell()
        if cell:
            self.end_cell_r.set(cell.row)
            self.end_cell_c.set(cell.column)
    # ----------------------------------------------- #


    def _set_random_distance_start_cell(self):
        cell = self._get_random_cell()
        if cell:
            self.distance_start_r.set(cell.row)
            self.distance_start_c.set(cell.column)
    # ----------------------------------------------- #


if __name__ == "__main__":
    window = tk.Tk()
    app = MazeApp(window)
    window.mainloop()
import tkinter as tk
from tkinter import ttk, filedialog, colorchooser
from PIL import Image, ImageTk

from aldous_broder import AldousBroder
from astar import AStar
from binary_tree import BinaryTree
from grid import Grid
from recursive_backtracker import RecursiveBacktracker
from recursive_division import RecursiveDivision
from sidewinder import Sidewinder


class MazeApp:
    def __init__(self, window):

        # Window configuration.
        self.window = window
        self.window.title("Ariadne's Thread")
        self.window.geometry("1400x950")
        self.window.wm_iconphoto(False, tk.PhotoImage(file="icons8-clew-32.png"))
        self.window.resizable(False, False)
        self.window.configure(background="white")

        # Default values that can be reset.
        self.DEFAULT_ROWS = 20
        self.DEFAULT_COLUMNS = 20
        self.DEFAULT_CELL_SIZE = 22
        self.DEFAULT_THIN_WALL = 1
        self.DEFAULT_THICK_WALL = 3
        self.DEFAULT_SMOOTH_EXP = 0.65
        self.DEFAULT_BG_COLOR = "#FFFFFF"
        self.DEFAULT_CHECKERBOARD_COLOR_1 = "#FFFFFF"
        self.DEFAULT_CHECKERBOARD_COLOR_2 = "#DFDFDF"
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
            "checkerboard_color_1": self.DEFAULT_CHECKERBOARD_COLOR_1,
            "checkerboard_color_2": self.DEFAULT_CHECKERBOARD_COLOR_2,
        }

        MazeGrid = Grid(20,20)
        RecursiveBacktracker.apply(MazeGrid)
        default_img = MazeGrid.to_png(cell_size=30, background_type="full_color", full_color=(255,255,255))


        # Status variables.
        self.maze_grid = None
        self.original_image = default_img
        self.current_image = default_img
        self.tk_image = None
        self.zoom_level = 1.0
        self.distances_all = None
        self.subset_path = None
        self.solution_path = None
        self.solution_start_cell = None
        self.solution_end_cell = None
        self.longest_path_start_cell = None
        self.longest_path_end_cell = None
        self.longest_path_distances = None
        self.longest_path = None
        self.distance_start_cell = None

        # UI variables.
        self.rows = tk.IntVar(value=self.DEFAULT_ROWS)
        self.columns = tk.IntVar(value=self.DEFAULT_COLUMNS)
        self.cell_size = tk.IntVar(value=self.DEFAULT_CELL_SIZE)
        self.smooth_exp = tk.DoubleVar(value=self.DEFAULT_SMOOTH_EXP)

        # Variabili per la soluzione A*
        self.start_cell_r = tk.IntVar(value=0)
        self.start_cell_c = tk.IntVar(value=0)
        self.end_cell_r = tk.IntVar(value=19)
        self.end_cell_c = tk.IntVar(value=19)
        self.distance_start_r = tk.IntVar(value=0)
        self.distance_start_c = tk.IntVar(value=0)
        self.thin_wall_width = tk.IntVar(value=self.DEFAULT_THIN_WALL)
        self.thick_wall_width = tk.IntVar(value=self.DEFAULT_THICK_WALL)

        # Traces for updating the maze config.
        self.start_cell_r.trace_add('write', self._update_solution_path_cells)
        self.start_cell_c.trace_add('write', self._update_solution_path_cells)
        self.end_cell_r.trace_add('write', self._update_solution_path_cells)
        self.end_cell_c.trace_add('write', self._update_solution_path_cells)
        self.distance_start_r.trace_add('write', lambda *args: self._update_distances_source_cell())
        self.distance_start_c.trace_add('write', lambda *args: self._update_distances_source_cell())
        self.thin_wall_width.trace_add('write', lambda *args: self._redraw_maze())
        self.thick_wall_width.trace_add('write', lambda *args: self._redraw_maze())

        # Button colors and style.
        self.color_buttons = {}
        self.color_previews = {}
        self.window.style = ttk.Style()

        # Generative algorithms.
        self.generators = {
            "Binary Tree": BinaryTree,
            "Sidewinder": Sidewinder,
            "Aldous Broder": AldousBroder,
            "Recursive Backtracker": RecursiveBacktracker,
            "Recursive Division": RecursiveDivision
        }

        # Options for visualizing the maze.
        self.algorithm_choice = tk.StringVar(value=list(self.generators.keys())[0])
        self.background_type = tk.StringVar(value="full_color")
        self.background_color = self.DEFAULT_BG_COLOR
        self.checkerboard_color_1 = self.DEFAULT_CHECKERBOARD_COLOR_1
        self.checkerboard_color_2 = self.DEFAULT_CHECKERBOARD_COLOR_2

        self.show_solution = tk.BooleanVar(value=False)
        self.show_longest_path = tk.BooleanVar(value=False)
        self.show_deadends = tk.BooleanVar(value=False)
        self.show_distances = tk.BooleanVar(value=False)
        self.distances_source_mode = tk.StringVar(value="All") # All, Solution, Longest
        self.show_gradient = tk.BooleanVar(value=False)
        self.show_solution_start_end = tk.BooleanVar(value=False) # toggle start/end cells for the solution path.
        self.solution_path_render_mode = tk.StringVar(value="Line") # toggle the solution path as gradient/colored line.
        self.show_longest_path_start_end = tk.BooleanVar(value=False) # toggle start/end cells for the longest path.
        self.longest_path_render_mode = tk.StringVar(value="Line") # toggle the longest path as gradient/colored line.

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

        # Layout configuration.
        self.frame_control = ttk.Frame(window, padding="10", width=300)
        self.frame_control.pack(side=tk.LEFT, fill=tk.Y)

        self.frame_colors = ttk.Frame(window, padding="10")
        self.frame_colors.pack(side=tk.RIGHT, fill=tk.Y)

        self.frame_image = ttk.Frame(window)
        self.frame_image.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.frame_image, bg="light gray")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Initialize widgets.
        self._setup_generation_controls()
        self._setup_display_controls()
        self._setup_options_controls()
        self._setup_color_controls()
        self._load_default_colors()

        self.canvas.bind("<MouseWheel>", self._on_mouse_wheel)

        self._update_color_preview('background_color', self.background_color)
        self._update_color_preview('checkerboard_color_1', self.checkerboard_color_1)
        self._update_color_preview('checkerboard_color_2', self.checkerboard_color_2)
    # ----------------------------------------------- #


    def _setup_generation_controls(self):

        # Algorithm choice.
        label_generation = ttk.Label(self.frame_control,
                                     text="Generation",
                                     font=("Arial", 11, "bold"))
        label_generation.pack(pady=(0, 5), anchor="w")

        ttk.Label(self.frame_control,
                  text="Algorithm:").pack(anchor="w")

        combobox_algo = ttk.Combobox(self.frame_control,
                                     textvariable=self.algorithm_choice,
                                     values=list(self.generators.keys()),
                                     state="readonly")
        combobox_algo.pack(fill=tk.X, pady=0)


        # Background type choice.
        ttk.Label(self.frame_control,
                  text="Background type:").pack(anchor="w", pady=15)

        # Full color option.
        frame_full_color_row = ttk.Frame(self.frame_control)
        frame_full_color_row.pack(fill=tk.X, anchor="w", pady=2)

        ttk.Radiobutton(frame_full_color_row,
                        text="Full color",
                        variable=self.background_type,
                        value="full_color",
                        command=self._redraw_maze).pack(side=tk.LEFT)

        frame_full_color_controls = ttk.Frame(frame_full_color_row)
        frame_full_color_controls.pack(side=tk.RIGHT)

        canvas_full_color_preview = tk.Canvas(frame_full_color_controls, width=20, height=20, borderwidth=1, relief="solid")
        canvas_full_color_preview.pack(side=tk.RIGHT, padx=(5, 5))
        self.color_previews['background_color'] = canvas_full_color_preview

        ttk.Button(frame_full_color_controls,
                   text="Background color",
                   command=lambda: self._choose_color('background_color'),
                   width=18).pack(side=tk.RIGHT)


        # Checkerboard option.
        frame_checkerboard_row = ttk.Frame(self.frame_control)
        frame_checkerboard_row.pack(fill=tk.X, anchor="w", pady=2)

        ttk.Radiobutton(frame_checkerboard_row,
                        text="Checkerboard",
                        variable=self.background_type,
                        value="checkerboard",
                        command=self._redraw_maze).pack(side=tk.LEFT)

        frame_checkerboard_controls = ttk.Frame(frame_checkerboard_row)
        frame_checkerboard_controls.pack(side=tk.RIGHT)

        canvas_checkerboard_color_2_preview = tk.Canvas(frame_checkerboard_controls, width=20, height=20, borderwidth=1, relief="solid")
        canvas_checkerboard_color_2_preview.pack(side=tk.RIGHT, padx=(5, 5))
        self.color_previews['checkerboard_color_2'] = canvas_checkerboard_color_2_preview
        ttk.Button(frame_checkerboard_controls,
                   text="Color 2",
                   command=lambda: self._choose_color('checkerboard_color_2'),
                   width=8).pack(side=tk.RIGHT)

        canvas_checkerboard_color_1_preview = tk.Canvas(frame_checkerboard_controls, width=20, height=20, borderwidth=1, relief="solid")
        canvas_checkerboard_color_1_preview.pack(side=tk.RIGHT, padx=(5, 5))
        self.color_previews['checkerboard_color_1'] = canvas_checkerboard_color_1_preview
        ttk.Button(frame_checkerboard_controls,
                   text="Color 1",
                   command=lambda: self._choose_color('checkerboard_color_1'),
                   width=8).pack(side=tk.RIGHT)


        # Dimensions.
        label_dimensions = ttk.Label(self.frame_control,
                                     text="Dimensions",
                                     font=("Arial", 11, "bold"))
        label_dimensions.pack(pady=(15, 0), anchor="w")

        frame_dim_and_cell = ttk.Frame(self.frame_control)
        frame_dim_and_cell.pack(fill=tk.X)

        ttk.Label(frame_dim_and_cell, text="Rows:").pack(side=tk.LEFT)
        ttk.Entry(frame_dim_and_cell, textvariable=self.rows, width=5).pack(side=tk.LEFT, padx=(0, 5))

        ttk.Label(frame_dim_and_cell, text="Columns:").pack(side=tk.LEFT)
        ttk.Entry(frame_dim_and_cell, textvariable=self.columns, width=5).pack(side=tk.LEFT, padx=(0, 5))

        ttk.Label(frame_dim_and_cell, text="Cell Size:").pack(side=tk.LEFT)
        ttk.Entry(frame_dim_and_cell, textvariable=self.cell_size, width=5).pack(side=tk.LEFT, padx=(5, 0))

        frame_thin_wall = ttk.Frame(self.frame_control)
        frame_thin_wall.pack(fill=tk.X, pady=(2, 5))
        ttk.Label(frame_thin_wall, text="Thin Wall Width:").pack(side=tk.LEFT)
        ttk.Entry(frame_thin_wall, textvariable=self.thin_wall_width, width=5).pack(side=tk.LEFT, padx=(5, 0))

        frame_thick_wall = ttk.Frame(self.frame_control)
        frame_thick_wall.pack(fill=tk.X, pady=(2, 5))
        ttk.Label(frame_thick_wall, text="Thick Wall Width:").pack(side=tk.LEFT)
        ttk.Entry(frame_thick_wall, textvariable=self.thick_wall_width, width=5).pack(side=tk.LEFT, padx=(5, 0))


        ttk.Button(self.frame_control,
                   text="Reset Details",
                   command=self._reset_dimensions_walls_cellsize,
                   style="Accent.TButton"
                   ).pack(fill=tk.X, pady=(5, 10))


        ttk.Separator(self.frame_control, orient='horizontal').pack(fill='x', pady=5)


        ttk.Button(self.frame_control,
                   text="Generate maze",
                   command=self.generate_maze,
                   style="Accent.TButton"
                   ).pack(fill=tk.X, pady=5)

        ttk.Separator(self.frame_control, orient='horizontal').pack(fill='x', pady=5)
    # ----------------------------------------------- #


    def _setup_display_controls(self):

        # Zoom options.
        label_display = ttk.Label(self.frame_control,
                                  text="Visualize",
                                  font=("Arial", 11, "bold"))
        label_display.pack(pady=(15, 0), anchor="w")

        frame_zoom = ttk.Frame(self.frame_control)
        frame_zoom.pack(fill=tk.X, pady=5)

        ttk.Button(frame_zoom,
                   text="Zoom +",
                   command=lambda: self.adjust_zoom(1.2)).pack(side=tk.LEFT, fill=tk.X)
        ttk.Button(frame_zoom,
                   text="Zoom -",
                   command=lambda: self.adjust_zoom(1/1.2)).pack(side=tk.LEFT, fill=tk.X)
        ttk.Button(frame_zoom,
                   text="Reset zoom",
                   command=lambda: self.adjust_zoom(1.0)).pack(side=tk.RIGHT, fill=tk.X)
    # ----------------------------------------------- #


    def _setup_options_controls(self):

        # Solution path options.
        label_options = ttk.Label(self.frame_control,
                                  text="Details",
                                  font=("Arial", 11, "bold"))
        label_options.pack(pady=(5, 5), anchor="w")

        label_solution = ttk.Label(self.frame_control,
                                   text="A* Solution (Pathfinding)",
                                   font=("Arial", 10, "bold"))
        label_solution.pack(pady=(5, 0), anchor="w")

        ttk.Checkbutton(self.frame_control,
                        text="Show solution (with A*)",
                        variable=self.show_solution,
                        command=self._on_toggle_solution).pack(anchor="w")

        ttk.Checkbutton(self.frame_control,
                        text="Show Start/End Cells",
                        variable=self.show_solution_start_end,
                        command=self._redraw_maze).pack(anchor="w", padx=(10, 0))

        frame_solution_path_render_mode = ttk.Frame(self.frame_control)
        frame_solution_path_render_mode.pack(anchor="w", padx=(10, 0))

        ttk.Label(frame_solution_path_render_mode, text="Solution Path as:").pack(side=tk.LEFT)
        ttk.Radiobutton(frame_solution_path_render_mode,
                        text="Solid Line",
                        variable=self.solution_path_render_mode,
                        value="Solid",
                        command=self._redraw_maze).pack(side=tk.LEFT, padx=(5, 5))
        ttk.Radiobutton(frame_solution_path_render_mode,
                        text="Gradient",
                        variable=self.solution_path_render_mode,
                        value="Gradient",
                        command=self._redraw_maze).pack(side=tk.LEFT)


        # Start Cell Inputs.
        frame_start = ttk.Frame(self.frame_control)
        frame_start.pack(fill=tk.X, pady=(2, 0))
        ttk.Label(frame_start, text="Start cell (R, C):").pack(side=tk.LEFT)
        ttk.Entry(frame_start, textvariable=self.start_cell_r, width=5).pack(side=tk.LEFT, padx=(5, 5))
        ttk.Entry(frame_start, textvariable=self.start_cell_c, width=5).pack(side=tk.LEFT)

        ttk.Button(frame_start,
                   text="Random Start cell",
                   command=self._set_random_a_star_start_cell,
                   width=8
                   ).pack(side=tk.LEFT, padx=(10, 0))

        # End Cell Inputs.
        frame_end = ttk.Frame(self.frame_control)
        frame_end.pack(fill=tk.X, pady=(2, 5))
        ttk.Label(frame_end, text="End cell (R, C):").pack(side=tk.LEFT)
        ttk.Entry(frame_end, textvariable=self.end_cell_r, width=5).pack(side=tk.LEFT, padx=(10, 5))
        ttk.Entry(frame_end, textvariable=self.end_cell_c, width=5).pack(side=tk.LEFT)

        ttk.Button(frame_end,
                   text="Random End cell",
                   command=self._set_random_a_star_end_cell,
                   width=8
                   ).pack(side=tk.LEFT, padx=(10, 0))


        ttk.Separator(self.frame_control, orient='horizontal').pack(fill='x', pady=5)


        # Longest path options.
        ttk.Checkbutton(self.frame_control,
                        text="Show longest path",
                        variable=self.show_longest_path,
                        command=self._on_toggle_longest_path).pack(anchor="w")

        ttk.Checkbutton(self.frame_control,
                        text="Show Start/End Cells",
                        variable=self.show_longest_path_start_end,
                        command=self._redraw_maze).pack(anchor="w", padx=(10, 0))

        frame_longest_path_render_mode = ttk.Frame(self.frame_control)
        frame_longest_path_render_mode.pack(anchor="w", padx=(10, 0))

        ttk.Label(frame_longest_path_render_mode, text="Longest Path as:").pack(side=tk.LEFT)
        ttk.Radiobutton(frame_longest_path_render_mode,
                        text="Solid Line",
                        variable=self.longest_path_render_mode,
                        value="Solid",
                        command=self._redraw_maze).pack(side=tk.LEFT, padx=(5, 5))
        ttk.Radiobutton(frame_longest_path_render_mode,
                        text="Gradient",
                        variable=self.longest_path_render_mode,
                        value="Gradient",
                        command=self._redraw_maze).pack(side=tk.LEFT)


        ttk.Separator(self.frame_control, orient='horizontal').pack(fill='x', pady=5)


        # Distances options.
        label_distance_start = ttk.Label(self.frame_control,
                                         text="Distances values",
                                         font=("Arial", 10, "bold"))
        label_distance_start.pack(pady=(5, 0), anchor="w")

        ttk.Checkbutton(self.frame_control,
                        text="Toggle distance values",
                        variable=self.show_distances,
                        command=self._redraw_maze).pack(anchor="w")

        ttk.Label(self.frame_control,
                  text="Distances Source:").pack(pady=(5, 0), anchor="w")

        frame_distance_source = ttk.Frame(self.frame_control)
        frame_distance_source.pack(fill=tk.X, pady=(2, 5))

        ttk.Radiobutton(frame_distance_source,
                        text="All",
                        variable=self.distances_source_mode,
                        value="All",
                        command=self._redraw_maze).pack(side=tk.LEFT, padx=5)

        ttk.Radiobutton(frame_distance_source,
                        text="Solution Path",
                        variable=self.distances_source_mode,
                        value="Solution",
                        command=self._redraw_maze).pack(side=tk.LEFT, padx=5)

        ttk.Radiobutton(frame_distance_source,
                        text="Longest Path",
                        variable=self.distances_source_mode,
                        value="Longest",
                        command=self._redraw_maze).pack(side=tk.LEFT, padx=5)

        # Starting cell for distances.
        frame_distance_start = ttk.Frame(self.frame_control)
        frame_distance_start.pack(fill=tk.X, pady=(2, 5))
        ttk.Label(frame_distance_start, text="Distances start cell (R , C):").pack(side=tk.LEFT)
        ttk.Entry(frame_distance_start, textvariable=self.distance_start_r, width=5).pack(side=tk.LEFT, padx=(5, 5))
        ttk.Entry(frame_distance_start, textvariable=self.distance_start_c, width=5).pack(side=tk.LEFT)

        ttk.Button(self.frame_control,
                   text="Random distances start cell",
                   command=self._set_random_distance_start_cell,
                   ).pack(fill=tk.X, pady=(0, 5))

        ttk.Separator(self.frame_control, orient='horizontal').pack(fill='x', pady=5)
    # ----------------------------------------------- #


    def _setup_color_controls(self):

        # Button colors.
        label_choose_color = ttk.Label(self.frame_colors,
                                       text="Colors",
                                       font=("Arial", 11, "bold"))
        label_choose_color.pack(anchor="w", pady=(5, 5))

        color_options = [
            ("start_cell_color", "Start cell color"),
            ("end_cell_color", "End cell color"),
            ("path_color", "Path color"),
            ("text_color", "Text color"),
            ("deadend_color", "Dead end color"),
            ("gradient_start", "Start gradient color"),
            ("gradient_middle", "Middle gradient color"),
            ("gradient_end", "End gradient color"),
            ("thin_wall_color", "Thin wall color"),
            ("thick_wall_color", "Thick wall color"),
        ]

        for target_attr, button_text in color_options:

            frame_row_colors = ttk.Frame(self.frame_colors)
            frame_row_colors.pack(fill=tk.X, pady=2)

            canvas_preview_color = tk.Canvas(frame_row_colors, width=20, height=20, borderwidth=1, relief="solid")
            canvas_preview_color.pack(side=tk.LEFT, padx=(0, 5))
            self.color_previews[target_attr] = canvas_preview_color

            button = ttk.Button(frame_row_colors,
                                text=button_text,
                                command=lambda t=target_attr: self._choose_color(t))
            button.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.color_buttons[target_attr] = button

        ttk.Button(self.frame_colors,
                   text="Reset Colors",
                   command=self._reset_colors,
                   style="Accent.TButton"
                   ).pack(fill=tk.X, pady=(10, 5))


        ttk.Separator(self.frame_colors, orient='horizontal').pack(fill='x', pady=5)


        # Gradient.
        label_gradient = ttk.Label(self.frame_colors,
                                   text="Gradient",
                                   font=("Arial", 11, "bold"))
        label_gradient.pack(pady=(5, 5), anchor="w")

        ttk.Checkbutton(self.frame_colors,
                        text="Toggle gradient",
                        variable=self.show_gradient,
                        command=self._redraw_maze).pack(anchor="w")


        # Smoothness exponent.
        frame_smooth_exp = ttk.Frame(self.frame_colors)
        frame_smooth_exp.pack(fill=tk.X, pady=15)
        ttk.Label(frame_smooth_exp, text="Smooth Exp:").pack(side=tk.LEFT)
        ttk.Entry(frame_smooth_exp, textvariable=self.smooth_exp, width=5).pack(side=tk.LEFT, padx=(5, 0))

        # Smoothness exponent slider
        slider_smooth_exp = ttk.Scale(
            self.frame_colors,
            from_=0.1,
            to=3.0,
            orient=tk.HORIZONTAL,
            variable=self.smooth_exp,
            command=lambda v: self._redraw_maze()
        )
        slider_smooth_exp.pack(fill=tk.X, pady=2)

        ttk.Label(self.frame_colors, textvariable=self.smooth_exp).pack(anchor="e")

        ttk.Button(self.frame_colors,
                   text="Reset Smooth Exp",
                   command=self._reset_smooth_exp,
                   style="Accent.TButton"
                   ).pack(fill=tk.X, pady=(5, 10))


        ttk.Separator(self.frame_colors, orient='horizontal').pack(fill='x', pady=5)


        # Dead ends.
        label_deadends = ttk.Label(self.frame_colors,
                                   text="Dead Ends",
                                   font=("Arial", 11, "bold"))
        label_deadends.pack(pady=(5, 5), anchor="w")

        ttk.Checkbutton(self.frame_colors,
                        text="Show deadends",
                        variable=self.show_deadends,
                        command=self._redraw_maze).pack(anchor="w")


        ttk.Separator(self.frame_colors, orient='horizontal').pack(fill='x', pady=5)


        # Save button.
        ttk.Button(self.frame_colors,
                   text="Save maze ...",
                   command=self.save_maze).pack(fill=tk.X, pady=10)

        ttk.Separator(self.frame_colors,
                      orient="horizontal").pack(fill='x', pady=5)
    # ----------------------------------------------- #


    def _update_color_preview(self, target, hex_color):
        if target in self.color_previews:
            self.color_previews[target].config(bg=hex_color)
    # ----------------------------------------------- #


    def _choose_checkerboard_color(self, target):

        current_color_str = getattr(self, target)

        _, hex_color = colorchooser.askcolor(
            title=f"Choose Checkerboard {target.split('_')[-1]} Color",
            initialcolor=current_color_str)

        if hex_color:
            setattr(self, target, hex_color)
            self._update_color_preview(target, hex_color)
            self._redraw_maze()
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

        color_targets = [
            "start_cell_color",
            "end_cell_color",
            "deadend_color",
            "path_color",
            "text_color",
            "gradient_start",
            "gradient_middle",
            "gradient_end",
            "thin_wall_color",
            "thick_wall_color",
            "background_color",
            "checkerboard_color_1",
            "checkerboard_color_2",
        ]

        for target in color_targets:
            hex_color = getattr(self, target)
            self._update_color_preview(target, hex_color)
    # ----------------------------------------------- #


    def _update_distances_source_cell(self, *args):

        # Redraw the maze based on the new distances.
        # Called whenever self.distance_start_r or self.distance_start_c change.

        if not self.maze_grid:
            return

        try:
            rows = self.maze_grid.rows
            columns = self.maze_grid.columns

            r = self.distance_start_r.get()
            c = self.distance_start_c.get()

            distance_start_row = max(0, min(r, rows - 1))
            distance_start_col = max(0, min(c, columns - 1))

            if distance_start_row != r:
                self.distance_start_r.set(distance_start_row)
            if distance_start_col != c:
                self.distance_start_c.set(distance_start_col)

            self.distance_start_cell = self.maze_grid[distance_start_row, distance_start_col]

            # Get the new distances
            self.distances_all = self.distance_start_cell.calc_all_distances()
            self.maze_grid._distances = self.distances_all

            # Get the new solution from the distances.
            # self._update_solution_path_cells()
            if self.solution_start_cell and self.solution_end_cell:
                self.solution_path = AStar.apply(self.maze_grid, self.solution_start_cell, self.solution_end_cell)


            # Update the maze.
            self._redraw_maze()

        except Exception as e:
            print(f"Error updating distance source cell: {e}")
            pass
    # ----------------------------------------------- #


    def _update_solution_path_cells(self, *args):

        # Update the solution path starting from the new start and end cells.
        # Redraw the maze.
        # Called whenever self.start_cell_r or self.start_cell_c are updated.

        if not self.maze_grid:
            return

        try:
            rows = self.maze_grid.rows
            columns = self.maze_grid.columns

            # Get and clamp Start cell
            start_r = max(0, min(self.start_cell_r.get(), rows - 1))
            start_c = max(0, min(self.start_cell_c.get(), columns - 1))

            if start_r != self.start_cell_r.get():
                self.start_cell_r.set(start_r)
            if start_c != self.start_cell_c.get():
                self.start_cell_c.set(start_c)

            self.solution_start_cell = self.maze_grid[start_r, start_c]

            # Get and clamp End cell
            end_r = max(0, min(self.end_cell_r.get(), rows - 1))
            end_c = max(0, min(self.end_cell_c.get(), columns - 1))

            if end_r != self.end_cell_r.get():
                self.end_cell_r.set(end_r)
            if end_c != self.end_cell_c.get():
                self.end_cell_c.set(end_c)

            self.solution_end_cell = self.maze_grid[end_r, end_c]

            # Recalculate solution path.
            self.solution_path = AStar.apply(self.maze_grid, self.solution_start_cell, self.solution_end_cell)

            # Redraw maze.
            self._redraw_maze()

        except Exception as e:
            print(f"Error updating solution path cells: {e}")
            pass
    # ----------------------------------------------- #


    def generate_maze(self):

        try:
            rows = self.rows.get()
            columns = self.columns.get()

            if rows <= 0 or columns <= 0:
                tk.messagebox.showerror("Error", "Rows and Columns must be greater than 0.")
                return

            self.maze_grid = Grid(rows, columns)

            generative_algo = self.generators[self.algorithm_choice.get()]
            generative_algo.apply(self.maze_grid)

            # Get the start and end cells.
            start_cell_row = max(0, min(self.start_cell_r.get(), rows - 1))
            start_cell_col = max(0, min(self.start_cell_c.get(), columns - 1))
            end_cell_row = max(0, min(self.end_cell_r.get(), rows - 1))
            end_cell_col = max(0, min(self.end_cell_c.get(), columns - 1))

            self.solution_start_cell = self.maze_grid[start_cell_row, start_cell_col]
            self.solution_end_cell = self.maze_grid[end_cell_row, end_cell_col]

            # Get the source cell to calculate the new distances from.
            distance_start_row = max(0, min(self.distance_start_r.get(), rows - 1))
            distance_start_col = max(0, min(self.distance_start_c.get(), columns - 1))
            self.distance_start_cell = self.maze_grid[distance_start_row, distance_start_col]

            # Calc the new distances.
            self.distances_all = self.distance_start_cell.calc_all_distances()
            self.maze_grid._distances = self.distances_all

            # Calc solution path from starting cell to end cell.
            self.solution_path = AStar.apply(self.maze_grid, self.solution_start_cell, self.solution_end_cell)

            # Longest path.
            longest_path_root, _, _ = self.distances_all.longest_path_from()
            distances_from_longest_path_root = longest_path_root.calc_all_distances()
            longest_path_goal, _, longest_path_cells = distances_from_longest_path_root.longest_path_from()

            self.longest_path_distances = distances_from_longest_path_root
            self.longest_path_start_cell = longest_path_root
            self.longest_path_end_cell = longest_path_goal

            self.longest_path = longest_path_cells

            # Reset UI viariables.
            self.start_cell_r.set(start_cell_row)
            self.start_cell_c.set(start_cell_col)
            self.end_cell_r.set(end_cell_row)
            self.end_cell_c.set(end_cell_col)
            self.distance_start_r.set(distance_start_row)
            self.distance_start_c.set(distance_start_col)

            # Update the new maze.
            self.original_image = self._redraw_maze()
            self.update_image(self.original_image)
            self.zoom_level = 1.0
            self._redraw_maze()

        except Exception as e:
            tk.messagebox.showerror("Generation error",
                                    f"Cannot generate the maze: {e}")
    # ----------------------------------------------- #


    def _redraw_maze(self):

        # Main redraw function. Collects all UI settings and calls grid.to_png()
        # with the requested arguments.

        if not self.maze_grid:
            return

        try:

            def _get_safe_value(tk_var, default_value):
                try:
                    return tk_var.get()
                except tk.TclError:
                    return default_value


            # Helper to convert hex to (r,g,b)
            def hex_to_rgb(hex_color):
                """Converts hex color string to RGB tuple for PIL."""
                if len(hex_color) < 7:
                    return (0, 0, 0)
                return tuple(int(hex_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))


            # Determine the type of path to be shown (solution or longest path).
            # Determine which way to render the path (solid line or gradient of cells).
            active_path_cells = None
            active_path_render_mode = "Solid"
            active_path_show_start_end = False
            draw_solid_line_flag = False

            if self.show_longest_path.get() and self.longest_path:
                active_path_cells = self.longest_path
                active_path_render_mode = self.longest_path_render_mode.get()
                active_path_show_start_end = self.show_longest_path_start_end.get()

            elif self.show_solution.get() and self.solution_path:
                active_path_cells = self.solution_path
                active_path_render_mode = self.solution_path_render_mode.get()
                active_path_show_start_end = self.show_solution_start_end.get()

            if active_path_cells and active_path_render_mode == "Solid":
                draw_solid_line_flag = True

            path_color_to_send = hex_to_rgb(self.path_color)
            start_cell_color_to_send = hex_to_rgb(self.start_cell_color)
            end_cell_color_to_send = hex_to_rgb(self.end_cell_color)


            # Determine the scope of the gradient (only the path or the full maze).
            gradient_scope = "none"
            if active_path_cells and active_path_render_mode == "Gradient":
                gradient_scope = "path"
            elif self.show_gradient.get():
                gradient_scope = "full"


            # Set the distances.
            distances_obj_to_send = None

            # Match the scope of the gradient with the source of the gradient and distances.
            if gradient_scope == "path":
                if self.show_longest_path.get() and self.longest_path:
                    distances_obj_to_send = self.longest_path_distances

                elif self.show_solution.get() and self.solution_path:
                    if self.distances_all and self.distances_all.root == self.solution_start_cell:
                        distances_obj_to_send = self.distances_all
                    else:
                        if self.solution_start_cell:
                            distances_obj_to_send = self.solution_start_cell.calc_all_distances()
                        else:
                            distances_obj_to_send = self.distances_all
                else:
                    # Fallback.
                    distances_obj_to_send = self.distances_all

            elif gradient_scope == "full":
                distances_obj_to_send = self.distances_all

            # Set the text if no gradient is active.
            if distances_obj_to_send is None:
                distances_mode = self.distances_source_mode.get()

                if distances_mode == "All" and self.distances_all:
                    distances_obj_to_send = self.distances_all

                elif distances_mode == "Solution" and self.solution_path and self.distances_all:
                    distances_obj_to_send, _ = self.distances_all.shortest_path_to(self.solution_end_cell)

                elif distances_mode == "Longest" and self.longest_path and self.longest_path_distances:
                    distances_obj_to_send, _ = self.longest_path_distances.shortest_path_to(self.longest_path_end_cell)

                else:
                    # Fallback.
                    distances_obj_to_send = self.distances_all


            # Determine final parameters to send to to_png().
            path_cells_to_send = active_path_cells

            to_png_args = {
                'cell_size': self.cell_size.get(),
                'smooth_exp': self.smooth_exp.get(),

                # Background
                'background_type': self.background_type.get(),
                'full_color': hex_to_rgb(self.background_color),
                'checkerboard_color_1': hex_to_rgb(self.checkerboard_color_1),
                'checkerboard_color_2': hex_to_rgb(self.checkerboard_color_2),

                # Walls
                'thin_wall_width': _get_safe_value(self.thin_wall_width, self.DEFAULT_THIN_WALL),
                'thick_wall_width': _get_safe_value(self.thick_wall_width, self.DEFAULT_THICK_WALL),
                'thin_wall_color': hex_to_rgb(self.thin_wall_color),
                'thick_wall_color': hex_to_rgb(self.thick_wall_color),

                # Colors
                'text_color': hex_to_rgb(self.text_color),
                'deadend_color': hex_to_rgb(self.deadend_color),
                'gradient_start': hex_to_rgb(self.gradient_start),
                'gradient_middle': hex_to_rgb(self.gradient_middle),
                'gradient_end': hex_to_rgb(self.gradient_end),

                # Path Colors
                'path_color': path_color_to_send,
                'start_cell_color': start_cell_color_to_send,
                'end_cell_color': end_cell_color_to_send,

                # Data / Toggles
                'show_deadends': self.show_deadends.get(),
                'distances_obj': distances_obj_to_send,
                'show_distance_text': self.show_distances.get(),
                'gradient_scope': gradient_scope,
                'path_cells': path_cells_to_send,
                'draw_solid_path_line': draw_solid_line_flag,
                'show_path_start_end_cells': active_path_show_start_end
            }

            # Update the maze image.
            self.original_image = self.maze_grid.to_png(**to_png_args)

            self.current_image = self.original_image.resize(
                (int(self.original_image.width * self.zoom_level),
                 int(self.original_image.height * self.zoom_level)),
                Image.NEAREST
            )
            self.tk_image = ImageTk.PhotoImage(self.current_image)
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, image=self.tk_image, anchor=tk.NW)
            self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

        except Exception as e:
            tk.messagebox.showerror("Redraw Error", f"Cannot redraw maze: {e}")
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

        self.current_image = image
        self.tk_image = ImageTk.PhotoImage(self.current_image)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.tk_image, anchor=tk.NW)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))
    # ----------------------------------------------- #


    def adjust_zoom(self, factor):

        if self.original_image is None:
            return

        self.zoom_level *= factor
        if self.zoom_level < 0.1: self.zoom_level = 0.1
        if self.zoom_level > 10.0: self.zoom_level = 10.0

        self._redraw_maze()
    # ----------------------------------------------- #


    def _on_mouse_wheel(self, event):

        if event.delta > 0:
            self.adjust_zoom(1.1)
        else:
            self.adjust_zoom(1 / 1.1)
    # ----------------------------------------------- #


    def save_maze(self):

        if self.current_image is None:
            tk.messagebox.showwarning("Warning", "You must generate a maze")
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

        for target, default_hex in self.DEFAULT_COLORS.items():
            setattr(self, target, default_hex)
            self._update_color_preview(target, default_hex)

        self.background_color = self.DEFAULT_BG_COLOR
        self._update_color_preview('background_color', self.DEFAULT_BG_COLOR)

        self._redraw_maze()
    # ----------------------------------------------- #


    def _reset_background_color(self):
        self.background_color = self.DEFAULT_BG_COLOR
        self._update_color_preview('background_color', self.DEFAULT_BG_COLOR)
        self._redraw_maze()
    # ----------------------------------------------- #


    def _reset_checkerboard_colors(self):
        self.checkerboard_color_1 = self.DEFAULT_CHECKERBOARD_COLOR_1
        self.checkerboard_color_2 = self.DEFAULT_CHECKERBOARD_COLOR_2
        self._update_color_preview('checkerboard_color_1', self.DEFAULT_CHECKERBOARD_COLOR_1)
        self._update_color_preview('checkerboard_color_2', self.DEFAULT_CHECKERBOARD_COLOR_2)
    # ----------------------------------------------- #


    def _reset_dimensions_walls_cellsize(self):

        # Reset Dimensions and Walls
        self.rows.set(self.DEFAULT_ROWS)
        self.columns.set(self.DEFAULT_COLUMNS)
        self.cell_size.set(self.DEFAULT_CELL_SIZE)
        self.thin_wall_width.set(self.DEFAULT_THIN_WALL)
        self.thick_wall_width.set(self.DEFAULT_THICK_WALL)

        # Reset Checkerboard Colors
        self._reset_checkerboard_colors()

        self._redraw_maze()
    # ----------------------------------------------- #


    def _reset_smooth_exp(self):
        self.smooth_exp.set(self.DEFAULT_SMOOTH_EXP)
        self._redraw_maze()
    # ----------------------------------------------- #


    def _set_random_a_star_start_cell(self):

        if not self.maze_grid:
            tk.messagebox.showwarning("Warning", "Generate a maze first.")
            return

        try:
            start_cell = self.maze_grid.random_cell()
            self.start_cell_r.set(start_cell.row)
            self.start_cell_c.set(start_cell.column)
        except Exception as e:
            tk.messagebox.showerror("Error", f"Cannot set random A* start cell: {e}")
    # ----------------------------------------------- #


    def _set_random_a_star_end_cell(self):

        if not self.maze_grid:
            tk.messagebox.showwarning("Warning", "Generate a maze first.")
            return

        try:
            end_cell = self.maze_grid.random_cell()
            self.end_cell_r.set(end_cell.row)
            self.end_cell_c.set(end_cell.column)
        except Exception as e:
            tk.messagebox.showerror("Error", f"Cannot set random A* end cell: {e}")
    # ----------------------------------------------- #


    def _set_random_distance_start_cell(self):

        if not self.maze_grid:
            tk.messagebox.showwarning("Warning", "Generate a maze first.")
            return

        try:
            # Source cell of distances.
            start_cell = self.maze_grid.random_cell()

            # Update the variables, their trace will update the distances
            # and redraw the maze.
            self.distance_start_r.set(start_cell.row)
            self.distance_start_c.set(start_cell.column)
        except Exception as e:
            tk.messagebox.showerror("Error", f"Cannot set random distance start cell: {e}")
    # ----------------------------------------------- #


if __name__ == "__main__":
    window = tk.Tk()
    app = MazeApp(window)
    window.mainloop()
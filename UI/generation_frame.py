import tkinter as tk
from tkinter import ttk


class GenerationFrame(ttk.LabelFrame):


    def __init__(self, parent, controller):
        super().__init__(parent, text="Generation", padding="10")
        self.controller = controller
        self._create_widgets()
    # ----------------------------------------------- #


    def _create_widgets(self):

        # Choice of generative algorithm
        frame_algo = ttk.Frame(self)
        frame_algo.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(frame_algo, text="Algorithm:").pack(side=tk.LEFT, padx=(0, 5))

        combobox_algo = ttk.Combobox(
            frame_algo,
            textvariable=self.controller.algorithm_choice,
            values=list(self.controller.GENERATOR_ALGOS.keys()),
            state="readonly")
        combobox_algo.pack(side=tk.LEFT, fill=tk.X, expand=True)


        ttk.Separator(self, orient='horizontal').pack(fill=tk.X, pady=5)


        # Background of the maze (full color or checkerboard style).
        frame_background_type = ttk.LabelFrame(self, text="Background style", padding="10")
        frame_background_type.pack(fill=tk.X, pady=5)

        # Full color.
        frame_full_color = ttk.Frame(frame_background_type)
        frame_full_color.pack(fill=tk.X, anchor="w", pady=2)
        ttk.Radiobutton(
            frame_full_color,
            text="Full color",
            variable=self.controller.background_type,
            value="full_color",
            command=self.controller._redraw_maze
        ).pack(side=tk.LEFT)
        canvas_full_color_preview = tk.Canvas(frame_full_color, width=20, height=20, borderwidth=1, relief="solid")
        canvas_full_color_preview.pack(side=tk.RIGHT, padx=(5, 5))
        self.controller.color_previews["background_color"] = canvas_full_color_preview
        ttk.Button(
            frame_full_color,
            text="Background color",
            command=lambda: self.controller._choose_color("background_color"),
            width=18
        ).pack(side=tk.RIGHT)

        # Checkerboard.
        frame_checkerboard = ttk.Frame(frame_background_type)
        frame_checkerboard.pack(fill=tk.X, anchor="w", pady=2)
        ttk.Radiobutton(
            frame_checkerboard,
            text="Checkerboard",
            variable=self.controller.background_type,
            value="checkerboard",
            command=self.controller._redraw_maze
        ).pack(side=tk.LEFT)

        canvas_checkerboard_preview_2 = tk.Canvas(frame_checkerboard, width=20, height=20, borderwidth=1, relief="solid")
        canvas_checkerboard_preview_2.pack(side=tk.RIGHT, padx=(5, 5))
        self.controller.color_previews["checkerboard_color_2"] = canvas_checkerboard_preview_2
        ttk.Button(
            frame_checkerboard,
            text="Color 2",
            command=lambda: self.controller._choose_color("checkerboard_color_2"),
            width=8
        ).pack(side=tk.RIGHT)

        canvas_checkerboard_preview_1 = tk.Canvas(frame_checkerboard, width=20, height=20, borderwidth=1, relief="solid")
        canvas_checkerboard_preview_1.pack(side=tk.RIGHT, padx=(5, 5))
        self.controller.color_previews["checkerboard_color_1"] = canvas_checkerboard_preview_1
        ttk.Button(
            frame_checkerboard,
            text="Color 1",
            command=lambda: self.controller._choose_color("checkerboard_color_1"),
            width=8
        ).pack(side=tk.RIGHT)


        ttk.Separator(self, orient='horizontal').pack(fill=tk.X, pady=5)


        # Dimensions of the maze properties.
        frame_dimensions = ttk.LabelFrame(self, text="Dimensions", padding="10")
        frame_dimensions.pack(fill=tk.X, pady=5)

        # Size of the maze and cell size.
        frame_maze_size = ttk.Frame(frame_dimensions)
        frame_maze_size.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(frame_maze_size, text="Rows:").pack(side=tk.LEFT)
        ttk.Spinbox(frame_maze_size, textvariable=self.controller.rows, width=5, from_=1, to=1000).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Label(frame_maze_size, text="Columns:").pack(side=tk.LEFT)
        ttk.Spinbox(frame_maze_size, textvariable=self.controller.columns, width=5, from_=1, to=1000).pack(side=tk.LEFT, padx=(0, 5))

        frame_cell_size = ttk.Frame(frame_dimensions)
        frame_cell_size.pack(fill=tk.X, pady=5)
        ttk.Label(frame_cell_size, text="Cell size:").pack(side=tk.LEFT)
        ttk.Spinbox(frame_cell_size, textvariable=self.controller.cell_size, width=5, from_=1, to=100).pack(side=tk.LEFT, padx=(5, 0))


        ttk.Separator(self, orient='horizontal').pack(fill=tk.X, pady=5)


        # Thickness and colors of the walls.
        frame_thin = ttk.Frame(frame_dimensions)
        frame_thin.pack(fill=tk.X, pady=2)

        ttk.Label(frame_thin, text="Thin wall width:").pack(side=tk.LEFT)
        ttk.Spinbox(frame_thin, textvariable=self.controller.thin_wall_width, width=4, from_=1, to=10).pack(side=tk.LEFT, padx=5)


        frame_thick = ttk.Frame(frame_dimensions)
        frame_thick.pack(fill=tk.X, pady=2)

        ttk.Label(frame_thick, text="Thick wall width:").pack(side=tk.LEFT)
        ttk.Spinbox(frame_thick, textvariable=self.controller.thick_wall_width, width=4, from_=1, to=10).pack(side=tk.LEFT, padx=5)


        ttk.Button(
            self,
            text="Reset options",
            command=self.controller._reset_dimensions,
            style="Accent.TButton"
        ).pack(fill=tk.X, pady=(5, 10))

        ttk.Button(
            self,
            text="Generate maze",
            command=self.controller.generate_maze,
            style="Accent.TButton"
        ).pack(fill=tk.X, pady=5)
    # ----------------------------------------------- #
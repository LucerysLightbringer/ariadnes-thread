import tkinter as tk
from tkinter import ttk


class DetailsFrame(ttk.LabelFrame):


    def __init__(self, parent, controller):
        super().__init__(parent, text="Details", padding="10")
        self.controller = controller

        self._create_solution_widgets()
        ttk.Separator(self, orient='horizontal').pack(fill='x', pady=10)

        self._create_longest_path_widgets()
        ttk.Separator(self, orient='horizontal').pack(fill='x', pady=10)

        self._create_distances_widgets()
    # ----------------------------------------------- #


    def _create_solution_widgets(self):

        ttk.Checkbutton(
            self,
            text="Show solution (with A*)",
            variable=self.controller.show_solution,
            command=self.controller._on_toggle_solution
        ).pack(anchor="w")

        ttk.Checkbutton(
            self,
            text="Show Start/End cells",
            variable=self.controller.show_solution_start_end,
            command=self.controller._redraw_maze
        ).pack(anchor="w", padx=(10, 0))


        # The type of path to show (solid line or color gradient).
        frame_solution_path_render_mode = ttk.Frame(self)
        frame_solution_path_render_mode.pack(anchor="w", padx=(10, 0))

        ttk.Label(frame_solution_path_render_mode, text="Solution Path as:").pack(side=tk.LEFT)

        ttk.Radiobutton(
            frame_solution_path_render_mode,
            text="Solid Line",
            variable=self.controller.solution_path_render_mode,
            value="solid",
            command=self.controller._redraw_maze
        ).pack(side=tk.LEFT, padx=(5, 5))

        ttk.Radiobutton(
            frame_solution_path_render_mode,
            text="Gradient",
            variable=self.controller.solution_path_render_mode,
            value="gradient",
            command=self.controller._redraw_maze
        ).pack(side=tk.LEFT)


        # Start Cell
        frame_start = ttk.Frame(self)
        frame_start.pack(fill=tk.X, pady=(5, 0))
        ttk.Label(frame_start, text="Start cell (R, C):").pack(side=tk.LEFT)
        ttk.Entry(frame_start, textvariable=self.controller.start_cell_r, width=5).pack(side=tk.LEFT, padx=(5, 5))
        ttk.Entry(frame_start, textvariable=self.controller.start_cell_c, width=5).pack(side=tk.LEFT)
        ttk.Button(
            frame_start,
            text="Random cell",
            command=self.controller._set_random_solution_start_cell,
            width=8
        ).pack(side=tk.LEFT, padx=(10, 0))

        # End Cell
        frame_end = ttk.Frame(self)
        frame_end.pack(fill=tk.X, pady=(2, 5))
        ttk.Label(frame_end, text="End cell (R, C):  ").pack(side=tk.LEFT)
        ttk.Entry(frame_end, textvariable=self.controller.end_cell_r, width=5).pack(side=tk.LEFT, padx=(5, 5))
        ttk.Entry(frame_end, textvariable=self.controller.end_cell_c, width=5).pack(side=tk.LEFT)
        ttk.Button(
            frame_end,
            text="Random cell",
            command=self.controller._set_random_solution_end_cell,
            width=8
        ).pack(side=tk.LEFT, padx=(10, 0))
    # ----------------------------------------------- #


    def _create_longest_path_widgets(self):

        ttk.Checkbutton(
            self,
            text="Show longest path",
            variable=self.controller.show_longest_path,
            command=self.controller._on_toggle_longest_path
        ).pack(anchor="w")

        ttk.Checkbutton(
            self,
            text="Show Start/End Cells",
            variable=self.controller.show_longest_path_start_end,
            command=self.controller._redraw_maze
        ).pack(anchor="w", padx=(10, 0))


        # The type of path to show (solid line or color gradient).
        frame_longest_path_render_mode = ttk.Frame(self)
        frame_longest_path_render_mode.pack(anchor="w", padx=(10, 0))

        ttk.Label(frame_longest_path_render_mode, text="Longest Path as:").pack(side=tk.LEFT)

        ttk.Radiobutton(
            frame_longest_path_render_mode,
            text="Solid Line",
            variable=self.controller.longest_path_render_mode,
            value="solid",
            command=self.controller._redraw_maze
        ).pack(side=tk.LEFT, padx=(5, 5))

        ttk.Radiobutton(
            frame_longest_path_render_mode,
            text="Gradient",
            variable=self.controller.longest_path_render_mode,
            value="gradient",
            command=self.controller._redraw_maze
        ).pack(side=tk.LEFT)
    # ----------------------------------------------- #


    def _create_distances_widgets(self):

        ttk.Checkbutton(
            self,
            text="Toggle distance values",
            variable=self.controller.show_distances,
            command=self.controller._redraw_maze
        ).pack(anchor="w")

        # The type of distances to show (All the maze, only the solution cells,
        # only the longest path cells)
        ttk.Label(self, text="Distances Source:").pack(pady=(5, 0), anchor="w")
        frame_distance_source = ttk.Frame(self)
        frame_distance_source.pack(fill=tk.X, pady=(2, 5))

        ttk.Radiobutton(
            frame_distance_source,
            text="All",
            variable=self.controller.distances_source_mode,
            value="all_maze",
            command=self.controller._redraw_maze
        ).pack(side=tk.LEFT, padx=5)

        ttk.Radiobutton(
            frame_distance_source,
            text="Solution Path",
            variable=self.controller.distances_source_mode,
            value="solution_path",
            command=self.controller._redraw_maze
        ).pack(side=tk.LEFT, padx=5)

        ttk.Radiobutton(
            frame_distance_source,
            text="Longest Path",
            variable=self.controller.distances_source_mode,
            value="longest_path",
            command=self.controller._redraw_maze
        ).pack(side=tk.LEFT, padx=5)


        # Distance source cell.
        frame_distance_start = ttk.Frame(self)
        frame_distance_start.pack(fill=tk.X, pady=(2, 5))
        ttk.Label(frame_distance_start, text="Distances start cell (R , C):").pack(side=tk.LEFT)
        ttk.Entry(frame_distance_start, textvariable=self.controller.distance_start_r, width=5).pack(side=tk.LEFT, padx=(5, 5))
        ttk.Entry(frame_distance_start, textvariable=self.controller.distance_start_c, width=5).pack(side=tk.LEFT)

        ttk.Button(
            frame_distance_start,
            text="Random",
            command=self.controller._set_random_distance_start_cell,
            width=8
        ).pack(side=tk.LEFT, padx=(10, 0))
    # ----------------------------------------------- #
import tkinter as tk
from tkinter import ttk


class DisplayFrame(ttk.LabelFrame):


    def __init__(self, parent, controller):
        super().__init__(parent, text="Visualize", padding="10")
        self.controller = controller
        self._create_widgets()
    # ----------------------------------------------- #


    def _create_widgets(self):

        frame_zoom = ttk.Frame(self)
        frame_zoom.pack(fill=tk.X, pady=5)

        ttk.Button(frame_zoom,
                   text="Zoom +",
                   command=lambda: self.controller.adjust_zoom(1.2)).pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Button(frame_zoom,
                   text="Zoom -",
                   command=lambda: self.controller.adjust_zoom(1/1.2)).pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Button(
            self,
            text="Reset zoom",
            command=lambda: self.controller.adjust_zoom(1.0, reset=True),
            style="Accent.TButton"
        ).pack(fill=tk.X, pady=5)
    # ----------------------------------------------- #
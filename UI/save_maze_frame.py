import tkinter as tk
from tkinter import ttk


class SaveMazeFrame(ttk.Frame):


    def __init__(self, parent, controller):
        super().__init__(parent, padding="10")
        self.controller = controller
        self._create_widgets()
    # ----------------------------------------------- #


    def _create_widgets(self):

        ttk.Button(
            self,
            text="Save Maze as PNG",
            command=self.controller.save_maze_image,
            style="Accent.TButton"
        ).pack(fill=tk.X, expand=True)
    # ----------------------------------------------- #
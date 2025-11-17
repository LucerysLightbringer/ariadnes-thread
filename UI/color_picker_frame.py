import tkinter as tk
from tkinter import ttk


class ColorPickerFrame(ttk.LabelFrame):


    def __init__(self, parent, controller):
        super().__init__(parent, text="Colors", padding="10")
        self.controller = controller
        self._create_widgets()
    # ----------------------------------------------- #


    def _create_widgets(self):

        color_options = [
            ("start_cell_color", "Start cell"),
            ("end_cell_color", "End cell"),
            ("path_color", "Path"),
            ("text_color", "Text"),
            ("deadend_color", "Dead end"),
            ("gradient_start", "Start gradient"),
            ("gradient_middle", "Middle gradient"),
            ("gradient_end", "End gradient"),
            ("thin_wall_color", "Thin wall"),
            ("thick_wall_color", "Thick wall"),
        ]

        # Set the button and canvas preview of every color.
        for target_attr, button_text in color_options:

            frame_color = ttk.Frame(self)
            frame_color.pack(fill=tk.X, pady=2)

            canvas_color_preview = tk.Canvas(frame_color, width=20, height=20, borderwidth=1, relief="solid")
            canvas_color_preview.pack(side=tk.LEFT, padx=(0, 5))
            self.controller.color_previews[target_attr] = canvas_color_preview

            button = ttk.Button(
                frame_color,
                text=button_text,
                command=lambda t=target_attr: self.controller._choose_color(t)
            )
            button.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.controller.color_buttons[target_attr] = button

        ttk.Button(
            self,
            text="Reset colors",
            command=self.controller._reset_colors,
            style="Accent.TButton"
        ).pack(fill=tk.X, pady=(10, 5))
    # ----------------------------------------------- #
import tkinter as tk
from tkinter import ttk


class OptionsFrame(ttk.LabelFrame):


    def __init__(self, parent, controller):
        super().__init__(parent, text="Options", padding="10")
        self.controller = controller
        self._create_widgets()
    # ----------------------------------------------- #


    def _create_widgets(self):

        label_gradient = ttk.Label(self, text="Gradient", font=("Arial", 10, "bold"))
        label_gradient.pack(pady=(0, 5), anchor="w")

        ttk.Checkbutton(
            self,
            text="Toggle gradient (full maze)",
            variable=self.controller.show_gradient,
            command=self.controller._redraw_maze
        ).pack(anchor="w")

        # Smoothness exponent
        frame_smooth_exp = ttk.Frame(self)
        frame_smooth_exp.pack(fill=tk.X, pady=(15, 2))
        ttk.Label(frame_smooth_exp, text="Smooth Exp:").pack(side=tk.LEFT)
        ttk.Entry(frame_smooth_exp, textvariable=self.controller.smooth_exp, width=10).pack(side=tk.LEFT, padx=(5, 0))

        slider_smooth_exp = ttk.Scale(
            self,
            from_=0.1,
            to=3.0,
            orient=tk.HORIZONTAL,
            variable=self.controller.smooth_exp,
            command=lambda v: self.controller._update_smooth_slider(v)
        )
        slider_smooth_exp.pack(fill=tk.X, pady=2)

        self.controller.smooth_exp_label = ttk.Label(self, text=f"{self.controller.smooth_exp.get():.2f}")
        self.controller.smooth_exp_label.pack(anchor="e")


        ttk.Button(
            self,
            text="Reset Smooth Exponent",
            command=self.controller._reset_smooth_exp,
            style="Accent.TButton"
        ).pack(fill=tk.X, pady=(5, 10))


        ttk.Separator(self, orient='horizontal').pack(fill='x', pady=10)


        # Dead ends
        label_deadends = ttk.Label(self, text="Dead Ends", font=("Arial", 10, "bold"))
        label_deadends.pack(pady=(0, 5), anchor="w")
        ttk.Checkbutton(
            self,
            text="Show deadends",
            variable=self.controller.show_deadends,
            command=self.controller._redraw_maze
        ).pack(anchor="w")
    # ----------------------------------------------- #
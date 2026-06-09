"""Status bar component for displaying file info."""

import tkinter as tk


class StatusBar(tk.Frame):
    """Bottom status bar showing image metadata."""

    def __init__(self, parent: tk.Widget, **kwargs):
        super().__init__(parent, bd=1, relief=tk.SUNKEN, **kwargs)
        self.label = tk.Label(self, text="Ready", anchor=tk.W)
        self.label.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def set_text(self, text: str) -> None:
        self.label.config(text=text)

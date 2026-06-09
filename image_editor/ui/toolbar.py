"""Toolbar component with emoji + text buttons."""

import tkinter as tk
from typing import Callable


class Toolbar(tk.Frame):
    """Top toolbar with grouped action buttons."""

    def __init__(self, parent: tk.Widget, callbacks: dict, **kwargs):
        super().__init__(parent, bd=1, relief=tk.RAISED, **kwargs)
        self.callbacks = callbacks
        self.buttons: dict[str, tk.Button] = {}
        self._build_toolbar()

    def _add_separator(self) -> None:
        sep = tk.Frame(self, width=2, bg="#999999")
        sep.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=2)

    def _add_button(self, name: str, text: str, command: Callable,
                    enabled: bool = True, side: str = tk.LEFT,
                    width: int = 8) -> tk.Button:
        btn = tk.Button(self, text=text, command=command, width=width)
        btn.pack(side=side, padx=2, pady=2)
        if not enabled:
            btn.config(state=tk.DISABLED)
        self.buttons[name] = btn
        return btn

    def _build_toolbar(self) -> None:
        c = self.callbacks

        # File group
        self._add_button("open", "📂 Open", c.get("open"), enabled=True)
        self._add_button("save", "💾 Save", c.get("save"), enabled=False)
        self._add_button("undo", "↩️ Undo", c.get("undo"), enabled=False)
        self._add_button("redo", "↪️ Redo", c.get("redo"), enabled=False)
        self._add_separator()

        # Crop group
        self._add_button("crop", "✂️ Crop", c.get("crop"), enabled=False)
        self._add_button("apply_crop", "🔲 Apply", c.get("apply_crop"), enabled=False)
        self._add_button("cancel_crop", "❌ Cancel", c.get("cancel_crop"), enabled=False)
        self._add_separator()

        # Filters group
        self._add_button("grayscale", "⚫ Gray", c.get("grayscale"), enabled=False)
        self._add_button("sepia", "🌅 Sepia", c.get("sepia"), enabled=False)
        self._add_button("blur", "🌫️ Blur", c.get("blur"), enabled=False)
        self._add_button("sharpen", "✨ Sharpen", c.get("sharpen"), enabled=False)
        self._add_button("invert", "🔄 Invert", c.get("invert"), enabled=False)
        self._add_button("edge", "🔍 Edge", c.get("edge"), enabled=False)
        self._add_button("brightness", "🔆 Brt/Cnt", c.get("brightness"), enabled=False)
        self._add_separator()

        # Transform group
        self._add_button("rotate_cw", "↻ CW", c.get("rotate_cw"), enabled=False)
        self._add_button("rotate_ccw", "↺ CCW", c.get("rotate_ccw"), enabled=False)
        self._add_button("resize", "📐 Resize", c.get("resize"), enabled=False)
        self._add_separator()

        # Zoom group
        self._add_button("zoom_in", "➕ Zoom", c.get("zoom_in"), enabled=False)
        self._add_button("zoom_out", "➖ Zoom", c.get("zoom_out"), enabled=False)
        self._add_button("fit", "⬜ Fit", c.get("fit"), enabled=False)
        self._add_button("actual", "🔲 1:1", c.get("actual"), enabled=False)
        self._add_separator()

        # View group
        self._add_button("fullscreen", "🖥️ Full", c.get("fullscreen"), enabled=True)

    def set_button_state(self, name: str, enabled: bool) -> None:
        if name in self.buttons:
            state = tk.NORMAL if enabled else tk.DISABLED
            self.buttons[name].config(state=state)

    def set_image_loaded(self, loaded: bool) -> None:
        """Enable/disable all image-dependent buttons."""
        image_dependent = [
            "save", "undo", "redo", "crop", "grayscale", "sepia",
            "blur", "sharpen", "invert", "edge", "brightness",
            "rotate_cw", "rotate_ccw", "resize",
            "zoom_in", "zoom_out", "fit", "actual"
        ]
        for name in image_dependent:
            self.set_button_state(name, loaded)

    def set_crop_mode(self, active: bool) -> None:
        """Toggle button states when entering/exiting crop mode."""
        self.set_button_state("apply_crop", active)
        self.set_button_state("cancel_crop", active)
        self.set_button_state("crop", not active)
        if active:
            self.buttons["crop"].config(relief=tk.SUNKEN, bg="#cccccc")
        else:
            self.buttons["crop"].config(relief=tk.RAISED, bg=self.cget("bg"))

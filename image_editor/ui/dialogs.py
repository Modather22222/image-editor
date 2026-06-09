"""Custom dialogs for image adjustments."""

import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageEnhance
from typing import Callable, Optional, Tuple


class BrightnessContrastDialog(tk.Toplevel):
    """Real-time brightness and contrast adjustment dialog."""

    def __init__(self, parent: tk.Widget, image: Image.Image,
                 on_apply: Callable[[Image.Image], None]):
        super().__init__(parent)
        self.title("Brightness & Contrast")
        self.geometry("350x250")
        self.transient(parent)
        self.grab_set()
        self.resizable(False, False)

        self.original_image = image
        self.on_apply = on_apply
        self.result_image: Optional[Image.Image] = None

        self.brightness_var = tk.DoubleVar(value=1.0)
        self.contrast_var = tk.DoubleVar(value=1.0)

        self._build_ui()
        self._preview()

    def _build_ui(self) -> None:
        tk.Label(self, text="Brightness:").pack(pady=(10, 0))
        self.brightness_scale = tk.Scale(
            self, from_=0.1, to=3.0, resolution=0.1,
            orient=tk.HORIZONTAL, variable=self.brightness_var,
            command=lambda _: self._preview()
        )
        self.brightness_scale.pack(fill=tk.X, padx=20)

        tk.Label(self, text="Contrast:").pack(pady=(10, 0))
        self.contrast_scale = tk.Scale(
            self, from_=0.1, to=3.0, resolution=0.1,
            orient=tk.HORIZONTAL, variable=self.contrast_var,
            command=lambda _: self._preview()
        )
        self.contrast_scale.pack(fill=tk.X, padx=20)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=15)
        tk.Button(btn_frame, text="OK", width=10, command=self._on_ok).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cancel", width=10, command=self._on_cancel).pack(side=tk.LEFT, padx=5)

    def _preview(self) -> None:
        img = ImageEnhance.Brightness(self.original_image).enhance(self.brightness_var.get())
        img = ImageEnhance.Contrast(img).enhance(self.contrast_var.get())
        self.result_image = img

    def _on_ok(self) -> None:
        if self.result_image is not None:
            self.on_apply(self.result_image)
        self.destroy()

    def _on_cancel(self) -> None:
        self.destroy()


class ResizeDialog(simpledialog.Dialog):
    """Dialog for resizing image with optional aspect ratio lock."""

    def __init__(self, parent: tk.Widget, current_size: Tuple[int, int]):
        self.current_width, self.current_height = current_size
        self.new_width: Optional[int] = None
        self.new_height: Optional[int] = None
        self.lock_ratio = True
        super().__init__(parent, title="Resize Image")

    def body(self, master: tk.Widget) -> tk.Widget:
        tk.Label(master, text="Width:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.width_entry = tk.Entry(master)
        self.width_entry.insert(0, str(self.current_width))
        self.width_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(master, text="Height:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.height_entry = tk.Entry(master)
        self.height_entry.insert(0, str(self.current_height))
        self.height_entry.grid(row=1, column=1, padx=5, pady=5)

        self.lock_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            master, text="Lock aspect ratio",
            variable=self.lock_var
        ).grid(row=2, column=0, columnspan=2, pady=5)

        self.width_entry.bind("<KeyRelease>", self._on_width_change)
        self.height_entry.bind("<KeyRelease>", self._on_height_change)
        return self.width_entry

    def _on_width_change(self, event: tk.Event) -> None:
        if not self.lock_var.get():
            return
        try:
            w = int(self.width_entry.get())
            h = int(w * self.current_height / self.current_width)
            self.height_entry.delete(0, tk.END)
            self.height_entry.insert(0, str(h))
        except ValueError:
            pass

    def _on_height_change(self, event: tk.Event) -> None:
        if not self.lock_var.get():
            return
        try:
            h = int(self.height_entry.get())
            w = int(h * self.current_width / self.current_height)
            self.width_entry.delete(0, tk.END)
            self.width_entry.insert(0, str(w))
        except ValueError:
            pass

    def validate(self) -> bool:
        try:
            self.new_width = int(self.width_entry.get())
            self.new_height = int(self.height_entry.get())
            if self.new_width <= 0 or self.new_height <= 0:
                raise ValueError
            return True
        except ValueError:
            import tkinter.messagebox as msg
            msg.showerror("Invalid Input", "Please enter positive integers for width and height.")
            return False

    def apply(self) -> None:
        pass

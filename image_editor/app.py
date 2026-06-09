"""Main application controller wiring UI to core logic."""

import os
from typing import Optional, Tuple

from PIL import Image

from image_editor.core.image_processor import ImageProcessor
from image_editor.core.history_manager import HistoryManager, Command
from image_editor.ui.main_window import MainWindow
from image_editor.ui.dialogs import BrightnessContrastDialog, ResizeDialog
from image_editor.utils.constants import MAX_HISTORY, SUPPORTED_OPEN_EXTENSIONS, SUPPORTED_SAVE_EXTENSIONS, JPEG_QUALITY


class ImageEditorApp:
    """Application controller managing UI and image state."""

    def __init__(self) -> None:
        self.history = HistoryManager(max_history=MAX_HISTORY)
        self.processor = ImageProcessor()
        self.window = MainWindow(self)

        self._current_image: Optional[Image.Image] = None
        self._image_path: Optional[str] = None

        self._startup_open()

    def _startup_open(self) -> None:
        """Prompt user to open an image on startup."""
        self.window.after(100, self.on_open)

    # ---- Properties ----

    @property
    def current_image(self) -> Optional[Image.Image]:
        return self._current_image

    def has_unsaved_changes(self) -> bool:
        return self.history.is_dirty

    # ---- UI helpers ----

    def _update_ui(self) -> None:
        loaded = self._current_image is not None
        self.window.toolbar.set_image_loaded(loaded)
        self.window.canvas_view.set_image(self._current_image)
        if self._current_image:
            self.window.status_bar.set_text(
                f"{os.path.basename(self._image_path or 'Untitled')} "
                f"({self._current_image.width}x{self._current_image.height}) "
                f"Zoom: {int(self.window.canvas_view.zoom * 100)}%"
            )
        else:
            self.window.status_bar.set_text("Ready")

    def _set_image(self, image: Image.Image, path: Optional[str] = None) -> None:
        self._current_image = image
        self._image_path = path
        self.history.reset(image)
        self._update_ui()

    def _push_command(self, name: str) -> None:
        if self._current_image is None:
            return
        cmd = Command(name=name, pre_image=self._current_image.copy())
        self.history.push(cmd)

    def _apply_and_push(self, image: Image.Image, name: str) -> None:
        self._push_command(name)
        self._current_image = image
        self._update_ui()

    # ---- File Operations ----

    def on_open(self) -> None:
        import tkinter as tk
        from tkinter import filedialog, messagebox
        import traceback
        path = filedialog.askopenfilename(filetypes=SUPPORTED_OPEN_EXTENSIONS)
        if path:
            try:
                img = Image.open(path)
                self._set_image(img, path)
            except Exception as e:
                error_detail = traceback.format_exc()
                messagebox.showerror(
                    "Error",
                    f"Could not open image:\n{path}\n\nError: {e}\n\n"
                    f"Please check the file exists and is a valid image."
                )
                print(f"[ERROR] Failed to open {path}:\n{error_detail}")

    def on_save(self) -> None:
        import tkinter as tk
        from tkinter import messagebox
        if self._current_image is None:
            messagebox.showwarning("Warning", "No image to save.")
            return
        if self._image_path:
            try:
                self._save_to_path(self._current_image, self._image_path)
                self.history.set_clean(self._current_image)
                self.window.status_bar.set_text(f"Saved: {os.path.basename(self._image_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save:\n{e}")
        else:
            self.on_save_as()

    def on_save_as(self) -> None:
        import tkinter as tk
        from tkinter import filedialog, messagebox
        if self._current_image is None:
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=SUPPORTED_SAVE_EXTENSIONS
        )
        if path:
            try:
                self._save_to_path(self._current_image, path)
                self._image_path = path
                self.history.set_clean(self._current_image)
                self.window.status_bar.set_text(f"Saved as: {os.path.basename(path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save:\n{e}")

    def _save_to_path(self, image: Image.Image, path: str) -> None:
        ext = os.path.splitext(path)[1].lower()
        if ext in (".jpg", ".jpeg"):
            if image.mode in ("RGBA", "P", "LA"):
                image = image.convert("RGB")
            image.save(path, quality=JPEG_QUALITY)
        else:
            image.save(path)

    # ---- Edit Operations ----

    def on_undo(self) -> None:
        prev = self.history.undo()
        if prev is not None:
            self._current_image = prev.copy()
            self._update_ui()
            self.window.status_bar.set_text("Undo")

    def on_redo(self) -> None:
        import tkinter as tk
        from tkinter import messagebox
        cmd = self.history.pop_redo()
        if cmd is None:
            return
        messagebox.showinfo("Redo", "Redo re-applies the last operation. Please use the menu to re-apply if needed.")

    # ---- Crop ----

    def on_toggle_crop(self) -> None:
        import tkinter as tk
        from tkinter import messagebox
        if self._current_image is None:
            messagebox.showwarning("Warning", "Open an image first.")
            return
        new_mode = not self.window.canvas_view.crop_mode
        self.window.canvas_view.set_crop_mode(new_mode)
        self.window.toolbar.set_crop_mode(new_mode)
        if new_mode:
            self.window.status_bar.set_text("Crop: Click and drag to select. Enter to apply, ESC to cancel.")
        else:
            self._update_ui()

    def on_apply_crop(self) -> None:
        self.window.canvas_view.apply_crop()

    def on_cancel_crop(self) -> None:
        self.window.canvas_view.cancel_crop()
        self.window.toolbar.set_crop_mode(False)
        self._update_ui()

    def on_crop_ready(self, box: Tuple[int, int, int, int]) -> None:
        if self._current_image is None:
            return
        try:
            cropped = self.processor.crop(self._current_image, box)
            self._apply_and_push(cropped, "crop")
            self.window.toolbar.set_crop_mode(False)
            self.window.canvas_view.set_crop_mode(False)
            self.window.status_bar.set_text(f"Cropped to {cropped.width}x{cropped.height}")
        except Exception as e:
            import tkinter as tk
            from tkinter import messagebox
            messagebox.showerror("Error", f"Could not crop:\n{e}")

    def on_crop_cancel(self) -> None:
        self.window.toolbar.set_crop_mode(False)
        self.window.canvas_view.set_crop_mode(False)
        self._update_ui()

    # ---- Filters ----

    def on_filter(self, name: str) -> None:
        import tkinter as tk
        from tkinter import messagebox
        if self._current_image is None:
            return
        try:
            method = getattr(self.processor, name)
            result = method(self._current_image)
            self._apply_and_push(result, name)
            self.window.status_bar.set_text(f"Applied: {name.capitalize()}")
        except Exception as e:
            messagebox.showerror("Error", f"Filter failed:\n{e}")

    def on_brightness_contrast(self) -> None:
        if self._current_image is None:
            return
        dialog = BrightnessContrastDialog(
            self.window, self._current_image.copy(),
            on_apply=lambda img: self._apply_and_push(img, "brightness/contrast")
        )
        self.window.wait_window(dialog)

    # ---- Transform ----

    def on_rotate_cw(self) -> None:
        if self._current_image is None:
            return
        result = self.processor.rotate_90_cw(self._current_image)
        self._apply_and_push(result, "rotate_cw")
        self.window.status_bar.set_text("Rotated 90° clockwise")

    def on_rotate_ccw(self) -> None:
        if self._current_image is None:
            return
        result = self.processor.rotate_90_ccw(self._current_image)
        self._apply_and_push(result, "rotate_ccw")
        self.window.status_bar.set_text("Rotated 90° counter-clockwise")

    def on_resize(self) -> None:
        if self._current_image is None:
            return
        dialog = ResizeDialog(self.window, (self._current_image.width, self._current_image.height))
        self.window.wait_window(dialog)
        if dialog.new_width and dialog.new_height:
            result = self.processor.resize(self._current_image, dialog.new_width, dialog.new_height)
            self._apply_and_push(result, "resize")
            self.window.status_bar.set_text(f"Resized to {dialog.new_width}x{dialog.new_height}")

    # ---- View ----

    def on_zoom_in(self) -> None:
        self.window.canvas_view.zoom_in()
        self._update_ui()

    def on_zoom_out(self) -> None:
        self.window.canvas_view.zoom_out()
        self._update_ui()

    def on_fit(self) -> None:
        self.window.canvas_view.fit_to_window()
        self._update_ui()

    def on_actual(self) -> None:
        self.window.canvas_view.actual_size()
        self._update_ui()

    def on_toggle_fullscreen(self) -> None:
        self.window.set_fullscreen(not self.window._fullscreen)

    # ---- Main Loop ----

    def run(self) -> None:
        self.window.mainloop()

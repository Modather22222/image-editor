"""Main application window composing all UI components."""

import tkinter as tk
from tkinter import filedialog, messagebox
from typing import TYPE_CHECKING

from image_editor.ui.toolbar import Toolbar
from image_editor.ui.canvas_view import CanvasView
from image_editor.ui.status_bar import StatusBar

if TYPE_CHECKING:
    from image_editor.app import ImageEditorApp


class MainWindow(tk.Tk):
    """Root window and menu bar."""

    def __init__(self, app_controller: "ImageEditorApp"):
        super().__init__()
        self.controller = app_controller
        self.title("Image Viewer & Editor")
        self.geometry("1200x800")
        self.minsize(800, 600)

        self._fullscreen = False
        self._build_menu()
        self._build_ui()
        self._bind_shortcuts()

    def _build_menu(self) -> None:
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=self.controller.on_open, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.controller.on_save, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As...", command=self.controller.on_save_as, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._on_exit)

        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=self.controller.on_undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=self.controller.on_redo, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Crop Mode", command=self.controller.on_toggle_crop)
        edit_menu.add_command(label="Resize...", command=self.controller.on_resize)

        filter_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Filters", menu=filter_menu)
        filter_menu.add_command(label="Grayscale", command=lambda: self.controller.on_filter("grayscale"))
        filter_menu.add_command(label="Sepia", command=lambda: self.controller.on_filter("sepia"))
        filter_menu.add_command(label="Blur", command=lambda: self.controller.on_filter("blur"))
        filter_menu.add_command(label="Sharpen", command=lambda: self.controller.on_filter("sharpen"))
        filter_menu.add_command(label="Edge Detect", command=lambda: self.controller.on_filter("edge"))
        filter_menu.add_command(label="Invert", command=lambda: self.controller.on_filter("invert"))
        filter_menu.add_separator()
        filter_menu.add_command(label="Brightness/Contrast...", command=self.controller.on_brightness_contrast)

        transform_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Transform", menu=transform_menu)
        transform_menu.add_command(label="Rotate 90 CW", command=self.controller.on_rotate_cw, accelerator="R")
        transform_menu.add_command(label="Rotate 90 CCW", command=self.controller.on_rotate_ccw, accelerator="Shift+R")

        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Zoom In", command=self.controller.on_zoom_in, accelerator="+")
        view_menu.add_command(label="Zoom Out", command=self.controller.on_zoom_out, accelerator="-")
        view_menu.add_command(label="Fit to Window", command=self.controller.on_fit, accelerator="Ctrl+0")
        view_menu.add_command(label="Actual Size", command=self.controller.on_actual, accelerator="Ctrl+1")
        view_menu.add_separator()
        view_menu.add_command(label="Fullscreen", command=self.controller.on_toggle_fullscreen, accelerator="F11")

    def _build_ui(self) -> None:
        callbacks = {
            "open": self.controller.on_open,
            "save": self.controller.on_save,
            "save_as": self.controller.on_save_as,
            "undo": self.controller.on_undo,
            "redo": self.controller.on_redo,
            "crop": self.controller.on_toggle_crop,
            "apply_crop": self.controller.on_apply_crop,
            "cancel_crop": self.controller.on_cancel_crop,
            "grayscale": lambda: self.controller.on_filter("grayscale"),
            "sepia": lambda: self.controller.on_filter("sepia"),
            "blur": lambda: self.controller.on_filter("blur"),
            "sharpen": lambda: self.controller.on_filter("sharpen"),
            "invert": lambda: self.controller.on_filter("invert"),
            "edge": lambda: self.controller.on_filter("edge"),
            "brightness": self.controller.on_brightness_contrast,
            "rotate_cw": self.controller.on_rotate_cw,
            "rotate_ccw": self.controller.on_rotate_ccw,
            "resize": self.controller.on_resize,
            "zoom_in": self.controller.on_zoom_in,
            "zoom_out": self.controller.on_zoom_out,
            "fit": self.controller.on_fit,
            "actual": self.controller.on_actual,
            "fullscreen": self.controller.on_toggle_fullscreen,
        }
        self.toolbar = Toolbar(self, callbacks)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        self.canvas_view = CanvasView(
            self,
            on_crop_ready=self.controller.on_crop_ready,
            on_crop_cancel=self.controller.on_crop_cancel
        )
        self.canvas_view.pack(fill=tk.BOTH, expand=True)

        self.status_bar = StatusBar(self)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def _bind_shortcuts(self) -> None:
        self.bind("<Control-o>", lambda e: self.controller.on_open())
        self.bind("<Control-s>", lambda e: self.controller.on_save())
        self.bind("<Control-Shift-S>", lambda e: self.controller.on_save_as())
        self.bind("<Control-z>", lambda e: self.controller.on_undo())
        self.bind("<Control-y>", lambda e: self.controller.on_redo())
        self.bind("<plus>", lambda e: self.controller.on_zoom_in())
        self.bind("<minus>", lambda e: self.controller.on_zoom_out())
        self.bind("<Control-0>", lambda e: self.controller.on_fit())
        self.bind("<Control-1>", lambda e: self.controller.on_actual())
        self.bind("<c>", lambda e: self.controller.on_toggle_crop())
        self.bind("<C>", lambda e: self.controller.on_toggle_crop())
        self.bind("<r>", lambda e: self.controller.on_rotate_cw())
        self.bind("<R>", lambda e: self.controller.on_rotate_ccw())
        self.bind("<F11>", lambda e: self.controller.on_toggle_fullscreen())
        self.bind("<Escape>", lambda e: self._on_escape())
        self.protocol("WM_DELETE_WINDOW", self._on_exit)

    def _on_escape(self) -> None:
        if self._fullscreen:
            self.controller.on_toggle_fullscreen()
        elif self.canvas_view.crop_mode:
            self.controller.on_cancel_crop()

    def _on_exit(self) -> None:
        if self.controller.has_unsaved_changes():
            ans = messagebox.askyesnocancel(
                "Unsaved Changes",
                "You have unsaved changes. Save before exiting?"
            )
            if ans is True:
                self.controller.on_save()
                if not self.controller.has_unsaved_changes():
                    self.destroy()
            elif ans is False:
                self.destroy()
        else:
            self.destroy()

    def set_fullscreen(self, enabled: bool) -> None:
        self._fullscreen = enabled
        self.attributes("-fullscreen", enabled)
        if enabled:
            self.toolbar.pack_forget()
            self.status_bar.pack_forget()
            self.config(menu="")
        else:
            self.toolbar.pack(side=tk.TOP, fill=tk.X)
            self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
            self._build_menu()

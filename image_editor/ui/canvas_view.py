"""Image canvas with zoom, pan, and crop selection."""

import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
from typing import Optional, Tuple, Callable


class CanvasView(tk.Frame):
    """Scrollable canvas for image display with crop support."""

    def __init__(self, parent: tk.Widget,
                 on_crop_ready: Callable[[Tuple[int, int, int, int]], None],
                 on_crop_cancel: Callable[[], None],
                 **kwargs):
        super().__init__(parent, **kwargs)

        self.on_crop_ready = on_crop_ready
        self.on_crop_cancel = on_crop_cancel

        self._image: Optional[Image.Image] = None
        self._display_image: Optional[ImageTk.PhotoImage] = None
        self._zoom = 1.0
        self._crop_mode = False
        self._crop_start: Optional[Tuple[float, float]] = None
        self._crop_rect_id: Optional[int] = None
        self._overlay_id: Optional[int] = None

        self._setup_scrollbars()
        self._setup_canvas()
        self._bind_events()

    def _setup_scrollbars(self) -> None:
        self.h_scroll = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.v_scroll = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    def _setup_canvas(self) -> None:
        self.canvas = tk.Canvas(
            self,
            bg="#2b2b2b",
            xscrollcommand=self.h_scroll.set,
            yscrollcommand=self.v_scroll.set,
            highlightthickness=0
        )
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.h_scroll.config(command=self.canvas.xview)
        self.v_scroll.config(command=self.canvas.yview)

    def _bind_events(self) -> None:
        self.canvas.bind("<ButtonPress-1>", self._on_press)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind("<Button-4>", self._on_mousewheel_linux)
        self.canvas.bind("<Button-5>", self._on_mousewheel_linux)
        # Middle click pan
        self.canvas.bind("<ButtonPress-2>", self._on_middle_press)
        self.canvas.bind("<B2-Motion>", self._on_middle_drag)

    @property
    def zoom(self) -> float:
        return self._zoom

    @property
    def crop_mode(self) -> bool:
        return self._crop_mode

    def set_image(self, image: Optional[Image.Image]) -> None:
        self._image = image
        self._zoom = 1.0
        self._clear_crop()
        self._render()

    def _render(self) -> None:
        self.canvas.delete("all")
        if self._image is None:
            self.canvas.config(scrollregion=(0, 0, 1, 1))
            return

        w = int(self._image.width * self._zoom)
        h = int(self._image.height * self._zoom)
        resized = self._image.resize((w, h), Image.Resampling.LANCZOS)
        self._display_image = ImageTk.PhotoImage(resized)

        # Center image in canvas viewport
        cw = max(self.canvas.winfo_width(), w)
        ch = max(self.canvas.winfo_height(), h)
        x = cw / 2
        y = ch / 2

        self.canvas.create_image(x, y, image=self._display_image, anchor=tk.CENTER, tags=("image",))
        self.canvas.config(scrollregion=(0, 0, cw, ch))

        # Draw checkerboard background behind image for transparency
        self._draw_checkerboard(x - w/2, y - h/2, w, h)

    def _draw_checkerboard(self, x: float, y: float, w: float, h: float) -> None:
        size = 20
        colors = ["#555555", "#777777"]
        for row in range(int(h / size) + 1):
            for col in range(int(w / size) + 1):
                color = colors[(row + col) % 2]
                x0 = x + col * size
                y0 = y + row * size
                self.canvas.create_rectangle(
                    x0, y0, x0 + size, y0 + size,
                    fill=color, outline="", tags=("bg",)
                )
        self.canvas.tag_lower("bg")

    def zoom_in(self) -> None:
        if self._image and self._zoom < 5.0:
            self._zoom = min(5.0, round(self._zoom + 0.1, 1))
            self._render()

    def zoom_out(self) -> None:
        if self._image and self._zoom > 0.1:
            self._zoom = max(0.1, round(self._zoom - 0.1, 1))
            self._render()

    def fit_to_window(self) -> None:
        if self._image is None:
            return
        cw = self.canvas.winfo_width() or 800
        ch = self.canvas.winfo_height() or 600
        scale_w = cw / self._image.width
        scale_h = ch / self._image.height
        self._zoom = max(0.1, min(5.0, round(min(scale_w, scale_h), 2)))
        self._render()

    def actual_size(self) -> None:
        self._zoom = 1.0
        self._render()

    def set_zoom(self, zoom: float) -> None:
        self._zoom = max(0.1, min(5.0, round(zoom, 2)))
        self._render()

    def _on_middle_press(self, event: tk.Event) -> None:
        self.canvas.scan_mark(event.x, event.y)

    def _on_middle_drag(self, event: tk.Event) -> None:
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def _on_mousewheel(self, event: tk.Event) -> None:
        if event.delta > 0:
            self.zoom_in()
        else:
            self.zoom_out()

    def _on_mousewheel_linux(self, event: tk.Event) -> None:
        if event.num == 4:
            self.zoom_in()
        elif event.num == 5:
            self.zoom_out()

    def set_crop_mode(self, enabled: bool) -> None:
        self._crop_mode = enabled
        self._clear_crop()
        if enabled and self._image:
            self.canvas.config(cursor="crosshair")
        else:
            self.canvas.config(cursor="")

    def _clear_crop(self) -> None:
        self._crop_start = None
        if self._crop_rect_id is not None:
            self.canvas.delete(self._crop_rect_id)
            self._crop_rect_id = None
        if self._overlay_id is not None:
            self.canvas.delete(self._overlay_id)
            self._overlay_id = None

    def _on_press(self, event: tk.Event) -> None:
        if not self._crop_mode or self._image is None:
            return
        self._crop_start = (self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        self._clear_crop()

    def _on_drag(self, event: tk.Event) -> None:
        if not self._crop_mode or self._crop_start is None or self._image is None:
            return
        cur_x = self.canvas.canvasx(event.x)
        cur_y = self.canvas.canvasy(event.y)
        if self._crop_rect_id is not None:
            self.canvas.delete(self._crop_rect_id)
        if self._overlay_id is not None:
            self.canvas.delete(self._overlay_id)
        self._crop_rect_id = self.canvas.create_rectangle(
            self._crop_start[0], self._crop_start[1],
            cur_x, cur_y,
            outline="red", width=2, dash=(5, 5)
        )
        self._draw_overlay(self._crop_start[0], self._crop_start[1], cur_x, cur_y)

    def _draw_overlay(self, x1: float, y1: float, x2: float, y2: float) -> None:
        img_item = self.canvas.find_withtag("image")
        if not img_item:
            return
        coords = self.canvas.coords(img_item[0])
        if not coords:
            return
        ix, iy = coords[0], coords[1]
        iw = self._image.width * self._zoom
        ih = self._image.height * self._zoom
        img_x1 = ix - iw / 2
        img_y1 = iy - ih / 2
        img_x2 = img_x1 + iw
        img_y2 = img_y1 + ih
        left = min(x1, x2)
        top = min(y1, y2)
        right = max(x1, x2)
        bottom = max(y1, y2)
        overlay = Image.new("RGBA", (self.canvas.winfo_width(), self.canvas.winfo_height()), (0, 0, 0, 128))
        draw = ImageDraw.Draw(overlay)
        draw.rectangle([left - img_x1, top - img_y1, right - img_x1, bottom - img_y1], fill=(0, 0, 0, 0))
        self._overlay_photo = ImageTk.PhotoImage(overlay)
        self._overlay_id = self.canvas.create_image(0, 0, image=self._overlay_photo, anchor=tk.NW)
        self.canvas.tag_lower(self._overlay_id, "image")
        self.canvas.tag_lower("bg", self._overlay_id)

    def _on_release(self, event: tk.Event) -> None:
        pass

    def apply_crop(self) -> None:
        if not self._crop_mode or self._crop_start is None or self._crop_rect_id is None:
            return
        coords = self.canvas.coords(self._crop_rect_id)
        if not coords:
            return
        cx1, cy1, cx2, cy2 = coords
        img_item = self.canvas.find_withtag("image")
        if not img_item:
            return
        ix, iy = self.canvas.coords(img_item[0])
        iw = self._image.width * self._zoom
        ih = self._image.height * self._zoom
        img_x1 = ix - iw / 2
        img_y1 = iy - ih / 2
        x1 = int((min(cx1, cx2) - img_x1) / self._zoom)
        y1 = int((min(cy1, cy2) - img_y1) / self._zoom)
        x2 = int((max(cx1, cx2) - img_x1) / self._zoom)
        y2 = int((max(cy1, cy2) - img_y1) / self._zoom)
        x1 = max(0, min(x1, self._image.width))
        y1 = max(0, min(y1, self._image.height))
        x2 = max(0, min(x2, self._image.width))
        y2 = max(0, min(y2, self._image.height))
        if x2 > x1 and y2 > y1:
            self.on_crop_ready((x1, y1, x2, y2))
        else:
            self.on_crop_cancel()

    def cancel_crop(self) -> None:
        self._clear_crop()
        self.set_crop_mode(False)
        self.on_crop_cancel()

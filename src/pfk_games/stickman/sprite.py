import time
import tkinter as tk

from pfk_games.stickman.coords import Coords, Point
from pfk_games.stickman.images import image_path


class Sprite:
    def __init__(self, canvas: tk.Canvas) -> None:
        self._canvas = canvas
        self._canvas_width: int = canvas.winfo_width()
        self._canvas_height: int = canvas.winfo_height()
        self._endgame = False
        self._coordinates = Coords()

    def tick(self) -> None:
        pass

    def coords(self) -> Coords:
        return self._coordinates


class PlatformSprite(Sprite):
    def __init__(self,
                 canvas: tk.Canvas,
                 source_image: tk.PhotoImage,
                 x: int, y: int,
                 width: int = 0, height: int = 0) -> None:
        super().__init__(canvas)

        if width == 0:
            width = source_image.width()
        if height == 0:
            height = source_image.height()

        self._source_image = source_image
        self._canvas_image = canvas.create_image(x, y, image=source_image, anchor="nw")
        self._coordinates = Coords(Point(x, y), Point(x + width, y + height))


class StickFigureSprite(Sprite):
    def __init__(self, canvas: tk.Canvas) -> None:
        super().__init__(canvas)
        self._images_left = [
            tk.PhotoImage(file=image_path("figure-l1.png")),
            tk.PhotoImage(file=image_path("figure-l2.png")),
            tk.PhotoImage(file=image_path("figure-l3.png"))
        ]
        self._images_right = [
            tk.PhotoImage(file=image_path("figure-r1.png")),
            tk.PhotoImage(file=image_path("figure-r2.png")),
            tk.PhotoImage(file=image_path("figure-r3.png"))
        ]
        top_left = Point(200, 470)
        bottom_right = Point(top_left.x + 27, top_left.y + 30)
        self._coordinates = Coords(top_left, bottom_right)
        self._canvas_image = canvas.create_image(top_left.x, top_left.y, image=self._images_left[0], anchor="nw")
        self._dx = -2
        self._dy = 0
        self._current_index = 0
        self._current_image = self._images_left[0]
        self._index_delta = 1
        self._jump_count = 0
        self._last_time = time.time()

    def turn_left(self) -> None:
        if self._dy == 0:
            self._dx = -2

    def turn_right(self) -> None:
        if self._dy == 0:
            self._dx = 2

    def jump(self) -> None:
        if self._dy == 0:
            self._dy = -4
            self._jump_count = 0

    def animate(self) -> None:
        self._cycle_current_image()
        self._canvas.itemconfig(self._canvas_image, image=self._current_image)

    def _cycle_current_image(self):
        if self._dx != 0 and self._dy == 0:
            now = time.time()
            if now - self._last_time > 0.1:
                self._last_time = now
                self._current_index += self._index_delta
                if self._current_index >= 2:
                    self._index_delta = -1
                if self._current_index <= 0:
                    self._index_delta = 1
        self._current_image = self._get_current_image()

    def _get_current_image(self) -> tk.PhotoImage:
        if self._dx < 0:
            if self._dy != 0:
                return self._images_left[2]
            else:
                return self._images_left[self._current_index]
        elif self._dx > 0:
            if self._dy != 0:
                return self._images_right[2]
            else:
                return self._images_right[self._current_index]
        return self._images_left[0]

    def tick(self) -> None:
        self.animate()
        if self._dx < 0 and self.coords().left <= 0:
            self._dx = 0
        if self._dy < 0 and self.coords().top <= 0:
            self._dy = -self._dy
        if self._dx > 0 and self.coords().right >= self._canvas_width:
            self._dx = 0
        if self._dy > 0 and self.coords().bottom >= self._canvas_height:
            self._dy = 0

        self._canvas.move(self._canvas_image, self._dx, self._dy)
        self._coordinates.move(self._dx, self._dy)

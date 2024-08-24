from __future__ import annotations
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

    @property
    def coords(self) -> Coords:
        return self._coordinates

    @property
    def endgame(self) -> bool:
        return self._endgame


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
    def __init__(self, canvas: tk.Canvas, sprites: list[Sprite]) -> None:
        super().__init__(canvas)
        self._sprites = sprites
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
        self._dx = 0
        self._dy = 0
        self._current_index = 0
        self._current_image = self._images_left[0]
        self._index_delta = 1
        self._jump_count = 0
        self._last_time = time.time()

    def _animate(self) -> None:
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

    def tick(self) -> None:
        self._animate()
        self._update_jump_state()
        self._keep_on_canvas()
        on_platform = False
        for sprite in self._sprites:
            on_platform = self._check_collision(sprite, on_platform)

        self._canvas.move(self._canvas_image, self._dx, self._dy)
        self._coordinates.move(self._dx, self._dy)

    def _moving_left(self) -> bool:
        return self._dx < 0

    def _moving_right(self):
        return self._dx > 0

    def _moving_up(self) -> bool:
        return self._dy < 0

    def _moving_down(self) -> bool:
        return self._dy > 0

    def _stop_horizontal(self) -> None:
        self._dx = 0

    def _stop_vertical(self) -> None:
        self._dy = 0

    def _update_jump_state(self) -> None:
        if self._moving_up():
            self._jump_count += 1
            if self._jump_count > 20:
                self._dy = 4
        if self._moving_down():
            self._jump_count -= 1

    def _keep_on_canvas(self) -> None:
        self._check_left_edge()
        self._check_right_edge()
        self._check_top_edge()
        self._check_bottom_edge()

    def _check_bottom_edge(self) -> None:
        if self._moving_down() and self.coords.bottom >= self._canvas_height:
            self._stop_vertical()

    def _check_top_edge(self) -> None:
        if self._moving_up() and self.coords.top <= 0:
            self._stop_vertical()

    def _check_left_edge(self) -> None:
        if self._moving_left() and self.coords.left <= 0:
            self._stop_horizontal()

    def _check_right_edge(self) -> None:
        if self._moving_right() and self.coords.right >= self._canvas_width:
            self._stop_horizontal()

    def _check_collision(self, sprite: Sprite, on_platform: bool) -> bool:
        if sprite == self:
            return on_platform
        if self._has_hit_top(sprite):
            self._dy = -self._dy
        if self._will_hit_bottom(sprite):
            self._dy = max(0, sprite.coords.top - self.coords.bottom)
        if (not on_platform and self._dy == 0 and
                self.coords.bottom < self._canvas_height and
                self.coords.collided_bottom(sprite.coords, 1)):
            on_platform = True
        if self._has_hit_left(sprite):
            self._stop_horizontal()
            if sprite.endgame:
                self._endgame = True
        if self._has_hit_right(sprite):
            self._stop_horizontal()
            if sprite.endgame:
                self._endgame = True
        if not on_platform and self._dy == 0 and self.coords.bottom < self._canvas_height:
            self._dy = 4
        return on_platform

    def _has_hit_right(self, sprite: Sprite) -> bool:
        return self._moving_right() and self.coords.collided_right(sprite.coords)

    def _has_hit_left(self, sprite: Sprite) -> bool:
        return self._moving_left() and self.coords.collided_left(sprite.coords)

    def _has_hit_top(self, sprite: Sprite) -> bool:
        return self._moving_up() and self.coords.collided_top(sprite.coords)

    def _will_hit_bottom(self, sprite: Sprite) -> bool:
        return self._moving_down() and self.coords.collided_bottom(sprite.coords, self._dy)


class DoorSprite(Sprite):
    def __init__(self,
                 canvas: tk.Canvas,
                 x: int, y: int,
                 width: int = 0, height: int = 0):
        super().__init__(canvas)

        self._closed_door = tk.PhotoImage(file=image_path("door1.png"))
        self._open_door = tk.PhotoImage(file=image_path("door2.png"))

        if width == 0:
            width = self._closed_door.width()
        if height == 0:
            height = self._closed_door.height()

        self._canvas_image = canvas.create_image(x, y, image=self._closed_door, anchor="nw")
        self._coordinates = Coords(Point(x, y), Point(x + int(width / 2), y + int(height / 2)))
        self._is_open = False
        self._endgame = True

    def tick(self) -> None:
        pass

    def open(self):
        self._is_open = True
        self._canvas.itemconfig(self._canvas_image, image=self._open_door)
        
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
        self._dx = -2
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
        state = StickFigureSprite.TickState(self.coords, self)
        for sprite in self._sprites:
            state.check_collision_with(sprite)

        self._canvas.move(self._canvas_image, self._dx, self._dy)
        self._coordinates.move(self._dx, self._dy)

    def _update_jump_state(self):
        if self._dy < 0:
            self._jump_count += 1
            if self._jump_count > 20:
                self._dy = 4
        if self._dy > 0:
            self._jump_count -= 1

    class TickState:
        def __init__(self, coords: Coords, sm: StickFigureSprite) -> None:
            self.co = coords
            self.sm = sm
            self.hit_left = self._has_hit_left_canvas(coords)
            self.hit_right = self._has_hit_right_canvas(coords)
            self.hit_top = self._has_hit_top_canvas(coords)
            self.hit_bottom = self._has_hit_bottom_canvas(coords)
            self.maybe_falling = True

        def check_collision_with(self, sprite: Sprite):
            if sprite == self.sm:
                return
            sprite_co = sprite.coords
            if not self.hit_top and self._will_hit_top(sprite_co):
                self.sm._dy = -self.sm._dy
                self.hit_top = True
            if not self.hit_bottom and self._will_hit_bottom(sprite_co):
                self.sm._dy = sprite_co.top - self.co.bottom
                if self.sm._dy < 0:
                    self.sm._dy = 0
                self.hit_bottom = True
                self.hit_top = True
            if (not self.hit_bottom and self.maybe_falling and self.sm._dy == 0 and
                    self.co.bottom < self.sm._canvas_height and
                    self.co.collided_bottom(sprite_co, 1)):
                self.maybe_falling = False
            if not self.hit_left and self._will_hit_left(sprite_co):
                self.sm._dx = 0
                self.hit_left = True
                if sprite.endgame:
                    self.sm._endgame = True
            if not self.hit_right and self._will_hit_right(sprite_co):
                self.sm._dx = 0
                self.hit_right = True
                if sprite.endgame:
                    self.sm._endgame = True
            if self.maybe_falling and not self.hit_bottom and self.sm._dy == 0 and self.co.bottom < self.sm._canvas_height:
                self.sm._dy = 4

        def _has_hit_bottom_canvas(self, co: Coords) -> bool:
            if self.sm._dy > 0 and co.bottom > self.sm._canvas_height:
                self.sm._dy = 0
                return True
            return False

        def _has_hit_top_canvas(self, co: Coords) -> bool:
            if self.sm._dy < 0 and co.top <= 0:
                self.sm._dy = 0
                return True
            return False

        def _has_hit_left_canvas(self, co: Coords) -> bool:
            if self.sm._dx < 0 and co.left <= 0:
                self.sm._dx = 0
                return True
            return False

        def _has_hit_right_canvas(self, co: Coords) -> bool:
            if self.sm._dx > 0 and co.right >= self.sm._canvas_width:
                self.sm._dx = 0
                return True
            return False

        def _will_hit_right(self, sprite_co: Coords) -> bool:
            return self.sm._dx > 0 and self.co.collided_right(sprite_co)

        def _will_hit_left(self, sprite_co: Coords) -> bool:
            return self.sm._dx < 0 and self.co.collided_left(sprite_co)

        def _will_hit_top(self, sprite_co: Coords) -> bool:
            return self.sm._dy < 0 and self.co.collided_top(sprite_co)

        def _will_hit_bottom(self, sprite_co: Coords) -> bool:
            return self.sm._dy > 0 and self.co.collided_bottom(sprite_co, self.sm._dy)


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
        
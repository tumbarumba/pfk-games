from __future__ import annotations
import time
import tkinter as tk

from pfk_games.stickman.hitbox import HitBox, Point
from pfk_games.stickman.images import image_path

TERMINAL_VELOCITY: int = 6


class Sprite:
    def __init__(self, canvas: tk.Canvas, hitbox: HitBox = HitBox()) -> None:
        self._canvas = canvas
        self._canvas_width: int = canvas.winfo_width()
        self._canvas_height: int = canvas.winfo_height()
        self._hitbox = hitbox
        self._endgame = False

    def tick(self) -> None:
        pass

    @property
    def hitbox(self) -> HitBox:
        return self._hitbox

    @property
    def endgame(self) -> bool:
        return self._endgame


class PlatformSprite(Sprite):
    @classmethod
    def _make_hitbox(cls, image: tk.PhotoImage, x: int, y: int, width: int, height: int) -> HitBox:
        if width == 0:
            width = image.width()
        if height == 0:
            height = image.height()
        return HitBox(Point(x, y), Point(x + width, y + height))

    def __init__(self,
                 canvas: tk.Canvas,
                 source_image: tk.PhotoImage,
                 x: int, y: int,
                 width: int = 0, height: int = 0) -> None:
        super().__init__(canvas, PlatformSprite._make_hitbox(source_image, x, y, width, height))
        self._source_image = source_image
        self._canvas_image = canvas.create_image(x, y, image=source_image, anchor="nw")




class ImageSequence:
    @classmethod
    def make_sequence(cls) -> ImageSequence:
        l1 = tk.PhotoImage(file=image_path("figure-l1.png")),
        l2 = tk.PhotoImage(file=image_path("figure-l2.png")),
        l3 = tk.PhotoImage(file=image_path("figure-l3.png"))
        left_seq = [l1, l2, l3, l2]

        r1 = tk.PhotoImage(file=image_path("figure-r1.png")),
        r2 = tk.PhotoImage(file=image_path("figure-r2.png")),
        r3 = tk.PhotoImage(file=image_path("figure-r3.png"))
        right_seq = [r1, r2, r3, r2]

        return ImageSequence(left_seq, l3, right_seq, r3)

    def __init__(self,
                 left_seq: list[tk.PhotoImage], left_jump: tk.PhotoImage,
                 right_seq: list[tk.PhotoImage], right_jump: tk.PhotoImage) -> None:
        self._left_seq = left_seq
        self._left_jump = left_jump
        self._right_seq = right_seq
        self._right_jump = right_jump
        self._index = 0

    def first(self, dx) -> tk.PhotoImage:
        if dx < 0:
            return self._left_seq[0]
        else:
            return self._right_seq[0]

    def next(self, dx) -> tk.PhotoImage:
        self._index = (self._index + 1) % len(self._left_seq)
        if dx < 0:
            return self._left_seq[self._index]
        else:
            return self._right_seq[self._index]

    def jumping(self, dx) -> tk.PhotoImage:
        if dx < 0:
            return self._left_jump
        else:
            return self._right_jump

class StickFigureSprite(Sprite):
    @classmethod
    def _make_hitbox(cls) -> HitBox:
        top_left = Point(200, 470)
        bottom_right = Point(top_left.x + 27, top_left.y + 30)
        return HitBox(top_left, bottom_right)

    def __init__(self, canvas: tk.Canvas, sprites: list[Sprite]) -> None:
        super().__init__(canvas, StickFigureSprite._make_hitbox())
        self._sprites = sprites
        self._image_seq = ImageSequence.make_sequence()
        self._current_image = self._image_seq.first(0)
        self._canvas_image = canvas.create_image(
            self.hitbox.top_left.x,
            self.hitbox.top_left.y,
            image=self._current_image,
            anchor="nw")
        self._dx = 0
        self._dy = 0
        self._jumping = False
        self._animation_time = time.time()
        self._gravity_time = time.time()

    def turn_left(self) -> None:
        if not self._jumping:
            self._dx = -2

    def turn_right(self) -> None:
        if not self._jumping:
            self._dx = 2

    def jump(self) -> None:
        if not self._jumping:
            self._jumping = True
            self._gravity_time = time.time()
            self._dy = -5
            self._current_image = self._image_seq.jumping(self._dx)

    def tick(self) -> None:
        self._animate()
        self._update_coordinates()
        self._canvas.moveto(self._canvas_image, self.hitbox.top_left.x, self.hitbox.top_left.y)

    def _animate(self) -> None:
        self._cycle_current_image()
        self._canvas.itemconfig(self._canvas_image, image=self._current_image)

    def _cycle_current_image(self):
        if self._dx != 0 and not self._jumping:
            now = time.time()
            if now - self._animation_time > 0.1:
                self._animation_time = now
                self._current_image = self._image_seq.next(self._dx)

    def _update_coordinates(self):
        if self._jumping:
            self._acceleration_due_to_gravity()
        self._check_if_on_platform()
        self._keep_on_canvas()
        for sprite in self._sprites:
            self._check_collision(sprite)
        self._hitbox = self._hitbox.move(self._dx, self._dy)

    def _acceleration_due_to_gravity(self) -> None:
        now = time.time()
        if now - self._gravity_time > 0.05:
            self._dy = min(TERMINAL_VELOCITY, self._dy + 1)
            self._gravity_time = now

    def _moving_left(self) -> bool:
        return self._dx < 0

    def _moving_right(self) -> bool:
        return self._dx > 0

    def _moving_up(self) -> bool:
        return self._dy < 0

    def _moving_down(self) -> bool:
        return self._dy > 0

    def _stop_horizontal(self) -> None:
        self._current_image = self._image_seq.first(self._dx)
        self._dx = 0

    def _stop_vertical(self) -> None:
        self._dy = 0

    def _keep_on_canvas(self) -> None:
        self._check_left_edge()
        self._check_right_edge()
        self._check_top_edge()
        self._check_bottom_edge()

    def _check_bottom_edge(self) -> None:
        if self._moving_down() and self.hitbox.bottom >= self._canvas_height:
            self._stop_vertical()
            self._jumping = False

    def _check_top_edge(self) -> None:
        if self._moving_up() and self.hitbox.top <= 0:
            self._stop_vertical()

    def _check_left_edge(self) -> None:
        if self._moving_left() and self.hitbox.left <= 0:
            self._stop_horizontal()

    def _check_right_edge(self) -> None:
        if self._moving_right() and self.hitbox.right >= self._canvas_width:
            self._stop_horizontal()

    def _check_if_on_platform(self) -> None:
        if self.hitbox.bottom >= self._canvas_height:
            # Bottom of screen
            self._jumping = False
            return

        for sprite in self._sprites:
            if isinstance(sprite, PlatformSprite):
                if self.hitbox.collided_bottom(sprite.hitbox, 1):
                    # We're on this platform
                    self._jumping = False
                    return

        # No longer on platform, start falling
        self._jumping = True

    def _has_hit_right(self, sprite: Sprite) -> bool:
        return self._moving_right() and self.hitbox.collided_right(sprite.hitbox)

    def _has_hit_left(self, sprite: Sprite) -> bool:
        return self._moving_left() and self.hitbox.collided_left(sprite.hitbox)

    def _has_hit_top(self, sprite: Sprite) -> bool:
        return self._moving_up() and self.hitbox.collided_top(sprite.hitbox)

    def _will_hit_bottom(self, sprite: Sprite) -> bool:
        return self._moving_down() and self.hitbox.collided_bottom(sprite.hitbox, self._dy)

    def _check_collision(self, sprite: Sprite) -> None:
        if sprite == self:
            return
        if self._will_hit_bottom(sprite):
            self._dy = max(0, sprite.hitbox.top - self.hitbox.bottom)
        elif (self._moving_down() and
                self.hitbox.bottom < self._canvas_height and
                self.hitbox.collided_bottom(sprite.hitbox, 1)):
            self._jumping = False
            self._stop_vertical()
        if self._has_hit_top(sprite):
            self._dy = -self._dy
        elif self._has_hit_left(sprite):
            self._stop_horizontal()
            if sprite.endgame:
                self._endgame = True
        elif self._has_hit_right(sprite):
            self._stop_horizontal()
            if sprite.endgame:
                self._endgame = True


class DoorSprite(Sprite):
    @classmethod
    def _make_hitbox(cls, x: int, y: int, width: int, height: int) -> HitBox:
        return HitBox(Point(x, y), Point(x + int(width / 2), y + int(height / 2)))

    def __init__(self, canvas: tk.Canvas, x: int, y: int, width: int, height: int):
        super().__init__(canvas, DoorSprite._make_hitbox(x, y, width, height))
        self._closed_door = tk.PhotoImage(file=image_path("door1.png"))
        self._open_door = tk.PhotoImage(file=image_path("door2.png"))
        self._canvas_image = canvas.create_image(x, y, image=self._closed_door, anchor="nw")
        self._is_open = False
        self._endgame = True

    def tick(self) -> None:
        pass

    def open(self):
        self._is_open = True
        self._canvas.itemconfig(self._canvas_image, image=self._open_door)
        
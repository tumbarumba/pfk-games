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


def _hitbox_from(image: tk.PhotoImage, x: int, y: int, width: int, height: int) -> HitBox:
    if width == 0:
        width = image.width()
    if height == 0:
        height = image.height()
    return HitBox(Point(x, y), Point(x + width, y + height))


class PlatformSprite(Sprite):
    def __init__(self,
                 canvas: tk.Canvas,
                 source_image: tk.PhotoImage,
                 x: int, y: int,
                 width: int = 0, height: int = 0) -> None:
        super().__init__(canvas, _hitbox_from(source_image, x, y, width, height))
        self._source_image = source_image
        self._canvas_image = canvas.create_image(x, y, image=source_image, anchor="nw")




class ImageSequence:
    @classmethod
    def left_sequence(cls) -> ImageSequence:
        image1 = tk.PhotoImage(file=image_path("figure-l1.png")),
        image2 = tk.PhotoImage(file=image_path("figure-l2.png")),
        image3 = tk.PhotoImage(file=image_path("figure-l3.png"))
        return ImageSequence([image1, image2, image3, image2], jumping=image3)

    @classmethod
    def right_sequence(cls) -> ImageSequence:
        image1 = tk.PhotoImage(file=image_path("figure-r1.png")),
        image2 = tk.PhotoImage(file=image_path("figure-r2.png")),
        image3 = tk.PhotoImage(file=image_path("figure-r3.png"))
        return ImageSequence([image1, image2, image3, image2], jumping=image3)

    def __init__(self, images: list[tk.PhotoImage], jumping: tk.PhotoImage) -> None:
        self._images = images
        self._index = 0
        self._jumping = jumping

    def first(self) -> tk.PhotoImage:
        return self._images[0]

    def next(self) -> tk.PhotoImage:
        self._index = (self._index + 1) % len(self._images)
        return self._images[self._index]

    def jumping(self) -> tk.PhotoImage:
        return self._jumping

class StickFigureSprite(Sprite):
    @classmethod
    def _make_hitbox(cls) -> HitBox:
        top_left = Point(200, 470)
        bottom_right = Point(top_left.x + 27, top_left.y + 30)
        return HitBox(top_left, bottom_right)

    def __init__(self, canvas: tk.Canvas, sprites: list[Sprite]) -> None:
        super().__init__(canvas, StickFigureSprite._make_hitbox())
        self._sprites = sprites
        self._left_seq = ImageSequence.left_sequence()
        self._right_seq = ImageSequence.right_sequence()
        self._current_image = self._left_seq.first()
        self._canvas_image = canvas.create_image(
            self.hitbox.top_left.x,
            self.hitbox.top_left.y,
            image=self._current_image,
            anchor="nw")
        self._dx = 0
        self._dy = 0
        self._current_index = 0
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
            if self._moving_left():
                self._current_image = self._left_seq.jumping()
            else:
                self._current_image = self._right_seq.jumping()

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
                if self._moving_left():
                    self._current_image = self._left_seq.next()
                else:
                    self._current_image = self._right_seq.next()

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

    def _moving_right(self):
        return self._dx > 0

    def _moving_up(self) -> bool:
        return self._dy < 0

    def _moving_down(self) -> bool:
        return self._dy > 0

    def _stop_horizontal(self) -> None:
        if self._moving_left():
            self._current_image = self._left_seq.first()
        else:
            self._current_image = self._right_seq.first()
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


def _door_hitbox(x: int, y: int, width: int, height: int) -> HitBox:
    return HitBox(Point(x, y), Point(x + int(width / 2), y + int(height / 2)))


class DoorSprite(Sprite):
    def __init__(self, canvas: tk.Canvas, x: int, y: int, width: int, height: int):
        super().__init__(canvas, _door_hitbox(x, y, width, height))
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
        
from __future__ import annotations
import time
import tkinter as tk

from pfk_games.stickman.sprite.hitbox import HitBox, Point
from pfk_games.stickman.images import image_path
from pfk_games.stickman.sprite import Sprite
from pfk_games.stickman.sprite.platform import PlatformSprite

TERMINAL_VELOCITY: int = 6


class ImageSequence:
    @classmethod
    def facing_left(cls) -> ImageSequence:
        l1 = tk.PhotoImage(file=image_path("figure-l1.png")),
        l2 = tk.PhotoImage(file=image_path("figure-l2.png")),
        l3 = tk.PhotoImage(file=image_path("figure-l3.png"))
        left_seq = [l1, l2, l3, l2]
        return ImageSequence(left_seq, l3)

    @classmethod
    def facing_right(cls) -> ImageSequence:
        r1 = tk.PhotoImage(file=image_path("figure-r1.png")),
        r2 = tk.PhotoImage(file=image_path("figure-r2.png")),
        r3 = tk.PhotoImage(file=image_path("figure-r3.png"))
        right_seq = [r1, r2, r3, r2]
        return ImageSequence(right_seq, r3)

    def __init__(self, images: list[tk.PhotoImage], jump: tk.PhotoImage) -> None:
        self._images = images
        self._jump = jump
        self._index = 0

    def first(self) -> tk.PhotoImage:
        return self._images[0]

    def next(self) -> tk.PhotoImage:
        self._index = (self._index + 1) % len(self._images)
        return self._images[self._index]

    def jumping(self) -> tk.PhotoImage:
        return self._jump

class StickManSprite(Sprite):
    @classmethod
    def _make_hitbox(cls) -> HitBox:
        top_left = Point(200, 470)
        bottom_right = Point(top_left.x + 27, top_left.y + 30)
        return HitBox(top_left, bottom_right)

    def __init__(self, canvas: tk.Canvas, sprites: list[Sprite]) -> None:
        super().__init__(canvas, StickManSprite._make_hitbox())
        self._sprites = sprites
        self._left_seq = ImageSequence.facing_left()
        self._right_seq = ImageSequence.facing_right()
        self._image_seq = self._left_seq
        self._current_image = self._image_seq.first()
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
            self._image_seq = self._left_seq

    def turn_right(self) -> None:
        if not self._jumping:
            self._dx = 2
            self._image_seq = self._right_seq

    def jump(self) -> None:
        if not self._jumping:
            self._jumping = True
            self._gravity_time = time.time()
            self._dy = -5
            self._current_image = self._image_seq.jumping()

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
                self._current_image = self._image_seq.next()

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
        self._current_image = self._image_seq.first()
        self._dx = 0

    def _stop_vertical(self) -> None:
        self._dy = 0

    def _keep_on_canvas(self) -> None:
        self._check_left_limit()
        self._check_right_limit()
        self._check_top_limit()
        self._check_bottom_limit()

    def _check_bottom_limit(self) -> None:
        if self._moving_down():
            if self.hitbox.bottom >= self._canvas_height:
                self._stop_vertical()
                self._jumping = False
            elif self.hitbox.bottom + self._dy >= self._canvas_height:
                self._dy = self._canvas_height - self.hitbox.bottom

    def _check_top_limit(self) -> None:
        if self._moving_up() and self.hitbox.top <= 0:
            self._stop_vertical()

    def _check_left_limit(self) -> None:
        if self._moving_left() and self.hitbox.left <= 0:
            self._stop_horizontal()

    def _check_right_limit(self) -> None:
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

    def _right_has_hit(self, sprite: Sprite) -> bool:
        return self._moving_right() and self.hitbox.collided_right(sprite.hitbox)

    def _left_has_hit(self, sprite: Sprite) -> bool:
        return self._moving_left() and self.hitbox.collided_left(sprite.hitbox)

    def _top_has_hit(self, sprite: Sprite) -> bool:
        return self._moving_up() and self.hitbox.collided_top(sprite.hitbox)

    def _bottom_will_hit(self, sprite: Sprite) -> bool:
        return self._moving_down() and self.hitbox.collided_bottom(sprite.hitbox, self._dy)

    def _bottom_has_hit(self, sprite: Sprite) -> bool:
        return self._moving_down() and self.hitbox.collided_bottom(sprite.hitbox, 1)

    def _check_collision(self, sprite: Sprite) -> None:
        if sprite == self:
            return

        # Falling onto platform
        if self._bottom_will_hit(sprite):
            self._dy = max(0, sprite.hitbox.top - self.hitbox.bottom)
        elif self._bottom_has_hit(sprite):
            self._jumping = False
            self._stop_vertical()

        if self._top_has_hit(sprite):
            # Bounce
            self._dy = -self._dy
        elif self._left_has_hit(sprite):
            self._stop_horizontal()
            sprite.handle_collision()
        elif self._right_has_hit(sprite):
            self._stop_horizontal()
            sprite.handle_collision()



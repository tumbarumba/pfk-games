import tkinter as tk

from pfk_games.stickman.sprite.hitbox import HitBox


class Sprite:
    def __init__(self, canvas: tk.Canvas, hitbox: HitBox = HitBox()) -> None:
        self._canvas = canvas
        self._canvas_width: int = canvas.winfo_width()
        self._canvas_height: int = canvas.winfo_height()
        self._hitbox = hitbox
        self._dx = 0
        self._dy = 0

    def tick(self) -> None:
        pass

    def start(self) -> None:
        pass

    def handle_collision(self) -> None:
        pass

    @property
    def hitbox(self) -> HitBox:
        return self._hitbox

    def _moving_left(self) -> bool:
        return self._dx < 0

    def _moving_right(self) -> bool:
        return self._dx > 0

    def _moving_up(self) -> bool:
        return self._dy < 0

    def _moving_down(self) -> bool:
        return self._dy > 0


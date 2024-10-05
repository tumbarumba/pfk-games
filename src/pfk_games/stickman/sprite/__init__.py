import tkinter as tk

from pfk_games.stickman.sprite.hitbox import HitBox


class Sprite:
    def __init__(self, canvas: tk.Canvas, hitbox: HitBox = HitBox()) -> None:
        self._canvas = canvas
        self._canvas_width: int = canvas.winfo_width()
        self._canvas_height: int = canvas.winfo_height()
        self._hitbox = hitbox

    def tick(self) -> None:
        pass

    def handle_collision(self) -> None:
        pass

    @property
    def hitbox(self) -> HitBox:
        return self._hitbox

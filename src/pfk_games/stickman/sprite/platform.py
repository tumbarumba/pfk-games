from __future__ import annotations

import tkinter as tk

from pfk_games.stickman.sprite.hitbox import HitBox, Point
from pfk_games.stickman.sprite import Sprite


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

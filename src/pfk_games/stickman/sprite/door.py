from __future__ import annotations

import tkinter as tk

from pfk_games.stickman.sprite.hitbox import HitBox, Point
from pfk_games.stickman.images import image_path
from pfk_games.stickman.sprite import Sprite


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

    def handle_collision(self):
        self._is_open = True
        self._canvas.itemconfig(self._canvas_image, image=self._open_door)

    @property
    def is_open(self) -> bool:
        return self._is_open

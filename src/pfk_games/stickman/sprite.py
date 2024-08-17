import tkinter as tk
from typing import Any

from pfk_games.stickman.coords import Coords


class Sprite:
    def __init__(self, game: Any) -> None:
        self.game = game
        self.endgame = False
        self.coordinates = None

    def move(self):
        pass

    def coords(self):
        return self.coordinates


class PlatformSprite(Sprite):
    def __init__(self,
                 game: Any,
                 source_image: tk.PhotoImage,
                 x: int, y: int,
                 width: int = 0, height: int = 0) -> None:
        super().__init__(game)

        if width == 0:
            width = source_image.width()
        if height == 0:
            height = source_image.height()

        self.source_image = source_image
        self.image = game.canvas.create_image(x, y, image=source_image, anchor="nw")
        self.coordinates = Coords(x, y, x + width, y + height)

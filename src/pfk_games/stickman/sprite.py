import tkinter as tk

from pfk_games.stickman.coords import Coords
from pfk_games.stickman.stickman import StickMan


class Sprite:
    def __init__(self, game: StickMan) -> None:
        self.game = game
        self.endgame = False
        self.coordinates = None

    def move(self):
        pass

    def coords(self):
        return self.coordinates


class PlatformSprite(Sprite):
    def __init__(self,
                 game: StickMan,
                 source_image: tk.PhotoImage,
                 x: int, y: int,
                 width: int, height: int) -> None:
        super().__init__(game)
        self.source_image = source_image
        self.image = game.canvas.create_image(x, y, image=source_image, anchor="nw")
        self.coordinates = Coords(x, y, x + width, y + height)

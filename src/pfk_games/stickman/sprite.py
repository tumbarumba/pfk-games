import time
import tkinter as tk

from pfk_games.stickman.coords import Coords
from pfk_games.stickman.images import image_path


class Sprite:
    def __init__(self, canvas: tk.Canvas) -> None:
        self.canvas = canvas
        self.endgame = False
        self.coordinates = None

    def move(self):
        pass

    def coords(self):
        return self.coordinates


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

        self.source_image = source_image
        self.image = canvas.create_image(x, y, image=source_image, anchor="nw")
        self.coordinates = Coords(x, y, x + width, y + height)

class StickFigureSprite(Sprite):
    def __init__(self, canvas: tk.Canvas) -> None:
        super().__init__(canvas)
        self.images_left = [
            tk.PhotoImage(file=image_path("figure-l1.png")),
            tk.PhotoImage(file=image_path("figure-l2.png")),
            tk.PhotoImage(file=image_path("figure-l3.png"))
        ]
        self.images_right = [
            tk.PhotoImage(file=image_path("figure-r1.png")),
            tk.PhotoImage(file=image_path("figure-r2.png")),
            tk.PhotoImage(file=image_path("figure-r3.png"))
        ]
        self.image = canvas.create_image(200, 470, image=self.images_left[0], anchor="nw")
        self.x = -2
        self.y = 0
        self.current_image = 0
        self.current_image_add = 1
        self.jump_count = 0
        self.last_time = time.time()
        self.coordinates = Coords()

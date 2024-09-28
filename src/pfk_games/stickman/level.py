import tkinter as tk
from abc import ABC, abstractmethod

from pfk_games.stickman.images import image_path
from pfk_games.stickman.sprite import Sprite, DoorSprite, StickFigureSprite, PlatformSprite


class Level(ABC):
    @abstractmethod
    def on_left(self) -> None:
        pass

    @abstractmethod
    def on_right(self) -> None:
        pass

    @abstractmethod
    def on_space(self) -> None:
        pass

    @abstractmethod
    def tick(self) -> None:
        pass

    @property
    @abstractmethod
    def complete(self) -> bool:
        pass


class Level1(Level):
    def __init__(self, canvas: tk.Canvas) -> None:
        self._canvas = canvas

        self._add_background()

        self._sprites: list[Sprite] = []
        self._door = DoorSprite(self._canvas, 45, 30, 40, 35)
        self._stick_man = StickFigureSprite(self._canvas, self._sprites)
        self._sprites.extend(self._make_sprites())
        self._sprites.extend([self._door, self._stick_man])
        self._complete = False

    def on_left(self):
        self._stick_man.turn_left()

    def on_right(self):
        self._stick_man.turn_right()

    def on_space(self):
        self._stick_man.jump()

    def tick(self):
        for sprite in self._sprites:
            sprite.tick()
        if self._stick_man.endgame:
            self._complete = True
            self._door.open()

    @property
    def complete(self) -> bool:
        return self._complete

    def _add_background(self) -> None:
        self._bg_image = tk.PhotoImage(file=image_path("background1.png"))
        w = self._bg_image.width()
        h = self._bg_image.height()
        for x in range(0, 5):
            for y in range(0, 5):
                self._canvas.create_image(x * w, y * h, image=self._bg_image, anchor="nw")

    def _make_sprites(self) -> list[Sprite]:
        sprites: list[Sprite] = []

        p1 = tk.PhotoImage(file=image_path("platform1.png"))
        sprites.append(PlatformSprite(self._canvas, p1, 0, 480))
        sprites.append(PlatformSprite(self._canvas, p1, 150, 440))
        sprites.append(PlatformSprite(self._canvas, p1, 300, 400))
        sprites.append(PlatformSprite(self._canvas, p1, 300, 160))

        p2 = tk.PhotoImage(file=image_path("platform2.png"))
        sprites.append(PlatformSprite(self._canvas, p2, 175, 350))
        sprites.append(PlatformSprite(self._canvas, p2, 50, 300))
        sprites.append(PlatformSprite(self._canvas, p2, 170, 120))
        sprites.append(PlatformSprite(self._canvas, p2, 45, 60))

        p3 = tk.PhotoImage(file=image_path("platform3.png"))
        sprites.append(PlatformSprite(self._canvas, p3, 170, 250))
        sprites.append(PlatformSprite(self._canvas, p3, 230, 200))

        return sprites

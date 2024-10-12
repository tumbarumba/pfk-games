import tkinter as tk
from abc import ABC, abstractmethod

from pfk_games.stickman.images import image_path
from pfk_games.stickman.sprite import Sprite
from pfk_games.stickman.sprite.door import DoorSprite
from pfk_games.stickman.sprite.platform import PlatformSprite, MovingPlatformSprite
from pfk_games.stickman.sprite.stickman import StickManSprite


class Level(ABC):
    def __init__(self, canvas: tk.Canvas, bg_path: str) -> None:
        self._canvas = canvas
        self._bg_image = self._set_background(bg_path)
        self._sprites = self._make_platforms()
        self._stick_man = StickManSprite(self._canvas, self._sprites)
        self._door = self._make_door()
        self._sprites.extend([self._door, self._stick_man])
        self._started = False
        self._complete = False

    def start(self) -> None:
        self._started = True
        for sprite in self._sprites:
            sprite.start()

    def on_left(self):
        self._stick_man.turn_left()

    def on_right(self):
        self._stick_man.turn_right()

    def on_space(self):
        self._stick_man.jump()

    def tick(self):
        if self._started and not self._complete:
            for sprite in self._sprites:
                sprite.tick()
            if self._door.is_open:
                self._complete = True

    def _set_background(self, bg_path: str) -> tk.PhotoImage:
        bg_image = tk.PhotoImage(file=bg_path)
        w = bg_image.width()
        h = bg_image.height()
        for x in range(0, 5):
            for y in range(0, 5):
                self._canvas.create_image(x * w, y * h, image=bg_image, anchor="nw")
        return bg_image

    @property
    def started(self) -> bool:
        return self._started

    @property
    def complete(self) -> bool:
        return self._complete

    @abstractmethod
    def _make_door(self) -> DoorSprite:
        pass

    @abstractmethod
    def _make_platforms(self) -> list[Sprite]:
        pass

class Level1(Level):
    def __init__(self, canvas: tk.Canvas) -> None:
        super().__init__(canvas, image_path("background1.png"))

    def _make_door(self) -> DoorSprite:
        return DoorSprite(self._canvas, 65, 30, 40, 35)

    def _make_platforms(self) -> list[Sprite]:
        long_platform = tk.PhotoImage(file=image_path("platform1.png"))
        medium_platform = tk.PhotoImage(file=image_path("platform2.png"))
        short_platform = tk.PhotoImage(file=image_path("platform3.png"))

        return [
            PlatformSprite(self._canvas, medium_platform, 65, 60),
            PlatformSprite(self._canvas, medium_platform, 190, 120),
            PlatformSprite(self._canvas, long_platform, 320, 160),
            PlatformSprite(self._canvas, short_platform, 250, 200),
            PlatformSprite(self._canvas, short_platform, 170, 250),
            PlatformSprite(self._canvas, medium_platform, 50, 300),
            PlatformSprite(self._canvas, medium_platform, 175, 350),
            PlatformSprite(self._canvas, long_platform, 300, 400),
            PlatformSprite(self._canvas, long_platform, 150, 440),
            PlatformSprite(self._canvas, long_platform, 0, 480),
        ]


class Level2(Level):
    def __init__(self, canvas: tk.Canvas) -> None:
        super().__init__(canvas, image_path("background2.png"))

    def _make_door(self) -> DoorSprite:
        return DoorSprite(self._canvas, 45, 30, 40, 35)

    def _make_platforms(self) -> list[Sprite]:
        long_platform = tk.PhotoImage(file=image_path("platform1.png"))
        medium_platform = tk.PhotoImage(file=image_path("platform2.png"))
        short_platform = tk.PhotoImage(file=image_path("platform3.png"))

        return [
            PlatformSprite(self._canvas, medium_platform, 45, 60),
            MovingPlatformSprite(self._canvas, long_platform, 400, 110),
            PlatformSprite(self._canvas, medium_platform, 190, 170),
            PlatformSprite(self._canvas, long_platform, 320, 210),
            PlatformSprite(self._canvas, short_platform, 250, 250),
            PlatformSprite(self._canvas, short_platform, 170, 300),
            PlatformSprite(self._canvas, medium_platform, 50, 340),
            PlatformSprite(self._canvas, medium_platform, 175, 380),
            PlatformSprite(self._canvas, long_platform, 300, 420),
            MovingPlatformSprite(self._canvas, long_platform, 0, 460)
        ]

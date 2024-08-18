import time
import tkinter as tk

from pfk_games.stickman.images import image_path
from pfk_games.stickman.sprite import PlatformSprite, StickFigureSprite, Sprite, DoorSprite

TICK_DURATION = 0.01


class StickMan:
    def __init__(self) -> None:
        self._root = tk.Tk()
        self._root.title("Mr. Stick Man Races for the Exit")
        self._root.resizable(False, False)
        self._root.wm_attributes("-topmost", 1)
        self._root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.window_closed = False

        self._canvas = tk.Canvas(self._root, width=500, height=500, bd=0, highlightthickness=0)
        self._canvas.pack()
        self._root.update()
        self._canvas_height = 500
        self._canvas_width = 500
        self._running = True

        self._sprites: list[Sprite] = []

        self._bg_image = tk.PhotoImage(file=image_path("background.png"))
        self._add_background()

        self._door = DoorSprite(self._canvas, 45, 30, 40, 35)
        self._stick_man = StickFigureSprite(self._canvas, self._sprites)
        self._add_sprites()

        self._bind_keys()

    def _add_background(self) -> None:
        w = self._bg_image.width()
        h = self._bg_image.height()
        for x in range(0, 5):
            for y in range(0, 5):
                self._canvas.create_image(x * w, y * h, image=self._bg_image, anchor="nw")

    def _add_sprites(self) -> None:
        p1 = tk.PhotoImage(file=image_path("platform1.png"))
        self._sprites.append(PlatformSprite(self._canvas, p1, 0, 480))
        self._sprites.append(PlatformSprite(self._canvas, p1, 150, 440))
        self._sprites.append(PlatformSprite(self._canvas, p1, 300, 400))
        self._sprites.append(PlatformSprite(self._canvas, p1, 300, 160))

        p2 = tk.PhotoImage(file=image_path("platform2.png"))
        self._sprites.append(PlatformSprite(self._canvas, p2, 175, 350))
        self._sprites.append(PlatformSprite(self._canvas, p2, 50, 300))
        self._sprites.append(PlatformSprite(self._canvas, p2, 170, 120))
        self._sprites.append(PlatformSprite(self._canvas, p2, 45, 60))

        p3 = tk.PhotoImage(file=image_path("platform3.png"))
        self._sprites.append(PlatformSprite(self._canvas, p3, 170, 250))
        self._sprites.append(PlatformSprite(self._canvas, p3, 230, 200))

        self._sprites.append(self._door)
        self._sprites.append(self._stick_man)

    def _bind_keys(self) -> None:
        self._canvas.bind_all("<KeyPress-Left>", self.on_left)
        self._canvas.bind_all("<KeyPress-Right>", self.on_right)
        self._canvas.bind_all("<space>", self.on_space)

    def on_left(self, _):
        self._stick_man.turn_left()

    def on_right(self, _):
        self._stick_man.turn_right()

    def on_space(self, _):
        self._stick_man.jump()

    def on_close(self) -> None:
        self.window_closed = True

    def tick(self) -> None:
        if self._running:
            for sprite in self._sprites:
                sprite.tick()
            if self._stick_man.endgame:
                self._running = False
                self._door.open()
        self._root.update_idletasks()
        self._root.update()

    def mainloop(self) -> None:
        while True:
            if self.window_closed:
                break
            self.tick()
            time.sleep(TICK_DURATION)

        self._root.destroy()

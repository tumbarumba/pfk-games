import time
import tkinter as tk

from pfk_games.stickman.images import image_path
from pfk_games.stickman.sprite import PlatformSprite

TICK_DURATION = 0.01


class StickMan:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Mr. Stick Man Races for the Exit")
        self.root.resizable(False, False)
        self.root.wm_attributes("-topmost", 1)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.window_closed = False

        self.canvas = tk.Canvas(self.root, width=500, height=500, bd=0, highlightthickness=0)
        self.canvas.pack()
        self.root.update()
        self.canvas_height = 500
        self.canvas_width = 500

        self.bg = tk.PhotoImage(file=image_path("background.png"))
        self.sprites = []
        self.running = True

        self._add_background()
        self._add_platforms()


    def _add_background(self) -> None:
        w = self.bg.width()
        h = self.bg.height()
        for x in range(0, 5):
            for y in range(0, 5):
                self.canvas.create_image(x * w, y * h, image=self.bg, anchor="nw")

    def _add_platforms(self) -> None:
        p1 = tk.PhotoImage(file=image_path("platform1.png"))
        self.sprites.append(PlatformSprite(self, p1, 0, 480))
        self.sprites.append(PlatformSprite(self, p1, 150, 440))
        self.sprites.append(PlatformSprite(self, p1, 300, 400))
        self.sprites.append(PlatformSprite(self, p1, 300, 160))

        p2 = tk.PhotoImage(file=image_path("platform2.png"))
        self.sprites.append(PlatformSprite(self, p2, 175, 350))
        self.sprites.append(PlatformSprite(self, p2, 50, 300))
        self.sprites.append(PlatformSprite(self, p2, 170, 120))
        self.sprites.append(PlatformSprite(self, p2, 45, 60))

        p3 = tk.PhotoImage(file=image_path("platform3.png"))
        self.sprites.append(PlatformSprite(self, p3, 170, 250))
        self.sprites.append(PlatformSprite(self, p3, 230, 200))

    def on_close(self) -> None:
        self.window_closed = True

    def tick(self):
        if self.running:
            for sprite in self.sprites:
                sprite.move()
        self.root.update_idletasks()
        self.root.update()

    def mainloop(self):
        while True:
            if self.window_closed:
                break
            self.tick()
            time.sleep(TICK_DURATION)

        self.root.destroy()

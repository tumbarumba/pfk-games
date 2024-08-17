import os
import time
import tkinter as tk

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

        this_dir = os.path.dirname(os.path.realpath(__file__))
        bg_path = os.path.join(this_dir, "images", "background.png")
        self.bg = tk.PhotoImage(file=bg_path)
        w = self.bg.width()
        h = self.bg.height()
        for x in range(0, 5):
            for y in range(0, 5):
                self.canvas.create_image(x * w, y * h, image=self.bg, anchor="nw")
        self.sprites = []
        self.running = True

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

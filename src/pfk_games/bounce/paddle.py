import tkinter as tk

START_X = 200
START_Y = 300


class Paddle:
    def __init__(self, canvas: tk.Canvas, color: str) -> None:
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas_width = self.canvas.winfo_width()
        self.x = 0
        self.reset()

    def reset(self) -> None:
        self.canvas.moveto(self.id, START_X, START_Y)
        self.x = 0

    def draw(self) -> None:
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 0
        elif pos[2] >= self.canvas_width:
            self.x = 0

    def turn_left(self) -> None:
        self.x = -2

    def turn_right(self) -> None:
        self.x = 2

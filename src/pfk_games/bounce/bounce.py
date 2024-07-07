import time
import tkinter as tk

from pfk_games.bounce.ball import Ball
from pfk_games.bounce.paddle import Paddle
from pfk_games.bounce.score import Score


class Bounce:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Bounce")
        self.root.resizable(False, False)
        self.root.wm_attributes("-topmost", 1)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.canvas = tk.Canvas(self.root, width=500, height=400, bd=0, highlightthickness=0)
        self.canvas.pack()
        self.root.update()

        self.score = Score(self.canvas, "green")
        self.paddle = Paddle(self.canvas, "blue")
        self.ball = Ball(self.canvas, self.score, self.paddle, "red")
        self.window_closed = False

    def on_close(self) -> None:
        self.window_closed = True

    def update_game(self):
        if not self.ball.hit_bottom:
            self.ball.draw()
            self.paddle.draw()
            self.score.draw()
        self.root.update_idletasks()
        self.root.update()

    def mainloop(self):
        while 1:
            if self.window_closed:
                break
            self.update_game()
            time.sleep(0.01)

        self.root.destroy()

import time
import tkinter as tk

from pfk_games.bounce.ball import Ball
from pfk_games.bounce.paddle import Paddle
from pfk_games.bounce.message import Message
from pfk_games.bounce.score import Score


class Bounce:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Bounce")
        self.root.resizable(False, False)
        self.root.wm_attributes("-topmost", 1)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.window_closed = False

        self.canvas = tk.Canvas(self.root, width=500, height=400, bd=0, highlightthickness=0)
        self.canvas.pack()
        self.root.update()

        self.canvas.bind_all("<space>", self.on_space)

        self.message = Message(self.canvas, "black", "")
        self.score = None
        self.paddle = None
        self.ball = None
        self.started = False
        self.game_over = False

        self.reset_game()

    def on_close(self) -> None:
        self.window_closed = True

    def reset_game(self):
        self.message.update("Press <space> to start")

        if self.score:
            self.canvas.delete(self.score.id)
        self.score = Score(self.canvas, "green")

        if self.paddle:
            self.canvas.delete(self.paddle.id)
        self.paddle = Paddle(self.canvas, "blue")

        if self.ball:
            self.canvas.delete(self.ball.id)
        self.ball = Ball(self.canvas, self.score, self.paddle, "red")

        self.started = False
        self.game_over = False

    def start_game(self):
        self.ball.start()
        self.started = True
        self.message.update("")

    def on_space(self, _) -> None:
        if self.game_over:
            self.reset_game()
        elif not self.started:
            self.start_game()

    def update_game(self):
        if self.ball.hit_bottom:
            if not self.game_over:
                self.message.update("Game Over\nPress <space> to reset")
                self.game_over = True
        else:
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

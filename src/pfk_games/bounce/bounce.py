import time
import tkinter as tk

from pfk_games.bounce.ball import Ball
from pfk_games.bounce.paddle import Paddle
from pfk_games.bounce.message import Message
from pfk_games.bounce.score import Score

TICK_DURATION = 0.01


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
        self.canvas.bind_all("<KeyPress-Left>", self.on_left)
        self.canvas.bind_all("<KeyPress-Right>", self.on_right)

        self.message = Message(self.canvas, "black", "")
        self.score = Score(self.canvas, "green")
        self.paddle = Paddle(self.canvas, "blue")
        self.ball = Ball(self.canvas, self.score, self.paddle, "red")
        self.started = False
        self.game_over = False

        self.reset_game()

    def on_close(self) -> None:
        self.window_closed = True

    def reset_game(self):
        self.message.update("Press <space> to start")
        self.score.reset()
        self.paddle.reset()
        self.ball.reset()
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

    def on_left(self, _) -> None:
        if self.started and not self.game_over:
            self.paddle.turn_left()

    def on_right(self, _) -> None:
        if self.started and not self.game_over:
            self.paddle.turn_right()

    def tick(self):
        if self.ball.hit_bottom:
            if not self.game_over:
                self.message.update("Game Over\nPress <space> to reset")
                self.game_over = True
        else:
            self.ball.tick()
            self.paddle.tick()
            self.score.tick()
        self.root.update_idletasks()
        self.root.update()

    def mainloop(self):
        while True:
            if self.window_closed:
                break
            self.tick()
            time.sleep(TICK_DURATION)

        self.root.destroy()

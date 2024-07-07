import random
import tkinter as tk

from pfk_games.bounce.paddle import Paddle
from pfk_games.bounce.score import Score


class Ball:
    def __init__(self, canvas: tk.Canvas, score: Score, paddle: Paddle, color: str) -> None:
        self.canvas = canvas
        self.score = score
        self.paddle = paddle
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.canvas.move(self.id, 245, 273)
        starts = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starts)
        self.x = 0
        self.y = 0
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all("<space>", self.start)
        self.started = False
        self.hit_bottom = False

    def start(self, _) -> None:
        if self.started:
            return

        starts = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starts)
        self.x = starts[0]
        self.y = -3
        self.started = True

    def hit_paddle(self, ball_pos: list[float]) -> bool:
        paddle_pos = self.canvas.coords(self.paddle.id)
        return Ball.is_aligned_horizontally(ball_pos, paddle_pos) and Ball.is_aligned_vertically(ball_pos, paddle_pos)

    @staticmethod
    def is_aligned_horizontally(ball_pos: list[float], paddle_pos: list[float]) -> bool:
        return ball_pos[2] >= paddle_pos[0] and ball_pos[0] <= paddle_pos[2]

    @staticmethod
    def is_aligned_vertically(ball_pos: list[float], paddle_pos: list[float]) -> bool:
        return paddle_pos[1] <= ball_pos[3] <= paddle_pos[3]

    def draw(self) -> None:
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y = 3
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
        if self.hit_paddle(pos):
            self.y = -3
            self.score.increment()
        if pos[0] <= 0:
            self.x = 3
        if pos[2] >= self.canvas_width:
            self.x = -3

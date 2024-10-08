import random
import tkinter as tk

from pfk_games.bounce.paddle import Paddle
from pfk_games.bounce.score import Score

START_X = 245
START_Y = 284


class Ball:
    def __init__(self, canvas: tk.Canvas, score: Score, paddle: Paddle, color: str) -> None:
        self.canvas = canvas
        self.score = score
        self.paddle = paddle
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False
        self.dx = 0
        self.dy = 0
        self.reset()

    def reset(self) -> None:
        self.canvas.moveto(self.id, START_X, START_Y)
        self.dx = 0
        self.dy = 0
        self.hit_bottom = False

    def start(self) -> None:
        starts = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starts)
        self.dx = starts[0]
        self.dy = -3

    def hit_paddle(self, ball_pos: list[float]) -> bool:
        paddle_pos = self.canvas.coords(self.paddle.id)
        return Ball.is_aligned_horizontally(ball_pos, paddle_pos) and Ball.is_aligned_vertically(ball_pos, paddle_pos)

    @staticmethod
    def is_aligned_horizontally(ball_pos: list[float], paddle_pos: list[float]) -> bool:
        return ball_pos[2] >= paddle_pos[0] and ball_pos[0] <= paddle_pos[2]

    @staticmethod
    def is_aligned_vertically(ball_pos: list[float], paddle_pos: list[float]) -> bool:
        return paddle_pos[1] <= ball_pos[3] <= paddle_pos[3]

    def tick(self) -> None:
        self.canvas.move(self.id, self.dx, self.dy)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.dy = 3
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
        if self.hit_paddle(pos):
            self.dy = -3
            self.score.increment()
        if pos[0] <= 0:
            self.dx = 3
        if pos[2] >= self.canvas_width:
            self.dx = -3

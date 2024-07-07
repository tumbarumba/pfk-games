import random
import time
import tkinter as tk


class Score:
    def __init__(self, canvas: tk.Canvas, color: str) -> None:
        self.canvas = canvas
        self.color = color
        self.score = 0
        self.id = self.make_score(color)

    def make_score(self, color):
        return self.canvas.create_text(
            self.canvas.winfo_width() - 55, 10,
            text=f"Score: {self.score:>3}",
            font=("monospace", 12),
            justify="right",
            fill=color)

    def draw(self) -> None:
        self.canvas.delete(self.id)
        self.id = self.make_score(self.color)

    def add(self):
        self.score += 1


class Paddle:
    def __init__(self, canvas: tk.Canvas, color: str) -> None:
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.id, 200, 300)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all("<KeyPress-Left>", self.turn_left)
        self.canvas.bind_all("<KeyPress-Right>", self.turn_right)

    def draw(self) -> None:
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 0
        elif pos[2] >= self.canvas_width:
            self.x = 0

    def turn_left(self, _) -> None:
        self.x = -2

    def turn_right(self, _) -> None:
        self.x = 2


class Ball:
    def __init__(self, canvas: tk.Canvas, score: Score, paddle: Paddle, color: str) -> None:
        self.canvas = canvas
        self.score = score
        self.paddle = paddle
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.canvas.move(self.id, 245, 100)
        starts = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starts)
        self.x = starts[0]
        self.y = -3
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False

    def hit_paddle(self, pos) -> bool:
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if paddle_pos[1] <= pos[3] <= paddle_pos[3]:
                return True
        return False

    def draw(self) -> None:
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y = 3
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
        if self.hit_paddle(pos):
            self.y = -3
            self.score.add()
        if pos[0] <= 0:
            self.x = 3
        if pos[2] >= self.canvas_width:
            self.x = -3


def main() -> None:
    root = tk.Tk()
    root.title("Bounce")
    root.resizable(False, False)
    root.wm_attributes("-topmost", 1)
    canvas = tk.Canvas(root, width=500, height=400, bd=0, highlightthickness=0)
    canvas.pack()
    root.update()

    score = Score(canvas, "green")
    paddle = Paddle(canvas, "blue")
    ball = Ball(canvas, score, paddle, "red")

    while 1:
        if not ball.hit_bottom:
            ball.draw()
            paddle.draw()
            score.draw()
        root.update_idletasks()
        root.update()
        time.sleep(0.01)


if __name__ == "__main__":
    main()

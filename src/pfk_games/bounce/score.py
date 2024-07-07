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

    def increment(self):
        self.score += 1

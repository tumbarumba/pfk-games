import tkinter as tk


class Score:
    def __init__(self, canvas: tk.Canvas, color: str) -> None:
        self.canvas = canvas
        self.color = color
        self.score = 0
        self.high_score = 0
        self.id = self.create_text()

    def create_text(self):
        return self.canvas.create_text(
            self.canvas.winfo_width() - 55, 20,
            text=f"Score: {self.score:>3}\nHigh: {self.high_score:>3}",
            font=("monospace", 12),
            justify="right",
            fill=self.color)

    def reset(self) -> None:
        self.score = 0
        self.canvas.delete(self.id)
        self.id = self.create_text()

    def increment(self):
        self.score += 1
        if self.score > self.high_score:
            self.high_score = self.score

        self.canvas.delete(self.id)
        self.id = self.create_text()

    def tick(self) -> None:
        pass

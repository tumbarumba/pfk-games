import tkinter as tk


class Score:
    def __init__(self, canvas: tk.Canvas, color: str) -> None:
        self.canvas = canvas
        self.color = color
        self.score = 0
        self.high_score = 0
        self.id = self.canvas.create_text(
            self.canvas.winfo_width() - 55, 20,
            text=self.format_score(),
            font=("monospace", 12),
            justify="right",
            fill=self.color)

    def format_score(self) -> str:
        return f"Score: {self.score:>3}\nHigh: {self.high_score:>3}"

    def reset(self) -> None:
        self.score = 0
        self.canvas.itemconfig(self.id, text=self.format_score())

    def increment(self):
        self.score += 1
        if self.score > self.high_score:
            self.high_score = self.score

        self.canvas.itemconfig(self.id, text=self.format_score())

    def tick(self) -> None:
        pass

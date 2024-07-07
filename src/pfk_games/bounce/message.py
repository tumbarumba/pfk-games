import tkinter as tk


class Message:
    def __init__(self, canvas: tk.Canvas, color: str, message: str) -> None:
        self.canvas = canvas
        self.color = color
        self.id = self.make_message(color, message)

    def make_message(self, color, message):
        return self.canvas.create_text(
            250, 350,
            text=message,
            font=("monospace", 12),
            justify="center",
            fill=color)

    def draw(self) -> None:
        pass

    def update(self, new_message: str) -> None:
        self.canvas.delete(self.id)
        self.id = self.make_message(self.color, new_message)

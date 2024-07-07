import tkinter as tk


class Message:
    def __init__(self, canvas: tk.Canvas, color: str, message: str) -> None:
        self.canvas = canvas
        self.color = color
        self.id = self.canvas.create_text(
            250, 350,
            text=message,
            font=("monospace", 12),
            justify="center",
            fill=color)

    def draw(self) -> None:
        pass

    def update(self, new_message: str) -> None:
        self.canvas.itemconfig(self.id, text=new_message)

import tkinter as tk


class Message:
    def __init__(self, canvas: tk.Canvas, colour: str, message: str) -> None:
        self._canvas = canvas
        self._rect_id = self._canvas.create_rectangle(
            (10, 200), (490, 300),
            outline="black",
            fill="white"
        )
        self._text_id = self._canvas.create_text(
            250, 250,
            text=message,
            font=("monospace", 12),
            justify="center",
            fill=colour
        )

    def remove(self) -> None:
        self._canvas.delete(self._rect_id)
        self._canvas.delete(self._text_id)

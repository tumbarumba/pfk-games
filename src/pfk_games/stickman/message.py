import tkinter as tk
from random import setstate


class Message:
    def __init__(self, canvas: tk.Canvas, colour: str, message: str = "") -> None:
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
        self.hide()

    def show(self, new_message: str) -> None:
        self._canvas.itemconfig(self._rect_id, state="normal")
        self._canvas.itemconfig(self._text_id, text=new_message, state="normal")

    def hide(self) -> None:
        self._canvas.itemconfig(self._rect_id, state="hidden")
        self._canvas.itemconfig(self._text_id, state="hidden")

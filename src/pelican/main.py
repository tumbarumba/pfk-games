from tkinter import *
import random
import time


class Ball:
    def __init__(self, canvas: Canvas, color: str):
        self.canvas = canvas
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.canvas.move(self.id, 245, 100)

    def draw(self):
        self.canvas.move(self.id, 0, -1)


def main() -> None:
    tk = Tk()
    tk.title("Game")
    tk.resizable(0, 0)
    tk.wm_attributes("-topmost", 1)
    canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)
    canvas.pack()

    ball = Ball(canvas, "red")

    while 1:
        ball.draw()
        tk.update_idletasks()
        tk.update()
        time.sleep(0.01)


if __name__ == "__main__":
    main()

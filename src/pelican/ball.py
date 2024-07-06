from tkinter import *
import random
import time

class Ball:
    def __init__(self, canvas: Canvas, color: str):
        self.canvas = canvas
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.canvas.move(self.id, 245, 100)

    def draw(self):
        pass

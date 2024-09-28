import time
import tkinter as tk

from pfk_games.stickman.level import Level, Level1
from pfk_games.stickman.message import Message

TICK_DURATION = 0.01


class StickMan:
    def __init__(self) -> None:
        self._root = tk.Tk()
        self._root.title("Mr. Stick Man Races for the Exit")
        self._root.resizable(False, False)
        self._root.wm_attributes("-topmost", 1)
        self._root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.window_closed = False

        self._canvas = tk.Canvas(self._root, width=500, height=500, bd=0, highlightthickness=0)
        self._canvas.pack()
        self._root.update()
        self._canvas_height = 500
        self._canvas_width = 500
        self._running = True

        self._level: Level = Level1(self._canvas)

        self._message: Message | None = None

        self._bind_keys()

    def _bind_keys(self) -> None:
        self._canvas.bind_all("<KeyPress-Left>", self.on_left)
        self._canvas.bind_all("<KeyPress-Right>", self.on_right)
        self._canvas.bind_all("<space>", self.on_space)

    def on_left(self, _):
        if not self._message:
            self._level.on_left()

    def on_right(self, _):
        if not self._message:
            self._level.on_right()

    def on_space(self, _):
        if self._message:
            self.hide_message()
            self._level.on_left()
        else:
            self._level.on_space()

    def on_close(self) -> None:
        self.window_closed = True

    def show_message(self, message: str) -> None:
        self._message = Message(self._canvas, "black", message)

    def hide_message(self) -> None:
        self._message.remove()
        self._message = None

    def tick(self) -> None:
        if self._running:
            self._level.tick()
            if self._level.complete:
                self._running = False
        self._root.update_idletasks()
        self._root.update()

    def mainloop(self) -> None:
        self.show_message("Level 1\n\nPress <space> to start")
        while True:
            if self.window_closed:
                break
            self.tick()
            time.sleep(TICK_DURATION)

        self._root.destroy()

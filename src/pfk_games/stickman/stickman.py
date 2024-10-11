import time
import tkinter as tk
from typing import Callable

from pfk_games.stickman.level import Level, Level1, Level2
from pfk_games.stickman.message import Message

TICK_INTERVAL = 0.01


level_builders: list[Callable[[tk.Canvas], Level]] = [Level1, Level2]
# level_builders: list[Callable[[tk.Canvas], Level]] = [Level2]


class StickManGame:
    def __init__(self, width: int, height: int) -> None:
        self._window_closed = False
        self._root = self._make_root_window()
        self._canvas = self._make_canvas(self._root, width, height)

        self._game_over = False
        self._level_index = -1
        self._level: Level
        self._message: Message | None = None

    def mainloop(self) -> None:
        self._restart_game()
        while not self._window_closed:
            processing_time = self.tick()
            sleep_time = max(0.0, TICK_INTERVAL - processing_time)
            time.sleep(sleep_time)

        self._root.destroy()

    def tick(self) -> float:
        tick_start = time.time()

        if not self._game_over:
            self._level.tick()
            if self._level.complete:
                self.show_message(f"Level {self._level_index + 1} complete\n\nPress <space> for next level")
        self._root.update_idletasks()
        self._root.update()

        return time.time() - tick_start

    def on_left(self, _):
        if not self._message:
            self._level.on_left()

    def on_right(self, _):
        if not self._message:
            self._level.on_right()

    def on_space(self, _):
        if not self._message:
            self._level.on_space()
            return

        self.hide_message()
        if self._game_over:
            self._restart_game()
        elif self._level.complete:
            self._try_start_next_level()
        elif not self._level.started:
            self._level.start()

    def on_close(self) -> None:
        self._window_closed = True

    def show_message(self, message: str) -> None:
        if self._message:
            self.hide_message()
        self._message = Message(self._canvas, "black", message)

    def hide_message(self) -> None:
        self._message.remove()
        self._message = None

    def _make_root_window(self) -> tk.Tk:
        root = tk.Tk()
        root.title("Mr. Stick Man Races for the Exit")
        root.resizable(False, False)
        root.wm_attributes("-topmost", 1)
        root.protocol("WM_DELETE_WINDOW", self.on_close)
        return root

    def _make_canvas(self, root: tk.Tk, width: int, height: int) -> tk.Canvas:
        canvas = tk.Canvas(root, width=width, height=height, bd=0, highlightthickness=0)
        canvas.pack()
        root.update()
        canvas.bind_all("<KeyPress-Left>", self.on_left)
        canvas.bind_all("<KeyPress-Right>", self.on_right)
        canvas.bind_all("<space>", self.on_space)
        return canvas

    def _restart_game(self):
        self._game_over = False
        self._level_index = -1
        self._start_next_level()

    def _try_start_next_level(self):
        if self._has_next_level():
            self._start_next_level()
        else:
            self._end_game()

    def _has_next_level(self) -> bool:
        return self._level_index < len(level_builders) - 1

    def _start_next_level(self):
        self._level_index += 1
        self._level = level_builders[self._level_index](self._canvas)
        self.show_message(f"Level {self._level_index + 1}\n\nPress <space> to start")

    def _end_game(self):
        self._game_over = True
        self.show_message("Game Over\n\nPress <space> to start again")

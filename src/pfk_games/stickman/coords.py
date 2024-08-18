from __future__ import annotations

class Point:
    def __init__(self, x: int = 0, y: int = 0) -> None:
        self._x = x
        self._y = y

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

class Coords:
    def __init__(self, top_left: Point, bottom_right: Point) -> None:
        self._top_left = top_left
        self._bottom_right = bottom_right

    @property
    def top_left(self) -> Point:
        return self._top_left

    @property
    def bottom_right(self) -> Point:
        return self._bottom_right

    @property
    def left(self) -> int:
        return self._top_left.x

    @property
    def right(self) -> int:
        return self.bottom_right.x

    @property
    def top(self) -> int:
        return self._top_left.y

    @property
    def bottom(self) -> int:
        return self._bottom_right.y

    def within_x(self, other: Coords) -> bool:
        return (other.left < self.left < other.right) or \
               (other.left < self.right < other.right) or \
               (self.left < other.left < self.right) or \
               (self.left < other.right < self.right)

    def within_y(self, other: Coords) -> bool:
        return (other.top < self.top < other.bottom) or \
               (other.top < self.bottom < other.bottom) or \
               (self.top < other.top < self.bottom) or \
               (self.top < other.bottom < self.bottom)

    def collided_left(self, other: Coords) -> bool:
        return self.within_y(other) and other.left <= self.left <= other.right

    def collided_right(self, other: Coords) -> bool:
        return self.within_y(other) and other.left <= self.right <= other.right

    def collided_top(self, other: Coords) -> bool:
        return self.within_x(other) and other.top <= self.top <= other.bottom

    def collided_bottom(self, other: Coords, y: int) -> bool:
        return self.within_x(other) and other.top <= (self.bottom + y) <= other.bottom

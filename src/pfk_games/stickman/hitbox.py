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

    def move(self, dx: int, dy: int) -> Point:
        return Point(self._x + dx, self._y + dy)


class HitBox:
    def __init__(self, top_left: Point = Point(), bottom_right: Point = Point) -> None:
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

    def intersect_x(self, other: HitBox) -> bool:
        return self.left < other.right and other.left < self.right

    def intersect_y(self, other: HitBox) -> bool:
        return self.top < other.bottom and other.top < self.bottom

    def collided_left(self, other: HitBox) -> bool:
        return self.intersect_y(other) and other.left <= self.left <= other.right

    def collided_right(self, other: HitBox) -> bool:
        return self.intersect_y(other) and other.left <= self.right <= other.right

    def collided_top(self, other: HitBox) -> bool:
        return self.intersect_x(other) and other.top <= self.top <= other.bottom

    def collided_bottom(self, other: HitBox, y: int) -> bool:
        return self.intersect_x(other) and other.top <= (self.bottom + y) <= other.bottom

    def move(self, dx, dy) -> HitBox:
        return HitBox(self.top_left.move(dx, dy), self.bottom_right.move(dx, dy))

from __future__ import annotations


class Coords:
    def __init__(self, x1=0, y1=0, x2=0, y2=0) -> None:
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def within_x(self, other: Coords) -> bool:
        return (other.x1 < self.x1 < other.x2) or \
               (other.x1 < self.x2 < other.x2) or \
               (self.x1 < other.x1 < self.x2) or \
               (self.x1 < other.x2 < self.x2)

    def within_y(self, other: Coords) -> bool:
        return (other.y1 < self.y1 < other.y2) or \
               (other.y1 < self.y2 < other.y2) or \
               (self.y1 < other.y1 < self.y2) or \
               (self.y1 < other.y2 < self.y2)

    def collided_left(self, other: Coords) -> bool:
        return self.within_y(other) and other.x1 <= self.x1 <= other.x2

    def collided_right(self, other: Coords) -> bool:
        return self.within_y(other) and other.x1 <= self.x2 <= other.x2

    def collided_top(self, other: Coords) -> bool:
        return self.within_x(other) and other.y1 <= self.y1 <= other.y2

    def collided_bottom(self, other: Coords, y: int) -> bool:
        return self.within_x(other) and other.y1 <= (self.y2 + y) <= other.y2

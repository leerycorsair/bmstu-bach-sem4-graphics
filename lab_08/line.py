from point import Point
from tools import swapper
from math import sqrt

class Line():
    def __init__(self, start: Point, end: Point) -> None:
        self.start = start
        self.end = end

    def swap_vertices(self):
        self.start, self.end = swapper(self.start, self.end)

    def is_vertical(self) -> bool:
        return self.start.x == self.end.x

    def is_horizontal(self) -> bool:
        if self.is_vertical():
            return False

        line_tg = self.line_tg()
        return line_tg == 0

    def line_tg(self) -> float:
        return (self.end.y - self.start.y) / (self.end.x - self.start.x)

    @staticmethod
    def make_parallel(line, start: Point, end: Point) -> Point:
        if line.is_vertical():
            return Point(start.x, end.y)
        elif line.is_horizontal():
            return Point(end.x, start.y)
        else:
            length = sqrt((end.x - start.x) ** 2 + (end.y - start.y) ** 2)
            dx = sqrt(length * length / (1 + line.line_tg()**2))
            dy = dx * line.line_tg()
            if (end.x - start.x) * dx < 0:
                dx, dy = -dx, -dy
            return Point(start.x + dx, start.y + dy)
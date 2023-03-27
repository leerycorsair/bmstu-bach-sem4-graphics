from point import Point
from tools import swapper


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
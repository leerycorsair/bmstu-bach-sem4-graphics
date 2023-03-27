from math import sqrt


class Point():
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def distance(self, point) -> float:
        return sqrt((self.x - point.x)**2 + (self.y - point.y)**2)

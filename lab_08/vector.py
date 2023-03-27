from line import Line
from point import Point


class Vector():
    def __init__(self, end=Point(0, 0), start=Point(0, 0)):
        self.x = end.x - start.x
        self.y = end.y - start.y

    def scalar_product(self, vector) -> float:
        return self.x * vector.x + self.y * vector.y

    def vector_product(self, vector) -> float:
        return self.x * vector.y - self.y * vector.x

    def set_coords(self, x: float, y: float):
        self.x = x
        self.y = y

    @staticmethod
    def get_normal(line: Line, check_point: Point):
        vect = Vector(line.start, line.end)
        normal = Vector()
        if vect.x == 0:
            normal.set_coords(1, 0)
        else:
            normal.set_coords(-vect.y / vect.x, 1)
        if normal.scalar_product(Vector(line.end, check_point)) < 0:
            normal.x, normal.y = -normal.x, -normal.y
        return normal

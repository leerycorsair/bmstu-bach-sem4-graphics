from math import copysign
from vector import Vector
from line import Line
from point import Point


class Clipper():
    def __init__(self) -> None:
        self.data: list[Point] = []

    def add_point(self, point: Point) -> None:
        self.data.append(point)

    def len(self) -> int:
        return len(self.data)

    def first_p(self) -> Point:
        return self.data[0]

    def last_p(self) -> Point:
        return self.data[-1]

    def pre_last_p(self) -> Point:
        return self.data[-2]

    def is_locked(self) -> bool:
        return self.first_p() == self.last_p() and self.len() > 1

    def is_empty(self) -> bool:
        return not bool(self.len())

    def get_nearest_edge(self, start: Point, end: Point) -> Line:
        distance = float("inf")
        for i in range(self.len() - 1):
            tmp_d1 = self.data[i].distance(start) + \
                self.data[i+1].distance(end)
            tmp_d2 = self.data[i].distance(end) + \
                self.data[i+1].distance(start)
            tmp_d = min(tmp_d1, tmp_d2)
            if (tmp_d < distance):
                distance = tmp_d
                tmp_line = Line(self.data[i], self.data[i + 1])
        return tmp_line

    def is_convex(self) -> bool:
        vect1 = Vector(self.data[0], self.data[1])
        vect2 = Vector(self.data[1], self.data[2])
        if vect1.vector_product(vect2) > 0:
            sign = 1
        else:
            sign = -1
        tmp_p = self.data.pop()
        for i in range(3, self.len() + 2):
            vect1 = vect2
            if i < self.len():
                vect2 = Vector(self.data[i - 1], self.data[i])
            elif i == self.len():
                vect2 = Vector(self.data[-1], self.data[0])
            else:
                vect2 = Vector(self.data[0], self.data[1])

            if sign * vect1.vector_product(vect2) < 0:
                self.data.append(tmp_p)
                return False
        self.data.append(tmp_p)
        return True

    def clip_lines(self, lines: list[Line]) -> list[Line]:
        clipped_lines: list[Line] = []
        tmp_p = self.data.pop()
        for line in lines:
            result = self.clip_line(line)
            if not (result is None):
                clipped_lines.append(result)
        self.data.append(tmp_p)
        return clipped_lines

    def clip_line(self, line: Line) -> Line:
        direction = Vector(line.start, line.end)
        t_min = 0
        t_max = 1
        for i in range(self.len()):
            c_line = Line(self.data[i],
                          self.data[(i + 1)%self.len()])
            normal = Vector.get_normal(c_line,
                                     self.data[(i + 2) % self.len()])
            border_point = self.data[i]
            w_vect = Vector(border_point, line.start)
            w_prod = w_vect.scalar_product(normal)
            d_prod = direction.scalar_product(normal)
            if d_prod != 0:
                t = -w_prod / d_prod
                if d_prod > 0:
                    if t > 1:
                        return None
                    t_min = max(t, t_min)
                else:
                    if t < 0:
                        return None
                    t_max = min(t, t_max)
            elif w_prod < 0:
                return None
        if t_min > t_max:
            return None
        start_x = line.start.x + (line.end.x - line.start.x) * t_min
        start_y = line.start.y + (line.end.y - line.start.y) * t_min
        end_x = line.start.x + (line.end.x - line.start.x) * t_max
        end_y = line.start.y + (line.end.y - line.start.y) * t_max
        return Line(Point(start_x, start_y), Point(end_x, end_y))
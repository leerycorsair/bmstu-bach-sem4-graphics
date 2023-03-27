from data.dot import Dot
from data.polygon import Polygon


class Figure:
    def __init__(self) -> None:
        self.data: list[Polygon] = [Polygon()]
        self.p_min = Dot(10000, 10000)
        self.p_max = Dot(-10, -10)

    def is_empty(self) -> bool:
        return len(self.data) == 1 and self.data[-1].size() == 0

    def clear(self) -> None:
        self.p_min = Dot(100000, 100000)
        self.p_max = Dot(-100000, -100000)
        self.data = [Polygon()]

    def add_polygon(self) -> None:
        self.data.append(Polygon())

    def add_vertex(self, vertex: Dot):
        self.p_max.x = max(vertex.x, self.p_max.x)
        self.p_max.y = max(vertex.y, self.p_max.y)

        self.p_min.x = min(vertex.x, self.p_min.x)
        self.p_min.y = min(vertex.y, self.p_min.y)

        self.data[-1].add_vertex(vertex)

    def close_this_polygon(self) -> None:
        self.data[-1].close()
        self.add_polygon()

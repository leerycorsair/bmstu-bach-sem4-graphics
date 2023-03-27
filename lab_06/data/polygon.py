from data.dot import Dot


class Polygon:
    def __init__(self):
        self.vertices: list[Dot] = []
        self.extrema: list[int] = []

    def add_vertex(self, vertex: Dot) -> None:
        self.vertices.append(vertex)

        if self.size() > 2:
            self.update_extrema()

    def update_extrema(self) -> None:
        vert, curr_index = self.vertices, len(self.vertices) - 2
        if vert[curr_index].y == min([p.y for p in vert[-3:]]) \
            or vert[curr_index].y == max([p.y for p in vert[-3:]]):
            self.extrema.append(curr_index)

    def is_closed(self) -> bool:
        return len(self.vertices) > 1 and (self.vertices[0]
                                           == self.vertices[-1])

    def close(self) -> None:
        self.add_vertex(self.vertices[0])

    def size(self) -> int:
        return len(self.vertices)
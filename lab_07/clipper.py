from line import Line
from point import Point
from tools import swapper


class ClipperLine(Line):
    def __init__(self, start: Point, end: Point) -> None:
        super().__init__(start, end)
        self.start_code = [0, 0, 0, 0]
        self.end_code = [0, 0, 0, 0]

    @staticmethod
    def from_default_line(line: Line):
        c_line = ClipperLine(line.start, line.end)
        return c_line

    def swap_vertices(self) -> None:
        self.start_code, self.end_code = swapper(self.start_code,
                                                 self.end_code)
        super().swap_vertices()

    def default_line(self) -> Line:
        return Line(self.start, self.end)


class Clipper():
    def __init__(self, x_left: int, x_right: int, y_bottom: int,
                 y_top: int) -> None:
        self.x_left = x_left
        self.x_right = x_right
        self.y_bottom = y_bottom
        self.y_top = y_top

    def clip_line(self, line: Line) -> Line:
        GENERAL_LINE, VERTICAL_LINE, HORIZONTAL_LINE = 1, -1, 0
        flag = GENERAL_LINE
        if line.is_vertical():
            flag = VERTICAL_LINE
        elif line.is_horizontal():
            flag = HORIZONTAL_LINE
        cutter_params = [self.x_left, self.x_right, self.y_bottom, self.y_top]
        for i in range(4):
            c_line = ClipperLine.from_default_line(line)
            visibility = self.is_visible(c_line)
            if visibility == 1:
                return c_line.default_line()
            if visibility == -1:
                return None
            if c_line.start_code[3 - i] == c_line.end_code[3 - i]:
                continue
            if c_line.start_code[3 - i] == 0:
                c_line.swap_vertices()
            if flag != VERTICAL_LINE and i <= 1:
                c_line.start.y = c_line.line_tg() * (
                    cutter_params[i] - c_line.start.x) + c_line.start.y
                c_line.start.x = cutter_params[i]
            elif flag != HORIZONTAL_LINE:
                if flag != VERTICAL_LINE:
                    c_line.start.x = (1 / c_line.line_tg()) * (
                        cutter_params[i] - c_line.start.y) + c_line.start.x
                c_line.start.y = cutter_params[i]
        return c_line.default_line()

    def clip_lines(self, lines: list[Line]) -> list[Line]:
        clipped_lines: list[Line] = []
        for line in lines:
            result = self.clip_line(line)
            if not (result is None):
                clipped_lines.append(result)
        return clipped_lines

    def codes_init(self, c_line: ClipperLine) -> None:
        def code_init(point: Point, clipper: Clipper, code: list[int]):
            code[3] = int(point.x < clipper.x_left)
            code[2] = int(point.x > clipper.x_right)
            code[1] = int(point.y < clipper.y_bottom)
            code[0] = int(point.y > clipper.y_top)

        code_init(c_line.start, self, c_line.start_code)
        code_init(c_line.end, self, c_line.end_code)

    def is_visible(self, c_line: ClipperLine) -> int:
        FULLY_VISIBLE = 1
        PARTLY_VISIBLE = 0
        INVISIBLE = -1

        self.codes_init(c_line)
        visibility = PARTLY_VISIBLE
        if sum(c_line.start_code) == 0 and sum(c_line.end_code) == 0:
            visibility = FULLY_VISIBLE
        elif Clipper.is_invisible(c_line):
            visibility = INVISIBLE
        return visibility

    @staticmethod
    def is_invisible(c_line: ClipperLine) -> bool:
        prod = 0
        for start_byte, end_byte in zip(c_line.start_code, c_line.end_code):
            prod += int((start_byte + end_byte) / 2)
        return bool(prod)

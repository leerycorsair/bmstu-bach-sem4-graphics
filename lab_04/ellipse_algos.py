from drawing import Dot
from my_round import my_round
import math


def dots_append_ellipse_sym(dots: list[Dot], center: Dot, x: int,
                            y: int) -> list[Dot]:
    dots.append(Dot(center.x + x, center.y + y))
    dots.append(Dot(center.x + x, center.y - y))
    dots.append(Dot(center.x - x, center.y + y))
    dots.append(Dot(center.x - x, center.y - y))
    return dots


def ellipse_general(x: int, y: int, a: int, b: int) -> list[Dot]:
    dots: list[Dot] = []
    center = Dot(x, y)

    x_inflect = my_round(a**2 / math.sqrt(a**2 + b**2))
    y_inflect = my_round(b**2 / math.sqrt(a**2 + b**2))

    for curr_x in range(0, x_inflect + 1, 1):
        curr_y = my_round(math.sqrt(1 - curr_x**2 / a**2) * b)
        dots = dots_append_ellipse_sym(dots, center, curr_x, curr_y)

    for curr_y in range(0, y_inflect + 1, 1):
        curr_x = my_round(math.sqrt(1 - curr_y**2 / b**2) * a)
        dots = dots_append_ellipse_sym(dots, center, curr_x, curr_y)

    return dots


def ellipse_param(x: int, y: int, a: int, b: int) -> list[Dot]:
    dots: list[Dot] = []
    center = Dot(x, y)

    curr_x, curr_y = a, 0
    t = 0

    y_inflect = my_round(b**2 / math.sqrt(a**2 + b**2))
    step_x, step_y = 1 / a, 1 / b

    while (curr_x > 0):
        curr_x = my_round(a * math.cos(t))
        curr_y = my_round(b * math.sin(t))
        dots = dots_append_ellipse_sym(dots, center, curr_x, curr_y)
        if curr_y <= y_inflect:
            t += step_y
        else:
            t += step_x

    return dots


def ellipse_bresenham(x: int, y: int, a: int, b: int) -> list[Dot]:
    dots: list[Dot] = []
    center = Dot(x, y)

    curr_x, curr_y = 0, b
    sqr_a = a * a
    sqr_a_2 = 2 * sqr_a
    sqr_b = b * b
    sqr_b_2 = 2 * sqr_b
    D = sqr_a + sqr_b - sqr_a_2 * curr_y
    while (curr_y >= 0):
        dots = dots_append_ellipse_sym(dots, center, curr_x, curr_y)
        if D == 0:
            curr_x += 1
            curr_y -= 1
            D += sqr_b_2 * curr_x + sqr_b + sqr_a - sqr_a_2 * curr_y
        elif D < 0:
            D1 = 2 * D + curr_y * sqr_a_2 - sqr_a
            if D1 > 0:
                curr_x += 1
                curr_y -= 1
                D += sqr_b_2 * curr_x + sqr_b + sqr_a - sqr_a_2 * curr_y
            else:
                curr_x += 1
                D += sqr_b_2 * curr_x + sqr_b
        else:
            D2 = 2 * D - sqr_b_2 * curr_x - sqr_b
            if D2 < 0:
                curr_x += 1
                curr_y -= 1
                D += sqr_b_2 * curr_x + sqr_b + sqr_a - sqr_a_2 * curr_y
            else:
                curr_y -= 1
                D += sqr_a - sqr_a_2 * curr_y
    return dots


def ellipse_middle(x: int, y: int, a: int, b: int) -> list[Dot]:
    dots: list[Dot] = []
    center = Dot(x, y)

    curr_x, curr_y = 0, b
    sqr_a = a * a
    sqr_a_2 = 2 * sqr_a
    sqr_b = b * b
    sqr_b_2 = 2 * sqr_b

    x_inflect = my_round(a**2 / math.sqrt(a**2 + b**2))

    df = 0
    f = my_round(sqr_b - sqr_a * b + 0.25 * sqr_a)
    delta = -sqr_a_2 * b

    while curr_x <= x_inflect:
        dots = dots_append_ellipse_sym(dots, center, curr_x, curr_y)

        if f >= 0:
            curr_y -= 1
            delta += sqr_a_2
            f += delta
        df += sqr_b_2
        f += df + sqr_b

        curr_x += 1

    delta = sqr_b_2 * curr_x
    f += my_round(-sqr_b * (curr_x + 0.75) - sqr_a*(curr_y - 0.75))
    df = -sqr_a_2 * curr_y

    while curr_y >= 0:
        dots = dots_append_ellipse_sym(dots, center, curr_x, curr_y)

        if f < 0:
            curr_x += 1
            delta += sqr_b_2
            f += delta
        df += sqr_a_2
        f += df + sqr_a

        curr_y -= 1
    
    return dots

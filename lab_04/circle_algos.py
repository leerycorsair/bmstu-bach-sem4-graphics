from drawing import Dot
from my_round import my_round
import math


def dots_append_circle_sym(dots: list[Dot], center: Dot, x: int,
                           y: int) -> list[Dot]:
    dots.append(Dot(center.x + x, center.y + y))
    dots.append(Dot(center.x - x, center.y - y))
    dots.append(Dot(center.x + x, center.y - y))
    dots.append(Dot(center.x - x, center.y + y))

    dots.append(Dot(center.x + y, center.y + x))
    dots.append(Dot(center.x - y, center.y - x))
    dots.append(Dot(center.x + y, center.y - x))
    dots.append(Dot(center.x - y, center.y + x))

    return dots


def circle_general(x: int, y: int, r: int) -> list[Dot]:
    dots: list[Dot] = []
    center = Dot(x, y)

    for curr_x in range(0, my_round(r / math.sqrt(2) + 1), 1):
        curr_y = my_round(math.sqrt(r * r - curr_x * curr_x))
        dots = dots_append_circle_sym(dots, center, curr_x, curr_y)

    return dots


def circle_param(x: int, y: int, r: int) -> list[Dot]:
    dots: list[Dot] = []
    center = Dot(x, y)

    t = 0
    while t <= (math.pi * r / 4):
        curr_x = my_round(r * math.cos(t / r))
        curr_y = my_round(r * math.sin(t / r))
        t += 1
        dots = dots_append_circle_sym(dots, center, curr_x, curr_y)
        
    return dots


def circle_bresenham(x: int, y: int, r: int) -> list[Dot]:
    dots: list[Dot] = []
    center = Dot(x, y)

    curr_x, curr_y = 0, r
    D = 2 * (1 - r)

    dots = dots_append_circle_sym(dots, center, curr_x, curr_y)
    while curr_y >= curr_x:
        if D < 0:
            D1 = 2 * (D + curr_y) - 1
            curr_x += 1
            if D1 < 0:
                D += 2 * curr_x + 1
            else:
                curr_y -= 1
                D += 2 * (curr_x - curr_y + 1)
        elif D == 0:
            curr_x += 1
            curr_y -= 1
            D += 2 * (curr_x - curr_y + 1)
        elif D > 0:
            D2 = 2 * (D - curr_x) - 1
            curr_y -= 1
            if D2 < 0:
                curr_x += 1
                D += 2 * (curr_x - curr_y + 1)
            else:
                D -= 2 * curr_y - 1
        dots = dots_append_circle_sym(dots, center, curr_x, curr_y)
    return dots


def circle_middle(x: int, y: int, r: int) -> list[Dot]:
    dots: list[Dot] = []
    center = Dot(x, y)

    curr_x = 0
    curr_y = r
    d = 1 - r

    dots = dots_append_circle_sym(dots, center, curr_x, curr_y)
    while curr_y >= curr_x:
        curr_x += 1
        if d < 0:
            d += 2 * curr_x + 1
        else:
            curr_y -= 1
            d += 2 * (curr_x - curr_y) + 1
        dots = dots_append_circle_sym(dots, center, curr_x, curr_y)
    return dots

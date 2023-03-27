

from random import randint
from config import CANVAS_HEIGHT, CANVAS_WIDTH
from numpy.ma import set_fill_value
from scipy.optimize import fsolve
import math


class Answer():
    def __init__(self):
        self.status_code = -1
        self.var1 = None
        self.var2 = None
        self.first_circle = None
        self.second_circle = None
        self.quadrilateral = None
        self.area = 0

    def create_message(self):
        if self.status_code == -1:
            return "Введеные вами точки лежат на одной прямой или одна из окружностей лежит внутри другой."
        if self.status_code == 1:
            return "Недостаточно точек в первом множестве. Нужно хотя бы 3."
        if self.status_code == 2:
            return "Недостаточно точек во втором множестве. Нужно хотя бы 3."
        if self.status_code == 0:
            return "Решением являются точки ({0:.2f};{1:.2f}) ({2:.2f};{3:.2f}) ({4:.2f};{5:.2f}) из первого множества \
и ({6:.2f};{7:.2f}) ({8:.2f};{9:.2f}) ({10:.2f};{11:.2f}) из второго. Они образуют четырехугольник с площадью {12:.2f},\
который в свою очередь построен на окружностях O1({13:.2f};{14:.2f}) R1={15:.2f},O2({16:.2f};{17:.2f}) R={18:.2f}."\
                    .format(self.var1[0][0], self.var1[0][1], self.var1[1][0], self.var1[1][1], self.var1[2][0], self.var1[2][1],
                            self.var2[0][0], self.var2[0][1], self.var2[1][0], self.var2[1][1], self.var2[2][0], self.var2[2][1],
                            self.area, self.first_circle[0], self.first_circle[1], self.first_circle[2],
                            self.second_circle[0], self.second_circle[1], self.second_circle[2])


def is_on_one_line(dot1, dot2, dot3):
    eps = 1e-6
    return abs((dot3[0]-dot1[0])*(dot2[1]-dot1[1])-(dot3[1]-dot1[1])*(dot2[0]-dot1[0])) <= eps


def find_circle(dot1, dot2, dot3):
    def func(params):
        return ((params[0]-dot1[0])**2+(params[1]-dot1[1])**2-params[2]**2,
                (params[0]-dot2[0])**2+(params[1]-dot2[1])**2 -
                params[2]**2, (params[0]-dot3[0])**2 +
                (params[1]-dot3[1])**2-params[2]**2)
    ans = fsolve(func, (dot1[0], dot1[1], dots_distance(dot1, dot2)), xtol=1e-7, maxfev=1000)
    return ans[0], ans[1], abs(ans[2])


def dots_distance(dot1, dot2):
    return math.sqrt((dot1[0]-dot2[0])**2 + (dot1[1]-dot2[1])**2)


def check_circles_pos(circle1_x, circle1_y, circle1_r, circle2_x, circle2_y, circle2_r):
    d = dots_distance((circle1_x, circle1_y), (circle2_x, circle2_y))
    return (d < abs(circle1_r - circle2_r))


def trap_area(circle1_x, circle1_y, circle1_r, circle2_x, circle2_y, circle2_r):
    return (circle1_r + circle2_r)/2 * dots_distance((circle1_x, circle1_y), (circle2_x, circle2_y))


def calc_quad(circle1_x, circle1_y, circle1_r, circle2_x, circle2_y, circle2_r):
    def func(x):
        return ((x[2]-x[0])*(circle1_x - x[0]) + (x[3]-x[1])*(circle1_y - x[1]),
                (x[2]-x[0])*(circle2_x - x[2]) +
                (x[3]-x[1])*(circle2_y - x[3]),
                (x[0]-circle1_x)**2 + (x[1] - circle1_y)**2 - circle1_r**2,
                (x[2]-circle2_x)**2 + (x[3] - circle2_y)**2 - circle2_r**2)


    ans = fsolve(func, (circle1_x + circle1_r, circle1_y + circle1_r,
                            circle2_x + circle2_r, circle2_y + circle2_r), xtol=1e-3, maxfev=1000)
    if (abs(ans[0] - ans[2]) < 0.1 and abs(ans[1]- ans[3])<0.1):
        ans = fsolve(func, (circle1_x - circle1_r, circle1_y - circle1_r,
                            circle2_x - circle2_r, circle2_y - circle2_r), xtol=1e-3, maxfev=1000)

    quad = [(circle1_x, circle1_y), (ans[0], ans[1]), (ans[2], ans[3]),
            (circle2_x, circle2_y)]
    return quad


def solve(var1, var2):
    sollution = Answer()
    if len(var1) < 3:
        sollution.status_code = 1
        return sollution
    if len(var2) < 3:
        sollution.status_code = 2
        return sollution

    for i_1 in range(len(var1)-2):
        for j_1 in range(i_1+1, len(var1)-1):
            for k_1 in range(j_1+1, len(var1)):
                if is_on_one_line(var1[i_1], var1[j_1], var1[k_1]):
                    continue
                for i_2 in range(len(var2)-2):
                    for j_2 in range(i_2+1, len(var2)-1):
                        for k_2 in range(j_2+1, len(var2)):
                            if is_on_one_line(var2[i_2], var2[j_2], var2[k_2]):
                                continue
                            circle1_x, circle1_y, circle1_r = find_circle(
                                var1[i_1], var1[j_1], var1[k_1])

                            circle2_x, circle2_y, circle2_r = find_circle(
                                var2[i_2], var2[j_2], var2[k_2])
                            if check_circles_pos(circle1_x, circle1_y, circle1_r, circle2_x, circle2_y, circle2_r) or \
                                    trap_area(circle1_x, circle1_y, circle1_r, circle2_x, circle2_y, circle2_r) < sollution.area:
                                continue
                            sollution.status_code = 0
                            sollution.first_circle = (
                                circle1_x, circle1_y, circle1_r)
                            sollution.second_circle = (
                                circle2_x, circle2_y, circle2_r)
                            sollution.var1 = (var1[i_1], var1[j_1], var1[k_1])
                            sollution.var2 = (var2[i_2], var2[j_2], var2[k_2])
                            sollution.quadrilateral = calc_quad(
                                circle1_x, circle1_y, circle1_r, circle2_x, circle2_y, circle2_r)
                            sollution.area = trap_area(
                                circle1_x, circle1_y, circle1_r, circle2_x, circle2_y, circle2_r)
    return sollution

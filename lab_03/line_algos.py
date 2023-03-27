import math

def my_round(num):
    if num>=0:
        return int(num+0.5)
    else:
        return int(num-0.5)


def algo_dda(dot1, dot2, color, stepping=0):
    if dot1[0] == dot2[0] and dot1[1] == dot2[1]:
        if stepping: 
            return [(dot1, color)],1
        return [(dot1, color)]
    dx, dy = dot2[0]-dot1[0], dot2[1]-dot1[1]
    if abs(dx) > abs(dy):
        l = abs(dx)
    else:
        l = abs(dy)
    dx, dy = dx/l, dy/l
    curr_x, curr_y = dot1[0], dot1[1]
    stairs = []
    curr_stair_len = 0
    dots = []
    for i in range(l+1):
        dots.append(((my_round(curr_x), my_round(curr_y)), color))
        if abs(my_round(curr_x + dx) - my_round(curr_x)) >= 1 and abs(my_round(curr_y + dy) - my_round(curr_y)) >= 1:
            stairs.append(curr_stair_len)
            curr_stair_len = 1
        elif i == l - 1:
            stairs.append(curr_stair_len)
        else:
            curr_stair_len += 1
        curr_x, curr_y = curr_x + dx, curr_y + dy
    if stepping:
        return dots, len(stairs)
    else:
        return dots


def algo_bresenham_int(dot1, dot2, color, stepping=0):
    if dot1[0] == dot2[0] and dot1[1] == dot2[1]:
        if stepping: 
            return [(dot1, color)],1
        return [(dot1, color)]
    dots = []
    curr_x, curr_y = dot1[0], dot1[1]
    dx, dy = dot2[0]-dot1[0], dot2[1]-dot1[1]
    xsign = 1 if dx > 0 else -1
    ysign = 1 if dy > 0 else -1
    dx = abs(dx)
    dy = abs(dy)
    if dy > dx:
        dx, dy, c_f = dy, dx, 1
    else:
        c_f = 0
    e = 2 * dy - dx
    stairs = []
    curr_stair_len = 1
    while curr_x != dot2[0] or curr_y != dot2[1]:
        dots.append(((curr_x, curr_y), color))
        if e >= 0:
            if c_f == 1:
                curr_x += xsign
            else:
                curr_y += ysign
            stairs.append(curr_stair_len)
            curr_stair_len = 1
            e -= 2 * dx
        else:
            curr_stair_len += 1
        if c_f == 1:
            curr_y += ysign
            if (curr_x == dot2[0] and curr_y == dot2[1]):
                stairs.append(curr_stair_len-1)
        else:
            curr_x += xsign
            if (curr_x == dot2[0] and curr_y == dot2[1]):
                stairs.append(curr_stair_len-1)
        e += 2 * dy
    dots.append(((my_round(curr_x), my_round(curr_y)), color))
    if stepping:
        return dots, len(stairs)
    else:
        return dots


def algo_bresenham_float(dot1, dot2, color, stepping=0):
    if dot1[0] == dot2[0] and dot1[1] == dot2[1]:
        if stepping: 
            return [(dot1, color)],1
        return [(dot1, color)]
    dots = []
    curr_x, curr_y = dot1[0], dot1[1]
    dx, dy = dot2[0]-dot1[0], dot2[1]-dot1[1]
    xsign = 1 if dx > 0 else -1
    ysign = 1 if dy > 0 else -1
    dx = abs(dx)
    dy = abs(dy)
    if dy > dx:
        dx, dy, c_f = dy, dx, 1
    else:
        c_f = 0
    m = dy/dx
    e = m - 0.5
    stairs = []
    curr_stair_len = 1
    while curr_x != dot2[0] or curr_y != dot2[1]:
        dots.append(((curr_x, curr_y), color))
        if e >= 0:
            if c_f == 1:
                curr_x += xsign
            else:
                curr_y += ysign
            stairs.append(curr_stair_len)
            curr_stair_len = 1
            e -= 1
        else:
            curr_stair_len += 1
        if c_f == 1:
            curr_y += ysign
            if (curr_x == dot2[0] and curr_y == dot2[1]):
                stairs.append(curr_stair_len-1)
        else:
            curr_x += xsign
            if (curr_x == dot2[0] and curr_y == dot2[1]):
                stairs.append(curr_stair_len-1)
        e += m
    dots.append(((my_round(curr_x), my_round(curr_y)), color))
    if stepping:
        return dots, len(stairs)
    else:
        return dots


def algo_bresenham_stepless(dot1, dot2, color, stepping=0):
    if dot1[0] == dot2[0] and dot1[1] == dot2[1]:
        if stepping: 
            return [(dot1, color)],1
        return [(dot1, color)]
    dots = []
    curr_x, curr_y = dot1[0], dot1[1]
    dx, dy = dot2[0]-dot1[0], dot2[1]-dot1[1]
    xsign = 1 if dx > 0 else -1
    ysign = 1 if dy > 0 else -1
    dx = abs(dx)
    dy = abs(dy)
    if dy > dx:
        dx, dy, c_f = dy, dx, 1
    else:
        c_f = 0
    m = dy/dx * 255
    e = 255/2
    w = 255 - m
    stairs = []
    curr_stair_len = 1
    while curr_x != dot2[0] or curr_y != dot2[1]:
        tmp_color = (color[0], color[1], color[2], int(e))
        dots.append(((curr_x, curr_y), tmp_color))
        if e < w:
            if c_f == 0:
                curr_x += xsign
            else:
                curr_y += ysign
            e += m
            curr_stair_len += 1
            if (curr_x == dot2[0] and curr_y == dot2[1]):
                stairs.append(curr_stair_len-1)
        else:
            curr_x += xsign
            curr_y += ysign
            stairs.append(curr_stair_len)
            curr_stair_len = 1
            if (curr_x == dot2[0] and curr_y == dot2[1]):
                stairs.append(curr_stair_len-1)
            e -= w
    tmp_color = (color[0], color[1], color[2], int(e))
    dots.append(((curr_x, curr_y), tmp_color))
            
    if stepping:
        return dots, len(stairs)
    else:
        return dots


def fpart(x):
    return x - int(x)


def get_endpoint(x_s, y_s, dots, m, color, steep):
    x_e = round(x_s)
    y_e = y_s + (x_e - x_s) * m
    x_gap = rfpart(x_s + 0.5)
    px, py = my_round(x_e), my_round(y_e)
    i1 = rfpart(y_e) * x_gap * 255
    i2 = fpart(y_e) * x_gap * 255
    if steep:
        buf_x, buf_y = py, px
    else:
        buf_x, buf_y = px, py
    tmp_color1 = (color[0], color[1], color[2], 255-my_round(i2))
    dots.append(((buf_x, buf_y), tmp_color1))
    tmp_color2 = (color[0], color[1], color[2], 255-my_round(i1))
    dots.append(((buf_x, buf_y), tmp_color2))
    return px


def rfpart(x):
    return 1 - fpart(x)


def algo_wu(dot1, dot2, color, stepping=0):
    if dot1[0] == dot2[0] and dot1[1] == dot2[1]:
        if stepping: 
            return [(dot1, color)],1
        return [(dot1, color)]
    x_start, y_start, x_end, y_end = dot1[0], dot1[1], dot2[0], dot2[1]
    dx, dy = dot2[0]-dot1[0], dot2[1]-dot1[1]
    steep = abs(dy) > abs(dx)
    if steep:
        x_start, y_start, x_end, y_end, dx, dy = y_start, x_start, y_end, x_end, dy, dx
    if x_end < x_start:
        x_start, x_end, y_start, y_end = x_end, x_start, y_end, y_start
    m = dy/dx
    intery = y_start + rfpart(x_start)*m
    dots = []
    x_s = get_endpoint(x_start, y_start, dots, m, color, steep) + 1
    x_e = get_endpoint(x_end, y_end, dots, m, color, steep)
    stairs = []
    curr_stair_len = 1
    for x in range(x_s, x_e):
        y = int(intery)
        i1 = rfpart(intery)*255
        i2 = fpart(intery)*255
        if steep:
            tmp_color1 = (color[0], color[1], color[2], 255-my_round(i2))
            dots.append(((y, x), tmp_color1))
            tmp_color2 = (color[0], color[1], color[2], 255-my_round(i1))
            dots.append(((y+1, x), tmp_color2))
        else:
            tmp_color1 = (color[0], color[1], color[2], 255-my_round(i2))
            dots.append(((x, y), tmp_color1))
            tmp_color2 = (color[0], color[1], color[2], 255-my_round(i1))
            dots.append(((x, y+1), tmp_color2))
        curr_stair_len += 1
        if abs(int(intery + m) - int(intery)):
            stairs.append(curr_stair_len)
            curr_stair_len = 0
        else:
            if x == x_e - 1:
                stairs.append(curr_stair_len)
        intery += m
    if stepping:
        return dots, len(stairs)
    else:
        return dots
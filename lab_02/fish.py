
import math


class Fish():

    def __init__(self,):
        self.body_x, self.body_y = self.ellipse_create(
            a=15, b=5, dx=0, dy=0, dots=1000)
        self.head_x, self.head_y = self.ellipse_create(
            a=2, b=2, dx=-12, dy=0, dots=100)
        self.eye_x, self.eye_y = self.ellipse_create(
            a=0.3, b=0.3, dx=-13, dy=0.5, dots=100)
        self.mouth_x, self.mouth_y = [-13.0, -11.0], [-1.0, -1.0]
        self.upper_fin_x, self.upper_fin_y = [-4.0,
                                              0.0, 8.0, 4.0], [4.0, 8.0, 8.0, 4.0]
        self.bottom_fin_x, self.bottom_fin_y = [-4.0,
                                                0.0, 8.0, 4.0], [-4.0, -8.0, -8.0, -4.0]
        self.tail_x, self.tail_y = [12.0, 16.0, 18.0, 17.0, 18.0, 16.0, 14.0, 12.0], [
            2.0, 6.0, 6.0, 0.0, -2.0, -6.0, -6.0, -2.0]

    def ellipse_create(self, a, b, dx, dy, dots):
        x_arr = []
        y_arr = []
        for i in range(dots+1):
            x = -a+2*a*i/dots
            y = math.sqrt((1 - x*x / (a*a))*b*b)
            x = x + dx
            y = y + dy
            x_arr.append(x)
            y_arr.append(y)
        for i in range(dots+1):
            x = a-2*a*i/dots
            y = math.sqrt((1 - x*x / (a*a))*b*b)
            x = x + dx
            y = -y + dy
            x_arr.append(x)
            y_arr.append(y)
        return x_arr, y_arr

    def move(self, dx, dy):
        for i in range(len(self.body_x)):
            self.body_x[i], self.body_y[i] = self.body_x[i] + \
                dx, self.body_y[i]+dy
        for i in range(len(self.head_x)):
            self.head_x[i], self.head_y[i] = self.head_x[i] + \
                dx, self.head_y[i]+dy
        for i in range(len(self.eye_x)):
            self.eye_x[i], self.eye_y[i] = self.eye_x[i]+dx, self.eye_y[i]+dy
        for i in range(len(self.mouth_x)):
            self.mouth_x[i], self.mouth_y[i] = self.mouth_x[i] + \
                dx, self.mouth_y[i]+dy
        for i in range(len(self.upper_fin_x)):
            self.upper_fin_x[i], self.upper_fin_y[i] = self.upper_fin_x[i] + \
                dx, self.upper_fin_y[i]+dy
        for i in range(len(self.bottom_fin_x)):
            self.bottom_fin_x[i], self.bottom_fin_y[i] = self.bottom_fin_x[i] + \
                dx, self.bottom_fin_y[i]+dy
        for i in range(len(self.tail_x)):
            self.tail_x[i], self.tail_y[i] = self.tail_x[i] + \
                dx, self.tail_y[i]+dy

    def copy(self):
        copy = Fish()
        copy.body_x = self.body_x.copy()
        copy.body_y = self.body_y.copy()
        copy.head_x = self.head_x.copy()
        copy.head_y = self.head_y.copy()
        copy.eye_x = self.eye_x.copy()
        copy.eye_y = self.eye_y.copy()
        copy.mouth_x = self.mouth_x.copy()
        copy.mouth_y = self.mouth_y.copy()
        copy.upper_fin_x = self.upper_fin_x.copy()
        copy.upper_fin_y = self.upper_fin_y.copy()
        copy.bottom_fin_x = self.bottom_fin_x.copy()
        copy.bottom_fin_y = self.bottom_fin_y.copy()
        copy.tail_x = self.tail_x.copy()
        copy.tail_y = self.tail_y.copy()
        return copy

    def scale(self, center_x, center_y, kx, ky):
        for i in range(len(self.body_x)):
            self.body_x[i], self.body_y[i] = self.body_x[i]*kx + \
                center_x*(1-kx), self.body_y[i]*ky+center_y*(1-ky)
        for i in range(len(self.head_x)):
            self.head_x[i], self.head_y[i] = self.head_x[i]*kx + \
                center_x*(1-kx), self.head_y[i]*ky+center_y*(1-ky)
        for i in range(len(self.eye_x)):
            self.eye_x[i], self.eye_y[i] = self.eye_x[i]*kx + \
                center_x*(1-kx), self.eye_y[i]*ky+center_y*(1-ky)
        for i in range(len(self.mouth_x)):
            self.mouth_x[i], self.mouth_y[i] = self.mouth_x[i] * \
                kx+center_x*(1-kx), self.mouth_y[i]*ky+center_y*(1-ky)
        for i in range(len(self.upper_fin_x)):
            self.upper_fin_x[i], self.upper_fin_y[i] = self.upper_fin_x[i] * \
                kx+center_x*(1-kx), self.upper_fin_y[i]*ky+center_y*(1-ky)
        for i in range(len(self.bottom_fin_x)):
            self.bottom_fin_x[i], self.bottom_fin_y[i] = self.bottom_fin_x[i] * \
                kx+center_x*(1-kx), self.bottom_fin_y[i]*ky+center_y*(1-ky)
        for i in range(len(self.tail_x)):
            self.tail_x[i], self.tail_y[i] = self.tail_x[i]*kx + \
                center_x*(1-kx), self.tail_y[i]*ky+center_y*(1-ky)

    def rotate(self, center_x, center_y, angle):
        angle = math.pi * angle / 180
        for i in range(len(self.body_x)):
            x = self.body_x[i]
            y = self.body_y[i]
            self.body_x[i] = center_x+(x - center_x) * \
                math.cos(angle)-(y-center_y)*math.sin(angle)
            self.body_y[i] = center_y+(x - center_x) * \
                math.sin(angle)+(y-center_y)*math.cos(angle)
        for i in range(len(self.head_x)):
            x = self.head_x[i]
            y = self.head_y[i]
            self.head_x[i] = center_x+(x - center_x) * \
                math.cos(angle)-(y-center_y)*math.sin(angle)
            self.head_y[i] = center_y+(x - center_x) * \
                math.sin(angle)+(y-center_y)*math.cos(angle)
        for i in range(len(self.eye_x)):
            x = self.eye_x[i]
            y = self.eye_y[i]
            self.eye_x[i] = center_x+(x - center_x) * \
                math.cos(angle)-(y-center_y)*math.sin(angle)
            self.eye_y[i] = center_y+(x - center_x) * \
                math.sin(angle)+(y-center_y)*math.cos(angle)
        for i in range(len(self.mouth_x)):
            x = self.mouth_x[i]
            y = self.mouth_y[i]
            self.mouth_x[i] = center_x+(x - center_x) * \
                math.cos(angle)-(y-center_y)*math.sin(angle)
            self.mouth_y[i] = center_y+(x - center_x) * \
                math.sin(angle)+(y-center_y)*math.cos(angle)
        for i in range(len(self.upper_fin_x)):
            x = self.upper_fin_x[i]
            y = self.upper_fin_y[i]
            self.upper_fin_x[i] = center_x+(x - center_x) * \
                math.cos(angle)-(y-center_y)*math.sin(angle)
            self.upper_fin_y[i] = center_y+(x - center_x) * \
                math.sin(angle)+(y-center_y)*math.cos(angle)
        for i in range(len(self.bottom_fin_x)):
            x = self.bottom_fin_x[i]
            y = self.bottom_fin_y[i]
            self.bottom_fin_x[i] = center_x+(x - center_x) * \
                math.cos(angle)-(y-center_y)*math.sin(angle)
            self.bottom_fin_y[i] = center_y+(x - center_x) * \
                math.sin(angle)+(y-center_y)*math.cos(angle)
        for i in range(len(self.tail_x)):
            x = self.tail_x[i]
            y = self.tail_y[i]
            self.tail_x[i] = center_x+(x - center_x) * \
                math.cos(angle)-(y-center_y)*math.sin(angle)
            self.tail_y[i] = center_y+(x - center_x) * \
                math.sin(angle)+(y-center_y)*math.cos(angle)

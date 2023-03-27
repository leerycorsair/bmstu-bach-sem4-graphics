from circle_algos import *
from drawing import Dot



def create_circle(data: dict, method_id: int) -> None:
    if method_id == 0:
        dots = circle_general(data["x"], data["y"], data["r"])
    if method_id == 1:
        dots = circle_param(data["x"], data["y"], data["r"])
    if method_id == 2:
        dots = circle_bresenham(data["x"], data["y"], data["r"])
    if method_id == 3:
        dots = circle_middle(data["x"], data["y"], data["r"])
    return dots


def circle_regulate(data):
    if data["r0"] > data["r1"]:
        data["r0"], data["r1"] = data["r1"], data["r0"]
    return data


def circle_step(data):
    if data["r0"] + data["st"] > data["r1"]:
        data["r0"] = data["r1"]
    else:
        data["r0"] += data["st"]
    return data

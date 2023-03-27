from ellipse_algos import *
from drawing import Dot


def create_ellipse(data: dict, method_id: int) -> list[Dot]:
    if method_id == 0:
        dots = ellipse_general(data["x"], data["y"], data["a"], data["b"])
    if method_id == 1:
        dots = ellipse_param(data["x"], data["y"], data["a"], data["b"])
    if method_id == 2:
        dots = ellipse_bresenham(data["x"], data["y"], data["a"], data["b"])
    if method_id == 3:
        dots = ellipse_middle(data["x"], data["y"], data["a"], data["b"])
    return dots


def ellipse_regulate(data):
    data["b_st"] = data["b0"] / data["a0"] * data["st"]
    data["b1"] = data["a1"] / data["a0"] * data["b0"]
    if data["a0"] > data["a1"]:
        data["a0"], data["a1"] = data["a1"], data["a0"]
        data["b0"], data["b1"] = data["b1"], data["b0"]
    return data


def ellipse_step(data):
    if data["a0"] + data["st"] > data["a1"]:
        data["b0"] = data["b1"]
        data["a0"] = data["a1"]
    else:
        data["a0"] += data["st"]
        data["b0"] += data["b_st"]
    return data
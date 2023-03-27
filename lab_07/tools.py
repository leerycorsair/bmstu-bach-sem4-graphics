def swapper(ent1, ent2) -> tuple:
    ent1, ent2 = ent2, ent1
    return ent1, ent2


def round(num: float) -> int:
    return int(num + (0.5 if num > 0 else -0.5))
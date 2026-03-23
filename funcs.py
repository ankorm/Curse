import math

def my1prog(a: float, b: float) -> tuple[float, float]:
    """
    Вычисляет величины e и f на основе входных параметров a и b.
    Параметры:
        a (float), b (float)  — аргументы
    Возвращает:
        tuple (e, f) — два вычисленных значения.
    """
    c: float = 3.5
    d: float = a / c * math.cos(b)
    e: float = a * (c * math.sin(b) + math.cos(math.pi - b))
    f: float = e / d
    return e, f


def f(x):
    return x / (4 + x**2)


def simpson(f, a, b, n):
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        x = a + i * h
        s += 4 * f(x) if i % 2 else 2 * f(x)
    return s * h / 3


def trapezonial(f, a, b, n):
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        x = a + i * h
        s += 2 * f(x)
    return s * h / 2


if __name__ == "__main__":
    result1 = trapezonial(f, 0, 1, 8)
    result2 = simpson(f, 0, 1, 8)
    print(result1)
    print(result2)

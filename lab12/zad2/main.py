import numpy as np


def f2(x):
    return 1 / (x ** 3 - 2 * x - 5)


def composite_simpsons_rule(xs, ys):
    h = [xs[i + 1] - xs[i] for i in range(0, len(xs) - 1)]
    sum = 0.0
    for i in range(1, len(xs) - 1, 2):
        sum += (h[i] + h[i - 1]) / 6.0 * (
                    (2 - h[i] / h[i - 1]) * ys[i - 1] + (h[i] + h[i - 1]) ** 2 / (h[i] * h[i - 1])*ys[i] + (
                        2 - h[i - 1] / h[i]) * ys[i + 1])
    if len(xs) % 2 == 0:
        alfa = (2 * (h[-1] ** 2) + 3 * h[-1] * h[-2]) / (6.0 * (h[-1] + h[-2]))
        beta = ((h[-1] ** 2) + 3 * h[-1] * h[-2]) / (6.0 * h[-2])
        eta = (h[-1] ** 3) / (6.0 * h[-2] * (h[-1] + h[-2]))
        sum += alfa * ys[-1] + beta * ys[-2] - eta * ys[-3]
    return sum


if __name__ == '__main__':
    xs = np.linspace(1, 2, 1000000)
    ys = [f2(x) for x in xs]
    print(composite_simpsons_rule(xs, ys))

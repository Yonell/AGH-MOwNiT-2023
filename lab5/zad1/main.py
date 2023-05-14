import matplotlib.lines
import mpl_toolkits.mplot3d.axes3d as p3
from matplotlib import pyplot as plt
import numpy as np
from math import cos, sin, pi as PI
import random


def a():
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    points_am = 20
    for si in range(0, points_am, 1):
        s = si * 2 * PI / points_am
        for ti in range(0, points_am, 1):
            t = ti * 2 * PI / points_am
            x = cos(s) * sin(t)
            y = sin(s) * sin(t)
            z = cos(t)
            ax.scatter(x, y, z, s=1, color='black')
    plt.show()


def b():
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    points_am = 20
    sphere = [[0.0 for _ in range(points_am*points_am)] for _ in range(3)]
    it = 0
    for si in range(0, points_am, 1):
        s = si * 2 * PI / points_am
        for ti in range(0, points_am, 1):
            t = ti * 2 * PI / points_am
            sphere[0][it] = (cos(s) * sin(t))
            sphere[1][it] = (sin(s) * sin(t))
            sphere[2][it] = (cos(t))
            ax.scatter(sphere[0][it], sphere[1][it], sphere[2][it], s=1, color='black')
            it += 1

    sphere = np.matrix(sphere)
    A1 = np.matrix(
        [[random.random() for _ in range(3)] for _ in range(3)]
    )
    A2 = np.matrix(
        [[random.random() for _ in range(3)] for _ in range(3)]
    )
    A3 = np.matrix(
        [[random.random() for _ in range(3)] for _ in range(3)]
    )
    el1 = np.matmul(A1, sphere)
    el2 = np.matmul(A2, sphere)
    el3 = np.matmul(A3, sphere)
    ax.scatter(el1[0], el1[1], el1[2], s=1, color='red')
    ax.scatter(el2[0], el2[1], el2[2], s=1, color='green')
    ax.scatter(el3[0], el3[1], el3[2], s=1, color='blue')
    plt.show()
    return sphere, A1, A2, A3, el1, el2, el3

def c(sphere, A1, A2, A3, el1, el2, el3):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    u1, s1, vh1 = np.linalg.svd(A1)
    u2, s2, vh2 = np.linalg.svd(A2)
    u3, s3, vh3 = np.linalg.svd(A3)
    ax.scatter(sphere[0], sphere[1], sphere[2], s=1, color='black')
    ax.scatter(el1[0], el1[1], el1[2], s=1, color='red')
    ax.scatter(el2[0], el2[1], el2[2], s=1, color='green')
    ax.scatter(el3[0], el3[1], el3[2], s=1, color='blue')
    ax.add_line(matplotlib.lines.Line3D([0, u1[0, 0]], [0, u1[1, 0]], [0, u1[2, 0]], color='red'))


if __name__ == '__main__':
    a()
    sphere, A1, A2, A3, el1, el2, el3 = b()
    c(sphere, A1, A2, A3, el1, el2, el3)

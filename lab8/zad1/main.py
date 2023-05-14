import numpy as np
import matplotlib.pyplot as plt



if __name__ == '__main__':
    size = 10000
    d = 0.95
    a = np.random.choice([0, 1], size=(size, size), p = [0.99, 0.01])
    delimit = np.linalg.norm(a, axis = 0)
    a = a/delimit
    r = np.ones(size)
    while True:
        ry = d * a @ r
        ry = ry/np.linalg.norm(ry)
        if np.allclose(ry, r):
            r = ry
            break
        r = ry
    plt.hist(r)
    plt.show()

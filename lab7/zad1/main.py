import numpy as np

def find_the_vector(A):
    x = np.array([1]*A.shape[1])
    while True:
        y = A@x
        y = y/np.linalg.norm(y)
        if np.allclose(x, y):
            break
        x = y
    x_abs = np.abs(x)
    max_index = np.argmax(x_abs)
    return x[max_index], x/np.linalg.norm(x)

if __name__ == "__main__":
    size = 3
    A = np.random.rand(size,size)
    Bmy = find_the_vector(A)
    print(Bmy)
    Blib = np.linalg.eig(A)
    print(Blib)
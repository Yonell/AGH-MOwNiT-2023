import numpy as np

def find_the_vector(A):
    x = np.array([1]*A.shape[1])
    while True:
        y = A@x
        if y[0] < 0:
            y = -y
        y = y/np.linalg.norm(y)
        if np.allclose(x, y):
            break
        x = y
    x_abs = np.abs(x)
    max_index = np.argmax(x_abs)
    return x[max_index], x/np.linalg.norm(x)

def find_the_eigenvalue(A, sigma):
    A_transformed = np.linalg.inv(A - sigma*np.eye(A.shape[0]))
    x, y = find_the_vector(A_transformed)
    return y

if __name__ == '__main__':
    size = 3
    A = np.random.rand(size,size)
    Bmy = find_the_eigenvalue(A, 0.5)
    print(Bmy)
    Blib = np.linalg.eig(A)
    print(Blib)
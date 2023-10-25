import numpy as np
import scipy as scipy


def f4(x,y):
    return 1/(np.sqrt(x+y)*(1+x+y)) if x >0 and y > 0 and x<=1 and y<=1-x else 0

def integrate_2_trapeze_method(f, a, b, ay, by, n):
    sum = 0.0
    linspace = np.linspace(a, b, n)
    linspace2 = np.linspace(ay, by, n)
    for i in range(0, n-1):
        for j in range(0, n-1):
            sum += (linspace[i+1] - linspace[i]) * (linspace2[j+1] - linspace2[j]) * f(linspace[i], linspace2[j])

    return sum



if __name__ == '__main__':
    print(scipy.integrate.dblquad(f4, 0, 1, 0, 1))
    print(integrate_2_trapeze_method(f4, 0, 1, 0, 1, 1000))
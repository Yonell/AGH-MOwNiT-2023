import random
import math
import matplotlib.pyplot
import matplotlib.lines


def generate_n_points(n, distribution="uniform", maxx=10, maxy=10):
    result = []
    if distribution == "uniform":
        for _ in range(n):
            result.append((random.random() * maxx, random.random() * maxy))
    elif distribution == "normal":
        for _ in range(n):
            result.append((random.normalvariate(0, maxx), random.normalvariate(0, maxy)))
    elif distribution == "nine_groups":
        groups_coords = [(random.random() * maxx, random.random() * maxy) for _ in range(9)]
        for _ in range(n):
            group = int(random.random() * 9)
            result.append((random.normalvariate(groups_coords[group][0], maxx / 50),
                           random.normalvariate(groups_coords[group][1], maxy / 50)))
    return result


def temp1(i):
    return ((990 / 1000) ** i) ** (1 / 10)


def temp2(i):
    it = 12500
    result = 1 - (i / it)
    if result < 0:
        return 0
    if result > 1:
        return 1
    return result


def temp3(i):
    it = 20000
    try:
        result = (math.log(-i + it, 10) + 2) / (math.log(it, 10) + 2)
    except ArithmeticError:
        return 0
    else:
        if result > 1:
            return 1
        return result ** 4


def path_length(permutation, cities):
    result_sum = 0
    for i in range(len(permutation) - 1):
        result_sum += math.sqrt((cities[permutation[i]][0] - cities[permutation[i + 1]][0]) ** 2 + (
                cities[permutation[i]][1] - cities[permutation[i + 1]][1]) ** 2)
    return result_sum


def find_the_best_solution(cities, temp_func=temp1, max_iter=1000, consecutive=False, y=None):
    if y is None:
        y = []
    y.clear()
    n = len(cities)
    permutation = [i for i in range(n)]
    random.shuffle(permutation)
    best_length = (path_length(permutation, cities), permutation.copy())
    for i in range(max_iter):
        if consecutive:
            a_swap = b_swap = n
            while b_swap == n:
                a_swap = (math.floor(random.random() * (n - 1)))
                b_swap = a_swap + 1
        else:
            a_swap = b_swap = n
            while (a_swap == n) or (b_swap == n):
                a_swap = (math.floor(random.random() * (n - 1)))
                b_swap = (math.floor(random.random() * (n - 1)))
        before_swap = path_length(permutation, cities)
        permutation[a_swap], permutation[b_swap] = permutation[b_swap], permutation[a_swap]
        after_swap = path_length(permutation, cities)
        if before_swap > after_swap:
            if best_length[0] > after_swap:
                best_length = (after_swap, permutation.copy())
        else:
            if random.random() > temp_func(i):
                permutation[a_swap], permutation[b_swap] = permutation[b_swap], permutation[a_swap]
        y.append(path_length(permutation, cities))
    return best_length[1]


def perform_tests(ax1, ax2, cities_count, distribution_type="uniform", maxx=20, maxy=20, temp_func=temp1, max_iter=1000,
                  consecutive=False, cities=None):
    if cities is None:
        cities = generate_n_points(cities_count, distribution_type, maxx, maxy)
    y = []
    permutation = find_the_best_solution(cities, temp_func=temp_func, max_iter=max_iter, consecutive=consecutive, y=y)
    ax1.scatter([i for i in range(max_iter)], y)
    ax2.plot([cities[i][0] for i in permutation], [cities[i][1] for i in permutation], 'C3', lw=3)
    ax2.scatter([cities[i][0] for i in permutation], [cities[i][1] for i in permutation], s=120, zorder=2.5)


def a():
    fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = matplotlib.pyplot.subplots(3, 2, figsize=(10, 12))
    fig.suptitle('Wizualizacja rozwiązania dla 3 różnych wartości n', fontsize=16)

    ax1.set_title("Funkcja energii w zależności od iteracji\nn=5")
    ax2.set_title("Wizualizacja rozwiązania\n")
    perform_tests(ax1, ax2, 5, "uniform", 20, 20, temp1, 10000, False)

    ax3.set_title("n = 30")
    perform_tests(ax3, ax4, 30, "uniform", 20, 20, temp1, 10000, False)

    ax5.set_title("n = 100")
    perform_tests(ax5, ax6, 100, "uniform", 20, 20, temp1, 10000, False)

    matplotlib.pyplot.show()

    fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = matplotlib.pyplot.subplots(3, 2, figsize=(10, 12))
    fig.suptitle('Wizualizacja rozwiązania dla 3 różnych rozkładów', fontsize=16)

    ax1.set_title("Funkcja energii w zależności od iteracji\nRokład jednostajny")
    ax2.set_title("Wizualizacja rozwiązania\n")
    perform_tests(ax1, ax2, 100, "uniform", 20, 20, temp1, 10000, False)

    ax3.set_title("Rozkład normalny")
    perform_tests(ax3, ax4, 100, "normal", 20, 20, temp1, 10000, False)

    ax5.set_title("Rozkład w 9 grupach")
    perform_tests(ax5, ax6, 100, "nine_groups", 20, 20, temp1, 10000, False)

    matplotlib.pyplot.show()


def b():
    fig, ((ax1, ax2), (ax3, ax4)) = matplotlib.pyplot.subplots(2, 2, figsize=(10, 8))
    fig.suptitle('Wizualizacja rozwiązania dla zamian sąsiednich i losowych', fontsize=16)
    ax1.set_title("Funkcja energii w zależności od iteracji\nSąsiednie (consecutive swap)")

    ax2.set_title("Wizualizacja rozwiązania\n")
    perform_tests(ax1, ax2, 100, "uniform", 20, 20, temp1, 10000, True)

    ax3.set_title("Losowe (arbitrary)")
    perform_tests(ax3, ax4, 100, "uniform", 20, 20, temp1, 10000, False)

    matplotlib.pyplot.show()
    fig, ((ax1, ax2, ax7), (ax3, ax4, ax8), (ax5, ax6, ax9)) = matplotlib.pyplot.subplots(3, 3, figsize=(12, 12))
    fig.suptitle('Wizualizacja rozwiązania dla temp1 i temp2', fontsize=16)

    ax1.set_title("Funkcja energii w zależności od iteracji\ntemp1")
    ax2.set_title("Wizualizacja rozwiązania\n")
    iteracji = 20000
    perform_tests(ax1, ax2, 100, "uniform", 20, 20, temp1, iteracji, False)

    ax3.set_title("temp2")
    perform_tests(ax3, ax4, 100, "uniform", 20, 20, temp2, iteracji, False)

    ax3.set_title("temp3")
    perform_tests(ax5, ax6, 100, "uniform", 20, 20, temp3, iteracji, False)

    ax7.set_title("Funkcja temperatury\nT1(i)")
    ax7.scatter([i for i in range(iteracji)], [temp1(i) for i in range(iteracji)])
    ax8.set_title("T2(i)")
    ax8.scatter([i for i in range(iteracji)], [temp2(i) for i in range(iteracji)])
    ax9.set_title("T2(i)")
    ax9.scatter([i for i in range(iteracji)], [temp3(i) for i in range(iteracji)])

    matplotlib.pyplot.show()


if __name__ == '__main__':
    a()
    b()
    # c jest zrobione w a i b


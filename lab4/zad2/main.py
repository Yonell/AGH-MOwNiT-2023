import random
from PIL import Image
from matplotlib import pyplot as plt
from math import log, sqrt
import time
import multiprocessing


def temp1(iteration, it=700):
    return (990 / 1000) ** (iteration / 700)


def temp2(iteration, it=700):
    it = it * 3 / 4
    result = 1 - (iteration / it)
    if result <= 0:
        return 0
    if result > 1:
        return 1
    return result


def temp3(iteration, it=700):
    it = it * 3 / 4
    if it <= 0:
        return 0
    if -iteration + it <= 0:
        return 0
    result = (log(-iteration + it, 10) + 2) / (log(it, 10) + 2)
    if result > 1:
        return 1
    return result ** 10


def get_4_neighbours(board, x, y):
    result = []
    if x > 0:
        result.append((x - 1, y))
    if x < len(board) - 1:
        result.append((x + 1, y))
    if y > 0:
        result.append((x, y - 1))
    if y < len(board[0]) - 1:
        result.append((x, y + 1))
    return result


def get_8_neighbours(board, x, y):
    result = get_4_neighbours(board, x, y)
    if x > 0:
        if y > 0:
            result.append((x - 1, y - 1))
        if y < len(board[0]) - 1:
            result.append((x - 1, y + 1))
    if x < len(board) - 1:
        if y > 0:
            result.append((x + 1, y - 1))
        if y < len(board[0]) - 1:
            result.append((x + 1, y + 1))
    return result


def get_16_neighbours(board, x, y):
    result = get_8_neighbours(board, x, y)
    if x > 1:
        result.append((x - 2, y))
    if x < len(board) - 2:
        result.append((x + 2, y))
    if y > 1:
        result.append((x, y - 2))
    if y < len(board[0]) - 2:
        result.append((x, y + 2))
    if x > 1:
        if y > 1:
            result.append((x - 2, y - 2))
        if y < len(board[0]) - 2:
            result.append((x - 2, y + 2))
    if x < len(board) - 2:
        if y > 1:
            result.append((x + 2, y - 2))
        if y < len(board[0]) - 2:
            result.append((x + 2, y + 2))
    return result


def get_24_neighbours(board, x, y):
    result = get_16_neighbours(board, x, y)
    if x > 1:
        if y > 0:
            result.append((x - 2, y - 1))
        if y < len(board[0]) - 1:
            result.append((x - 2, y + 1))
    if x < len(board) - 2:
        if y > 0:
            result.append((x + 2, y - 1))
        if y < len(board[0]) - 1:
            result.append((x + 2, y + 1))
    if y > 1:
        if x > 0:
            result.append((x - 1, y - 2))
        if x < len(board) - 1:
            result.append((x + 1, y - 2))
    if y < len(board[0]) - 2:
        if x > 0:
            result.append((x - 1, y + 2))
        if x < len(board) - 1:
            result.append((x + 1, y + 2))
    return result


def get_neighbours_within(board, x, y, r=5):
    result = []
    for i in range(max(0, x - r), min(len(board), x + r + 1)):
        for j in range(max(0, y - r), min(len(board[0]), y + r + 1)):
            if (i != x) or (j != y):
                if sqrt((i - x) ** 2 + (j - y) ** 2) <= r:
                    result.append((i, j))
    # if (y == 0):
    # print(str(x) + " " + str(y))
    return result


def cross_neighbours(board, x, y, r=3):
    result = []
    for i in range(max(0, x - r), min(len(board), x + r + 1)):
        for j in range(max(0, y - r), min(len(board[0]), y + r + 1)):
            if (i != x) or (j != y):
                if abs(i - x <= 1) or abs(j - y <= 1):
                    result.append((i, j))
    return result


def cross_energy_func(board, x, y, neighbours_lookup):
    neighbours = neighbours_lookup[x][y]
    suma = 0
    for i in neighbours:
        if i[0] == x or i[1] == y:
            suma += (-1 if board[i[0]][i[1]] == board[x][y] else 1)
        else:
            suma += (1 if board[i[0]][i[1]] == board[x][y] else -1)
    return suma


def crystal_cell_energy_func(board, x, y, neighbours_lookup):
    neighbours = neighbours_lookup[x][y]
    suma = 0
    for i in neighbours:
        chebyshev = max(abs(x - i[0]), abs(y - i[1]))
        suma += (-1 if (board[i[0]][i[1]] == board[x][y]) ^ (chebyshev == 1) else 1)
    return suma


def we_like_similar_cell_energy_func(board, x, y, neighbours_lookup):
    neighbours = neighbours_lookup[x][y]
    suma = 0
    for i in neighbours:
        suma += (-1 if board[i[0]][i[1]] == board[x][y] else 1)
    return suma


def return_board_image(board):
    image = Image.new('RGB', (len(board), len(board[0])), color='white')
    for x_image in range(len(board)):
        for y_image in range(len(board[0])):
            if board[x_image][y_image] == 1:
                image.putpixel((x_image, y_image), (0, 0, 0))
    return image


def get_swap_coords(board, consecutive, neighbours_lookup, width, height):
    if consecutive:
        a_x_swap = random.randint(0, width - 1)
        a_y_swap = random.randint(0, height - 1)
        neighbours = neighbours_lookup[a_x_swap][a_y_swap]
        random_neighbour = neighbours[random.randint(0, len(neighbours) - 1)]
        b_x_swap = random_neighbour[0]
        b_y_swap = random_neighbour[1]
        return a_x_swap, a_y_swap, b_x_swap, b_y_swap
    else:
        a_x_swap = random.randint(0, width - 1)
        a_y_swap = random.randint(0, height - 1)
        b_x_swap = random.randint(0, width - 1)
        b_y_swap = random.randint(0, height - 1)
    while (board[a_x_swap][a_y_swap] == board[b_x_swap][b_y_swap]):
        if consecutive:
            a_x_swap = random.randint(0, width - 1)
            a_y_swap = random.randint(0, height - 1)
            neighbours = neighbours_lookup[a_x_swap][a_y_swap]
            random_neighbour = neighbours[random.randint(0, len(neighbours) - 1)]
            b_x_swap = random_neighbour[0]
            b_y_swap = random_neighbour[1]
        else:
            a_x_swap = random.randint(0, width - 1)
            a_y_swap = random.randint(0, height - 1)
            b_x_swap = random.randint(0, width - 1)
            b_y_swap = random.randint(0, height - 1)
    return a_x_swap, a_y_swap, b_x_swap, b_y_swap


def minimize_energy_AS(starting_board, get_neighbours, cell_energy_func, max_iter=1000, temp_func=temp1,
                       consecutive=False, energy_values=None, swaps_at_a_time=1):
    neighbours_lookup = [[[] for i in range(len(starting_board[0]))] for j in range(len(starting_board))]
    for i in range(len(starting_board)):
        for j in range(len(starting_board[0])):
            neighbours_lookup[i][j] = get_neighbours(starting_board, i, j)
    neighbours_for_lookup = [[[] for i in range(len(starting_board[0]))] for j in range(len(starting_board))]
    for i in range(len(starting_board)):
        for j in range(len(starting_board[0])):
            for k in neighbours_lookup[i][j]:
                neighbours_for_lookup[k[0]][k[1]].append((i, j))
    cells_energy = [[cell_energy_func(starting_board, j, i, neighbours_lookup)
                     for i in range(len(starting_board[0]))]
                    for j in range(len(starting_board))]

    if energy_values is None:
        energy_values = []
    gif = []
    energy_values.clear()
    width = len(starting_board[0])
    height = len(starting_board)

    best_energy = (sum([sum(row) for row in cells_energy]), [row[:] for row in starting_board])

    for iteration in range(max_iter):
        swaps = []
        for swap_id in range(swaps_at_a_time):
            swaps.append(get_swap_coords(starting_board, consecutive, neighbours_lookup, width, height))

        before_energy = sum([sum(row) for row in cells_energy])

        for a_x_swap, a_y_swap, b_x_swap, b_y_swap in swaps:
            starting_board[a_x_swap][a_y_swap], starting_board[b_x_swap][b_y_swap] = starting_board[b_x_swap][b_y_swap], \
                starting_board[a_x_swap][a_y_swap]
            for i in neighbours_for_lookup[a_x_swap][a_y_swap]:
                cells_energy[i[0]][i[1]] = cell_energy_func(starting_board, i[0], i[1], neighbours_lookup)
            for i in neighbours_for_lookup[b_x_swap][b_y_swap]:
                cells_energy[i[0]][i[1]] = cell_energy_func(starting_board, i[0], i[1], neighbours_lookup)
            cells_energy[a_x_swap][a_y_swap] = cell_energy_func(starting_board, a_x_swap, a_y_swap, neighbours_lookup)
            cells_energy[b_x_swap][b_y_swap] = cell_energy_func(starting_board, b_x_swap, b_y_swap, neighbours_lookup)

        after_energy = sum([sum(row) for row in cells_energy])

        if after_energy <= before_energy:
            if after_energy < best_energy[0]:
                best_energy = (after_energy, [row[:] for row in starting_board])
        else:
            if random.random() > temp_func(iteration, max_iter):
                for swap_id in range(swaps_at_a_time - 1, -1, -1):
                    a_x_swap, a_y_swap, b_x_swap, b_y_swap = swaps[swap_id]
                    starting_board[a_x_swap][a_y_swap], starting_board[b_x_swap][b_y_swap] = starting_board[b_x_swap][
                        b_y_swap], starting_board[a_x_swap][a_y_swap]
                    for i in neighbours_for_lookup[a_x_swap][a_y_swap]:
                        cells_energy[i[0]][i[1]] = cell_energy_func(starting_board, i[0], i[1], neighbours_lookup)
                    for i in neighbours_for_lookup[b_x_swap][b_y_swap]:
                        cells_energy[i[0]][i[1]] = cell_energy_func(starting_board, i[0], i[1], neighbours_lookup)
                    cells_energy[a_x_swap][a_y_swap] = cell_energy_func(starting_board, a_x_swap, a_y_swap,
                                                                        neighbours_lookup)
                    cells_energy[b_x_swap][b_y_swap] = cell_energy_func(starting_board, b_x_swap, b_y_swap,
                                                                        neighbours_lookup)
            else:
                pass

        energy_values.append(sum([sum(row) for row in cells_energy]))

        if iteration % 100 == 0:
            # print(iteration)
            image = return_board_image(starting_board)
            gif.append(image)
    return starting_board, gif


def save_images(board_arg, energy_values, gif_imgs, delta_value, temtype, energytype, iter_count, consecutive,
                neighbours, swaps_at_a_time):
    name = 'd' + str(delta_value) + '_'
    if temtype == 0:
        name += 'custom_'
    if temtype == 1:
        name += 'fastcool_'
    elif temtype == 2:
        name += 'medcool_'
    elif temtype == 3:
        name += 'slowcool_'
    name += energytype + '_'
    name += str(iter_count) + 'iter_'
    if consecutive:
        name += 'consecutive_'
    else:
        name += 'nonconsecutive_'
    name += neighbours + "_"
    name += str(len(board_arg)) + 'res_'
    name += str(swaps_at_a_time) + 'saat'

    image = return_board_image(board_arg)

    image.save(name + '_board.png')

    plt.plot([i for i in range(len(energy_values))], energy_values)
    plt.savefig(name + '_energyplot.png')
    plt.close()

    if temtype == 1:
        plt.plot([i for i in range(iter_count)], [temp1(i, iter_count) for i in range(iter_count)])
    elif temtype == 2:
        plt.plot([i for i in range(iter_count)], [temp2(i, iter_count) for i in range(iter_count)])
    elif temtype == 3:
        plt.plot([i for i in range(iter_count)], [temp3(i, iter_count) for i in range(iter_count)])
    plt.savefig(name + '_tempplot.png')
    plt.close()

    gif_imgs[0].save(name + '_gif.gif', save_all=True, append_images=gif_imgs[1:], optimize=False, duration=10, loop=0)


def start_simulation_with_random_board(delta, board_res, iter_count, consecutive, neighbours_type, temp_type,
                                       energy_type, swaps_at_a_time, q):
    board = [[(1 if random.random() < delta else 0) for i in range(board_res)] for j in range(board_res)]
    y = []
    start = time.time()
    temp_func = temp1 if temp_type == 1 else temp2 if temp_type == 2 else temp3
    neighbours_func = get_neighbours_within if neighbours_type == 'within' else get_4_neighbours if neighbours_type == '4nei' else get_8_neighbours if neighbours_type == '8nei' else get_16_neighbours if neighbours_type == '16nei' else get_24_neighbours if neighbours_type == '24nei' else cross_neighbours
    energy_func = we_like_similar_cell_energy_func if energy_type == 'similar' else crystal_cell_energy_func if energy_type == 'crystal' else cross_energy_func if energy_type == 'cross' else None
    gif = []
    try:
        board, gif = minimize_energy_AS(board, neighbours_func, energy_func, max_iter=iter_count,
                                        temp_func=temp_func, consecutive=consecutive, energy_values=y,
                                        swaps_at_a_time=swaps_at_a_time)
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    print("Time elapsed: " + str(time.time() - start) + "s")
    # save_images(board, y, gif, delta, temp_type, energy_type, iter_count, consecutive, neighbours_type, swaps_at_a_time)
    q.put((board, y, gif, delta, temp_type, energy_type, iter_count, consecutive, neighbours_type, swaps_at_a_time))
    return True


def listener(q):
    while 1:
        m = q.get()
        if m == "kill":
            break
        save_images(m[0], m[1], m[2], m[3], m[4], m[5], m[6], m[7], m[8], m[9])


if __name__ == '__main__':
    # start_simulation_with_random_board(0.3, 256, 600000, True, 'within', 2, 'similar', 16)
    manager = multiprocessing.Manager()
    q = manager.Queue()
    pool = multiprocessing.Pool(multiprocessing.cpu_count() + 2)
    watcher = pool.apply_async(listener, (q,))

    result = []
    result.append(
        pool.apply_async(start_simulation_with_random_board, (0.1, 256, 600000, True, 'within', 2, 'similar', 12, q)))
    result.append(
        pool.apply_async(start_simulation_with_random_board, (0.2, 256, 600000, True, 'within', 2, 'similar', 12, q)))
    result.append(
        pool.apply_async(start_simulation_with_random_board, (0.3, 256, 600000, True, 'within', 2, 'similar', 12, q)))
    result.append(
        pool.apply_async(start_simulation_with_random_board, (0.5, 256, 600000, True, 'within', 2, 'similar', 12, q)))
    result.append(
        pool.apply_async(start_simulation_with_random_board, (0.5, 256, 600000, True, 'within', 1, 'crystal', 12, q)))
    result.append(
        pool.apply_async(start_simulation_with_random_board, (0.5, 256, 600000, True, 'within', 2, 'crystal', 12, q)))
    result.append(
        pool.apply_async(start_simulation_with_random_board, (0.5, 256, 600000, True, 'within', 3, 'crystal', 12, q)))
    result.append(
        pool.apply_async(start_simulation_with_random_board, (0.5, 256, 600000, True, 'cross', 3, 'cross', 12, q)))
    result.append(
        pool.apply_async(start_simulation_with_random_board, (0.3, 256, 600000, True, 'within', 1, 'similar', 12, q)))
    result.append(
        pool.apply_async(start_simulation_with_random_board, (0.3, 256, 600000, True, 'within', 3, 'similar', 12, q)))
    for i in result:
        i.wait()
    for i in result:
        print("Task ended successfully: " + str(i.get()))

    q.put("kill")
    watcher.wait()
    pool.close()
    pool.join()

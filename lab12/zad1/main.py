import numpy as np

def calculate_distance(timings=None, speed=None):
    if speed is None:
        speed = []
    if timings is None:
        timings = []
    if len(timings) != len(speed):
        return None
    if len(timings) == 0:
        return
    if len(timings) == 1:
        return speed[0] * timings[0]
    distance = 0
    for i in range(len(timings) - 1):
        distance += (speed[i]+speed[i+1]) * ((timings[i + 1] - timings[i])/3600)/2
    return distance











if __name__ == '__main__':
    timings = [i for i in range(0, 3600)]
    speed = [3 for i in range(0, 3600)]
    print(calculate_distance(timings, speed))

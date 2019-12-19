from pprint import pprint
import numpy


TIME_DELTA = 1e-3
EPS = 1e-2


def dps(matrix, probabilities):
    n = len(matrix)
    return [
        TIME_DELTA * sum(
            [
                probabilities[j] * (-sum(matrix[i]) + matrix[i][i])
                if i == j else
                probabilities[j] * matrix[j][i]
                for j in range(n)
            ]
        )
        for i in range(n)
    ]


def calc_limit_probabilities(matrix):
    n = len(matrix)
    return numpy.linalg.solve(
        [
            [
                -sum(matrix[i]) + matrix[i][i] if i == j else matrix[j][i]
                for j in range(n)
            ]
            if i != n - 1 else [1 for j in range(n)]
            for i in range(n)
        ],
        [0 if i != n - 1 else 1 for i in range(n)]
    ).tolist()


def calc_stabilization_times(matrix, start_probabilities, limit_probabilities):
    n = len(matrix)
    current_time = 0
    current_probabilities = start_probabilities.copy()
    stabilization_times = [0 for i in range(n)]
    for c in range(10000000):
        curr_dps = dps(matrix, current_probabilities)
        for i in range(n):
            if (
                    not stabilization_times[i] and
                    abs(current_probabilities[i] - limit_probabilities[i]) <= EPS and
                    curr_dps[i] <= EPS
            ):
                stabilization_times[i] = current_time
            current_probabilities[i] += curr_dps[i]
        if all(stabilization_times):
            break
        current_time = round(current_time + TIME_DELTA, 6)
    return stabilization_times


if __name__ == '__main__':
    start_probabilities = [0.25, 0.25, 0.25, 0.25]
    matrix = [
        [0, 0.455, 0.068, 0.300],
        [0.882, 0, 0.358, 0.936],
        [0.758, 0.779, 0, 0.924],
        [0.973, 0.159, 0.691, 0],
    ]
    limit_probabilities = calc_limit_probabilities(matrix)
    stabilization_times = calc_stabilization_times(matrix, start_probabilities, limit_probabilities)
    pprint(limit_probabilities)
    pprint(stabilization_times)

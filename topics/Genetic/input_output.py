import os

here = os.path.abspath(os.path.dirname(__file__))


def io(input_function, path):
    cost_map = input_function(path)
    return lambda source, distanation: cost_map[source][distanation]


# DATA_1
def matrice_data_reader(path):
    cost_map = []
    with open(os.path.join(here, path), 'r') as data:
        dimension = int(data.readline())
        for i in range(dimension):
            cost_map.append(
                list(map(int, data.readline().strip().split(" " * 4))))

    return cost_map

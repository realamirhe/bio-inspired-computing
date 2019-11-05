import random
import math
from input_output import io, matrice_data_reader
from algorithm import genetic

# CONST
MIN_CUT_SIZE = 3
MAX_CUT_SIZE_COEFFICIENT = .5
DISTANCE = io(matrice_data_reader, '.\\assets\\data1.txt')


class Chromosome:
    def __init__(self, chromosome, evaluate=False):
        self.chromosome = chromosome[:]

        if (evaluate):
            self.fitness = self.evaluate_fitness()

    def __add__(self, parent):
        return cross_over(self.chromosome, parent.chromosome)

    def __mul__(self, ratio):
        return mutation(self.chromosome, ratio)

    def evaluate_fitness(self):
        return fitness(self.chromosome)

    def __repr__(self):
        return '->'.join(map(repr, self.chromosome + [self.chromosome[0]]))


class Memory:
    def __init__(self, chromosome):
        self.best = chromosome

        self.count = 0
        self.t_step = 0  # -θ, 0, θ

    def observer(self, iteration, n, population):
        """ map through population finding best of pop
        update best if current_best is better
         """
        population_best = max(
            population, key=lambda x: x.fitness)

        self.t_step = population_best.fitness - self.best.fitness

        if (self.t_step > 0):
            self.best = Chromosome(population_best.chromosome, True)
            self.count = 0  # Increment
        elif (self.t_step == 0):
            self.count += 1  # stable
        else:
            self.count = 0  # decrement
        return stop_condition(self.count, self.t_step, self.best.fitness, n, iteration, population), self.best


# fitness
def fitness(chromosome) -> float:
    cost = DISTANCE(chromosome[-1], chromosome[0])
    for i in range(len(chromosome) - 1):
        cost += DISTANCE(chromosome[i], chromosome[i + 1])

    return 1 / cost
    # / max(DISTANCE, key=lambda row: max(row))

# Crossover


def cross_over(X, Y, exploit=0.5) -> (Chromosome, Chromosome):
    """ order_recombination  """
    length = len(X)

    size = int(exploit *
               (length * MAX_CUT_SIZE_COEFFICIENT -
                MIN_CUT_SIZE)) + MIN_CUT_SIZE

    start = random.randint(0, length - size - 1)

    x, y = [None]*length, [None]*length

    # copy middle cut
    x[start:start + size], \
        y[start:start + size] = X[start:start+size], Y[start:start+size]

    # for x copy rest from Y
    active_ind = start + size
    for i in range(length):
        current_ind = (i + start + size) % length
        if (Y[current_ind] not in x):
            x[active_ind] = Y[current_ind]
            active_ind = (active_ind + 1) % length

    # for y copy rest from X
    active_ind = start + size
    for i in range(length):
        current_ind = (i + start + size) % length
        if (X[current_ind] not in y):
            y[active_ind] = X[current_ind]
            active_ind = (active_ind + 1) % length

    return Chromosome(x), Chromosome(y)


# Mutation
def mutation(X, mutation_ration, exploit=0.3) -> Chromosome:
    """ scramble """
    if random.random() > mutation_ration:
        return Chromosome(X, True)

    length = len(X)
    scramble_size = int(exploit *
                        (length * MAX_CUT_SIZE_COEFFICIENT -
                         MIN_CUT_SIZE)) + MIN_CUT_SIZE

    start_entry = random.randint(0, length - scramble_size - 1)
    # copy chromosome
    mutated = X[start_entry:start_entry+scramble_size]
    random.shuffle(mutated)
    mutated = X[0:start_entry] + mutated + X[start_entry+scramble_size:]
    return Chromosome(mutated, True)


# Initiate
def permutation(size) -> list:
    standard_list = [i for i in range(size)]
    random.shuffle(standard_list)
    return standard_list


def initiate(size) -> Chromosome:
    return Chromosome(permutation(size), True)


def stop_condition(count, t_step, fitness, n, iteration, population) -> bool:
    # iteration > 5000
    # count > 700 (for t_step = 0)
    # best - average_of_distance < threshold
    if count > 500 and t_step == 0:
        print("Terminated:: NO IMPROVEMENT ::")
    if iteration > max(n // 5 * 100, 2000):
        print("Terminated:: MAX ITERATION ::")
    if converges(population):
        print("Terminated:: CONVERGED ::")
    return (count > 700 and t_step == 0) or iteration > max(n // 5 * 100,  5000) or converges(population)


def converges(population):
    average = sum(
        [chromosome.fitness for chromosome in population]) / len(population)
    best = max(population, key=lambda chromosome: chromosome.fitness)

    return math.log(best.fitness - average) < -10

# Selection


def next_generation(population, size, top):
    """ Elitism with Exploration"""
    ranked = sorted(
        population, key=lambda individual: individual.fitness, reverse=True)
    tops_count = int(size * top)

    # tops + worst_nearby + randoms + best_nearby
    return ranked[:tops_count] + \
        [ranked[-1] * 0.7] + \
        random.sample(ranked, size - tops_count - 2) + \
        [ranked[0] * 0.7]


def parent_select(population, n):
    return (tournament_selection(population) for _ in range(n // 5 + 2))


def tournament_selection(population):
    size = len(population)
    indexes = [i for i in range(size)]
    random.shuffle(indexes)

    return (
        population[max(indexes[:size // 2],
                       key=lambda i: population[i].fitness)],
        population[max(indexes[size // 2:],
                       key=lambda i: population[i].fitness)]
    )


# report
def report(iteration, chromosome, solution=False):
    print(f"{iteration=} fitness~={chromosome.fitness}")
    if (solution):
        print(f":::{repr(chromosome)}:::")


if __name__ == "__main__":
    # Genetic size >= 4
    genetic(100, 20, initiate, Memory, 0.6,
            parent_select, next_generation, report)

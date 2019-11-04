import math
import random
from algorithm import PSO

# CONST
ω = 0.3
μ = 0.4
θ = 0.3


class Vector:
    def __init__(self, bounds, value=None):
        self.bounds = bounds
        self.value = self.in_range(value)

    def random_point(self):
        return tuple(real_rand(l, u) for (l, u) in bounds)

    def in_range(self, value: tuple):
        if not value:
            return self.random_point()
        for (ind, (lower, upper)) in enumerate(self.bounds):
            if not (lower <= value[ind] <= upper):
                # print(f"value {value} is out_of_range")
                return self.random_point()
        return value

    def update(self, value):
        self.value = self.in_range(value)

    def __add__(self, other):
        x_plus_y = tuple(i+j for (i, j) in zip(self.value, other.value))
        return Vector(self.bounds, x_plus_y)

    def __sub__(self, other):
        x_minus_y = tuple(i-j for (i, j) in zip(self.value, other.value))
        return Vector(self.bounds, x_minus_y)

    def __mul__(self, scale):
        x_times_y = tuple(i*scale for i in self.value)
        return Vector(self.bounds, x_times_y)

    def __repr__(self):
        return f"({', '.join(map(str,self.value))})"

    def copy(self):
        return Vector(self.bounds, self.value)


def real_rand(lower, upper):
    """ Return random real number in range [lower, upper]. (upper - lower >= 1) """
    real_field = random.randint(lower, upper)
    if real_field == upper:
        return real_field
    return real_field + random.random()


class Particle:
    def __init__(self, bounds, evaluate=False, vector=None):
        # position in Space
        self.vector = Vector(bounds, vector)
        # Personal best
        self.p_best = self.vector.copy()
        # inertia
        self.v = self.vector.copy()
        # update fitness if necessary
        self.fitness = 0
        if evaluate:
            self.update_fitness()

    def update_fitness(self):
        current_fitness = fitness(self.vector)
        if (current_fitness > self.fitness):
            self.fitness = current_fitness
            self.p_best = self.vector.copy()
        else:
            self.fitness = current_fitness

    def update_pos(self, g_best):
        self.v = self.v * ω + \
            (self.p_best - self.vector) * (μ * p_rand()) + \
            (g_best.vector - self.vector) * (θ * g_rand())

        self.vector = self.vector + self.v

        self.update_fitness()

    def copy(self):
        return Particle(self.vector.bounds, True, self.vector.value)


class Memory:
    def __init__(self, particle):
        self.best = particle

        self.count = 0
        self.t_step = 0  # -θ, 0, θ

    def observer(self, iteration, n, swarm):
        """ map through swarm finding best of swarm
        update best if current_best is better
         """
        swarm_best = max(
            swarm, key=lambda x: x.fitness)

        self.t_step = swarm_best.fitness - self.best.fitness

        if (self.t_step > 0):
            self.best = Particle(swarm_best.vector.bounds,
                                 True, swarm_best.vector.value)
            self.count = 0  # Increment
        elif (self.t_step == 0):
            self.count += 1  # stable
        else:
            self.count = 0  # decrement
        return stop_condition(self.count, self.t_step, self.best.fitness, n, iteration), self.best


def stop_condition(count, t_step, fitness, n, iteration) -> bool:
    return (random.random() < 0.15) and ((count > math.floor(n * 1000 / 60)) or iteration > (n // 5) * 100 * n)


def initate(bounds):
    return Particle(bounds, evaluate=True)


def g_rand():
    return 1


def p_rand():
    return 1


def fitness(vector):
    # minimization objective
    return -1 * cost_function(*vector.value)


# f
def f(x, y):
    return - 1 * abs(math.sin(x) * math.cos(y) *
                     math.e ** abs(1 - (math.sqrt(x**2 + y**2)) / math.pi))


# g
def g(x, y):
    return 0.5 + \
        (math.cos(math.sin(abs(x ** 2 - y ** 2)) ** 2 - 0.5)) / \
        math.floor(1 + 1.001*(x**2 + y**2)) ** 2

# report


def report(iteration, particle, solution=False):
    print(f"{iteration=} fitness~={particle.fitness}")
    if (solution):
        print(f":::{repr(particle.vector)}:::")


if __name__ == "__main__":
    global cost_function
    cost_function = f
    bounds = [(-10, 10), (-10, 10)]
    PSO(30, bounds, Memory, initate, report)

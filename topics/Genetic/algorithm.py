def genetic(n, size, initate, Memory, mutate_ratio, parent_select, next_generation,  report):
    # initate
    population = [initate(size) for _ in range(n)]

    # memorize one of individuals
    memory = Memory(population[0])
    # iteration count
    iteration = 0
    stop_condition = False

    # repeat until stop condition reached
    while not stop_condition:
        iteration += 1

        # selection
        for (X, Y) in parent_select(population):
            # crossover
            x, y = X + Y
            # mutation
            x = x * mutate_ratio
            y = y * mutate_ratio
            # update population
            population.append(x)
            population.append(y)

        # generation selection
        population = next_generation(population, n, 0.3)

        stop_condition, best_ever = memory.observer(iteration, n, population)

        report(iteration, best_ever)
    report(iteration, best_ever, solution=True)

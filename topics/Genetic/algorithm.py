def genetic(size, Chromosome, Memory, next_generation, stop_condition, report=print):
    # initate
    population = [Chromosome.initate() for i in range(size)]
    # memorize one of individuals
    memory = Memory.initate(population[0])
    # iteration count
    iteration = 0
    stop_condition = False

    # repeat until stop condition reached
    while True:
        iteration = 0

        if stop_condition:
            break

        # selection
        for (X, Y) in parent_select(population):
            # crossover
            x, y = X + Y
            # mutation
            x = x * mutate_ratio
            y = y * mutate_ratio

            x = Chromosome.initate(x)
            y = Chromosome.initate(y)

            population.append(x)
            population.append(y)

        # generation selection
        population = next_generation(population)

        stop_condition, best_ever = memory.observe(population)

        report(iteration, best_ever)

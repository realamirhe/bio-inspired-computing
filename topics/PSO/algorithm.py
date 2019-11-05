def PSO(n, bounds, Memory, initate, report):
    # initate
    swarm = [initate(bounds) for _ in range(n)]
    # memorize one of individuals
    memory = Memory(swarm[0])
    best_ever = max(swarm, key=lambda particle: particle.fitness).copy()
    # iteration count
    iteration = 0
    stop_condition = False

    # repeat until stop condition reached
    while not stop_condition:
        iteration += 1

        # update velocity and position for each particle
        for particle in swarm:
            particle.update_pos(best_ever, iteration)

        stop_condition, best_ever = memory.observer(iteration, n, swarm)

        report(iteration, best_ever)
    report(iteration, best_ever, solution=True)

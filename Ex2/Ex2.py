import numpy as np
import random


def fn(x: np.array) -> np.array:
    return c + b.T @ x + x.T @ A @ x


def generate_population():
    population = []

    for _ in range(population_size):
        individual = np.zeros((d,))
        for i in range(d):
            individual[i] = random.randint(i - 2 ** d, 2 ** d)
        population.append(individual)

    return np.array(population, dtype=np.int64)


def display_population(population):
    for id, element in enumerate(population):
        print(f"{id}: {element}")


def fitness_calculation(population):
    scores = []

    for individual in population:
        scores.append(fn(individual))

    return np.array(scores)


if __name__ == '__main__':

    d = int(input("Enter the number of dimensions - d: "))
    while d < 1:
        d = int(input("Dimension must be greater than 0. Enter new number of dimensions - d: "))

    c = float(input("Enter the constant - c: "))

    nums_b = list(map(int, input(f'Enter {d} numbers for vector b separated by space: ').split()))
    b = np.array(nums_b)
    while b.size != d:
        nums_b = list(map(int, input(f'Incorrect input. Enter {d} numbers separated by space: ').split()))
        b = np.array(nums_b)

    nums_A = list(
        map(int, input(f'Enter {d * d} numbers for matrix A in starting from top left to bottom right: ').split()))
    while len(nums_A) != d * d:
        nums_A = list(map(int, input(f'Incorrect input. Enter {d * d} numbers separated by space: ').split()))
    A = np.array(nums_A).reshape(d, d)

    population_size = int(input("Enter the population size: "))
    while population_size < 2:
        population_size = int(input("Population size has to be greater than 2. Enter new population size: "))

    crossover_prob = float(input("Enter the crossover probability: "))
    while crossover_prob < 0 or crossover_prob > 1:
        crossover_prob = float(
            input("Crossover probability has to be between 0 and 1. Enter new crossover probability: "))

    mutation_prob = float(input("Enter the mutation probability: "))
    while mutation_prob < 0 or mutation_prob > 1:
        mutation_prob = float(input("Mutation probability has to be between 0 and 1. Enter new mutation probability: "))

    iterations = int(input("Enter the number of iterations: "))
    while iterations <= 0:
        iterations = int(input("Iterations must be greater than 0. Enter new number of iterations: "))

    """
    # Testing
    d = 3
    A = [[-2, 1, 0], [1, -2, 1], [0, 1, -2]]
    b = [-14, 14, -2]
    c = -23.5
    population_size = 50
    crossover_probability = 0.9
    mutation_probability = 0.05
    iterations = 1000
    A = np.array(A).reshape(3, 3)
    b = np.array(b)
    """

    pop = generate_population()
    display_population(pop)
    print(fitness_calculation(pop))

import numpy as np
import random


def fn(x):
    return c + b.T @ x + x.T @ A @ x


def generate_population():
    population = []

    for _ in range(population_size):
        individual = np.zeros((dim,))
        for i in range(dim):
            individual[i] = random.randint(i - 2 ** d, 2 ** d)
        population.append(individual)

    return np.array(population, dtype=np.int64)


def fitness_calculation(population):
    scores = []

    for individual in population:
        scores.append(fn(individual))

    return np.array(scores)


def display_population(population):
    for i, e in enumerate(population):
        print(f"{i+1}: {e} = {fn(e)}")


def roulette_wheel(population):
    scores = fitness_calculation(population)

    if scores.min() != scores.max():
        scores = (scores - scores.min()) / (scores.max() - scores.min())
   

    probabilities = scores / scores.sum()

    indices = np.random.choice(population.shape[0], size=population_size, p=probabilities)

    return np.array([population[i] for i in indices])

def mutate(ind):
    individiual = np.copy(ind)
    
    for i, cell in enumerate(individiual):
        new_cell = ""
        for chromosome in cell:
            if np.random.rand() < mutation_probability:
                if chromosome == "0":
                    new_cell += "1"
                else:
                    new_cell += "0"
            else:
                new_cell += chromosome
        individiual[i] = new_cell
    return individiual


def mutation(population):
    m_pop = []
    for individual in population:
        m_pop.append(mutate(individual))

    return np.array(m_pop)    


def decimal_to_binary(n):
    bits = dim + 1

    return np.binary_repr(n, bits)


def binary_to_decimal(binary):
    unsigned = int(binary, 2)
    if binary[0] == "1":
        decimal = unsigned - 2**(dim+1)
        return decimal
    else:
        return unsigned


def crossover(population):
    crossed= []
        
    for i in range(0, population_size - 1, 2):

        c1 = population[i]
        c2 = population[i + 1]
        temp_p1 = ''.join(c1)
        temp_p2 = ''.join(c2)
        m = len(c1[0])
        if np.random.rand() < crossover_probability:
            point = random.randint(1, len(temp_p1) - 2)
            temp_c1 = temp_p1[:point] + temp_p2[point:]
            temp_c2 = temp_p2[:point] + temp_p1[point:]
            for i in range(0, len(temp_p1) - m + 1, m):
                np.append(c1, temp_c1[i:i + m])
                np.append(c2, temp_c2[i:i + m])

        crossed += [c1, c2]

    return np.array(crossed)


def to_gray_mod(num_i, shift, bit_len) -> str:
    num_i = num_i + shift
    num_i = num_i ^ (num_i >> 1)  
    x_b = format(num_i, bit_len+'b')   
    return x_b


def to_gray(matrix):
    pop_b = []
    for i in range(population_size):
        for j in range(dim):
            pop_b.append(to_gray_mod(matrix[i][j], -(j - 2 ** d) - 1, '0' + str((2 ** d) // 2)))
    pop_b = np.array(pop_b).reshape(population_size, dim)
    return np.array(pop_b)


def inverse_gray_mod(binary, shift):  
    num_i = int(binary, 2)
    inv = 0
    while num_i:
        inv = inv ^ num_i
        num_i = num_i >> 1

    return inv - shift


def to_decimal(matrix):
    pop_b = []
    for i in range(population_size):
        for j in range(dim):
            pop_b.append(inverse_gray_mod(matrix[i][j], -(j - 2 ** d) - 1))
    pop_b = np.array(pop_b).reshape(population_size, dim)
    
    return np.array(pop_b)


def replacement(crossed, mutated):
    n = len(mutated)
    return np.concatenate((mutated, crossed[n:]))


def fittest_individual(population):
    max_value = np.max(fitness_calculation(population))
    best = np.where(max_value == fitness_calculation(population))[0][0]
    return population[best], max_value


def genetic_algorithm():
    population = generate_population()

    best_overall_individual = population[0]
    best_overall_score = fn(best_overall_individual)
    final_population = population

    for _ in range(iterations):        
        s_pop = roulette_wheel(population)
        b_pop = to_gray(s_pop)
        c_pop = crossover(b_pop)
        m_pop = mutation(c_pop)
        r_pop = replacement(to_decimal(c_pop), to_decimal(m_pop))


        best_iteration_individual, best_iteration_score = fittest_individual(
                r_pop)
        if best_iteration_score > best_overall_score:
                best_overall_individual = best_iteration_individual
                best_overall_score = best_iteration_score
                final_population = r_pop
    print("\nFinal Population\n----------------------------------")
    display_population(final_population)
    print(
        f"\nBest: {best_overall_individual} Score: {best_overall_score}")



if __name__ == '__main__':
    
    dim = int(input("Enter the number of dimensions - dim: "))
    while dim < 1:
        dim = int(input("Dimension must be greater than 0. Enter new number of dimensions - dim: "))

    c = float(input("Enter the constant - c: "))

    nums_b = list(map(int, input(f'Enter {dim} numbers for vector b separated by space: ').split()))
    b = np.array(nums_b)
    while b.size != dim:
        nums_b = list(map(int, input(f'Incorrect input. Enter {dim} numbers separated by space: ').split()))
        b = np.array(nums_b)

    nums_A = list(
        map(int, input(f'Enter {dim * dim} numbers for matrix A in starting from top left to bottom right: ').split()))
    while len(nums_A) != dim * dim:
        nums_A = list(map(int, input(f'Incorrect input. Enter {dim * dim} numbers separated by space: ').split()))
    A = np.array(nums_A).reshape(dim, dim)

    d = int(input("Enter the number for range - d: "))
    while d < 1:
        d = int(input("Range must be greater than 0. Enter new number for d - d: "))

    population_size = int(input("Enter the population size: "))
    while population_size < 2 or population_size % 2 != 0:
        population_size = int(input("Population size has to be greater than 2 and an even number. Enter new population size: "))

    crossover_probability = float(input("Enter the crossover probability: "))
    while crossover_probability < 0 or crossover_probability > 1:
        crossover_probability = float(
            input("Crossover probability has to be between 0 and 1. Enter new crossover probability: "))

    mutation_probability = float(input("Enter the mutation probability: "))
    while mutation_probability < 0 or mutation_probability  > 1:
        mutation_probability  = float(input("Mutation probability has to be between 0 and 1. Enter new mutation probability: "))

    iterations = int(input("Enter the number of iterations: "))
    while iterations <= 0:
        iterations = int(input("Iterations must be greater than 0. Enter new number of iterations: "))

    genetic_algorithm()
    
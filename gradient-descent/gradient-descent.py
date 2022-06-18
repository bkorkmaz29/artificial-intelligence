import numpy as np
import random


# Calculating value of F(x) at x
def get_f(a, b, c, d, x):
    return a * x ** 3 + b * x ** 2 + c * x + d


# Gradient Descent Algorithm for F(x)
def gd_f(tolerance, learning_rate, max_iterations, a, b, c, d, x0):
    f = get_f(a, b, c, d, x0)
    gd = lambda x: 3 * a * x ** 2 + 2 * b * x + c
    count = 0
    step_size = tolerance + 1
    while count < max_iterations and step_size > tolerance:
        x1 = x0
        x0 = x0 - (gd(x1) * learning_rate)
        count += 1
        step_size = abs(x0 - x1)
        f = get_f(a, b, c, d, x0)

    return x0, f


# Gradient for G(x)
def gradient_g(matrix, vector, omega):
    return np.add((np.dot((matrix.T + matrix), omega)), vector)


def get_g(a, b, c, x0):
    return c + np.add(np.dot(b.T, x0), np.dot(np.dot(x0.T, a), x0))


# Gradient Descent Algorithm for G(x)
def gd_g(tolerance, learning_rate, max_iterations, a, b, c, x0):
    g = c + np.add(np.dot(b.T, x0), np.dot(np.dot(x0.T, a), x0))
    count = 0
    step_size = tolerance + 1
    while count < max_iterations and np.all(step_size > tolerance):
        x1 = x0
        x0 = x0 - np.dot(gradient_g(a, b, x0), learning_rate)
        count += 1
        step_size = abs(x0 - x1)
        g = c + np.add(np.dot(b.T, x0), np.dot(np.dot(x0.T, a), x0))

    return x0, g


# Newton Algorithm for F(x)
def newton_f(tolerance, max_iter, a, b, c, d, x0):
    f_derr = lambda x: 3 * a * x ** 2 + 2 * b * x + c
    f_derr_2 = lambda x: 6 * a * x + 2 * b
    f = f_derr(x0)
    count = 0
    while count < max_iter and abs(f) > tolerance:
        f = f_derr(x0)
        f_prime = f_derr_2(x0)
        x0 = x0 - (f / f_prime)
        count += 1
    return x0, get_f(a, b, c, d, x0)


# Newton Algorithm for G(x)
def newton_g(tolerance, max_iter, a, b, c, x0):
    g = c + np.add(np.dot(b.T, x0), np.dot(np.dot(x0.T, a), x0))
    inv_hessian = np.linalg.inv(np.add(a, a.T))
    count = 0
    while count < max_iter and abs(g) > tolerance:
        x1 = x0 - np.dot(gradient_g(a, b, x0), inv_hessian)
        x0 = x1
        g = c + np.add(np.dot(b.T, x0), np.dot(np.dot(x0.T, a), x0))
        count += 1
    return x0, g


# Getting parameters from user for F(x)
def get_params_f():
    print('Enter a number for a')
    a = int(input())
    print('Enter a number for b')
    b = int(input())
    print('Enter a number for c')
    c = int(input())
    print('Enter a number for d')
    d = int(input())

    return a, b, c, d


# Getting parameters from user for G(x)
def get_params_g(dim):
    print('Enter numbers for vector b separated by space')
    nums_b = list(map(int, input().split()))
    b = np.array(nums_b)
    while b.size != dim:
        print(f'Size of vector b must be equal to {dim}. Enter numbers for vector b separated by space')
        nums_b = list(map(int, input().split()))
        b = np.array(nums_b)

    print('Enter numbers for matrix A in order of each row separated by space')
    nums_a = list(map(int, input().split()))
    while True:
        if len(nums_a) != dim * dim:
            print(f'Matrix size must be equal to {dim}x{dim}. Enter {dim * dim} numbers')
            nums_a = list(map(int, input().split()))
            continue
        a = np.array(nums_a).reshape(b.size, b.size)
        if np.any(np.linalg.eigvals(a) <= 0):  # Checking if given matrix is positive-definite
            print(f'The matrix is not positive-definite. Enter new {dim * dim} numbers')
            nums_a = list(map(int, input().split()))
            continue
        else:
            break

    print('Enter c')
    c = float(input())

    return a, b, c


# Getting parameters from user for optimization
def get_params():
    print('Enter tolerance')
    tolerance = float(input())
    while tolerance < 0:
        print('Incorrect input. Enter a non-negative number')
        tolerance = float(input())

    print('Enter limit of iterations')
    max_iterations = int(input())
    while max_iterations <= 0:
        print('Incorrect input. Enter a positive number')
        max_iterations = int(input())

    print('Enter learning rate (Enter 0 if not applicable)')
    learning_rate = float(input())
    while learning_rate < 0:
        print('Incorrect input. Enter a positive number')
        learning_rate = float(input())

    return tolerance, max_iterations, learning_rate


# Minimization for F(x)
def minimization_f(a, b, c, d, x):
    tolerance, max_iterations, learning_rate = get_params()
    solution = {}

    print('Select method\n1-Gradient Descent\n2- Newton')
    while True:
        selected = int(input())
        if selected == 1:
            if learning_rate != 0:
                sol, f = gd_f(tolerance, learning_rate, max_iterations, a, b, c, d, x)
                solution['Solution by Gradient Descent:  '] = sol
                solution['F(x) by Gradient Descent: '] = f
            else:
                print('Learning rate is 0, hence Gradient Descent cannot be run')

        if selected == 2:
            sol, f = newton_f(tolerance, max_iterations, a, b, c, d, x)
            solution['Solution by Newton Method: '] = sol
            solution['F(x) by Newton Method: '] = f

        if selected != 1 and selected != 2:
            print('Incorrect option chosen')
            continue
        return solution


# Minimization for G(x)
def minimization_g(a, b, c, x):
    tolerance, max_iterations, learning_rate = get_params()

    solution = {}

    print('Select method\n1-Gradient Descent\n2- Newton')
    while True:
        selected = int(input())
        if selected == 1:
            if learning_rate != 0:
                sol, j = gd_g(tolerance, learning_rate, max_iterations, a, b, c, x)
                solution['Solution by Gradient Descent:  '] = sol
                solution['G(x) by Gradient Descent: '] = j
            else:
                print('Learning rate is 0, hence Gradient Descent cannot be run')

        if selected == 2:
            sol, j = newton_g(tolerance, max_iterations, a, b, c, x)
            solution['Solution by Newton Method: '] = sol
            solution['G(x) by Newton Method: '] = j

        if selected != 1 and selected != 2:
            print('Incorrect option chosen')
            continue
        return solution


# Checking learning rate if it is greater than zero
def check_learning_rate(learning_rate):
    if learning_rate <= 0:
        print('Learning rate must be greater than zero')
        learning_rate = float(input())
        while learning_rate <= 0:
            print('Learning rate must be greater than zero')
            learning_rate = float(input())
    return learning_rate


# Newton method batch mode for F(x)
def newton_batch_f(coeff, params, n, x_nums):
    a, b, c, d = coeff
    tolerance, max_iterations, learning_rate = params
    newton_solution = []
    newton_fx = []
    for i in range(n):
        x = random.uniform(x_nums[0], x_nums[1])
        newton_solution.append((newton_f(tolerance, max_iterations, a, b, c, d, x))[0])
        newton_fx.append((newton_f(tolerance, max_iterations, a, b, c, d, x))[1])
    print('\nSTD and MEAN for solution found by Newton Method \n')
    print(np.std(newton_solution, axis=0))
    print(np.mean(newton_solution, axis=0))
    print('\nSTD and MEAN for F(x) found by Newton Method \n')
    print(np.std(newton_fx, axis=0))
    print(np.mean(newton_fx, axis=0))


# Gradient Descent method batch mode for F(x)
def gd_batch_f(coeff, params, n, x_nums):
    a, b, c, d = coeff
    tolerance, max_iterations, learning_rate = params
    learning_rate = check_learning_rate(learning_rate)
    gd_solution = []
    gd_fx = []
    for i in range(n):
        x = random.uniform(x_nums[0], x_nums[1])
        gd_solution.append((gd_f(tolerance, learning_rate, max_iterations, a, b, c, d, x))[0])
        gd_fx.append((gd_f(tolerance, learning_rate, max_iterations, a, b, c, d, x))[1])
    print('\nSTD and MEAN for solution found by Gradient Descent \n')
    print(np.std(gd_solution, axis=0))
    print(np.mean(gd_solution, axis=0))
    print('\nSTD and MEAN for F(x) found by Gradient Descent \n')
    print(np.std(gd_fx, axis=0))
    print(np.mean(gd_fx, axis=0))


# Newton method batch mode for G(x)
def newton_batch_g(coeff, params, dim, n, x_nums):
    a, b, c = coeff
    tolerance, max_iterations, learning_rate = params
    newton_solution = []
    newton_gx = []
    for i in range(n):
        x = []
        for i in range(dim):
            x.append(random.uniform(x_nums[0], x_nums[1]))
        newton_solution.append((newton_g(tolerance, max_iterations, a, b, c, np.array(x)))[0])
        newton_gx.append((newton_g(tolerance, max_iterations, a, b, c, np.array(x)))[1])
    print('\nSTD and MEAN for solution found by Newton Method \n')
    print(np.std(newton_solution, axis=0))
    print(np.mean(newton_solution, axis=0))
    print('\nSTD and MEAN for G(x) found by Newton Method \n')
    print(np.std(newton_gx, axis=0))
    print(np.mean(newton_gx, axis=0))


# Gradient Descent method batch mode for G(x)
def gd_batch_g(coeff, params, dim, n, x_nums):
    a, b, c = coeff
    tolerance, max_iterations, learning_rate = params
    learning_rate = check_learning_rate(learning_rate)
    gd_solution = []
    gd_gx = []
    for i in range(n):
        x = []
        for i in range(dim):
            x.append(random.uniform(x_nums[0], x_nums[1]))
        gd_solution.append((gd_g(tolerance, learning_rate, max_iterations, a, b, c, np.array(x)))[0])
        gd_gx.append((gd_g(tolerance, learning_rate, max_iterations, a, b, c, np.array(x)))[1])
    print('\nSTD and MEAN for solution found by Gradient Descent \n')
    print(np.std(gd_solution, axis=0))
    print(np.mean(gd_solution, axis=0))
    print('\nSTD and MEAN for G(x) found by Gradient Descent \n')
    print(np.std(gd_gx, axis=0))
    print(np.mean(gd_gx, axis=0))

# MAIN

print('Select function type\n1- 𝐹(𝑥)=𝑎𝑥^3+𝑏𝑥^2+𝑐𝑥+𝑑\n2- 𝐺(𝑥)=𝑐+𝑏^T𝑥+𝑥^T𝐴𝑥')
while True:
    selected = int(input())
    if selected == 1:
        print('Enter...\n1- Normal Mode\n2- Batch Mode')
        while True:
            selected = int(input())
            if selected == 1:
                print('Select option\n1- Define initial point\n2- Choose a range')
                while True:
                    selected = int(input())
                    if selected == 1:
                        print('Enter initial x')
                        x = int(input())
                        a, b, c, d = get_params_f()
                        solution = minimization_f(a, b, c, d, x)
                        for i in solution:
                            print(i, solution[i])
                        break
                    elif selected == 2:
                        print('Enter range for x separated by space')
                        x_nums = list(map(float, input().split()))
                        x = random.uniform(x_nums[0], x_nums[1])
                        a, b, c, d = get_params_f()
                        solution = minimization_f(a, b, c, d, x)
                        for i in solution:
                            print(i, solution[i])
                        break
                    elif selected != 1 and selected != 2:
                        print('Wrong selection')
                break

            elif selected == 2:
                print('Enter n = number of times to run methods')
                n = int(input())
                print('Enter range for x separated by space')
                x_nums = list(map(float, input().split()))
                x = random.uniform(x_nums[0], x_nums[1])
                print('Choose a method\n1- Gradient Descent\n2- Newton')
                while True:
                    selected = int(input())
                    if selected == 1:
                        gd_batch_f(get_params_f(), get_params(), n, x_nums)
                        break
                    elif selected == 2:
                        newton_batch_f(get_params_f(), get_params(), n, x_nums)
                        break
                    elif selected != 1 and selected != 2:
                        print('Wrong selection')
                break
            elif selected != 1 and selected != 2:
                print('Wrong selection')
    elif selected == 2:
        print('Enter...\n1- Normal Mode\n2- Batch Mode')
        while True:
            selected = int(input())
            if selected == 1:
                print('Select option\n1- Define initial vector\n2- Choose a range')
                while True:
                    selected = int(input())
                    if selected == 1:
                        print('Enter dimension')
                        dimension = int(input())
                        print('Enter numbers for x separated by space')
                        nums = list(map(int, input().split()))
                        x0 = np.array(nums)
                        a, b, c = get_params_g(dimension)
                        solution = minimization_g(a, b, c, x0)
                        for i in solution:
                            print(i, solution[i])
                        break
                    elif selected == 2:
                        print('Enter dimension')
                        dim = int(input())
                        print('Enter range for x separated by space')
                        x_nums = list(map(float, input().split()))
                        x = []
                        for i in range(dim):
                            x.append(random.uniform(x_nums[0], x_nums[1]))
                        a, b, c = get_params_g(dim)
                        solution = minimization_g(a, b, c, np.array(x))
                        for i in solution:
                            print(i, solution[i])
                        break
                    elif selected != 1 and selected != 2:
                        print('Wrong selection')
                break
            elif selected == 2:
                print('Enter n = number of times to run methods')
                n = int(input())
                print('Enter dimension')
                dim = int(input())
                print('Enter range for x separated by space')
                x_nums = list(map(float, input().split()))
                print('Choose a method\n1- Gradient Descent\n2- Newton')
                while True:
                    selected = int(input())
                    if selected == 1:
                        gd_batch_g(get_params_g(dim), get_params(), dim, n, x_nums)
                        break
                    elif selected == 2:
                        newton_batch_g(get_params_g(dim), get_params(), dim, n, x_nums)
                        break
                    elif selected != 1 and selected != 2:
                        print('Wrong selection')
                break
            elif selected != 1 and selected != 2:
                print('Wrong selection')
    elif selected != 1 and selected != 2:
        print('Wrong selection')

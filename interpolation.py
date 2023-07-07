import math
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from scipy.misc import derivative
plt.style.use('seaborn-poster')

def function(arg):
    return math.sin(arg * arg)

def define_intervals(number, length, left_boarder):
    delta = length / (number - 1)
    x_array = np.array([left_boarder + i*delta for i in range(number)], dtype = float)
    return x_array

def define_function(x_array):
    y_array = np.array([function(x_array[i]) for i in range(len(x_array))], dtype = float)
    return y_array

def factorial(number):
    if number == 0:
        return 1
    return factorial(number-1)*number

def lagrange_polynom(x_array, y_array, value):
    result = 0
    for i in range(len(y_array)):
        numerator = 1
        denominator = 1
        for j in range(len(x_array)):
            if i == j:
                pass
            else:
                numerator *= value - x_array[j]
                denominator *= x_array[i]-x_array[j]
        result += y_array[i]*numerator/denominator
    return result



def counting_divided_differences(x_array,y_array):
    divided_differences = [[None for i in range(len(x_array))] for j in range(len(x_array))]
    for i in range(len(x_array)):
        divided_differences[i][0] = y_array[i]
    for i in range(1, len(x_array)):
        for j in range(len(x_array) - i):
            divided_differences[j][i] = (divided_differences[j + 1][i - 1] - divided_differences[j][i - 1]) / (x_array[j + i] - x_array[j])
    return divided_differences

def newton_polynom(x_array, y_array, value):
    divided_differences = counting_divided_differences(x_array, y_array)
    y_count = [None for i in range(len(x_array))]
    x_count = 1
    y_count[0] = divided_differences[0][0]
    for i in range(1, len(x_array)):
        x_count *= (value - x_array[i - 1])
        result = y_count[i - 1] + divided_differences[0][i] * x_count
        y_count[i] = result
    return result

def interpolation_error(x_array, y_array, value):
    y_result = [derivative(function, x_array[i], len(x_array)) for i in range(len(x_array))]
    x_result = 1
    for i in range(len(x_array)):
        x_result *= abs(value - x_array[i].astype(float))
    y_max = np.max(y_result)
    error = y_max * x_result / factorial(len(x_array))
    return error

def main():
    #left_boarder = int(input("Define the left boarder: "))
    #right_boarder = int(input("Define the right boarder: "))
    #number = int(input("Define the node number: "))

    # Defining initial conditions
    left_boarder = -3
    right_boarder = 3
    number = 5
    length = right_boarder - left_boarder
    x_array = define_intervals(number, length, left_boarder)
    y_array = define_function(x_array)


    # PLOTTING LAGRANGE INTERPOLATION
    ####################################################
    fig = plt.figure(figsize=(13, 7))
    plt.title('Sin(x^2) Lagrange interpolation')
    plt.xlabel('x-axis')
    plt.ylabel('y-axis')
    plt.grid(True, linestyle='--')
    x_sin = np.linspace(-3, 3, 200)
    y_sin = np.sin(x_sin ** 2)
    plt.plot(x_sin, y_sin, color = 'green', label='Sin(x^2)')
    x_linear = np.linspace(np.min(x_array), np.max(x_array), 200)

    y_lagrange = [lagrange_polynom(x_array, y_array, value) for value in x_linear]
    plt.plot(x_linear, y_lagrange, color = 'blue', linestyle = 'dashed', linewidth = 2, markersize = 1, label = 'Lagrange polynom')

    # Approximate error
    y_lagrange_approx_error = [interpolation_error(x_array, y_array, value) for value in x_linear]
    plt.plot(x_linear, y_lagrange_approx_error, color='orange', linestyle='-.', linewidth=3, markersize=2, label='Approximate interpolation error')

    # Real error
    y_lagrange_real_error = [abs(lagrange_polynom(x_array, y_array, value) - function(value)) for value in x_linear]
    plt.plot(x_linear, y_lagrange_real_error, color = 'brown', linestyle = ':', linewidth = 3, markersize = 2, label = 'Real interpolation error')

    plt.legend()
    ####################################################



    # PLOTTING NEWTON INTERPOLATION#
    ####################################################
    fig2 = plt.figure(figsize=(13, 7))
    plt.title('Sin(x^2) Newton interpolation')
    plt.xlabel('x-axis')
    plt.ylabel('y-axis')
    plt.grid(True, linestyle='--')
    plt.plot(x_sin, y_sin, color='green', label='Sin(x^2)')

    y_newton = [newton_polynom(x_array, y_array, value) for value in x_linear]
    plt.plot(x_linear, y_newton, color='red', linestyle='dashed', linewidth=2, markersize=1, label='Newton polynom')

    # Approximate error
    y_lagrange_approx_error = [interpolation_error(x_array, y_array, value) for value in x_linear]
    plt.plot(x_linear, y_lagrange_approx_error, color='orange', linestyle='-.', linewidth=3, markersize=2, label='Approximate interpolation error')

    # Real error
    y_newton_real_error = [abs(newton_polynom(x_array, y_array, value) - function(value)) for value in x_linear]
    plt.plot(x_linear, y_newton_real_error, color='brown', linestyle=':', linewidth=3, markersize=2, label='Real interpolation error')

    plt.legend()
    ####################################################

    plt.show()


if __name__ == '__main__':
    main()
import numpy as np
import math
from scipy import integrate
import pandas as pd

def def_intervals(n, l_boarder, r_boarder):
    delta = abs(r_boarder - l_boarder) / n
    x_array = [delta * i + l_boarder for i in range(n + 1)]
    return x_array

def f(arg):
    return arg * math.sin(arg)

def Simpson(x_array, l_boarder, r_boarder, n):
    h = (r_boarder - l_boarder) / n
    result = f(x_array[0]) + f(x_array[-1])
    for i in range(1, len(x_array) - 1):
        if i % 2 == 0:
            result += 2 * f(x_array[i])
        else:
            result += 4 * f(x_array[i])
    result *= h / 3
    return result

def Gauss(x_array):
    result = 0
    for i in range(0, len(x_array)):
        try:
            x1 = (x_array[i] + x_array[i+1])/2 + np.sqrt(3)*(x_array[i+1] - x_array[i])/6
            x2 = (x_array[i] + x_array[i + 1])/2 - np.sqrt(3) * (x_array[i + 1] - x_array[i]) / 6
            result += (x_array[i+1] - x_array[i])/2 * (f(x1) + f(x2))
        except:
            IndexError
    return result

def Runge(x_array, l_boarder, r_boarder, n, exp_acc, arg):
    h = x_array[1] - x_array[0]
    p = exp_acc
    x_array2 = def_intervals(int(n / 2), l_boarder, r_boarder)
    if arg == 'Simpson':
        i_n = Simpson(x_array2, l_boarder, r_boarder, n/2)
        i_2n = Simpson(x_array, l_boarder, r_boarder, n)
        return (abs(i_2n - i_n)*(2 ** p)) / ((2 ** p - 1)*(h**p)), (abs(i_2n - i_n)*(2 ** p)) / ((2 ** p - 1))
    i_2n = Gauss(x_array)
    i_n = Gauss(x_array2)
    return (abs(i_2n - i_n)*(2 ** p)) / ((2 ** p - 1)*(h**p)), (abs(i_2n - i_n)*(2 ** p)) / ((2 ** p - 1))

def exp_accuracy(x_array, l_boarder, r_boarder, n, arg, real_integral):
    x_array2 = def_intervals(int(n / 2), l_boarder, r_boarder)
    if arg == 'Simpson':
        i_2h = Simpson(x_array, l_boarder, r_boarder, n)
        i_h = Simpson(x_array2, l_boarder, r_boarder, int(n/2))
        p = math.log2(abs((i_2h - real_integral)/(i_h - real_integral)))
        return p
    i_2h = Gauss(x_array)
    i_h = Gauss(x_array2)
    p = math.log2(abs((i_2h - real_integral) / (i_h - real_integral)))
    return p

def exp_accuracy_without_real(x_array, l_boarder, r_boarder, n, arg):
    x_array2 = def_intervals(int(n/2), l_boarder, r_boarder)
    x_array4 = def_intervals(int(n/4), l_boarder, r_boarder)
    if arg == 'Simpson':
        i_h = Simpson(x_array, l_boarder, r_boarder, n)
        i_h_half = Simpson(x_array2, l_boarder, r_boarder, int(n/2))
        i_h_forth = Simpson(x_array4, l_boarder, r_boarder, int(n/4))
        value = abs((i_h_half - i_h) / (i_h_forth - i_h_half))
        p = math.log2(value)
        return p
    i_h = Gauss(x_array)
    i_h_half = Gauss(x_array2)
    i_h_forth = Gauss(x_array4)
    value = abs((i_h_half - i_h) / (i_h_forth - i_h_half))
    p = math.log2(value)
    return p

def main():
    l_boarder = 0
    r_boarder = 4
    n = 128
    x_array = def_intervals(n, l_boarder, r_boarder)
    real_integral = integrate.quad(f, l_boarder, r_boarder)
    real_integral = real_integral[0]

    result_simpson = Simpson(x_array, l_boarder, r_boarder, n)
    print(f"По Симпсону: {result_simpson}, погрешность: {abs(result_simpson - real_integral)}")
    result_gauss = Gauss(x_array)
    print(f"По Гауссу: {result_gauss}, погрешность: {abs(result_gauss - real_integral)}")

    exp_acc_gauss = exp_accuracy(x_array, l_boarder, r_boarder, n, 'Gauss', real_integral)
    exp_acc_simpson = exp_accuracy(x_array, l_boarder, r_boarder, n, 'Simpson', real_integral)
    print(f"Экспериментальная точность по Симпсону: {abs(exp_acc_simpson)}")
    print(f"Экспериментальная точность по Гауссу: {abs(exp_acc_gauss)}")

    c_simpson, error_simpson1 = Runge(x_array, l_boarder, r_boarder, n, exp_acc_simpson ,'Simpson')
    c_gauss, error_gauss1 = Runge(x_array, l_boarder, r_boarder, n, exp_acc_gauss, 'Gauss')
    print(f"C для Симпсона: {abs(c_simpson)}")
    print(f"С для Гаусса: {abs(c_gauss)}")
    print(f"Значение по правилу Рунге по Симпсону: {abs(error_simpson1)}")
    print(f"Значение по правилу Рунге по Гауссу: {abs(error_gauss1)}")

    exp_acc_simpson2 = exp_accuracy_without_real(x_array, l_boarder, r_boarder, n, 'Simpson')
    exp_acc_gauss2 = exp_accuracy_without_real(x_array, l_boarder, r_boarder, n, 'Gauss')
    print(f"Экспериментальная точность по Симпсону (без использования реального значения): {abs(exp_acc_simpson2)}")
    print(f"Экспериментальная точность по Гауссу (без использования реального значения): {abs(exp_acc_gauss2)}")

if __name__ == "__main__":
    main()
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def f(x):
     # return math.sin(x)
     return 100


def spline(x):
    for i in range(n - 1):
        if (x_s[i] <= x) and (x <= x_s[i + 1]):
            return (-m[i] * ((x - x_s[i + 1]) ** 3)) / (6 * (x_s[i + 1] - x_s[i])) \
                   + (m[i + 1] * ((x - x_s[i]) ** 3)) / (6 * (x_s[i + 1] - x_s[i])) \
                   + ((f(x_s[i + 1]) - f(x_s[i])) / (x_s[i + 1] - x_s[i]) + ((x_s[i + 1] - x_s[i]) / 6) * (
                    m[i] - m[i + 1])) * (x - x_s[i]) \
                   + (f(x_s[i]) - ((m[i] * ((x_s[i + 1] - x_s[i]) ** 2))) / 6)


# Начальные условия:
n = 5
a = 0
b = 10
A = 5
B = -3

# x_s = [a + (b-a)*(i+0.4*math.cos(5*i))/(n-1) for i in range(n)]
# x_s[0] = a
# x_s[n-1] = b

x_s = [0]*n
x_s[0] = a
x_s[n - 1] = b
for i in range(1, n - 1):
    x_s[i] = a + (b-a)*(i+0.4*math.cos(5*i))/(n-1)

print(f"Узлы: {x_s}")
y_s = [f(x) for x in x_s]

# Прогонка:
alpha_s = [0 for i in range(n)]
beta_s = [0 for i in range(n)]
alpha_s[0] = -1 / 2
beta_s[0] = 3 * (y_s[1] - y_s[0]) / ((x_s[1] - x_s[0]) ** 2) - 3 * A / (x_s[1] - x_s[0])
for i in range(1, n - 1):
    A_i = (x_s[i] - x_s[i - 1]) / 6
    B_i = ((x_s[i] - x_s[i - 1]) + (x_s[i + 1] - x_s[i])) / 3
    C_i = (x_s[i + 1] - x_s[i]) / 6
    F_i = (y_s[i + 1] - y_s[i]) / (x_s[i + 1] - x_s[i]) - (y_s[i] - y_s[i - 1]) / (x_s[i] - x_s[i - 1])
    alpha_s[i] = -(C_i) / (A_i * alpha_s[i - 1] + B_i)
    beta_s[i] = (F_i - A_i * beta_s[i - 1]) / (A_i * alpha_s[i - 1] + B_i)
m = [0 for i in range(n)]
m[-1] = B
for i in range(n - 2, -1, -1):
    m[i] = m[i + 1] * alpha_s[i] + beta_s[i]

# Значения производных:
eps = 10 ** (-3)
firsts_a = []
seconds_a = []
firsts_b = []
seconds_b = []
accuracy = 10
for i in range(5):
    firsts_a.append(f"{((spline(a + eps) - spline(a)) / eps):.{accuracy}f}")
    seconds_a.append(f"{((spline(a) - 2 * spline(a + eps) + spline(a + 2 * eps)) / eps ** 2):.{accuracy}f}")
    firsts_b.append(f"{((spline(b - eps) - spline(b)) / eps):.{accuracy}f}")
    seconds_b.append(f"{((spline(b) - 2 * spline(b - eps) + spline(b - 2 * eps)) / eps ** 2):.{accuracy}f}")
    eps /= 10
data = {
    "f'(a)": firsts_a,
    "f''(a)": seconds_a,
    "f'(b)": firsts_b,
    "f''(b)": seconds_b
}
ind = ["10^(-3)", "10^(-4)", "10^(-5)", "10^(-6)", "10^(-7)"]
frame = pd.DataFrame(data, index=ind)
print(frame)

# График:
x_plot = np.linspace(a, b, 1000)
y_f = [f(x) for x in x_plot]
y_spline = [spline(x) for x in x_plot]
fig1 = plt.figure(figsize=(13, 7))
plt.title('Spline')
plt.xlabel('x-axis')
plt.ylabel('y-axis')
plt.grid(True, linestyle='--')
plt.plot(x_s, y_s, color = 'orange', marker = 'o')
plt.plot(x_plot, y_f, color='green', label='Function')
plt.plot(x_plot, y_spline, color='red', linestyle='--', label='Spline')
plt.legend()
plt.show()

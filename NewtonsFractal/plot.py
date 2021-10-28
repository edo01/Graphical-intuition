import cmath
import math

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

zeros = [complex(-1, 0),
         complex(0, 1),
         complex(-1, -1)]

zeros_color_values = {zeros[0]: 1,
                      zeros[1]: 0,
                      zeros[2]: 2}


def function(x):
    return (x - zeros[0]) * (x - zeros[1]) * (x - zeros[2])


def derivative(x):
    return (x - zeros[0]) * (x - zeros[2]) + \
           (x - zeros[1]) * (x - zeros[2]) + \
           (x - zeros[1]) * (x - zeros[0])


def newton_method(x, iterations):
    # print("x = " + str(x))
    for i in range(iterations):
        x = x - (function(x) / derivative(x))
    return x


def get_closest_zero(x, iterations):
    res = newton_method(x, iterations)
    # print(res)
    min_dist = math.inf
    for zero in zeros:
        if cmath.polar(zero-res)[0] < min_dist:
            min_dist = cmath.polar(zero-res)[0]
            closest_zero = zero

    return closest_zero


x_start, y_start = -1.5, -0.75  # an interesting region starts here
width, height = 1, 1  # for 3 units up and right
density_per_unit = 500  # how many pixels per unit
ITERATIONS = 10

# real and imaginary axis
re = np.linspace(x_start, x_start + width, int(width * density_per_unit))
im = np.linspace(y_start, y_start + height, int(height * density_per_unit))

fig = plt.figure(figsize=(10, 10))  # instantiate a figure to draw
ax = plt.axes()  # create an axes object


def animate(it):
    # print("animate")
    ax.clear()  # clear axes object
    # print("oh no")
    ax.set_xticks([])  # clear x-axis ticks
    ax.set_yticks([])  # clear y-axis ticks
    # print("bella")
    X = np.empty((len(re), len(im)))  # re-initialize the array-like image
    # threshold = round(1.15 ** (i + 1))  # calculate the current threshold
    # print(it)
    # iterations for the current threshold
    for i in range(len(re)):
        for j in range(len(im)):
            # print("c = "+str(complex(re[i], im[i])))
            # print(complex(re[i], im[i]))
            # X[i, j] = mandelbrot(re[i], im[j], threshold)
            # print(get_closest_zero(complex(re[i], im[i]), it))
            # X[i, j] = zeros_color_values.get(get_closest_zero(complex(re[i], im[i]), ITERATIONS))
            X[i, j] = zeros_color_values.get(get_closest_zero(complex(re[i], im[j]), ITERATIONS))
    print("Printing animation at " + str(it))
    # print(X)
    # associate colors to the iterations with an iterpolation
    img = ax.imshow(X.T, interpolation="bicubic", cmap='inferno')
    return [img]


anim = animation.FuncAnimation(fig, animate, frames=1, interval=500, blit=True)
plt.show()
anim.save('mandelbrot.gif', writer='imagemagick')

"""
Program to animate the Newton's Fractal.
To animate set ANIMATE to true and set the FRAME.
To get a single image set ANIMATE to False and the FRAME to 1.
To get different image colors change the colormap of the animation.
"""

import cmath
import math

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import threading

# Zeros of the function
zeros = [complex(-1, 0),
         complex(0, 1),
         complex(-1, -1)]

# Associate each zero with a value
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
        if cmath.polar(zero - res)[0] < min_dist:
            min_dist = cmath.polar(zero - res)[0]
            closest_zero = zero
    return closest_zero


x_start, y_start = -1.5, -0.75  # an interesting region starts here
width, height = 1, 1  # for 3 units up and right
density_per_unit = 1000  # how many pixels per unit
ITERATIONS = 10
ANIMATE = True
FRAME = 10

# real and imaginary axis
re = np.linspace(x_start, x_start + width, int(width * density_per_unit))
im = np.linspace(y_start, y_start + height, int(height * density_per_unit))

fig = plt.figure(figsize=(10, 10))  # instantiate a figure to draw
ax = plt.axes()  # create an axes object
result = np.empty((len(re), len(im)))  # re-initialize the array-like image

def im_axes(i, it):
        for j in range(len(im)):
            if ANIMATE:
                result[i, j] = zeros_color_values.get(get_closest_zero(complex(re[i], im[j]), it))
            else:
                result[i, j] = zeros_color_values.get(get_closest_zero(complex(re[i], im[j]), ITERATIONS))


def animate(it):
    ax.clear()  # clear axes object
    ax.set_xticks([])  # clear x-axis ticks
    ax.set_yticks([])  # clear y-axis ticks

    # Calculating the function for each point in complex plane
    for i in range(len(re)):
        t = threading.Thread(target=im_axes, args=(i,it,))
        t.start()

    print("Calculating frame " + str(it))
    # associate colors to the iterations with an interpolation, trasponing the result matrix
    """
    Change the interpolation to get different image result, and the
    cmap to get different color scheme
    """
    img = ax.imshow(result.T, interpolation="bicubic", cmap='inferno')
    return [img]


# Create the animation
anim = animation.FuncAnimation(fig, animate, frames=FRAME, interval=100, blit=True)

# Shows the image
plt.show()
# Saves the image as .gif
anim.save('mandelbrot.gif', writer='imagemagick')

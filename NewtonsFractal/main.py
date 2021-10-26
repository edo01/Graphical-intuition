"""
Python script to plot a fractal emerging from the Newton's Method
to approximate the zeros of a function.
Inspired by 3Blue1Brown : https://www.youtube.com/watch?v=-RdOwhmqP5s
Author : Luca Domeniconi    
"""

import math
import cmath
from PIL import Image, ImageDraw

real_zeros = [complex(4, -4),
              complex(5, 5),
              complex(-1, -3)]
color_map = {real_zeros[0]: 'Aqua',
             real_zeros[1]: 'Crimson',
             real_zeros[2]: 'Blue'}


def function(x):
    return (x - real_zeros[0]) * (x - real_zeros[1]) * (x - real_zeros[2])


def derivative(x):
    return (x - real_zeros[0]) * (x - real_zeros[2]) + \
           (x - real_zeros[1]) * (x - real_zeros[2]) + \
           (x - real_zeros[1]) * (x - real_zeros[0])


def newton_method(x, iterations):
    for i in range(iterations):
        x = x - (function(x) / derivative(x))
    return x


def get_closest_zero(x, iterations):
    res = newton_method(x, iterations)
    min_dist = math.inf
    for zero in real_zeros:
        if cmath.polar(zero - res)[0] < min_dist:
            min_dist = cmath.polar(zero - res)[0]
            closest_zero = zero

    return closest_zero


# Plot window
RE_START = -10
RE_END = 10
IM_START = -10
IM_END = 10
WIDTH = 750
HEIGHT = 750
ITERATIONS = 10

im = Image.new('RGB', (WIDTH, HEIGHT), (0, 0, 0))
draw = ImageDraw.Draw(im)

for x in range(0, WIDTH):
    for y in range(0, HEIGHT):
        # Convert pixel coordinate to complex number
        c = complex(RE_START + (x / WIDTH) * (RE_END - RE_START),
                    -(IM_START + (y / HEIGHT) * (IM_END - IM_START)))
        # Drawing the point with the closest zero color
        draw.point([x, y], color_map.get(get_closest_zero(c, ITERATIONS)))

# Draw black circles for the real zeros
for z in real_zeros:
    x = WIDTH * (z.real - RE_START) / (RE_END - RE_START)
    y = HEIGHT * (z.imag - IM_START) / (IM_END - IM_START)
    radius = 5
    draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill='black')

im.save('output.png', 'PNG')

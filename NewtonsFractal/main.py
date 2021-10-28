"""
Python script to plot a fractal emerging from the Newton's Method
to approximate the zeros of a function.
Inspired by 3Blue1Brown : https://www.youtube.com/watch?v=-RdOwhmqP5s
Author : Luca Domeniconi    
"""

import math
import cmath
import time

from PIL import Image, ImageDraw, ImageFilter
import numpy as np

real_zeros = np.array([0 + 1j,
                      -1 + 0j,
                      1 + -1j])

color_map = {real_zeros[0]: '#082032',
             real_zeros[1]: '#2C394B',
             real_zeros[2]: '#FF4C29'}


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
    t = time.time()
    res = newton_method(x, iterations)
    print("Time for Newton : " + str(time.time() - t))

    print(np.vectorize(closest_zero)(res))
    print(np.vectorize(get_color)(res))
    # for zero in real_zeros:
        #if cmath.polar(zero - res)[0] < min_dist:
        # if (res.real ** 2 + res.imag ** 2).any() < min_dist:
    #        min_dist = res.real*res.real + res.imag*res.imag
    #        closest_zero = zero

    #return closest_zero

def closest_zero(x):
    min_dist = math.inf
    for zero in real_zeros:
        if x.real ** 2 + x.imag ** 2 < min_dist:
            min_dist = x.real ** 2 + x.imag ** 2
            z = zero
    return z

def get_color(x):
    return color_map.get(x)

# Plot window
RE_START = -8
RE_END = 8
IM_START = -8
IM_END = 8
WIDTH = 1000
HEIGHT = 1000
ITERATIONS = 10

im = Image.new('RGB', (WIDTH, HEIGHT), (0, 0, 0))
draw = ImageDraw.Draw(im)

real, imag = np.meshgrid(np.arange(WIDTH),np.arange(HEIGHT))
real = RE_START + (real / WIDTH) * (RE_END - RE_START)
imag = -(IM_START + (imag / HEIGHT) * (IM_END - IM_START))
t = time.time()
c = real + imag * 1j
print("Time for c :" + str(time.time() - t))
t = time.time()
cz = get_closest_zero(c,ITERATIONS)
print("Time for get closet zero :" + str(time.time()-t))
# print(cz)
# print(get_closest_zero(c, ITERATIONS))
#for value,color in color_map.items():
#    c = np.where(c == value,)

# for x in range(0, WIDTH):
#    for y in range(0, HEIGHT):
        # Convert pixel coordinate to complex number
        # c = complex(RE_START + (x / WIDTH) * (RE_END - RE_START),
        #            -(IM_START + (y / HEIGHT) * (IM_END - IM_START)))
        # Drawing the point with the closest zero color
#            draw.point([x, y], color_map.get(get_closest_zero(c[x,y], ITERATIONS)))
for p,color in np.nditer(c),np.nditer(cz):
    draw.point([p.real,p.imag],color_map[color])

# Draw black circles for the real zeros
for z in real_zeros:
    x = WIDTH * (z.real - RE_START) / (RE_END - RE_START)
    y = HEIGHT * (-z.imag - IM_START) / (IM_END - IM_START)
    radius = 5
    draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill='black')
im = im.resize((int(WIDTH // 2), int(HEIGHT // 2)), resample=Image.ANTIALIAS)
im.save('output.png', 'PNG', quality=100)

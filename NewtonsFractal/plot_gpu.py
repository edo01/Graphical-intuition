"""
Program to animate the Newton's Fractal.
To animate set ANIMATE to true and set the FRAME.
To get a single image set ANIMATE to False and the FRAME to 1.
To get different image colors change the colormap of the animation.
"""

import time

import torch
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# if 'cuda' runs on GPU, if 'cpu' runs on CPU
device = 'cpu'

# Zeros of the function
zeros = torch.tensor([-1 + 0j, 0 + 1j, -1 - 1j]).to(device)

# Associate each zero with a value
zeros_color_values = {zeros[0]: torch.tensor(1 + 0j).to(device),
                      zeros[1]: torch.tensor(0 + 0j).to(device),
                      zeros[2]: torch.tensor(2 + 0j).to(device)}


def function(x):
    return (x - zeros[0]) * (x - zeros[1]) * (x - zeros[2])


def derivative(x):
    return (x - zeros[0]) * (x - zeros[2]) + \
           (x - zeros[1]) * (x - zeros[2]) + \
           (x - zeros[1]) * (x - zeros[0])


def newton_method(x, iterations):
    for _ in range(iterations):
        x = x - (function(x) / derivative(x))
    return x


def get_closest_zero(x, iterations):
    res = newton_method(x, iterations)

    # (H, W) -> (1, H, W)
    res = res.unsqueeze(0)
    # (N) -> (N, 1, 1)
    zeros_ = zeros.unsqueeze(-1).unsqueeze(-1)

    # distance to each zero
    dist = torch.abs(res - zeros_)
    # min_dist is the distance to the closest zeros, closest_zero is the index of the closest zero
    min_dist, closest_zero = torch.min(dist, axis=0)
    # convert the index of the zero to the actual value of the zero
    closest_zero = zeros[closest_zero]

    return closest_zero, dist.float(), min_dist.float()


def to_color(x):
    for k, v in zeros_color_values.items():
        x = torch.where(x == k, v, x)
    return x


x_start, y_start = -2, -2  # an interesting region starts here
width, height = 4, 4  # for 3 units up and right
density_per_unit = 500  # how many pixels per unit
ITERATIONS = 20
ANIMATE = False
FRAME = 1

# real and imaginary axis
re = torch.linspace(x_start, x_start + width, int(width * density_per_unit)).to(device)
im = torch.linspace(y_start, y_start + height, int(height * density_per_unit)).to(device)

re_, im_ = torch.meshgrid(re, im)
cmpl = re_ + im_ * 1j

fig = plt.figure(figsize=(10, 10))  # instantiate a figure to draw
ax = plt.axes()  # create an axes object


def animate(it):
    if ANIMATE:
        print("Calculating frame " + str(it))
    else:
        print("Calculating image for " + str(ITERATIONS) + " iterations")
    ax.clear()  # clear axes object
    ax.set_xticks([])  # clear x-axis ticks
    ax.set_yticks([])  # clear y-axis ticks

    # result, dist = get_closest_zero(cmpl, it)
    result, all_dist, min_dist = get_closest_zero(cmpl, it)
    result = to_color(result).real

    # associate colors to the iterations with an interpolation, trasponing the result matrix
    """
    Change the interpolation to get different image result, and the
    cmap to get different color scheme
    """

    result = result.detach().cpu().numpy()
    # result_colored = (cmap(result)[:3] * 255).astype(np.uint8)

    img = ax.imshow(result, interpolation="bicubic", cmap='inferno')
    return [img]


t = time.time()

if ANIMATE:
    # Create the animation
    anim = animation.FuncAnimation(fig, animate, frames=FRAME, interval=200, blit=True)
    # Shows the image
    plt.show()
    # Saves the image as .gif
    anim.save('output.gif', writer='imagemagick')
else:
    # Just call the animate function 1 time and saves
    animate(ITERATIONS)
    plt.savefig('output.png')

print("Total render time : " + str(time.time() - t))

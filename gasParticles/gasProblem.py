import matplotlib.pyplot as plt
import numpy as np
import random
import matplotlib.animation as animation
import time

cMinX, cMaxX = -5.0, 5.0
cMinY, cMaxY = -5.0, 5.0
center = (cMaxX - cMinX)/2.0
deltaC = .5
cx, cy = np.meshgrid(np.arange(cMinX, cMaxX, deltaC), np.arange(cMinY, cMaxY, deltaC))


p = .6
q = 1-p
N = 20

#histogram
HIST_BINS = np.linspace(0, N, N)
data = []
n, _ = np.histogram(data, HIST_BINS)


fig, (ax, ax2) = plt.subplots(2,1)

def plot(i):
	ax.clear()
	np.histogram(data, HIST_BINS)
	right = 0
	for x in range(N):
	    side = center
	    if(random.random()<p):
	        side = 0
	        right += 1
	    x = side + center*random.random()
	    y = (cMinY-cMaxY)*random.random()
	    #print(str(x) +  "\t" + str(y))
	    ax.plot(x, y, 'o', color='blue')
	data.append(right)
	ax2.hist(data, HIST_BINS, lw=1,ec="yellow", fc="green", alpha=0.5)



frames = 100 
interval = 10
ax2.set_ylim(top=frames)

_, _, bar_container = ax2.hist(data, HIST_BINS, lw=1,
                              ec="yellow", fc="green", alpha=0.5)
anim = animation.FuncAnimation(fig, plot,frames = frames, interval=interval)

plt.show()


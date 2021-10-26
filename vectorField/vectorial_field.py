import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
import math
#settings
# s0 -> rot graph
# s1 -> vectorial field
s0,s1 = True, True

#x,y = np.meshgrid(np.linspace(-5,5,10),np.linspace(-5,5,10))

def div(x,y):
    return np.cos(x)

def curl(x,y):
    return 10*np.cos(y)-10*np.cos(x)

def f(x,y):
    return np.sin(y)*10, np.sin(x)*10

fig, ((ax3, ax4),(ax1, ax2)) = plt.subplots(2, 2)


# Curl graph
deltaC = .005
cMinX, cMaxX = -5.0, 5.0
cMinY, cMaxY = -5.0, 5.0
cx, cy = np.meshgrid(np.arange(cMinX, cMaxX, deltaC), np.arange(cMinY, cMaxY, deltaC))
cZ = curl(cx,cy)

# style
cmap = plt.get_cmap('autumn')
levels = MaxNLocator(nbins=40).tick_values(cZ.min(), cZ.max())
norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)


# 2-D Vectorial field
deltaV = .5
vMinX, vMaxX = -5.0, 5.0
vMinY, vMaxY = -5.0, 5.0
vx, vy = np.meshgrid(np.arange(vMinX, vMaxX, deltaV), np.arange(vMinY, vMaxY, deltaV))
vfx, vfy = f(vx, vy) 


# StreamLine
strm = ax3.streamplot(vx, vy, vfx, vfy, color=vfx**2+vfy**2, linewidth=2, cmap='autumn')
fig.colorbar(strm.lines)
ax3.set_title('Linee di campo')


# Divergence
deltaD = .005
dMinX, dMaxX = -5.0, 5.0
dMinY, dMaxY = -5.0, 5.0
dx, dy = np.meshgrid(np.arange(dMinX, dMaxX, deltaD), np.arange(dMinY, dMaxY, deltaD))
dz = div(dx,dy)


ax4.set_title('Divergenza')
ax4.pcolormesh(dx,dy,dz)

ax1.set_title('Rotore')
ax1.pcolormesh(cx,cy,cZ, cmap = "autumn", norm = norm)

ax2.set_title('Campo vettoriale')
ax2.quiver(vx,vy,vfx,vfy)

plt.show()

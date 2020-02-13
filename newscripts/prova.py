# By Luca
#### DEMO

from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import make_lupton_rgb
from astropy.visualization import *

forCasting = np.float_()

### READING
b = fits.open("data/"+"M66-Blue.fts")[0].data
r = fits.open("data/"+"M66-Red.fts")[0].data 
g = fits.open("data/"+"M66-Green.fts")[0].data

### CASTING
r = np.array(r,forCasting)
g = np.array(g,forCasting)
b = np.array(b,forCasting)

### STRETCHING
stretch = LogStretch
r = LogStretch(values = r, clip=False)
g = LogStretch(values = g, clip=False)
b = LogStretch(values = b, clip=False)

### SAVING
rgb_default = make_lupton_rgb(r, g, b, minimum=1000, stretch=900, Q=100, filename="provafinale.jpeg")
plt.imshow(rgb_default, origin='lower')
plt.show()


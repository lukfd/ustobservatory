# By Luca
#### DEMO
from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import make_lupton_rgb
from astropy.visualization import *
# import astroalign as aa

forCasting = np.float_()

### READING
b = fits.open("data/"+"M66-Blue.fts")[0].data
r = fits.open("data/"+"M66-Red.fts")[0].data 
g = fits.open("data/"+"M66-Green.fts")[0].data

### IMAGE REGISTRATION
# registered_image is now a transformed (numpy array) image of source that will match pixel to pixel to target.
# registered_image, footprint = aa.register(r, g)
# registered_image, footprint = aa.register(registered_image, b)

### CASTING
r = np.array(r,forCasting)
g = np.array(g,forCasting)
b = np.array(b,forCasting)

### Zscale
interval = ZScaleInterval()

### STRETCHING ### SQRT
stretch = SqrtStretch() + ZScaleInterval()
# r = LogStretch(r)
# g = LogStretch(g)
# b = LogStretch(b)

r = stretch(b)
g = stretch(r)
b = stretch(g)

plt.imshow(r, origin='lower')
plt.show()
plt.imshow(g, origin='lower')
plt.show()
plt.imshow(b, origin='lower')
plt.show()

### SAVING
# rgb_default = make_lupton_rgb(r, g, b, minimum=1000, stretch=900, Q=100, filename="provafinale.png")
rgb_default = make_lupton_rgb(r, g, b, filename="provafinale.png")
plt.imshow(rgb_default, origin='lower')
plt.show()


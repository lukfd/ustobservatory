# By Luca
#### DEMO
from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import make_lupton_rgb
from astropy.visualization import *
# import astroalign as aa

def make_colored(image_r, image_g, image_b, filename=None):
	image_r = np.asarray(image_r)
	image_g = np.asarray(image_g)
	image_b = np.asarray(image_b)

	# if (image_r.shape != image_g.shape) or (image_g.shape != image_b.shape):
	#     msg = "The image shapes must match. r: {}, g: {} b: {}"
	#     raise ValueError(msg.format(image_r.shape, image_g.shape, image_b.shape))
	    
	rgb = np.dstack(image_r, image_g, image_b).astype(np.uint8)
	import matplotlib.image
	matplotlib.image.imsave(filename, rgb, origin = 'lower')

### READING
b = fits.open("data/"+"M66-Blue.fts")[0].data
r = fits.open("data/"+"M66-Red.fts")[0].data 
g = fits.open("data/"+"M66-Green.fts")[0].data

### IMAGE REGISTRATION
# registered_image is now a transformed (numpy array) image of source that will match pixel to pixel to target.
# registered_image, footprint = aa.register(r, g)
# registered_image, footprint = aa.register(registered_image, b)

### CASTING
forCasting = np.float_()
# r = np.array(r,forCasting)
# g = np.array(g,forCasting)
# b = np.array(b,forCasting)

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
# rgb_default = make_lupton_rgb(r, g, b, filename="provafinale.png")
rgb_default = make_colored(r,g,b, filename = "provafinale.png")
plt.imshow(rgb_default, vmin = 0, vmax = 1,origin='lower')
plt.show()

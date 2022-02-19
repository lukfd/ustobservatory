import numpy as np

def createColoredImage(image_r, image_g, image_b, filename=None):
	image_r = np.asarray(image_r)
	image_g = np.asarray(image_g)
	image_b = np.asarray(image_b)
	    
	rgb = np.dstack(image_r, image_g, image_b).astype(np.uint8)
	import matplotlib.image
	matplotlib.image.imsave(filename, rgb, origin = 'lower')
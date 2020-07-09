# University of St. Thomas' Observatory
*These data are property of the St. Thomas University. All rights are reserved.*
> Luca Comba : comb6457@stthomas.edu
> for other infos [lukfd.github.io](https://lukfd.github.io/)
---

Using photoshop we should be able to process it easily, Nothing is better than coding it !
Using fit, fits, fts files to get colorized pictures

---
# ToDo List

see newscript folder

- [ ] allign images
It's called Image Registration. 
[Astronomical Image Registration Docs](https://image-registration.readthedocs.io/en/latest/)
,[Github tutorial](https://github.com/keflavich/image_registration)
,[A paper about it](https://arxiv.org/pdf/1909.02946.pdf)
- [ ] merge green, red and blue fits images
- [ ] adjust colors levels
- [ ] rotate images correctly
- [x] Read Fit imgs
- [x] manipulate data
- [x] manipulate pixels

**Things to keep in mind :**
- img with moving objects
- bad pixels
- light pollution
- circle pixels

---

# Documentation

## readfit.py
Object to create is FitsData(filename)
from this class there are these methods :

**1. General Read Fits files***

- __init__(filename)
- close()

**2. Reading meta data**

- printInfo()
- printDate()
- setHeader(targname, observer)
- getHeaderKeys() : return a list of the header's key
- getHeaderKey(key) : return the key's value

**3. Reading Image data**

- getShape() : return tuple of the shape of the image
- getNameType() : return data type
- getPixelArray() : return ENTIRE array of pixels values
***
## colorastro.py (a faster way to make RGB pictures)

It is a simplified Astropy application for processing RGB image stored in the /data directory.

using : aplply [for making RGB](https://aplpy.readthedocs.io/en/stable/api/aplpy.make_rgb_image.html#aplpy.make_rgb_image) and for image registration [Image-registration.py](https://image-registration.readthedocs.io/en/latest/image_registration.html#) or could use [AstroAlign](https://astroalign.readthedocs.io/en/latest/?fbclid=IwAR2t__2JR2mswh50jVfTIPIGzHDDtsK4Iv5rrT-AKHxIA9vFdX3-AAHLfRw)

From some people insights we can try to use other Python pachages to color the pictures:

- make_lupton_rgb just apply a asinh stretch and assumes that the input image is linear. Therefore you would just need to apply scale and Q as parameters of the method. Another problem that could be related to **make_lupton_rgb** is that is needed to change vmin and vmax [Reddit Post](https://www.reddit.com/r/askastronomy/comments/g078q6/problem_with_making_colored_images_in_astropy/)
- Use matplotlib. [Here is an Example of MATPLOTLIB for coloring pictures](https://github.com/soar-telescope/goodman_pipeline/blob/f0e050e1762e984e491577bdda383d63c49d7ab4/goodman_pipeline/core/core.py?fbclid=IwAR2o2UprDblvUramMnZVuoRfNy3KGukHahg7jIMoEJ6n-vT_JyG5CgXr0N8#L3193-L3209) The only imporntat part is to define the lower and upper limits as is Z1 and Z2, so then in imshow() use clim(Z1, Z2) where formulas for Z1 and Z2 come form iraf.
- Another method is to use [APLpy](https://aplpy.readthedocs.io/en/stable/rgb.html?fbclid=IwAR1E8DeXcgFvlXJOzcY2QJO92zr-51ADO4rIg7sl-Qo_5YcTc0Srz1Lnyzg) Making RGB Images!

Use django for making an app online
***
# Useful links and DOCs
- [Astropy](http://docs.astropy.org/en/stable/index.html) (DOCs for astropy)
- [Astropy tutorials](http://learn.astropy.org/)(Search Astropy tutorials)
- [Pillow](https://pillow.readthedocs.io/en/stable/index.html) (DOCs of a Pyhton library for image processing)
- [Scipy](http://scipy-lectures.org/advanced/image_processing/) (tips for image processing)
- [PyFits](https://pythonhosted.org/pyfits/#creating-a-new-image-file) (DOCs for PyFits by STSI)
- [Python code to convert](https://astromsshin.github.io/science/code/Python_fits_image/index.html) (python direction to convert fits images)
- [http://prancer.physics.louisville.edu/astrowiki/index.php/Image_processing_with_Python_and_SciPy](http://prancer.physics.louisville.edu/astrowiki/index.php/Image_processing_with_Python_and_SciPy)(FITS images hints)
- [Fitstoimg](https://github.com/psds075/fitstoimg) (fits extension to Jpg)
- [SCIKIT- IMAGE a Py Library on GitHub](https://github.com/scikit-image/scikit-image)
- [An Astropy library to make it easy? APLPY](https://aplpy.readthedocs.io/en/stable/fitsfigure/quick_reference.html) (APLPY library)


#### Other general links

- [Space Telescope Science Institute - Home | STScI](http://www.stsci.edu/) , We help humanity explore the universe with advanced space telescopes and ever-growing data archives. 
- NASA Fits support [Website](https://fits.gsfc.nasa.gov/), 
- NASA SOFTWARE for data and Image processing [Website](https://software.nasa.gov/data_and_image_processing)
- scikit-Image [Python Library](https://scikit-image.org/)
- Ginga [a japanese Python library](http://www.astropython.org/packages/ginga/)

#### files from the ssh observatory.
present in the file system :
 Scripts (pipeline)
which uses pyRaf

#### Good resources
- [Facebook group](https://www.facebook.com/groups/1596306890613995/search/?q=luca%20comba) for ASTROPY
- [Reddit group](https://www.reddit.com/r/askastronomy/)
- [Image Registration Reddit](https://www.reddit.com/r/askastronomy/comments/g8p1oz/image_registration_in_python/)
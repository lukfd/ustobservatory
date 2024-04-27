# University of St. Thomas' Observatory S
*These data are property of the St. Thomas University. All rights are reserved.*
Authors:
- Luca Comba, [luca.comba98@gmail.com](luca.comba98@gmail.com)

## Image Registration

From some people insights we can try to use other Python pachages to color the pictures:

make_lupton_rgb just apply a asinh stretch and assumes that the input image is linear. Therefore you would just need to apply scale and Q as parameters of the method. Another problem that could be related to **make_lupton_rgb** is that is needed to change vmin and vmax [Reddit Post](https://www.reddit.com/r/askastronomy/comments/g078q6/problem_with_making_colored_images_in_astropy/)

Use matplotlib. [Here is an Example of MATPLOTLIB for coloring pictures](https://github.com/soar-telescope/goodman_pipeline/blob/f0e050e1762e984e491577bdda383d63c49d7ab4/goodman_pipeline/core/core.py?fbclid=IwAR2o2UprDblvUramMnZVuoRfNy3KGukHahg7jIMoEJ6n-vT_JyG5CgXr0N8#L3193-L3209) The only imporntat part is to define the lower and upper limits as is Z1 and Z2, so then in imshow() use clim(Z1, Z2) where formulas for Z1 and Z2 come form iraf.

Another method is to use [APLpy](https://aplpy.readthedocs.io/en/stable/rgb.html?fbclid=IwAR1E8DeXcgFvlXJOzcY2QJO92zr-51ADO4rIg7sl-Qo_5YcTc0Srz1Lnyzg) Making RGB Images!

The issue with the M66 image seems to be that the background is too dark in respect to the object observed, we need to do some **Flat Fielding** [The github issue](https://github.com/keflavich/image_registration/issues/26)


## Other Resources
- [Astropy](http://docs.astropy.org/en/stable/index.html) (DOCs for astropy)
- [APLPY](https://aplpy.readthedocs.io/en/stable/#) (Making RGB from FITS)
- [image_registration](https://image-registration.readthedocs.io/en/latest/image_registration.html) (shifting and image registration in python)


- [Astropy tutorials](http://learn.astropy.org/)(Search Astropy tutorials)
- [Pillow](https://pillow.readthedocs.io/en/stable/index.html) (DOCs of a Pyhton library for image processing)
- [Scipy](http://scipy-lectures.org/advanced/image_processing/) (tips for image processing)
- [PyFits](https://pythonhosted.org/pyfits/#creating-a-new-image-file) (DOCs for PyFits by STSI)
- [Python code to convert](https://astromsshin.github.io/science/code/Python_fits_image/index.html) (python direction to convert fits images)
- [http://prancer.physics.louisville.edu/astrowiki/index.php/Image_processing_with_Python_and_SciPy](http://prancer.physics.louisville.edu/astrowiki/index.php/Image_processing_with_Python_and_SciPy)(FITS images hints)
- [Fitstoimg](https://github.com/psds075/fitstoimg) (fits extension to Jpg)
- [SCIKIT- IMAGE a Py Library on GitHub](https://github.com/scikit-image/scikit-image)
- [scikit-image.org/docs](https://scikit-image.org/docs/stable/api/api.html)

## Online Communities

- [Space Telescope Science Institute - Home | STScI](http://www.stsci.edu/) , We help humanity explore the universe with advanced space telescopes and ever-growing data archives. 
- NASA Fits support [Website](https://fits.gsfc.nasa.gov/), 
- NASA SOFTWARE for data and Image processing [Website](https://software.nasa.gov/data_and_image_processing)
- scikit-Image [Python Library](https://scikit-image.org/)
- Ginga [a japanese Python library](http://www.astropython.org/packages/ginga/)
- [Reddit group](https://www.reddit.com/r/askastronomy/)
- [Image Registration Reddit](https://www.reddit.com/r/askastronomy/comments/g8p1oz/image_registration_in_python/)

# University of St. Thomas' Observatory
*These data are property of the St. Thomas University. All rights are reserved.*
> Luca Comba : comb6457@stthomas.edu
> for other infos [lukfd.github.io](https://lukfd.github.io/)
---

Using photoshop we should be able to process it easily, Nothing is better than coding it !
Using fit, fits, fts files to get colorized pictures
# ToDo
see newscript folder
- [x] Read Fit imgs
- [ ] manipulate data
- [ ] manipulate pixels

**Things to keep in mind :**
- moving earth
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

#### Other general links
- [Space Telescope Science Institute - Home | STScI](http://www.stsci.edu/) , We help humanity explore the universe with advanced space telescopes and ever-growing data archives. 
- NASA Fits support [Website](https://fits.gsfc.nasa.gov/), 
- NASA SOFTWARE for data and Image processing [Website](https://software.nasa.gov/data_and_image_processing)
- scikit-Image [Python Library](https://scikit-image.org/)

#### files from the ssh observatory.
present in the file system :
 Scripts (pipeline)
which uses pyRaf

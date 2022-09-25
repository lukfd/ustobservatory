from astropy.io import fits
import numpy as np

# Returns a np.ndarray
def convertImageToNdarray(filePath):
    with fits.open(filePath) as hdul:
        return np.float_(hdul[0].data)
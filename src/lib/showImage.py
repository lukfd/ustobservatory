import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.visualization import hist


def showImageGray(file):
    image_data = fits.getdata(file)
    plt.imshow(image_data, cmap='gray')
    plt.colorbar()
    plt.show()


def showImageGrayLog(file):
    from matplotlib.colors import LogNorm
    image_data = fits.getdata(file)
    plt.imshow(image_data, cmap='gray', norm=LogNorm())
    plt.colorbar()
    plt.show()


def showImageHistogram(file):
    image_data = fits.getdata(file)
    plt.hist(image_data.flatten(), bins='auto')

def plotArrayHistogram(array):
    hist(array.tolist(), bins='blocks')


def showImageCoordinates(file):
    from astropy.wcs import WCS

    hdu = fits.open(file)[0]
    wcs = WCS(hdu.header)

    plt.subplot(projection=wcs)
    plt.imshow(hdu.data, origin='lower')
    plt.grid(color='white', ls='solid')
    plt.xlabel('Galactic Longitude')
    plt.ylabel('Galactic Latitude')

    plt.show()

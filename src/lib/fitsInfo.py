from email.mime import image
from astropy.io import fits


def getImageInfo(file):
    with fits.open(file) as hdul:
        hdul.info()


def getImageShape(file):
    image_data = fits.getdata(file)
    print(image_data.shape)


def getImageType(file):
    image_data = fits.getdata(file)
    print(type(image_data))


def getImageHeader(file):
    hdul = fits.open(file)
    return hdul[0].header


def printImageHeaderList(file):
    print(repr(getImageHeader(file)))


def printImageColorFilter(file):
    print(getImageHeader(file)['FILTER'])


def printImageDate(file):
    print(getImageHeader(file)['DATE'])

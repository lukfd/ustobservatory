from astropy.visualization import make_lupton_rgb
from astropy.visualization import SqrtStretch
from astropy.convolution import Gaussian2DKernel, convolve
import matplotlib.pyplot as plt
from datetime import datetime as date

# Return a process to blur or remove the contrast in an image.
# https://docs.astropy.org/en/stable/convolution/index.html
def convolveImage(imageNdArray):
    # Create kernel
    g = Gaussian2DKernel(x_stddev = 1)
    # Convolve data
    z = convolve(imageNdArray, g)
    return z

def applySqrtStrech(imageNdArray):
    stretch = SqrtStretch()
    return stretch(imageNdArray)

# Return a flatten image
# Reference: https://linuxtut.com/en/2d82fe71f41fc00cb6f8/
# 
def flatFieldCorrection(imageNdArray):
    return

def plotColoredImage(redNdarray, greenNdarray, blueNdarray):
    print("plotting colored image")
    rgbProcessed = make_lupton_rgb(
        redNdarray, 
        greenNdarray, 
        blueNdarray, 
        filename="../processed/" + date.now().strftime("%m-%d-%Y %H-%M-%S") + ".jpeg")
    plt.imshow(rgbProcessed, origin='lower')
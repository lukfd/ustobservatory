#### LUCA COMBA
from astropy.stats import SigmaClip
from photutils import MeanBackground
####
from astroalign import astroalign as aa
import numpy as np
from astropy.io import fits
from astropy.visualization import *
import aplpy
###
from astropy import units as u
import numpy as np
from astropy.nddata import CCDData
import ccdproc

from astropy.modeling import models
###
from image_registration import image_registration as image_registration
from image_registration.image_registration.fft_tools import shift

### Reading the data
h_r = fits.open("data/"+"M66-Red.fts")[0].header
h_g = fits.open("data/"+"M66-Green.fts")[0].header
h_b = fits.open("data/"+"M66-Blue.fts")[0].header

b = fits.open("data/"+"M66-Blue.fts")[0].data
r = fits.open("data/"+"M66-Red.fts")[0].data 
g = fits.open("data/"+"M66-Green.fts")[0].data

### CASTING ???

### STRETCHING
# stretch = SqrtStretch() + ZScaleInterval()
# r = stretch(b)
# g = stretch(r)
# b = stretch(g)

# Flat Fielding RED
'''
data = CCDData(img, unit=u.adu)
data_with_deviation = ccdproc.create_deviation(
                          data, gain=1.5 * u.electron/u.adu,
                          readnoise=5 * u.electron)
data_with_deviation.header['exposure'] = 30.0  # for dark subtraction

gain_corrected = ccdproc.gain_correct(data_with_deviation, 1.5*u.electron/u.adu)

cr_cleaned = ccdproc.cosmicray_lacosmic(gain_corrected, sigclip=5)

oscan_subtracted = ccdproc.subtract_overscan(cr_cleaned,
                                             overscan=cr_cleaned[:, 200:],
                                             overscan_axis=1)
poly_model = models.Polynomial1D(1)  # one-term, i.e. constant
oscan_subtracted = ccdproc.subtract_overscan(cr_cleaned,
                                             overscan=cr_cleaned[:, 200:],
                                             overscan_axis=1,
                                             model=poly_model)

trimmed = ccdproc.trim_image(oscan_subtracted[:, :200])

fake_bias_data = np.random.normal(size=trimmed.shape)  # just for illustration
master_bias = CCDData(fake_bias_data, unit=u.electron,
                      mask=np.zeros(trimmed.shape))
bias_subtracted = ccdproc.subtract_bias(trimmed, master_bias)

master_dark = master_bias.multiply(0.1)  # just for illustration
master_dark.header['exposure'] = 15.0
dark_subtracted = ccdproc.subtract_dark(bias_subtracted, master_dark,
                                        exposure_time='exposure',
                                        exposure_unit=u.second,
                                        scale=True)

fake_flat_data = np.random.normal(loc=1.0, scale=0.05, size=trimmed.shape)
master_flat = CCDData(fake_flat_data, unit=u.electron)
reduced_image = ccdproc.flat_correct(dark_subtracted, master_flat)
'''




# do a Image registration OR ASTRO ALIGN ???
image = r
shifted = g
dx,dy,edx,edy = image_registration.chi2_shift(image, shifted, upsample_factor='auto')
g = shift.shiftnd(shifted, (dx, dy))

image = r
shifted = b
dx,dy,edx,edy = image_registration.chi2_shift(image, shifted, upsample_factor='auto')
b = shift.shiftnd(shifted, (dx, dy))

# saving as a fits
fits.writeto('M66_R.fits', r, header= h_r, overwrite=True)
fits.writeto('M66_G.fits', g, header= h_g, overwrite=True)
fits.writeto('M66_B.fits', b, header= h_b, overwrite=True)

############ Creating RGB Image
# aplpy.make_rgb_image(['data/M66-Blue.fts', 'data/M66-Green.fts',
#                      'data/M66-Red.fts'],
#                      output = 'M66_rgb.png')

aplpy.make_rgb_image(['M66_R.fits', 'M66_G.fits',
                     'M66_B.fits'], output = 'M66_rgb.png')

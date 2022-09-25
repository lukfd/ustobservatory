from image_registration import chi2_shift
from image_registration.fft_tools import shift

# Return a shifted np.ndarray based on the chi2 calculation of the offeset
# Check: https://image-registration.readthedocs.io/en/latest/index.html
#        https://github.com/keflavich/image_registration/blob/master/examples/Cross%20Correlation.ipynb
# Warning: Might be bad for stelar images
def getShiftedImage(imageNdarray, imageShiftedNdarray):
    xoff, yoff, exoff, eyoff = chi2_shift(imageNdarray, imageShiftedNdarray, return_error=True, upsample_factor='auto')
    imageShiftedNdarray = shift.shiftnd(imageShiftedNdarray, (-yoff, -xoff))
    #print(imageShiftedNdarray)
    return imageShiftedNdarray
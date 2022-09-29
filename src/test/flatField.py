# TEST SCRIPT TO SIMULATE HISTOGRAM IN https://linuxtut.com/en/2d82fe71f41fc00cb6f8/
import matplotlib.pyplot as plt
import sys
sys.path.append("../lib")
import convertUtils as converter
from astropy import stats as astropy

# Convert images to ndarray
print("Converting images to ndarray")
ndarrayR = converter.convertImageToNdarray("../../data/M66-Color/M66-S001-Red-R001-Red.fts")

data = astropy.histogram(ndarrayR, bins='scott')

plt.hist(data)
plt.title('Histogram of Data')
plt.xlabel('data')
plt.ylabel('count')

plt.show()

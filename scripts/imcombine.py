import glob
from astropy.io import fits
from pprint import pprint as pp
from numpy import *
from time import clock

files = glob.glob('./*.fits')

start = clock()

# Build the array
hd = fits.open(files[0])
result = ones(append(hd[0].data.shape, size(files)))



plane = 0
for f in files:
		
	print f
	hd = fits.open(f,memmap=True)

	result[:,:,plane] = hd[0].data
	
#	if plane == 0:
#		result = hd[0].data
#	else:
#		result = dstack((result,hd[0].data))

	plane += 1

	
print "Calculating median"
r = median(result,axis=2)

print r.shape

end = clock()

print "Elapsed time ",end-start



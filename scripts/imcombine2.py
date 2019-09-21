from pyraf import iraf
from time import clock

start = clock()

# Set up task parameters
iraf.imcombine.unlearn()					# Default parameter list
iraf.imcombine.input = "@images.txt"		# comma delimited list of input files
iraf.imcombine.output = "Out2"				# output file
iraf.imcombine.combine = "median"			# Median combine bias frames
iraf.imcombine.mode = "h"

# Run imcombine
iraf.imcombine()							

end = clock()

print "Elapsed time: ", end-start

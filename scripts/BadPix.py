#! /usr/bin/python

import os
from BasicProcessing.PipeLineSupport import *
from pyraf import iraf

def main():
	outdir = '/raid/data/home/observatory/data/scheduler/Calibration/BadPixelMask'

	bias_dir = '/raid/data/home/observatory/data/scheduler/Calibration/BiasTest'
	bfile = os.path.join(outdir,'cBias.fits')

	flat_dir = '/raid/data/home/observatory/data/scheduler/Calibration/20140629/Flat'
	ffile = os.path.join(outdir,'cFlat.fits')


	if not os.path.exists(bfile):
		MakecBias(bias_dir, bfile)
	
	MakecFlat(flat_dir)

def MakecBias(bias_dir, outfile):
	##########################
	# Combine bias frames
	########################## 
	bframes = filter(fits_filter, os.listdir(bias_dir))
	bframes = [os.path.join(bias_dir,i) for i in bframes]

	tfile = tempfile.mkstemp()
	os.write(tfile[0],"\n".join(bframes)+"\n")
	os.close(tfile[0])


	iraf.imcombine.unlearn()					# Default parameter list
	iraf.imcombine.input = "@" + tfile[1]		# comma delimited list of input files
	iraf.imcombine.output = outfile				# output file
	iraf.imcombine.combine = "median"			# Median combine bias frames
	iraf.imcombine.mode = "h"

	# Run imcombine
	iraf.imcombine()							

	os.remove(tfile[1])


def MakecFlat(flat_dir, outfile, filter="Luminance"):

	fimages = filter(fits_filter, os.listdir(flat_dir))	
	fimages = [os.path.join(flat_dir,i) for i in fimages]
	
	# Get only the desired filter
	fimages = filter(lambda x: GetHeaderKeyword(x, 'filter')==f, fimages)

	
	


if __name__=="__main__":main()
#########################################
# Luca Comba, for UST
#########################################

import os
import numpy as np
import sys
import math
import numpy
from PIL import Image
from astropy.io import fits
from matplotlib.colors import *
import matplotlib.pyplot as plt
from astropy.visualization import *
from astropy.utils.data import get_pkg_data_filename

'''USEFUL FUNCTIONS'''
# Fuction to visualize the array of pixels
def exportingArrayAsTxt(pixelarray):
	pixelarray = np.array2string(pixelarray)
	file = open("pixelarray.txt", "w+")

	for array in pixels:
		file.write(array)

	file.close()

def imageStack():
	return True

'''CREATING FITS IMAGE OBJECT
Methods : __init__ , close ,
  printInfo, printDate , setHeader , getHeaderKeys ,
  getShape , getNameType , getPixelArray , getPixelByIndex,
  printStats, stretchMinMax.
''' 
class FitsData:
	############
	# CONTRUCTOR
	def __init__(self, filename):
		self.img = fits.open("data/"+filename)
		self.hdr = self.img[0].header
		self.data = self.img[0].data
	
	def close(self):
		self.img.close()
	############
	# META
	def printInfo(self):
		print(self.img.info())

	def printDate(self):
		print(self.img[0].header["DATE"])

	def setHeader(self, targname, observer):
		self.hdr['targname'] = targname
		self.hdr['observer'] = observer

	def getHeaderKeys(self):
		self.hdr = self.img[0].header
		self.hdr = list(self.hdr.keys())
		return self.hdr

	def getHeaderKey(self, key):
		#key : must be a string
		self.hdr = self.img[0].header
		return self.hdr[key]

	def printStats(self, Min, Max, Mean, StDev):
		if (Min == True):
			print('Min:', np.min(self.data[0:]))
		elif (Max == True):
			print('Max:', np.max(self.data[0:]))
		elif (Mean == true):
			print('Mean:', np.mean(self.data[0:]))
		elif (StDev == True):
			print('Stdev:', np.std(self.data[0:]))
		else:
			print('Min:', np.min(self.data[0:]))
			print('Max:', np.max(self.data[0:]))
			print('Mean:', np.mean(self.data[0:]))
			print('Stdev:', np.std(self.data[0:]))
	##################
	# WORKING WITH IMG
	def getShape(self):
		base = self.getShape()[0]
		height = self.getShape()[1]
		return self.data.shape
	def getNameType():
		return self.data.dtype.name
	def getPixelArray(self):
		return self.data[0:]
	# TABLE DATA
	def getPixelByIndex(self, index):
		tbdata = self.img[0].data
		return tbdata[index]
	# IMAGE VISUALIZATION
	def stretchMinMax(self, typeStretch = LinearStretch(), show = True):
		pixels = self.data[0:]
		stretch = typeStretch
		norm = ImageNormalize(pixels, interval=MinMaxInterval(), stretch=stretch)
		if(show==True):
			fig = plt.figure()
			ax = fig.add_subplot(1, 1, 1)
			im = ax.imshow(pixels, origin='lower', norm=norm, cmap='gray')
			fig.colorbar(im)
			plt.show()
		else:
			return norm

def arrayStretchShow(pixels, typeStretch = LinearStretch(), show = True):
	stretch = typeStretch
	norm = ImageNormalize(pixels, interval=MinMaxInterval(), stretch=stretch)
	if(show==True):
		fig = plt.figure()
		ax = fig.add_subplot(1, 1, 1)
		im = ax.imshow(pixels, origin='lower', norm=norm, cmap='gray')
		fig.colorbar(im)
		plt.show()
	else:
		return norm

def arrayStretch(pixels, typeStretch):
	makeIt = typeStretch
	makeIt(values = pixels, clip=False, out = pixels)
	return pixels

### MAIN RUNNING PROGRAM

def Main():
	forCasting = np.float_()
	path = os.getcwd()
	for filename in os.listdir(path+"/data"):
		if filename.endswith(".fit") or filename.endswith(".fits") or filename.endswith(".fts"):
			# want to print all the data ?
			np.set_printoptions(threshold=sys.maxsize)
			# Creating the object
			hudl = FitsData(filename)
			pixels = hudl.getPixelArray()
			### Stretching on object image			
			hudl.stretchMinMax(SqrtStretch(), show = False)

			### SAVING
			forCasting = np.float_()
			if ('Red' in filename or 'red' in filename):
				image_r = np.array(pixels, forCasting)
				## stretching on array
				image_r = arrayStretch(image_r, SqrtStretch())
				image_r = np.array(image_r, forCasting)
			elif ('Green' in filename or 'green' in filename):
				image_g = np.array(pixels, forCasting)
				image_g = arrayStretch(image_g, SqrtStretch())
				image_g = np.array(image_g, forCasting)

			elif ('Blue' in filename or 'blue' in filename):
				image_b = np.array(pixels, forCasting)
				image_b = arrayStretch(image_b, SqrtStretch())
				image_b = np.array(image_b, forCasting)
			
			### Closing
			hudl.close()
	
	##### EXPORTING FINAL IMAGE

	#registration, pyraf,zscal(minmax), blending,
	image = make_lupton_rgb(image_g,image_r,image_b) #, filename = 'final.jpeg' 
	#norm = ImageNormalize(image, interval=MinMaxInterval(),stretch=PowerStretch(0.5))
	plt.imshow(image, origin='lower')
	plt.show()
	
###### RUNNING PROGRAM
Main()


'''
Remeber HOW TO BASIC : 

- PLOT AN IMAGE :
	plt.imshow(image_r, origin='lower')
	plt.show()

- MAKE RGB IMAGE
	https://docs.astropy.org/en/stable/api/astropy.visualization.make_lupton_rgb.html
	make_lupton_rgb(image_r, image_g, image_b, minimum=0, stretch=5, Q=8, filename=None)


'''

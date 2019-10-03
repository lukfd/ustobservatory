#########################################
# Luca Comba, for UST
#########################################
import os
import numpy as np
from PIL import Image
from astropy.io import fits

"""
CREATING FITS IMAGE OBJECT
Methods : __init__ , close, printInfo, printData
setHeader, 
""" 
class FitsData:
	#General
	def __init__(self, filename):
		self.img = fits.open("data/"+filename)
		self.hdr = self.img[0].header
		self.data = self.img[0].data
	
	def close(self):
		self.img.close()
	#Meta
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

	#WORKING WITH IMG
	def getShape(self):
		base = self.getShape()[0]
		height = self.getShape()[1]
		return self.data.shape
	def getName():
		return self.data.dtype.name
	def getPixelArray(self):
		return self.data[0:]

def Main():
	path = os.getcwd()
	for filename in os.listdir(path+"/data"):
		if filename.endswith(".fit") or filename.endswith(".fits") or filename.endswith(".fts"):
			# read fits as Astropy do :
			"""
			hdul = fits.open("data/"+filename)
			hdul.close()
			"""

			hudl = FitsData(filename)
			print(hudl.getPixelArray())
			hudl.close()

Main()






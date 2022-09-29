import argparse
# OUR LIBS
import lib.imageRegistration as imageRegistration
import lib.imageProcessing as processor
import lib.convertUtils as converter

# we assume that these data
# have been background-subtracted, if necessary linearized,
# flat-fielded, and scaled appropriately.

# command line args
# https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_argument
parser = argparse.ArgumentParser(description='Process fits images and produce a color image')
parser.add_argument("-r", "--red", default="../data/M66-Color/M66-S001-Red-R001-Red.fts",
                    help="Relative path to red image", dest="ndarrayR")
parser.add_argument("-g", "--green", default="../data/M66-Color/M66-S001-Green-R001-Green.fts",
                    help="Relative path to green image", dest="ndarrayG")
parser.add_argument("-b", "--blue", default="../data/M66-Color/M66-S002-Blue-R002-Blue.fts",
                    help="Path to blue image", dest="ndarrayB")
# NOT IMPLEMENTED
parser.add_argument("-s", "--stretch", nargs=1, default=["linear,70,0.3"],
                    help="Comma separated list of stretch and its parameter. Example: linear,70,0.3", 
                    dest="inputStretch")

args = parser.parse_args()
ndarrayR = args.ndarrayR
ndarrayG = args.ndarrayG
ndarrayB = args.ndarrayB

# Convert images to ndarray
print("Converting images to ndarray")
ndarrayR = converter.convertImageToNdarray(ndarrayR)
ndarrayG = converter.convertImageToNdarray(ndarrayG)
ndarrayB = converter.convertImageToNdarray(ndarrayB)

# Stretch arrays
print("Stretching images")
ndarrayR = processor.applyStrech(ndarrayR, slope=70, intercept=0.3)
ndarrayG = processor.applyStrech(ndarrayG, slope=50, intercept=0.2)
ndarrayB = processor.applyStrech(ndarrayB, slope=100, intercept=0.3)

# print("NDARRA RED")
# print(ndarrayR)
# print("")

# print("NDARRA GREEN")
# print(ndarrayG)
# print("")

# print("NDARRA BLUE")
# print(ndarrayB)
# print("")

# Shift images
print("Shifting images")
ndarrayG = imageRegistration.getShiftedImage(ndarrayR, ndarrayG)
ndarrayB = imageRegistration.getShiftedImage(ndarrayR, ndarrayB)

# Create color picture
print("Processing to color image")
processor.plotColoredImage(ndarrayR, ndarrayG, ndarrayB)
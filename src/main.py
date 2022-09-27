# OUR LIBS
import lib.showImage as show
import lib.fitsInfo as fit
import lib.imageRegistration as imageRegistration
import lib.imageProcessing as processor
import lib.convertUtils as converter

# we assume that these data
# have been background-subtracted, if necessary linearized,
# flat-fielded, and scaled appropriately.

# Convert images to ndarray
print("Converting images to ndarray")
ndarrayR = converter.convertImageToNdarray("../data/M66-Color/M66-S001-Red-R001-Red.fts")
ndarrayG = converter.convertImageToNdarray("../data/M66-Color/M66-S001-Green-R001-Green.fts")
ndarrayB = converter.convertImageToNdarray("../data/M66-Color/M66-S002-Blue-R002-Blue.fts")

# Stretch arrays
# print("Stretching images")
ndarrayR = processor.applyStrech(ndarrayR, slope=70, intercept=0.3)
ndarrayG = processor.applyStrech(ndarrayG, slope=50, intercept=0.2)
ndarrayB = processor.applyStrech(ndarrayB, slope=100, intercept=0.3)

print("NDARRA RED")
print(ndarrayR)
print("")

print("NDARRA GREEN")
print(ndarrayG)
print("")

print("NDARRA BLUE")
print(ndarrayB)
print("")

# print("Plotting histogram")
# show.plotArrayHistogram(ndarrayR)

#gbImages = [ndarrayG, ndarrayB]

# Shift images
print("Shifting images")
# shifitedImages = [ndarrayR]
# for image in gbImages:
#     shifitedImages.append(imageRegistration.getShiftedImage(ndarrayR, image))
ndarrayG = imageRegistration.getShiftedImage(ndarrayR, ndarrayG)
ndarrayB = imageRegistration.getShiftedImage(ndarrayR, ndarrayB)

# Create color picture
processor.plotColoredImage(ndarrayR, ndarrayG, ndarrayB)
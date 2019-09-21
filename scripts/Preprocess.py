#! /usr/bin/env python

############################################################################
#
#	Perform basic pre-processing of image frames.
#		1. Bias subtract
#		2. Dark subtract
#		3. Flat Field
#
############################################################################

from PipeLineSupport import *	# Bring in the support routines

############################################################################
# NAME: main
#
# DESCRIPTION:
#   For stand-alone use when called from the commandline.  
#   Sets calibration path and image path and calls PreProcessImages in debug mode. 
#   Debug mode causes all output to go to the console rather than a log file
#
# PARAMETERS: None
# OPTIONAL PARAMETERS: None
# RETURNS: None
############################################################################
def main(): 
#    cal_path = '/nfs/home/observatory/data/scheduler/Calibration'
#    image_path = '/nfs/home/observatory/data/scheduler/Images/'
    cal_path = '/nfs/home/observatory/data/scheduler/Testing/Calibration'
    image_path = '/nfs/home/observatory/data/scheduler/Testing/Images'
    PreProcessImages(image_path, cal_path, debug=True)

############################################################################
# NAME: PreprocessImages
#
# DESCRIPTION:
# 	Scan a directory tree containing raw images and perform the basic preprocessing steps:
#		1. Bias Subtract
#		2. Dark Subtract
#		3. Flat Field
#	Processed images go into a subdirectory of the original image location named 'Processed'.
#	The name of the processed image is the orignal image name prepended with a 'P'
# 	All subdirectories named 'Processed' are skipped in the scan.
#	
# PARAMETERS:
# 	image_path 	- Root of the directory to scan
#	cal_path 	- path to calibration data
#
# KEYWORD PARAMETERS
#	debug (default = False) - When set to true, output goes to stdout rather than log files.
#
# RETURNS:
#	No returns.  Records activity to log files
#
############################################################################
def PreProcessImages(image_path, cal_path, debug=False):

    # Save the original pointer to stdout so that we can reset it later.
    orig_stdout = sys.stdout

	# Open a log file a image_path\Logs with the 
	# current date time in iso format as the filename
    if not debug: 
        top_log = open(os.path.join(image_path,'PreProcess.log'),'a')
        sys.stdout = top_log 

    print datetime.datetime.today().isoformat()[:19] + ": Image Path '" + image_path + "'"
    print datetime.datetime.today().isoformat()[:19] + ": Calibration Path: " + cal_path + "'"

    # Process every fits file in the tree rooted at image_path
    for root,dirs,files in os.walk(image_path):

        # Skip the 'Processed' directory as this is where 
        # processed files are stored.
        if 'Processed' in dirs:
            dirs.remove('Processed')	

        # Fix spaces in directory names because they annoy
        cur_dir = os.getcwd()
        os.chdir(root)

        dirs[:] = FixFilenames(dirs)
        os.chdir(cur_dir)
			
        # Select image files to process
        images = filter(fits_filter, files)		# filter out the non-fits files

		# filter out already processed images - 
		# remove from the list images with a counterpart in the Processed sub-directory
        images = filter(lambda x: not os.path.exists(os.path.join(root,'Processed',"P"+os.path.splitext(x)[0]+".fits")),images)
        images = [os.path.join(root,i) for i in images]


        # Process the images
        if len(images) > 0:		# Anything to do here?
			
            print datetime.datetime.today().isoformat()[:19] + ": Processing '" +  root + "'"

            # Redirect detailed output to local log file.
            if not debug:
	            tmp_stdout = sys.stdout
	            sys.stdout = open(os.path.join(root,'PreProcess.log'),'a')

            # Print a time stamp
            print datetime.datetime.today().isoformat()

            bs_images = []
            bsd_images = []

            # Pyraf hates spaces in filenames (and so do I)
            # Eradicate them.
            images = FixFilenames(images)

            m_images = ApplyBadPixelMask(images,cal_path)
            bs_images = BiasSubtract(m_images,cal_path)
            bsd_images = DarkSubtract(bs_images, cal_path)
            bsf_images = FlatField(bsd_images, cal_path)

            # Create the processed directory
            if not os.path.exists(os.path.join(root,'Processed')):
	            os.mkdir(os.path.join(root,'Processed'))

            # Rename and move the flat fielded images into the Processed directory
            for i in range(len(bsf_images)):
	            outf = "P"+os.path.splitext(os.path.basename(images[i]))[0] + ".fits"
	            outf = os.path.join(root,'Processed',outf) 
	            os.rename(bsf_images[i], outf)

            if not debug:
	            sys.stdout.close
	            sys.stdout = tmp_stdout

            # Clean up ancillary files
            CleanAncillary(m_images)
            CleanAncillary(bs_images)
            CleanAncillary(bsd_images)
		
    if not debug: 
        top_log.close()
        sys.stdout = orig_stdout
			
if  __name__ =='__main__':main()

#! /usr/bin/python

#target_dir = "/nfs/home/observatory/data/scheduler/Images/20140607/NGC_7160/Processed/tmp"
target_dir = "/nfs/home/observatory/data/scheduler/Testing/Images/20140629/M63_Lum/Processed"
# ***********************************************************
# Pyraf Script to stack and add files in a given directory 
# ***********************************************************
from BasicProcessing.PipeLineSupport import *  # Bring in the support routines
import tempfile

def Stack(target_dir, no_unlearn=False): 


    # Get a list of fits files in the target directory
    images = filter(fits_filter,os.listdir(target_dir))
    images = [os.path.join(target_dir,i) for i in images]

    # Sort the list by the Date stamp in the header.
    images = sorted(images,key=GetObsDateTime)

    # Align all images to the first image taken.
    aligned_images = wcsRegister(images,images[0],no_unlearn=no_unlearn)

    # Combine images by filter
    CombineByFilter(aligned_images,no_unlearn=no_unlearn)


############################################################################
# NAME: wcsRegister
#
# DESCRIPTION:
#   Calls IRAF wregister to align a stack of images to a reference image.
#   Assumes that the images have WCS.  
#
# PARAMETERS:
#   images - a list containing the filenames of the images to register 
#   reference - filename of the reference image
#
# OPTIONAL PARAMETERS:
#	output_files - 		A list the fully qualified name of the desired output files. 
#						The list must be the same length as images
#						If output_files = '', the output filenames will be
#						the same as the input file names with an 'r' prepended.
#						default = ''
#   no_unlearn -        Don't set wregister to default parameters prior to calling.
#
# RETURNS:
#	A list containing the output file names.
# 	An empty list if something went wrong.
#   
###############################################################################
def wcsRegister(images,reference,output_files='',no_unlearn=False):
	
	# If the output file list doesn't exsist, create it.
    if len(output_files) == 0:
       output_files = [os.path.join(os.path.dirname(i), 'r' + os.path.basename(i)) for i in images]				

    # Call wregister for each image 
    for (Input, Output) in zip(images,output_files):

        try:

            # Set up to call the task
            iraf.set(clobber='yes')
            iraf.images()
            iraf.immatch()

            if no_unlearn == False: 
                iraf.wregister.unlearn()

            iraf.wregister.input = Input
            iraf.wregister.reference = reference
            iraf.wregister.output = Output

            iraf.wregister()
                
	except iraf.IrafError, e:
            print "registration failed"
            print "error #" + str(e.errno)
            print "Msg: " + e.errmsg
            print "Task: " + e.errtask
            raise e


    return output_files



############################################################################
# NAME: CombineByFilter
#
# DESCRIPTION:
#   Calls IRAF imcombine to combine a stack of images by filter.
#   Creates one combined image per filter.
#   Filter is determined by the header filter keyword.
#   Assumes that the images have WCS.  
#
# PARAMETERS:
#   images - a list containing the filenames of the images to combine
#
# OPTIONAL PARAMETERS:
#   output - The base name of the output file.  Output files will have the 
#			 filter name prepended.
#			 if output = '', the output file will be the first filename
#			 in images prepended with the filter name.
#			 default = ''
#	filter_keyword - The header keyword containing the filter name.
#					 default = 'filter'
#
# RETURNS:
#   A list containing the output file names.
#   An empty list if something went wrong.
#   
###############################################################################
def CombineByFilter(images,output='',filter_keyword='filter',no_unlearn=False):

    outfiles = []
	
	# Get a list of filters for these images
    filters = [GetHeaderKeyword(i, filter_keyword) for i in images]   
    filters = list(set(filters))   # "uniqeify" the filter list.

    # Create a combined image for each filter.
    for f in filters:
        
        # Get only the images for this filter
        fimages = filter(lambda x: GetHeaderKeyword(x, filter_keyword)==f, images)
		
		# Create a temporary file to hold the input image list
        tfile = tempfile.mkstemp()
        os.write(tfile[0],"\n".join(fimages)+"\n")
        os.close(tfile[0])
		
		# Create the output file name
        if output == '':
            out_file = os.path.join(os.path.dirname(images[0]), f + os.path.basename(images[0]))
        else:
            out_file = f + output
			
		# Call IRAF imcombine to do the image combine
        try: 
            iraf.set(clobber='yes')
            iraf.images()	# Select images package
            iraf.immatch()	# Select immatch package

            if no_unlearn == False: 	# Clear old parameters
                iraf.imcombine.unlearn()

            iraf.imcombine.input = "@" + tfile[1]
            iraf.imcombine.output = out_file

            iraf.imcombine()  # Call imcombine

            outfiles.append(out_file)
		
        except iraf.IrafError, e:
            print "imcombine failed"
            print "error #" + str(e.errno)
            print "Msg: " + e.errmsg
            print "Task: " + e.errtask
            raise e
        finally:
            os.remove(tfile[1])		# remove the tempfile
			
    return outfiles


# Invoke the main loop
if __name__ == "__main__":
    sys.exit(Stack(target_dir, unlearn=unlearn))

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	

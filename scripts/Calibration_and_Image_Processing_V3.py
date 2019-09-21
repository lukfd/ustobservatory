#! /usr/bin/python

#############################################################################################
# Calibration and Image Processing Script
#
# Purpose: This script is used to generate master calibration frames and processed images from
#   raw telescope data in the form of FITS files. The master frames used to do the calibration
#   of the images may be formulated specifically for the observation night if calibration frames
#   were obtained that night. Otherwise, a set of standard master calibration frames are used.
#
# Execution: To execute this script, it simply needs to be run. All of the processing will happen
#   automatically, and no inputs are needed.
#
# Directory and File Naming Conventions:
#   Directories:
#       Calibration:
#           The Calibration directory contains the Standard directory, which contains the standard
#               master calibration frames. It also contains date directories for specific observation
#               nights with the title as the date "yyyymmdd" with no punctuation.
#           Within each directory in the Calibration directory, there are three directories:
#               "Bias", "Dark", and "Flat".
#           Within each "Flat" directory, there is a directory for each filter. The title is the
#               capitalized filter name (e.g. "Red").
#       Images:
#           The format of the image directories does not have to be strict. When the images are
#               processed, all images that grow off of the root directory are touched, so it does
#               not matter what the names of the directories are.
#           When images are processed, they are all placed in the "Processed" subdirectory of the
#               directory in which they reside.
#           
#   Files:
#       Master Calibration Frames:
#           All of the master frames generated for a specific date have the date at the beginning
#               of their names in the format "yyyymmdd" with no punctuation.
#           The standard frames have no date at the beginning of their names.
#           A master bias frame has name "mbias".
#           A master dark frame for a particular exposure time has name "mdark" with the exposure
#               time as a float at the end.
#           A general master dark frame has the name "mdarkgen".
#           A master flat frame for a particular filter has the name "mflat" with a capital letter
#               at the end which is the first letter of the filter name.
#           All master frames generated for a specific day reside in the directory in which the
#               frames from which they were created reside.
#       Processed Images:
#           A processed image has the same name as its raw image counterpart except for a capital
#               "P" at the beginning of its name signaling that it is processed.
#           A processed image is stored in the "Processed" subdirectory of the directory that contains
#               its raw image counterpart.
#       Text File Logs:
#           A calibration log is generated each time master calibration frames are generated for a
#               specific date. This log is stored in the date directory and has the date in the format
#               "yyyymmdd" at the beginning of its name, "log.txt". There is one log for each date.
#           An image processing log is generated for each directory containing raw images that are
#               processed. The log has the title "Processed_Log.txt" and resides in the "Processed"
#               directory that contains the processed images.

import os,sys,datetime,string,traceback,numpy,pyfits
import pdb
#pdb.set_trace()
#root_directory_path = '/nfs/home/observatory/data/scheduler'
root_directory_path = '/nfs/home/observatory/data/scheduler/Images'
cal_path = '/nfs/home/observatory/data/scheduler/Calibration'
    # Path to directory of calibration files
stand_cal_path = os.path.join(cal_path,'Standard')
    # Path to directory of standard calibrations

### Pathname manipulation utility function ###
    
def get_dir_paths(root_dir_path):
    #######################################################################################
    # get_dir_paths returns a list of the pathnames of all of the files and directories in a 
    #   root directory. The input is the pathname of the root directory.
    root_dir_contents = os.listdir(root_dir_path) # list of directories in the root directory
    dir_contents_paths = list(os.path.join(root_dir_path,root_dir_contents[i]) for i
                              in range(len(root_dir_contents)))
    return dir_contents_paths


### Extract image data functions ###

def fits_file_image_array(fits_file_path):
    #######################################################################################
    # fits_file_image_array is a simple function that takes the file path of a FITS file and
    #   returns the image data in a NumPy array, assuming that the data is in the Primary
    #   header data unit. 
    hdulist = pyfits.open(fits_file_path)
    image_data = hdulist[0].data
    hdulist.close() # Make sure to close the FITS file after the data is extracted.
    return image_data # The output is the image data in an n-dimensional array.

def frame_exposure_time(fits_file_path):
    #######################################################################################
    # frame_exposure_time simply extracts the exposure time of an image from from the FITS
    #   file header. It takes the file path of the FITS image file and returns the exposure
    #   time as a float. The purpose of this function is mostly for use in finding the
    #   exposure times of the dark frames so that they can be organized by this time.
    hdulist = pyfits.open(fits_file_path)
    exptime = hdulist[0].header['exptime']
    hdulist.close()
    return exptime

### Extract dark and flat frame data functions ###

def dark_image_array(dark_file_path):
    #######################################################################################
    # dark_image_array takes the pathname of a dark frame FITS file and returns the image
    #   array of that file that has been bias subtracted and normalized by the exposure
    #   time of the image
    hdulist = pyfits.open(dark_file_path)
    image_data = hdulist[0].data
    if os.path.exists(bias_path) and os.listdir(bias_path):
        # Assume the path to the Bias directory has already been defined. 
        mbias_path = os.path.join(bias_path, date + 'mbias.fit')
            # If the Bias directory exists and is not empty, use the master bias frame that has 
            #   already been generated
    else:
        stand_mbias_path = os.path.join(stand_cal_path, 'Bias','mbias.fit')
        mbias_path = stand_mbias_path
            # Otherwise use the Standard bias frame
    try:
        mbias_file = pyfits.open(mbias_path)
    except IOError:
        # If the master bias frame cannot be opened for some reason, record this in the
        #   Calibration log and return False
        record_opening_error(mbias_path, cal_log)
        hdulist.close()
        return False
    else: # If opening the file is successful, extract the data
        mbias_data = mbias_file[0].data # The master bias frame image data in an array
        mbias_file.close()
        bias_sub = image_data - mbias_data
            # Bias subtract the image data
        exptime = hdulist[0].header['exptime']
            # Exposure time of the frame
        norm_image_data = bias_sub/exptime
            # Normalize by dividing by the exposure time
        hdulist.close()
        return norm_image_data
            # The bias subtracted and normalized image array is returned 
    
def flat_image_array(flat_file_path):
    #######################################################################################
    # flat_image_array takes the pathname of a flat frame FITS file and returns the calibrated
    #   image array that has been bias subtracted, normalized by the exposure time, dark
    #   subtracted and normalized by the mean pixel value.
    hdulist = pyfits.open(flat_file_path)
    image_data = hdulist[0].data
    if os.path.exists(bias_path) and os.listdir(bias_path):
        # Assume the path to the Bias directory has already been defined. 
        mbias_path = os.path.join(bias_path, date + 'mbias.fit')
            # If the Bias directory exists and is not empty, use the master bias frame that has 
            #   already been generated
    else:
        stand_mbias_path = os.path.join(stand_cal_path, 'Bias','mbias.fit')
        mbias_path = stand_mbias_path
            # Otherwise use the Standard bias frame

    try:
        mbias_file = pyfits.open(mbias_path)
    except IOError:
        # If the master bias frame cannot be opened for some reason, record this in the
        #   Calibration log and return False
        record_opening_error(mbias_path,cal_log)
        hdulist.close()
    else: # If opening the file is successful, extract the data
        mbias_data = mbias_file[0].data # The master bias frame image data in an array
        mbias_file.close()
        bias_sub = image_data - mbias_data
            # Bias subtract the image data
        exptime = hdulist[0].header['exptime']
            # Exposure time of the frame
        hdulist.close()
        norm_image_data = bias_sub/exptime
            # Normalize by dividing by the exposure time
        
        # Assume that the pathname of the dark frames directory, specifically the path to the 
        #   Dark directory in the calibration directory for a specific date, has already been
        #   defined. 
        ideal_mdark_path = os.path.join(dark_path, date + 'mdark' + str(exptime) + '.fit')
            # If the Dark directory for the night in question exists and is not empty, the "ideal" 
            #   master dark frame would be the one for that night of observations and for the same 
            #   exposure time as the flat frame.
        mdark_gen_path = os.path.join(dark_path,date + 'mdarkgen.fit')
            # The second choice is the "general" master frame for that night, the one that averages
            #   all of the dark frames taken that night
        stand_ideal_mdark_path = os.path.join(stand_cal_path,'Dark','mdark' + str(exptime) + '.fit')
            # If no master dark frames exist for that night, default to the Standard Calibration
            #   directory. The ideal choice is the master dark frame with the same exposure time.
        stand_mdark_gen_path = os.path.join(stand_cal_path,'Dark', 'mdarkgen.fit')
            # The last choice is the general master dark frame in the Standard Calibration directory
        if os.path.exists(ideal_mdark_path): 
            mdark_path = ideal_mdark_path
        elif os.path.exists(mdark_gen_path): 
            mdark_path = mdark_gen_path
        elif os.path.exists(stand_ideal_mdark_path):
            mdark_path = stand_ideal_mdark_path
        else:
            mdark_path = stand_mdark_gen_path
            
        try:
            mdark_array = fits_file_image_array(mdark_path)
        except IOError:
            # If the master dark frame cannot be opened for some reason, record this in the
            #   Calibration log and return False
            record_opening_error(mdark_path,cal_log)
            hdulist.close()
            return False
        else: # If opening the dark master frame file is successful, process the data
            dark_sub = norm_image_data - mdark_array
                # Dark subtract from the already bias subtracted and normalized image array
            flat_image_array = dark_sub/numpy.mean(dark_sub)
                # Divide by the mean pixel value
            return flat_image_array
                # The calibrated image array is returned


### Write a master frame header function ###
                
def master_frame_header(frame_path_list):
    #######################################################################################
    # master_frame_header formulates a FITS header for the master calibration file given
    #   a list of the pathnames of the frames from which the master frame is generated
    hdulist = pyfits.open(frame_path_list[0])
        # The header from the first file on the frame path list is used as the base header.
        #   The master file header is modified from this.
    image_data = hdulist[0].data
        # "Touch" the data so that if the storage data is scaled, the header will represent
        #   the physical data and not the scaled storage data.
    header = hdulist[0].header
    exptimes = list(pyfits.getheader(frame_path_list[i],0)['exptime'] for i
                    in range(len(frame_path_list)))
        # A list of the exposure times of each frame
    avgexptime = sum(exptimes)/len(exptimes) # Average exposure time of the frames
    header.update('exptime',avgexptime,'Average exposure time in secs')
    header.update('exposure',avgexptime,'Average exposure time in secs')
        # The exposure time on the header will be the average exposure time of the frames
    if avgexptime != 0.0:
        # If the exposure time is non-zero (e.g. if it is not a bias frame), the frames
        #   are normalized by their exposure times, so the effective exposure time is
        #   one second.
        header.update('effexp',1.0,'Effective exposure time in secs', after= 'exposure')
    date = datetime.datetime.utcnow().isoformat()[:19]
        # Date time stamp is placed in the header as the current time when the function
        #   is called
    header.update('date', date, 'Date FITS file created, UTC', after = 'date-obs')
    frame_list = list(os.path.basename(frame_path_list[i]) for i
                      in range(len(frame_path_list)))
        # A list of the frame file names
    for i in range(len(frame_list)):
        # For all frames in the list of frame file names, add a card into the master frame
        #   header giving its name
        header.update('frame' + str(i+1),frame_list[i])
    header.update('numim',len(frame_path_list),'Number of images combined')
        # Add a card giving the number of images the master frame is made from
    hdulist.close()
    return header # The output is a PyFITS header object, not the physical header itself


### Log recording functions ###

def write_to_cal_log(master_frame_path,frame_list):
    #######################################################################################
    # When called with the pathname of a master calibration frame and a Python list of frames
    #   from which the master frame was made, write_to_cal_log records the log information
    #   about the creation of the master frame in an already existing calibration log. The
    #   log records the name of the master calibration frame, its path, the time of creation,
    #   and the names of the frames from which it was generated.
    master_frame = os.path.basename(master_frame_path) 
    master_frame_header = pyfits.getheader(master_frame_path)
    date_of_creation = master_frame_header['date']
        # Date-time string of when the master frame file was created 
    cal_log.write('Master frame ' + master_frame + ' with path\n')
        # The "cal_log" file object is already existing because it is created in code that
        #   is executed previous to the calling of this function
    cal_log.write(master_frame_path + '\n')
    cal_log.write('was created on ' + date_of_creation + ', UTC,\n')
    cal_log.write('from ' + str(len(frame_list)) + ' frames:\n')
    for i in range(len(frame_list)):
        cal_log.write(frame_list[i] + '\n')
    cal_log.write('\n\n')

def record_empty_directory(empty_directory_path):
    #######################################################################################
    # record_empty_directory is for use in the processing of master calibration frames.
    #   Assuming that the Calibration log has already been opened when this function is
    #   called, it takes as an input the pathname of an empty Calibration directory (Bias,
    #   Dark, etc.) and writes information about the empty directory to the Calibration log.
    directory = os.path.basename(empty_directory_path)
        # Name of the empty directory
    date_time_string = datetime.datetime.utcnow().isoformat()[:19]
        # Time stamp created when this function is called
    cal_log.write('The directory ' + directory + ' with path\n')
        # The "cal_log" Calibration log file object has already been defined
    cal_log.write(empty_directory_path + '\n')
    cal_log.write('contained no frames at ' + date_time_string + ', UTC.\n\n')

def record_opening_error(frame_path, log_file_object):
    #######################################################################################
    # record_opening_error records the details of an "IOError" (which occurs when a file
    #   cannot be opened or accessed) to a log file. It takes as inputs the pathname of the
    #   frame that raises the exception and the file object of the log to which the error is
    #   recorded.
    frame = os.path.basename(frame_path)
    log_file_object.write('There was an error in opening the frame: ' + frame + '\n')
    log_file_object.write('which has path: ' + frame_path + '\n')
    traceback.print_exc(file = log_file_object)
        # This traceback function prints exception information and the stack trace where the
        #   exception occured to the log file. 

def fits_filter(filename):
    #######################################################################################
    # fits_filter Returns true if the the file descrbed by filename is a "fits" file.
    #             Returns false otherwise         
    #             Looks at the file extension and returns true if the extension is 
    #             'fits', 'fit', or 'fts'

    extension = os.path.splitext(filename)[1]
    return extension == '.fits' or extension == '.fit' or extension == '.fts'


        


### Image processing function ###
        
def process_image_data(image_file_path):
    #######################################################################################
    # process_image_data is the general processing of a raw image. It takes the pathname of
    #   a single image file and returns a list of the calibrated image data array, and the titles
    #   of the master frames used to do the calibration.
    hdulist = pyfits.open(image_file_path)
    header = hdulist[0].header

    obs_time = header['date-obs']
        # Observation date and time of the image, UTC, with format "YYYY-MM-ddThh:mm:ss"
    exptime = header['exptime'] # Exposure time of the image
    Filter = header['filter'] # Filter image was taken with
    image_data = hdulist[0].data 
    obs_date = datetime.datetime.strptime(obs_time,'%Y-%m-%dT%H:%M:%S')
        # Convert the observation datetime string to a Python datetime object
    if obs_date.hour < 12:
        # If the hour in the observation datetime string is less than twelve (the datetime string
        #   uses a 24-hour clock system), then the date of the observation in the datetime string
        #   refers to the observation night of the previous date. 
        
        obs_night = obs_date.date() - datetime.timedelta(days = 1)
            # Subtract one day if the hour is less than twelve
        date = obs_night.isoformat().translate(None,string.punctuation)
    else:
        date = obs_date.date().isoformat().translate(None,string.punctuation)
            # Format the date so there is no punctuation ("yyyymmdd")
    
    cal_date_path = os.path.join(cal_path, date)
        # Path to the calibration directory for the night of the observation
    stand_mbias_path = os.path.join(stand_cal_path,'Bias','mbias.fit')
        # Path to the master bias frame in the Standard directory
    stand_mdark_path = os.path.join(stand_cal_path,'Dark','mdark' + str(exptime) + '.fit')
        # Path to the Standard master dark frame, the one with the same exposure time as the
        #   image frame
    stand_mdark_gen_path = os.path.join(stand_cal_path,'Dark','mdarkgen.fit')
        # Path to the Standard general master dark frame
    stand_mflat_path = os.path.join(stand_cal_path,'Flat',Filter,'mflat' + Filter[0] + '.fit')
        # Path to the Standard master flat frame for the filter the image was taken with    
    if os.path.exists(cal_date_path):
        # If the calibration directory exists for the observation night of the image, then the
        #   master frames generated for that night will be used if they exist.

        ### Find path to master bias frame
        ideal_mbias_path = os.path.join(cal_date_path, 'Bias',date + 'mbias.fit')
            # Path to the master bias frame for the night of the observation
        if os.path.exists(ideal_mbias_path):
            mbias_path = ideal_mbias_path
        else:
            mbias_path = stand_mbias_path
                

        ### Find path to master dark frame
        ideal_mdark_path = os.path.join(cal_date_path,'Dark', date + 'mdark' + str(exptime) + '.fit')
            # Path to the ideal master dark frame for the night of the observation, the one with
            #   the same exposure time as the image frame
        mdark_gen_path = os.path.join(cal_date_path,'Dark',date + 'mdarkgen.fit')
            # Path to the general master dark frame for the night of the observation, the average
            #   of all dark frames taken that night
        if os.path.exists(ideal_mdark_path):
            mdark_path = ideal_mdark_path
                # If the "ideal" exists, use it
        elif os.path.exists(mdark_gen_path):
            mdark_path = mdark_gen_path
                # If the "ideal" doesn't exist, use the general master frame for the
                #   night if it exists
        elif os.path.exists(stand_mdark_path): # Default to Standard calibrations
            mdark_path = stand_mdark_path
                # If the Standard master frame exists for the same exposure time as the
                #   image, use it
        else:
            mdark_path = stand_mdark_gen_path
                # Otherwise, use the general Standard master frame
                

        ### Find path to master flat frame
        ideal_mflat_path = os.path.join(cal_date_path,'Flat',Filter,date + 'mflat' + Filter[0] + '.fit')
            # Path to the ideal master flat frame for the night of the observation, the one
            #   taken with the same filter as the image
        if os.path.exists(ideal_mflat_path):
            mflat_path = ideal_mflat_path
                # If the master frame exists for the filter the image was taken with,use it
        else:
            mflat_path = stand_mflat_path
            # If the master frame doesn't exist for the filter the image was taken with, or if
            #   there is no Flat directory for the observation night, use the Standard frame

    else:
        # If the calibration directory does not exist for the observation night, default to use
        #   the Standard master frames
        mbias_path = stand_mbias_path
        mflat_path = stand_mflat_path
        if os.path.exists(stand_mdark_path):
            mdark_path = stand_mdark_path
        else:
            mdark_path = stand_mdark_gen_path


    # Having obtained the pathnames for the master calibration frames, obtain the filename
    #   and data arrays for each master frame
    success = True
        # Assert that success in opening the master frames is true
    master_frame_paths = [mbias_path,mdark_path,mflat_path]
    for path in master_frame_paths:
        # For each master frame pathname, try to extract data from the FITS file. If the file
        #   cannot be found or opened, record this to the image processing log and assert that
        #   success in opening the master frame is false.
        try:
            image_array = fits_file_image_array(path)
        except IOError:
            success = False
            record_opening_error(path, im_process_log)

    if success:
        # If opening the master frame files raised no exceptions, get the filename and data arrays
        #   for each master frame
        mbias_frame = os.path.basename(mbias_path)
        mdark_frame = os.path.basename(mdark_path)
        mflat_frame = os.path.basename(mflat_path)
        mbias_array = fits_file_image_array(mbias_path)
        mdark_array = fits_file_image_array(mdark_path)
        mflat_array = fits_file_image_array(mflat_path)

        bias_sub = image_data - mbias_array
            # Subtract the bias array from the image array
        norm_image_data = bias_sub/exptime
            # Normalize by dividing by the exposure time of the image
        dark_sub = norm_image_data - mdark_array
            # Subtract the dark array
        flat_div = numpy.true_divide(dark_sub,mflat_array)
            # Divide by the flat array
        return [flat_div,mbias_frame,mdark_frame,mflat_frame]
            # The output is a list of length four; the first component is the calibrated image
            #   array. The last three components are the filenames of the master bias, dark
            #   and flat frames used to do the calibrations.
    else:
        # If opening the master frame files raised exceptions, do not try to process the image and
        #   return false 
        return False
    
def process_image_header(image_file_path):
    #######################################################################################
    # process_image_header formulates a FITS header for the processed (calibrated) image
    #   given the pathname of the raw image.
    hdulist = pyfits.open(image_file_path)
        # The processed image file's header is modified from the header of the raw image file
    data = hdulist[0].data
        # "Touch" the raw data so that if the storage data is scaled, the header will represent
        #   the physical data and not the scaled storage data.
    header = hdulist[0].header
    date = datetime.datetime.utcnow().isoformat()[:19]
    header.update('date',date,'Date processed image file was created, UTC', after = 'date-obs')
        # Datetime string of the current time when the function is called is placed in the
        #   header as the time stamp of the creation of the processed image file
    processed_image_array_and_mframes = process_image_data(image_file_path)
        # A list of the processed image array and the titles of the master frames used to
        #   calibrate the raw image
    [mbias_frame,mdark_frame,mflat_frame] = processed_image_array_and_mframes[1:]
    header.update('mbias',mbias_frame,'Master bias frame used')
    header.update('mdark',mdark_frame,'Master dark frame used')
    header.update('mflat',mflat_frame,'Master flat frame used')
        # Cards are added into the processed image file header to document the filenames of the
        #   master frames used in the calibrations
    return header # The output is a PyFITS header object


### Log recording function ###

def record_image_processing(processed_image_path):
    # record_image_processing records the processing information of a raw image to an (already
    #   existing) image processing log. It takes the pathname of a processed image. There is one
    #   image processing log for each directory that contains raw images. The log is stored in
    #   the "Processed" subdirectory of the directory which contains raw images.
    raw_image_frame = filename
        # This function will be called when the directory tree of images is being traversed.  
        #   Each file in the root directory has title "filename".
    date = processed_image_header['date']
        # The processed_image_header is already defined when this function is called. It is the
        #   FITS file header object of the processed image frame.
    processed_image_frame = os.path.basename(processed_image_path)
    im_process_log.write('Raw image ' + raw_image_frame + '\n')
    im_process_log.write('was processed on ' + date + ', UTC,\n')
    im_process_log.write('with master calibration frames\n')
    im_process_log.write(mbias_frame + ', ' + mdark_frame + ', and ' + mflat_frame + '.\n')
    im_process_log.write('The processed image is named ' + processed_image_frame + '\n\n')
    im_process_log.close()
        # Close the image processing log because when this function is called, it might be the last
        #   time the log is added to.



### Process images ###
print "Processing Image Data..."
for root,dirs,files in os.walk(root_directory_path):
    #######################################################################################
    # os.walk traverses the entire directory tree rooted at the root directory path. This
    #   enables every image file that lies in the root directory and all subdirectories to
    #   to be processed and stored in a subdirectory of the image's root called "Processed".
    
    print "Checking: " + root + "\n"
    
    for filename in files:
        # Iterate through every filename generated by os.walk
        processed_image_path = os.path.join(root,'Processed','P' + filename)
            # The processed image path is the pathname to the processed image file of a
            #   raw image file given by the "name" of the current iteration. This path
            #   may or may not already exist.
        FITS_extensions = ['.fit','.fits','.fts']
        for ext in FITS_extensions:
            # For each file extension option for a FITS file, see if the file has one of these
            #   extensions. If it does, set FITS_file to True.
            if ext in filename:
                FITS_file = True
                break
            else:
		FITS_file = False
                continue
        if not FITS_file:
            # If the file is not a FITS file, pass it.
            pass
        elif 'Processed' in root:
            # If the directory "Processed" is in the pathname to the filename of the
            #   current iteration, this means the file is already a processed image,
            #   so it should be passed.
            pass
        elif os.path.isfile(processed_image_path): 
            # If the file is a raw image but it's processed counterpart already exists in
            #   the "Processed" subdirectory, pass it.
            pass
        else:
            # If the file hasn't been passed, then it is a raw image file that needs to be
            #   processed.
            if not os.path.isdir(os.path.join(root,'Processed')):
                os.mkdir(os.path.join(root,'Processed'))
                # If the "Processed" subdirectory where the processed image will be stored
                #   does not already exist(from previous program runs or the processing of
                #   images in previous iterations), create it.
            else:
                pass
            

            im_process_log = open(os.path.join(root,'Processed','Processed_Log.txt'),'a')
                # The image processing log is the text file that records the processing of images
                #   in a given root directory containing raw images. The log is stored in the
                #   processed subdirectory and is called "Processed_Log.txt".
            image_path = os.path.join(root,filename)
            print "Processing: " + image_path

            processed_image_array_and_mframes = process_image_data(image_path)
                # This is a list with the  processed image data array of the given raw image and the 
                #   filenames of the master calibration frames used to process it if no exceptions
                #   were raised when processing the raw image.
            if type(processed_image_array_and_mframes) == bool:
                # If exceptions were raised when processing the raw image, processed_image_array_and_
                #   mframes will be "False", so the os.walk loop should continue to the next image file.
                continue
            else:
                [mbias_frame,mdark_frame,mflat_frame] = processed_image_array_and_mframes[1:]
                    # Names of the master frames used to calibrate the image
                processed_image_data = processed_image_array_and_mframes[0]
                    # The processed image data array
                processed_image_header = process_image_header(image_path)
                    # The FITS file header object of the processed image
                pyfits.writeto(processed_image_path,processed_image_data,processed_image_header)
                    # The processed image is stored in the "Processed" subdirectory of the directory
                    #   where it's raw image counterpart resides.
                record_image_processing(processed_image_path)
                    # Record the processing of the image to the image processing log
                im_process_log.close()
                    # Close the image processing log in case it is the last time it is touched
                


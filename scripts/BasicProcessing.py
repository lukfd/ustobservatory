#! /usr/bin/env python

###############################################################################
#                            BasicProcessing.py                               
# Peforms basic processing of all unprocessded data from the observatory      
#     1. Calls on CreateCalibration.py to create master calibration frames
#		 from raw data.	
#
#     2. Calls on Preprocess.py to peform basic calibration steps on raw
#	     image data
#
# ####  A Note on Logging ####
# There are two types of log file
# 	Type 1: Top level activity.  
# 		A per-run log file describing which directories had fresh data that was 
# 		subsequently processed.  Major errors, that is any untrapped errors 
# 		that would abort the script, should be logged in the top level file.
# 
# 	Type 2: File level activity.  
# 		By directory log files describing what actions were taken on each file 
# 		and any erros in processing (unfound calibration files, etc).  These 
# 		file level errors should not abort the script, but should be trapped
# 		and logged in the file level log.
#
# #### ToDo: ####
#	1. Move configuration information (such as calibration 
#      paths and log directories) to a configuration file.
#
###############################################################################

# Fetch calibration and image processing routines
import CreateCalibration as cal
import Preprocess as pre 

# Set calibration and image directories
cal_path = '/nfs/home/observatory/data/scheduler/Calibration'
image_path = '/nfs/home/observatory/data/scheduler/Images/'

#cal_path = '/nfs/home/observatory/data/scheduler/Testing/Calibration'
#image_path = '/nfs/home/observatory/data/scheduler/Testing/Images/'

# Make calibration frames
try:
	cal.CreateCalibration(cal_path)
except Exception as e:
	print "Why didn't you catch this error?" 
	print e 

# Processing image data
try: 
	pre.PreProcessImages(image_path, cal_path)
except Exception as e:
	print "Why didn't you catch this error?" 
	print e 



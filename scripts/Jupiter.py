#! /usr/bin/python

# ***********************************************************
# Pyraf Script to process data for the Jupiter Lab.
# 
# Responsible for: 
#	Dispatching observation requests to the telescope
#	Processing and packaging the resulting data for user download
#	Updating the SQL database with current status
# ***********************************************************

# Import the requisite packages
import MySQLdb as mdb
import sys
import os
import zipfile
import shutil
from operator import itemgetter		# Odd little operator for the sort algorithm... 
									# picks a row/column to sort on for nested lists
				# Get the debugger
import Coadd_Images					# Get the image combiner
from datetime import datetime

import pycurl

# Set up some global parameters
data_root = "/nfs/home/observatory/data/scheduler/Images/AstroLab" # Root of the data directory
zip_root = "MoonsOfJupiter/data"
web_root = "/nfs/html/"
url_root = "http://ida.phys.stthomas.edu/"
#data_root = "/nfs/bigdisk/work/Images" # Root of the data directory

# Define main
def Jupiter():
	
	# Connect to the database	
	JDB = JupiterDB()

	# For each project pending
	for plan in JDB.GetPendingPlans():	


		# Construct the name of the directory where data should be found for this plan
		id = "S" + str(plan['section']) + "G" + str(plan['group'])
		path = os.path.join(data_root, plan['short_name'] + "_" + id + "_Jupiter")

		print "Processing: " + plan['name'] + "-" + id

		if os.path.exists(path):	# Anything here yet?

			# Is there any unprocessed data here?
			if ProcessNewData(path):
				plan['Observation_Pending'] = 0		#Update the database.
				JDB.UpdateObservation_Pending(plan['name'], plan['section'], plan['group'], 0)				
		
			# Scan to see if the data is ready to go
			images = DataReady(path, plan['images_per_night'], plan['number_of_nights']) 
			if images:
				file_name = PackageData(path, images)
				
				# Copy data into the web directory
				zip_dest = os.path.join(web_root, zip_root, plan['short_name'], id)
				if os.path.isdir(zip_dest):
					shutil.rmtree(zip_dest)
				if not os.path.isdir(zip_dest):
					if not os.path.isdir(os.path.join(web_root, zip_root, plan['short_name'])):
						os.mkdir(os.path.join(web_root, zip_root, plan['short_name']))
					os.mkdir(zip_dest)
				shutil.copy(file_name, os.path.join(zip_dest, 'Jupiter.zip'))
				
				zip_url = os.path.join(url_root, zip_root, plan['short_name'], id, 'Jupiter.zip')
				JDB.UpdateData_Path(plan['name'], plan['section'], plan['group'], zip_url)
				JDB.UpdateReady(plan['name'], plan['section'], plan['group'], 1)
				plan['ready'] = 1
		
				
		# If the Data is not ready to go and no observations are pending 
		# Submit an observation request to the telescope. 
		if plan['ready'] == 0 and plan['Observation_Pending'] == 0:
			print "Submitting Observation Request\n"
			submitted = SubmitObservation(plan['name'], plan['short_name'], plan['section'], plan['group'],	\
			  			      plan['images_per_night'], plan['time_between_images'], plan['number_of_nights'])
			
			# Update the database if all went well.
			if submitted: 
				JDB.UpdateObservation_Pending(plan['name'], plan['section'], plan['group'], 1)
				JDB.UpdateScheduled(plan['name'], plan['section'], plan['group'], 1)

# ***********************************************************
# NAME: ProcessNewData
# DESCRIPTION: Scan subdirectories of 'path'. If
#	'path/Processed' exists but 'path/Processed/Combined' doesn't,
#	call the combiner with 'path/Processed'.  Combiner will combine images
#	and create the Combined directory
#
# PARAMETERS
#	path - The path to scan.
#
# RETURNS:
#	True if any data was processed.
#	False if no data was processed.
# ***********************************************************
def ProcessNewData(path):

	ret = False
#	ref_image = None
	ref_image = "/nfs/home/observatory/data/scheduler/Calibration/Standard/JupiterReference/PJupiter-Jupiter-Luminance-S001-R001.fts"

	# Create a sorted list of directories
	# We expect the directory names to be numerical as follows:
	# YYYYMMDD where YYYY = Year, MM = 2 digit month, DD = 2 digit day
	dirs = [os.path.join(path, d) for d in os.listdir(path)]	
	dirs = sorted(filter(os.path.isdir, dirs))
		
	for d in dirs:
		print "Checking: " + d
		
		if os.path.exists(os.path.join(d,'Processed')) and os.path.basename(d) != 'Processed':
	
			# Pick a reference image for alignment.  
			# First image (chronologically by the date in the fits header) in the first available directory
			if not ref_image:
				files = filter(Coadd_Images.fits_filter, os.listdir(os.path.join(d,'Processed')))
				files = [os.path.join(d, 'Processed', f) for f in files]
				files = sorted(files, key=Coadd_Images.get_fits_date)
				if len(files) > 0:
					ref_image = files[0]
					
			# If processed exists, but combined does not, do the combine
			if not os.path.exists(os.path.join(d,'Processed','Coadded')):
				print "Processing: " + os.path.join(d,'Processed')
				Coadd_Images.combine_images(os.path.join(d,'Processed'), ref_image)
				ret = True
		
	return(ret)


# ***********************************************************
# NAME: DataReady
# DESCRIPTION: Scan subdirectories of 'path' for the 'path/Processed/Combined' 
#	subdirectory.  If there are enough images per night for enough 
#	consecutive nights (with one night of bad weather allowed), return a
# 	sorted list of images
#
#  If the file "accept" is in a given directory, take that night
#  as complete regardless of how many images are in it.
#
# PARAMETERS
#	path - The path to scan.
#	images_per_night - The minimum number of images per night
#	number_of_nights - The minimum number of nights of data
#
# RETURNS:
#	A list of images that fulfill the observing request if all data is ready
#	An empty list of more data is needed.
# ***********************************************************
def DataReady(path, images_per_night, number_of_nights):
	
    clouds = 0			# Number of cloudy nights
    image_list = []		# Final list of images
    first_clear_index = 0		# First post-cloudy night 
    prev_date = None	

    # Scan each subdirectory in DATENIGHT order 	
    for d in filter(lambda p: os.path.isdir(os.path.join(path,p)), sorted(os.listdir(path))):

        if os.path.basename(d) == 'zip':   #Skip the zip directory if it exists.
            continue
	
        # Is this a valid night of data? (Do the proper number of images exist?)
        lpath = os.path.join(path,d,'Processed', 'Coadded')		# Current local path
        if os.path.isdir(lpath):
            # Fetch the list of fits files
    	    files = filter(Coadd_Images.fits_filter, os.listdir(lpath))	# Get the file list
        else:
		    # Oops!  No data directory
            print "Warning! " + lpath + " does not exist"
            files = []

        # If "accept" is present in the directory, take the data anyway
        if len(files) < images_per_night and not os.path.exists(os.path.join(lpath,'accept')):
         			
         # Too few images in the data directory
		    print "Too few images in " + lpath + ".  Want " + str(images_per_night) + ", have " + str(len(files))
		    continue	 			
	
        # Append these files to the image list
        image_list.append([os.path.join(lpath,f) for f in files])	
        data_date = datetime.strptime(os.path.split(d)[1],"%Y%m%d")			# Construct the date these files were taken

        # if this is not the first useable night Do the cloudy night analysis
        # Must have no more than one missing night in the data set
        if len(image_list) > 1:	


            # Cloudy night(s)?
            diff = data_date - prev_date
            if diff.days > 1:			
	            clouds += (diff.days -1)
	
	            # If there are too many cloudy nights, chop off some data
	            if clouds > 1:
		            if diff.days-1 >= 2: 			# Two or more consecutive cloudy nights?
			            image_list = [image_list[len(image_list)-1]]	
			            clouds = 0
			            first_clear_index = 0
		            else:						# Cloudy cloudy nights with good data in between 
			            image_list = image_list[first_clear_index:] 
			            clouds -= 1
			            first_clear_index = len(image_list)-1 # This night was the last clear night
	            else:
		            first_clear_index = len(image_list)-1		
		
        # Set previous date for next iteration
        prev_date = data_date						

    # Success?		
    print "We have " + repr(len(image_list)) + " nights out of " + repr(number_of_nights) + " requested"
    if len(image_list) >= number_of_nights:

        #image_list is a list of lists... 
        # Convert to a single long list
        ilist = []
        for i in image_list:
            ilist += i
        return ilist   # and return it
    else: return []
		
# ***********************************************************
# NAME: PackageData
# DESCRIPTION: 
#
# PARAMETERS
#
# RETURNS:
# ***********************************************************
def PackageData(path, images):
	
	zip_dir = os.path.join(path,'Processed','zip')
	
	# Does the directory already exist?
	if os.path.isdir(zip_dir): 
		shutil.rmtree(zip_dir)		# Delete and recreate it now.
	
	#Create a home for the processed data
	if not os.path.isdir(os.path.join(path,'Processed')):
		os.mkdir(os.path.join(path,'Processed'))
	
	# Move images into the zip directory
	os.mkdir(zip_dir)
	images = sorted(images, key=Coadd_Images.get_fits_date)

	indx = 0
	for i in images:
		shutil.copyfile(i,os.path.join(zip_dir,'jupiter'+str(indx)+'.fit'))
		indx += 1
	
	# Move into the zip directory
	old_dir = os.getcwd()
	os.chdir(zip_dir)

	
	# Put ds9 into the zip directory
	shutil.copytree('/nfs/home/observatory/software/ds9','./ds9')
	
	# Copy the region file and the spreadsheet
	shutil.copy('/nfs/home/observatory/software/JupitersMoonsSuplement/jupiter_data.xls', './')
	shutil.copy('/nfs/home/observatory/software/JupitersMoonsSuplement/Measure.reg', './')

	# Create the time stamp table
	images = filter(Coadd_Images.fits_filter, os.listdir('./'))
	images = sorted(images, key=Coadd_Images.get_fits_date)
	start_time = Coadd_Images.get_fits_date(images[0])
	f = open(os.path.join(zip_dir,'time_stamp.csv'), 'w')
	f.write('Image, Date, Elapsed Time (hours)\n')
	for i in images:
		image_time = Coadd_Images.get_fits_date(i)
		elapsed_time =  image_time - start_time
		hours = float(elapsed_time.days*24) + float(elapsed_time.seconds)/3600.0
		f.write('{0:30},{1:30},{2:.3f}\n'.format(i, image_time.isoformat(), hours))
	f.close()

	# zip everything up
	z = zipfile.ZipFile(os.path.join(path, 'Processed','Jupiter.zip'), 'w', zipfile.ZIP_DEFLATED)
	for (root, dirs, files) in os.walk('./'):
		for f in files: 
			print os.path.join(root,f)
			z.write(os.path.join(root,f))
	z.close()	
		
	os.chdir(old_dir)
	
	return os.path.join(path,'Processed','Jupiter.zip')

# ***********************************************************
# NAME: SubmitObservation
#
# DESCRIPTION:
#	Construct and Submit an observing request to the telescope. 
#
# PARAMETERS
# 	name, section, group - Identify the institution, section, and group making the request
#	short_name           - Abbreviated institudtion name
#	images_per_night	 - Number of images per night requested
#	time_between_images  - Number of minutes between images
#	number_of_nights     - Total number of nights requested
#
# RETURNS:
#	True on succsessful submission of an observing request.
#	False on failure.
# ***********************************************************
def SubmitObservation(name, short_name, section, group, images_per_night, time_between_images, number_of_nights):
	
	ret = False
	
	# build the user id
	_id = "S" + str(section) + "G" + str(group)

	# build the targets section of the rtml document
	targets = ""
	for i in range(images_per_night):
		if i == 0: 
			targets += "		<Target>\n"
		else: 
			targets += "		<Target timefromprev=\"" + str(time_between_images/60.0) +"\" tolfromprev=\"0.08333\">\n"

		targets += \
			"			<ID>Jupiter's Moons</ID>\n" 				+ \
			"			<Name>Jupiter</Name>\n" 					+ \
			"			<Planet>Jupiter</Planet>\n" 				+ \
			"			<Picture count=\"5\">\n" 					+ \
			"				<Name>Jupiter</Name>\n" 				+ \
			"				<ExposureTime>0.02</ExposureTime>\n" 	+ \
			"				<Filter>Luminance</Filter>\n" 			+ \
			"			</Picture>\n" 								+ \
			"		</Target>\n" 									
	 
	# Construct the rtml document
	rtml = \
		"<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>\n" + \
		"<RTML version=\"2.3\">\n" 							+ \
		"	<Contact>\n" 									+ \
		"		<User>" + short_name + "</User>\n" 			+ \
		"		<Email>Me@Nowhere.net</Email>\n" 			+ \
		"		<Organization>" + name + "</Organization>\n"+ \
		"	</Contact>\n" 									+ \
		"	<Request>\n" 									+ \
		"		<ID>" + _id + "</ID>\n" 						+ \
		"		<UserName>Astronomy Lab User</UserName>\n" 	+ \
		"		<Observers></Observers>\n" 					+ \
		"		<Project>" + short_name + "_" + _id + "_Jupiter</Project>\n" 	+ \
				targets										+ \
		"	</Request>\n" 									+ \
		"</RTML>\n" 
		

	# write the rtml file
	file_name = short_name + "_S" + str(section) + "G" + str(group) + "_Jupiter.rtml"
	f = open(file_name, "w")
	f.write(rtml)
	f.close()
	
	# Submit the reml to the server
	r = RTML_Submit()
	
	return r.Submit(file_name)

def print_response(buf):
	print buf
	
	
# ***********************************************************
# NAME: DateSortedDirList
# DESCRIPTION: Returns a directory listing of 'path' sorted by date.  
#
# PARAMETERS
#	path - The path to scan.
#
# RETURNS:
#	A list of subdirectories (not inluding 'path') sorted by creation date
#	The empty list if there are no subdirectories
# ***********************************************************
def DateSortedDirList(path):

	ret = []

	# Build a list of [directory, creation time] lists.
	if os.path.exists(path):
		for listing in os.listdir(path):
			p = os.path.join(path,listing)
			ret.append([p, os.path.getctime(p)])
				
	# Sort the list
	ret = sorted(ret, key=itemgetter(1))	
				
	if len(ret) > 0:
		return [r[0] for r in ret]	# Strip off the ctime and return the listing
	else: return ret


# *************************************************
# rtml request submission class
# *************************************************
class RTML_Submit(object):
	
	def Submit(self, file_name):
		
		self.Success = False;
		
		try :
		
			c = pycurl.Curl()
			c.setopt(c.POST, 1)
			c.setopt(c.URL, "http://140.209.115.152/ac/asuploadrtml.asp")
#			c.setopt(c.URL, "http://140.209.115.152/sc/suploadrtml.asp")
			c.setopt(c.HTTPPOST, [("file1", (c.FORM_FILE, file_name))])
			c.setopt(c.USERPWD, "AstroLab:AL@49!")
			c.setopt(c.WRITEFUNCTION, self.write_back)
			#c.setopt(c.VERBOSE, 1)
			c.perform()
			c.close()
		
		except :  
			self.Success = False
		
		return self.Success

	def write_back(self,buf):
		if buf.find("uploaded successfully") > -1: 
			self.Success = True
		else: 
			self.Success = False 
			print buf

# *************************************************
# Data base class 
# 
# Methods:
#	
# *************************************************
class JupiterDB(object):

	# *************************************************
	# Init function: 
	# *************************************************
	def __init__(self, host='localhost', user='ObsScript', passwd='ast1r040', db='observatory'):
		
		
		self._host = host
		self._user = user
		self._passwd = passwd
		self._db = db

		self._con = None

		try: 
			self._con = mdb.connect(self._host, self._user, self._passwd, self._db)
			self._cur = self._con.cursor(mdb.cursors.DictCursor)

		except mdb.Error, e:
			print "Error %d: %s" % (e.args[0],e.args[1])
			if self._con:
				self._con.close()

	

	# *************************************************
	# *************************************************
	def GetPendingPlans(self):

		query = "SELECT name, short_name, section, `group`, images_per_night, \
                        time_between_images, number_of_nights, scheduled, ready, Observation_Pending\
				 FROM institution INNER JOIN user USING(institution_id, year, term)\
                 INNER JOIN jupiter USING (user_id)\
				 WHERE ready=0"

		self._cur.execute(query)
		return self._cur.fetchall()

	# *************************************************
	#
	# *************************************************
	def UpdateScheduled(self, name, section, group, status):

		query = "UPDATE jupiter\
					INNER JOIN user USING(user_id)\
					INNER JOIN institution USING(institution_id, year, term)\
				SET scheduled=" + str(status) + "\
				WHERE name='" + name + "' AND section=" + str(section) + " AND `group`=" + str(group)

		self._cur.execute(query)

	# *************************************************
	#
	# *************************************************
	def UpdateObservation_Pending(self, name, section, group, Observation_Pending):

		query = "UPDATE jupiter\
					INNER JOIN user USING(user_id)\
					INNER JOIN institution USING(institution_id, year, term)\
				SET Observation_Pending=" + str(Observation_Pending) + "\
				WHERE name='" + name + "' AND section=" + str(section) + " AND `group`=" + str(group)

		self._cur.execute(query)


	# *************************************************
	#
	# *************************************************
	def UpdateData_Path(self, name, section, group, file_name):

		query = "UPDATE jupiter\
					INNER JOIN user USING(user_id)\
					INNER JOIN institution USING(institution_id, year, term)\
				SET file_name='" + file_name + "' \
				WHERE name='" + name + "' AND section=" + str(section) + " AND `group`=" + str(group)
		
		self._cur.execute(query)

	# *************************************************
	#
	# *************************************************
	def UpdateReady(self, name, section, group, ready):

		query = "UPDATE jupiter\
					INNER JOIN user USING(user_id)\
					INNER JOIN institution USING(institution_id, year, term)\
				SET ready=" + str(ready) + " \
				WHERE name='" + name + "' AND section=" + str(section) + " AND `group`=" + str(group)
		
		self._cur.execute(query)

	# *************************************************
	# del function - Destructor!
	# *************************************************
	def __del__(self):
		print "Fine!  I'm leaving!"
		if self._con: 
			print "And I'll close the door."
			self._con.close()



# ************************************************
# Data Processing Class
# ************************************************
#class JupiterData(Object):

# Invoke the main loop
if __name__ == "__main__":
	sys.exit(Jupiter())






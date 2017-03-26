"""
This script periodically checks for any updates in the dropbox folder
and downloads any changes that have occured. It can be run in the 
background manually or specified as a cron job.
The variable LOCAL_UP_DIRECTORY and LOCAL_DOWN_DIRECTORY can be set
up in init.py to change the local directory to be synchronized.
Other variables can also be initialized using init.py
"""

import time
import sys
import dropbox
import os
from init import ACCESS_TOKEN, DROPBOX_ROOT_DIRECTORY, LOCAL_UP_DIRECTORY, LOCAL_DOWN_DIRECTORY
import unicodedata

#Starting a connection
client = dropbox.Dropbox(ACCESS_TOKEN)

#Getting the contents of the dropbox folder
dropbox_results = client.files_list_folder("",recursive=True)
dropbox_results = dropbox_results.entries

#iterating over the contents of the dropbox folder
for item in dropbox_results:
	if isinstance(item,dropbox.files.FileMetadata):
		
		#getting file paths
		file_path = item.path_display

		#file_path is returned in unicode and to save space we can
		#convert it to ascii
		file_path=unicodedata.normalize('NFKD', file_path).encode('ascii','ignore')
		
		#downloading the file
		metadata, response = client.files_download(file_path)
		file_data = response.content
		
		#setting the local path for the file using LOCAL_DOWN_DIRECTORY
		file_path = file_path.replace(DROPBOX_ROOT_DIRECTORY,"/home/",1)
		file_path = file_path.replace(LOCAL_UP_DIRECTORY,LOCAL_DOWN_DIRECTORY)

		#checking to see if the file already exists or not. If it does
		#we'll remove the old inconsistent data from it and write new
		#data into it.
		#Else, we'll simply create a new file
		if os.path.exists(file_path):
			with open(file_path,'rw') as f:
				pre_data = f.read()
				if file_data!=pre_data:
					f.seek(0)
					f.truncate()
					f.write(file_data)
		else:
			if os.path.exists(os.path.dirname(file_path)):
				with open(file_path, "w+") as f:
					f.write(file_data)
			else:
				os.mkdir(os.path.dirname(file_path),0755)
				with open(file_path, "w+") as f:
					f.write(file_data)			
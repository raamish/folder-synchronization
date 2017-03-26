"""
This script periodically checks for any updates in the dropbox folder
and downloads any changes that have occured. It can be run in the 
background manually or specified as a cron job.
The variable LOCAL_DIRECTORY can be set up in init.py to change the
local directory to be synchronized.
Other variables can also be initialized using init.py
"""

import time
import sys
import dropbox
import os
from init import ACCESS_TOKEN, DROPBOX_ROOT_DIRECTORY
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
		print file_path
		print sys.getsizeof(file_path)

		#file_path is returned in unicode and only to save space we
		#can convert it to ascii
		file_path=unicodedata.normalize('NFKD', file_path).encode('ascii','ignore')
		print sys.getsizeof(file_path)
		metadata, response = client.files_download(file_path)
		file_data = response.content
		
		#setting the local path for the file
		file_path = file_path.replace(DROPBOX_ROOT_DIRECTORY,"/home/",1)
		print file_path
		print os.path.dirname(file_path)
		if os.path.exists(file_path):
			with open(file_path,'rb') as f:
				data2 = f.read()
				if file_data!=data2:
					print "data is not same so gonna heckin' bamboozlin' deletin and rewritin'"
					f.seek(0)
					f.truncate()
					f.write(file_data)
		else:
			with open(file_path, "w+") as f:
				f.write(file_data)
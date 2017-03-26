"""
This script periodically checks for any updates in the dropbox folder
and downloads any changes that have occured (positive changes) and 
deletes any files or folders that were deleted from the cloud
(negative changes). 
It can be run in the background manually or specified as a cron job. 
The variable LOCAL_UP_DIRECTORY and LOCAL_DOWN_DIRECTORY can be set
up in init.py to change the local directory to be synchronized.
Other variables can also be initialized using init.py
"""

import time
import sys
import dropbox
import os
import unicodedata

from init import ACCESS_TOKEN, DROPBOX_ROOT_DIRECTORY, \
LOCAL_UP_DIRECTORY, LOCAL_DOWN_DIRECTORY


client = dropbox.Dropbox(ACCESS_TOKEN) #Starting a connection

def download_if_modified():
	
	"""
	Getting the contents of the dropbox folder
	"""
	dropbox_results = client.files_list_folder("",recursive=True)
	dropbox_results = dropbox_results.entries

	cloud_filepaths=[]
	local_filepaths=[]

	"""
	iterating over the contents of the dropbox folder
	"""
	for item in dropbox_results:
		if isinstance(item,dropbox.files.FileMetadata):
			
			file_path = item.path_display #getting file paths

			"""
			file_path is returned in unicode and to save space we can
			convert it to ascii
			"""

			file_path=unicodedata.normalize('NFKD', file_path). \
											encode('ascii','ignore')
				
			"""
			downloading the file via the api
			"""
			metadata, response = client.files_download(file_path)
			file_data = response.content
			
			"""
			setting the local path for the file using 
			LOCAL_DOWN_DIRECTORY
			"""
			file_path = file_path.replace(DROPBOX_ROOT_DIRECTORY,
										  "/home/",1)
			file_path = file_path.replace(LOCAL_UP_DIRECTORY,
										  LOCAL_DOWN_DIRECTORY)

			"""
			checking to see if the file already exists or not. If 
			it does, we'll remove the old inconsistent data from it
			and write new data into it.
			Else, we'll simply create a new file
			"""
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
			#getting a list of all cloud files present in dropbox
			cloud_filepaths.append(file_path)	

	"""
	getting a list of all local files present in 
	LOCAL_DOWN_DIRECTORY
	"""
	for subdirs, dirs, files in os.walk(LOCAL_DOWN_DIRECTORY):
		for file in files:
			path = os.path.join(subdirs,file)
			local_filepaths.append(path)

	"""
	delete_list contains all those files which have been deleted
	#from the cloud and must also be deleted from 
	LOCAL_DOWN_DIRECTORY to maintain synchronization among the two 
	devices
	"""
	delete_list = list(set(local_filepaths)-set(cloud_filepaths))

	for item in delete_list: #deleting files (negative changes)
		os.remove(item)


"""
The following function is used to recursively delete all empty 
folders inside the LOCAL_DOWN_DIRECTORY. It returns True if 
everything inside of the given directory was deleted
"""

def recursive_delete_if_empty(path):

    if not os.path.isdir(path):
        return False

    """
    Note that the list comprehension here is necessary, a
    generator expression would shortcut and we don't want that
    """
    if all([recursive_delete_if_empty(os.path.join(path, filename))
            for filename in os.listdir(path)]):

        """
        Either there was nothing here or it was all deleted
        """
        os.rmdir(path)
        return True
    else:
        return False

if __name__ == "__main__":
	download_if_modified()
	recursive_delete_if_empty(LOCAL_DOWN_DIRECTORY)
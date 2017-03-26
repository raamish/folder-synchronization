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
		file_path = item.path_display
		print file_path
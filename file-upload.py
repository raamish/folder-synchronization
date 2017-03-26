"""
This script uses watchdog to periodically check for any modifications
and uploads them to dropbox. This script can be run in the background
manually, or run as a daemon, or specified as a cron job.
The variable LOCAL_UP_DIRECTORY can be set up in init.py to change the
local directory to be synchronized.
Other variables can also be initialized using init.py
"""

import os
import dropbox
import sys
import time
import unicodedata
import time

from watchdog.observers import Observer  
from watchdog.events import PatternMatchingEventHandler, \
FileSystemEventHandler

from init import ACCESS_TOKEN, LOCAL_UP_DIRECTORY, \
DROPBOX_ROOT_DIRECTORY


client = dropbox.Dropbox(ACCESS_TOKEN) #Starting a connection

class UploadHandler(FileSystemEventHandler):
    """
    function to upload whenever a modification is observed
    """
    def on_modified(self,event):
        cloud_filepaths=[]
        local_filepaths=[]
        """
        Getting files currently present on cloud
        """
        dropbox_results = client.files_list_folder("",recursive=True)
        dropbox_results = dropbox_results.entries
        
        for item in dropbox_results:
            if isinstance(item,dropbox.files.FileMetadata):
        
                file_path = item.path_display #Getting file paths

                """
                file_path is returned in unicode and to save space 
                we canconvert it to ascii
                """
                file_path=unicodedata.normalize('NFKD', file_path)\
                                .encode('ascii','ignore')
                
                """
                appending all filenames in a list
                """
                cloud_filepaths.append(file_path)


        """
        looping over all the files and directories recursively
        """
        for root, dirs, files in os.walk(LOCAL_UP_DIRECTORY):
            for filename in files:
                """
                getting the full path from the file
                """
                full_path = os.path.join(root, filename)
                SERVER_PATH = full_path.replace("/home/","")
                
                """
                setting the server path for the file
                """
                SERVER_PATH = DROPBOX_ROOT_DIRECTORY + SERVER_PATH
                try:
                    with open(full_path, 'rb') as f:
                        data=f.read()
                    
                    """
                    uploading the file to dropbox    
                    """
                    client.files_upload(data, SERVER_PATH, 
                            mode=dropbox.files.WriteMode.overwrite)
                except Exception as e:
                    raise ValueError('Error in uploading files')

                """
                appending local files in a list
                """
                local_filepaths.append(SERVER_PATH)

        """
        delete_list contains all those files which have been deleted
        from the LOCAL_UP_DIRECTORY and must also be deleted from 
        the cloud to maintain synchronization among the two devices
        """  
        delete_list = list(set(cloud_filepaths)-set(local_filepaths))

        """
        deleting all files on cloud which are not currently in 
        LOCAL_UP_DIRECTORY
        """
        for item in delete_list:
            try:
                client.files_delete(item)
            except Exception as e:
                raise ValueError('Error in deleting files')


if __name__ == "__main__":

	
    event_handler = UploadHandler() #watchdog init
    observe = Observer()
    observe.schedule(event_handler, path=LOCAL_UP_DIRECTORY,
                     recursive=True)
    observe.start()
    
    """
    using a 1 second time delay for the observer
    """
    try:
        while True:
        	time.sleep(1)
    except KeyboardInterrupt:
		observe.stop()
    observe.join()
"""
This script uses watchdog to periodically check for any modifications
and uploads them to dropbox. This script can be run in the background
manually, or run as a daemon, or specified as a cron job.
The variable LOCAL_DIRECTORY can be set up in init.py to change the
local directory to be synchronized.
Other variables can also be initialized using init.py
"""
import os
import dropbox
import sys
import time
from watchdog.observers import Observer  
from watchdog.events import PatternMatchingEventHandler, FileSystemEventHandler
import time
from init import ACCESS_TOKEN,LOCAL_DIRECTORY,DROPBOX_ROOT_DIRECTORY


#Starting a connection
client = dropbox.Dropbox(ACCESS_TOKEN)

class UploadHandler(FileSystemEventHandler):
	
	#function to upload whenever a modification is observed
    def on_modified(self,event):
        #looping over all the files and directories recursively
        for root, dirs, files in os.walk(LOCAL_DIRECTORY):
            for filename in files:
                full_path = os.path.join(root, filename)
                SERVER_PATH = full_path.replace("/home/","")
                #DROPBOX_ROOT_DIRECTORY can be changed in init.py
                SERVER_PATH = DROPBOX_ROOT_DIRECTORY+SERVER_PATH
                try:
                    with open(full_path, 'rb') as f:
                        data=f.read()
                    client.files_upload(data, SERVER_PATH, mode=dropbox.files.WriteMode.overwrite)
                except Exception as e:
                    print e              

if __name__ == "__main__":

	#watchdog init
    event_handler = UploadHandler()
    observe = Observer()
    observe.schedule(event_handler, path=LOCAL_DIRECTORY, recursive=True)
    observe.start()
    #Using a 1 second time delay for the observer
    try:
        while True:
        	time.sleep(1)
    except KeyboardInterrupt:
		observe.stop()
    observe.join()
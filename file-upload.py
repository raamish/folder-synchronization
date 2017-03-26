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
    def on_modification(self,event):
        for root, dirs, files in os.walk(LOCAL_DIRECTORY):
            for filename in files:
                print (client.users_get_current_account())
                full_path = os.path.join(root, filename)
                server_path = local_path.replace("/home","")
                server_path = DROPBOX_ROOT_DIRECTORY+server_path
                try:
                    with open(local_path, 'rb') as f:
                        data=f.read()
                    client.files_upload(data, server_path, mode=dropbox.files.WriteMode.overwrite)
                    print "File upload done"
                except Exception as e:
                    print e              
        # f=open('test.txt')
		# client.files_upload(f.read(),'/test.txt')
		# for entry in client.files_list_folder('').entries:
		#     print entry.name


if __name__ == "__main__":

	#watchdog init
    event_handler = UploadHandler()
    observe = Observer()
    observe.schedule(event_handler, path=LOCAL_DIRECTORY, recursive=True)
    observe.start()
    try:
        while True:
        	time.sleep(1)
    except KeyboardInterrupt as e:
		observe.stop()
    observe.join()
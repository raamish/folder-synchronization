# Socialcops Task
Synchronizing the contents of two folders on different devices using Dropbox API.

## About
This is an attempt to synchronize the data contained in two folders on two different devices. This project uses two main scripts, both of which run continuously in the background to constantly sync the data between two folders.
Whenever any modifications occurs inside one folder, the upload script, running on one device, is triggered and it uploads/changes the files on Dropbox. The download script runs periodically on the other device to check for any changes and downloads/incorporates them accordingly into the other folder.

## Dependencies Installation
-dropbox (7.2.1)

-watchdog (0.8.3)

`pip install -r requirements.txt`

## Usage
1. Create an account on Dropbox and obtain an API ACCESS_TOKEN and other keys and set them up in init.py
2. Set up the LOCAL_UP_DIRECTORY and LOCAL_DOWN_DIRECTORY inside init.py
3. The file-download.py script automatically connects to Dropbox and acquires all the files present on it and accordingly
   downloads or deletes the files present in the LOCAL_DOWN_DIRECTORY. 
   The file-download.py can be set up as a cronjob. A cronjob in UNIX based systems can be set up by executing `crontab -e`
   Add a line which looks similar to the line below
   
   `*/1 * * * * /home/raamish/projects/socialcops-sync-folders/file-download.py >> /home/raamish/projects/cron.log`
   
   This ensures that cron runs our script every 1 minute.
4. Run the file-upload.py either manually indefinitely or in the background as a daemon. The script watches the
   LOCAL_UP_DIRECTORY and whenever any modifications occur, uploads them onto Dropbox (positive changes) or deletes 
   them from Dropbox (negative changes).

### CheckList

- [x] Dropbox Integration
- [x] Download Script
- [x] Upload Script  

### Minor Bug
Both the scripts handle deletions as well, and any changes are reflected correctly. The only minor issue is that Dropbox shows empty folders as well and their API doesn't supports any function to remove empty directories. However, this doesn't affects the synchronization part between the two devices, but just leaves empty folders on our Dropbox cloud.

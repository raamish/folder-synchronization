import os
import dropbox

ACCESS_TOKEN="3T90XwttljAAAAAAAAAACjFXD1mvS0vE8x3qQHY55YUv0a84SvLUVt219oq0O9Za"
APP_KEY="zuic01fv4jp0nbx"
APP_SECRET="uruh1q0ujbfboa5"

client = dropbox.Dropbox(ACCESS_TOKEN)
client.users_get_current_account()

f=open('test.txt')
client.files_upload(f.read(),'/test.txt')
for entry in client.files_list_folder('').entries:
    print entry.name

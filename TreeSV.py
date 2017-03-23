#Author: Eric Jacobson
#
#E-mail: erj826@bu.edu
#
#Phone: 508-395-0768
#
#TreeSV 
#Date: March 2017


#Uses Google Drive API
#License Not for Commerical Use


from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python TreeSV'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    
    #COMMENT OUT FOLLOWING LINE TO ALWAYS PROMPT FOR PERMISSIONS
    #if not credentials or credentials.invalid:
    flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
    flow.user_agent = APPLICATION_NAME
    if flags:
        credentials = tools.run_flow(flow, store, flags)
    else: # Needed only for compatibility with Python 2.6
        credentials = tools.run(flow, store)
    #WILL ALWAYS ASK FOR PERMISSION...STORAGE PATH IS REDUNDANT
    #print('Storing credentials to ' + credential_path)
    return credentials


def is_in_dir(file_name, items):
    for item in items:
        if file_name == item['name']:
            global glbl_root
            glbl_root = item
            return True
    return False

def print_files(items):
    print('Files:')
    for item in items:
        print('{0} ({1})'.format(item['name'], item['id']))


def main():
    """Generates a CSV file from the first four tiers of a google drive 
       directory.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    
    desired_directory = raw_input("Please enter a directory name:")

    results = service.files().list(
            fields="nextPageToken, files(id, name, parents)").execute()
    #potentially need pageSize=1000,

    items = results.get('files', [])

    if not items:
        print('No files found.')      
    else:
        while(is_in_dir(desired_directory, items) == False):
            print('Directory not found! Please try again!')
            desired_directory = raw_input("Please enter a directory name:")
     
    output_file = open(desired_directory + '.csv', 'w+')
    
    output_string = ''    
   
    for item in items:
        #Checking 2nd tier files
        if(str([glbl_root['id']]) == str(item.get('parents', []))):          
            for item2 in items:
                #Checking 3rd tier files
                if(str([item['id']]) == str(item2.get('parents', []))):                  
                    for item3 in items:
                        #Checking 4th tier files
                        if(str([item2['id']]) == str(item3.get('parents', []))):
                            #Creating CSV string   
                            output_string += (str(glbl_root['name']) + ',' +
                                              str(item['name']) + ',' +
                                                 str(item2['name']) + ',' +
                                                    str(item3['name']) + '\n')
                                               
                                  
    output_file.write(output_string)
    output_file.close
    

if __name__ == '__main__':
    main()

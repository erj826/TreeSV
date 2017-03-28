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


def is_in_dir(service, file_name):  
    """"Checks if desired_directory is in Drive and sets it as root node"""
    for item in items:
        if file_name == item['name']:
            global glbl_root
            glbl_root = item
            return True
    return False
        

def get_children(parentId, items):
    """Returns the sub-files of a given folder"""
    children = []  
    for item in items:
        if(str([parentId]) == str(item.get('parents', [])) and item not in children):
            children.append(item)   
    return children

def dftt(service, cur_node):
    """Depth first tree traversal"""
    ttr = ''
    children_of_cur_node = get_children(cur_node['id'], items)
    count = len(children_of_cur_node)
    while(count > 0):
        for child in children_of_cur_node:
            if ((count != len(children_of_cur_node)) and cur_node['name'] != desired_directory):
                ttr += desired_directory + ','
            
            count = len(children_of_cur_node)  
            
            ttr += cur_node['name'] + ',' + dftt(service, child)
            count -= 1

        return ttr

    return cur_node['name'] + '\n'


def main():
    """Generates a CSV file from the first four tiers of a google drive 
       directory.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    
    global desired_directory
    desired_directory = raw_input("Please enter a directory name:")
    
    #Get All files in drive:
    results = {}
    global items
    items= []
    page_token = None

    while True:
        results = service.files().list(
                    fields='nextPageToken, files(id, name, parents, mimeType)',
                    pageToken=page_token).execute()  
        
        for file in results.get('files', []):
            page_token = results.get('nextPageToken', None)
            items += (results.get('files', []))
            if page_token is None:
                break;
                
        if page_token is None:
            break;
            
    
    if not items:
        print('No files found.')
        
    while(is_in_dir(service, desired_directory) == False):
        print('Directory not found!')
        desired_directory = raw_input("Please enter a directory name:")
            
    output_file = open(desired_directory + '.csv', 'w+')  
    
    output_string = (dftt(service, glbl_root))

    output_file.write(output_string)
    output_file.close
    
if __name__ == '__main__':
    main()

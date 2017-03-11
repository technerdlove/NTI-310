#!/usr/bin/python
# Let's build our imports and make them our best friends... we can make them long
# Or we can make them 'not so long' imports.
from oauth2client.client import GoogleCredentials               # References https://cloud.google.com/compute/docs/tutorials/python-guide
from googleapiclient import discovery                           # https://cloud.google.com/compute/docs/reference/latest/instances/insert

# set projectid and zone
project = ""
zone = ""

# set up google cloud credencials
credentials = GoogleCredentials.get_application_default()

# initialize the api and buid an object
compute = discovery.build('compute', 'v1', credentials=credentials)


print "currently running:"
# list instances
def list_instances(compute, project, zone):
    result = compute.instances().list(project=project, zone=zone).execute()
    return result['items']

centos_server =     open('centos_config.json', 'r').read()      # Slightly edited Rest Json with variables
ubuntu_client =     open('ubuntu_config.json', 'r').read()      # Slightly edited Rest Json with variables

def create_instance(os_type, project, zone, config_script):
  

# We'll need to read in an additional file, which is the scripting file for the server we are creating.  
# I feel like that kind of needs to be a different function, but I'm open to thoughts on it.  Actually, I
# Think the path to that file needs to be passed into this and that this shoudl be called as a library...

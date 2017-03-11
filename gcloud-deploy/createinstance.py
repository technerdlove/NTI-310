#!/usr/bin/python

from oauth2client.client import GoogleCredentials                     # References https://cloud.google.com/compute/docs/tutorials/python-guide
from googleapiclient import discovery                                 # https://cloud.google.com/compute/docs/reference/latest/instances/insert

# set projectid and zone
project = ""
zone = ""

credentials = GoogleCredentials.get_application_default()             # set up google cloud credencials
compute = discovery.build('compute', 'v1', credentials=credentials)   # initialize the api and buid an object

print "currently running:"
# list instances
def list_instances(compute, project, zone):
    result = compute.instances().list(project=project, zone=zone).execute()
    return result['items']
    
def create_instance(compute, os_type, project, zone, name, config_script):
    centos_server =           open('centos_config.json', 'r').read()      # Slightly edited Rest Json with variables
    ubuntu_client =           open('ubuntu_config.json', 'r').read()      # Slightly edited Rest Json with variables
    configuration_script =    open('server_config.sh', 'r').read()        # We'll need to read this in, mod it, based on the hostname
                                                                          # and such, then write this out.
    image_response = compute.images().getFromFamily(
       project='centos-cloud', family='centos-7').execute()
    source_disk_image = image_response['selfLink']

    
     # Configure the machine
    machine_type = "zones/%s/machineTypes/f1-micro" % zone
    startup_script = open(
        os.path.join(
            os.path.dirname(__file__), 'configuration_script'), 'r').read()
    image_url = "https://s-media-cache-ak0.pinimg.com/736x/b2/59/b4/b259b4fb6fc7a18b432a01b6051a7bf7.jpg"
    image_caption = "Just Google It :P"
    
    
    config =         # which will contain the specs for the centos_server or the ubuntu client.  :D
                     # somewhere along the lines here, we need to customize the config...
                     # AAAAAAH

    return compute.instances().insert(
    project=project,
    zone=zone,
    body=config).execute()
  

# We'll need to read in an additional file, which is the scripting file for the server we are creating.  
# I feel like that kind of needs to be a different function, but I'm open to thoughts on it.  Actually, I
# Think the path to that file needs to be passed into this and that this shoudl be called as a library...

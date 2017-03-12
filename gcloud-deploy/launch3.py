#!/usr/bin/python

from oauth2client.client import GoogleCredentials
from googleapiclient import discovery
import pprint
import json

credentials = GoogleCredentials.get_application_default()
compute = discovery.build('compute', 'v1', credentials=credentials)

project = 'civil-epigram-138823'
zone = 'us-central1-b'
name = 'andoncemore22'
startup_script = open('startup-script.sh', 'r').read()
#centos7_config = open('centos7.json', 'r').read()
#ubuntu_conifg = open('ubuntu.json', 'r').read()

def list_instances(compute, project, zone):
    result = compute.instances().list(project=project, zone=zone).execute()
    return result['items']

def create_instance(compute, project, zone, name, startup_script):
    image_response = compute.images().getFromFamily(
      project='centos-cloud', family='centos-7').execute()

    source_disk_image = image_response['selfLink'] 
    machine_type = "zones/%s/machineTypes/f1-micro" % zone

    centos7_config = json.load('centos7.json', 'r')
    config = json.dump(centos7_config)
    return compute.instances().insert(
        project=project,
        zone=zone,
        body=config).execute()

newinstance = create_instance(compute, project, zone, name, startup_script)
instances = list_instances(compute, project, zone)

pprint.pprint(newinstance)
pprint.pprint(instances)

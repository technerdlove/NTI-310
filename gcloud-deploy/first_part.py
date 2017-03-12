

def create_instance(compute, project, zone, name):
    #Centos config for 'yall
    image_response = compute.images().getFromFamily(
      project='centos-cloud', family='centos-7').execute()
    source_disk_image = image_response['selfLink']
    
    machine_type = "zones/%s/machineTypes/n1-standard-1" % zone
    startup_script = open(
        os.path.join(
            os.path.dirname(__file__), 'startup-script.sh'), 'r').read()
    
    
  

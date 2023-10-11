#this is a file in order to demonstrate basic control over docker desktop, all on the same machine.
#in this file, I should demo:
#downloading docker container images
#starting containers - not done
#stoping containers - not done
#viewing running containers - not done
#deleteing containers - not done

import docker
client = docker.from_env()

def download():
    container = client.containers.run('alpine', 'echo hello world', detach=True) #args separated by commas, i.e. domainname=alpine, auto_remove=true
    container.logs()#shows logs from running container. If the detach argument is True, it will start the container and immediately return a Container object, similar to "docker run -d".
def start():

def stop():

def view():

def remove():

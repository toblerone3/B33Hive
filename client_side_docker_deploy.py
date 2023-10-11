import sys, docker.api, random, string, subprocess

#to do
#pull and configure images
#pull and configure dependencies
#create new containers
#remove containers
#Starting containers
#Stopping Containers
#Get Container Logs
#Get Container Uptime (?)
#Get Container Resource Usage (If possible, this would just be cool)
#Container config maybe?


client = docker.from_env()

try:
    open("flag", "x")
    client.images.pull('mysql')  # dependency for kippo
    # client.images.pull('alexeiled/nsenter') #old dependency, may still need
    client.images.pull('dariusbakunas/kippo')
    client.images.pull('dtagdevsec/glutton')
    client.images.pull('ktitan/glastopf')
    #dockertrap image made separately - https://github.com/mrhavens/DockerTrap/tree/master

except:
    print("\nimages already pulled, proceeding\n")

def randomword(length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

def menu():
    print(
        "\n1) create container \n2) destroy container \n3) start container \n4) stop container\n5) fetch logs\n6) fetch uptime\n6) fetch resource usage\n7) edit config\n8) exit")
    try:
        choice = int(input("enter a number: "))
    except:
        input("\ninvalid selection, press enter to continue...\n")

    if (choice == 1):
        create()
    elif (choice == 2):
        destroy()
    elif (choice == 3):
        start()
    elif (choice == 4):
        stop()
    elif (choice == 5):
        logs()
    elif (choice == 6):
        uptime()
    elif (choice == 7):
        resource()
    elif (choice == 8):
        config()
    elif (choice == 9):
        sys.exit()
    elif (choice == 69):
        exec(open("bee.py").read())
    else:
        print("\ninvalid choice\n")
        menu()

def create():
    print(
        "\n1) create glastopf  \n2) create glutton \n3) create kippo  \n4) create mysql \n5) create dockertrap \n6) exit ")
    try:
        choice = int(input("enter a number: "))
    except:
        input("\ninvalid selection, press enter to continue...\n")

    if (choice == 1):
        createname = "glastopf-" + randomword(8)
        client.containers.create(image="ktitan/glastopf", name=createname, ports={'80/tcp': 80}, volumes={'/data/glastopf': {'bind': '/opt/myhoneypot', 'mode': 'rw'})
    elif (choice == 2):
        client.containers.create()
    elif (choice == 3):
        client.containers.create()
    elif (choice == 4):
        client.containers.create()
    elif (choice == 5):
        client.containers.create()
    elif (choice == 6):
        menu()


    #client.containers.create()
def destroy():
    menu()
def start(container):
    print()
    client.containers.list(all=True)
    print()
    startname=''

    try:
        startname = input("input the name of the container to start")
    except:
        print("invalid selection")

    client.containers.run(name=startname)
    print()
    print("container status: " + container.name.status)
    input("\nfinished, press enter...\n")
    menu()

def stop(container):
    print()
    client.containers.list()
    print()
    stopname = ''

    try:
        stopname = input("input the name of the container to stop")
    except:
        print("invalid selection")

    client.containers.run(name=stopname)
    print()
    print("container status: " + container.name.status)
    input("\nfinished, press enter...\n")
    menu()
def logs():
    menu()
def uptime():
    menu()
def resource():
    menu()
def config():
    menu()